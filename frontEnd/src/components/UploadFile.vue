<script>
import AWS from 'aws-sdk';
import ProgressBar from 'vue-simple-progress';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import ImageCard from './ImageCard.vue';

export default {
  name: 'UploadFile',

  components: {
    ProgressBar,
    PulseLoader,
    ImageCard,
  },

  data() {
    return {
      upProg: 0, // update progress html element
      upSuccess: false, // status of full upload to S3 bucket
      errMessage: '', // generic placeholder for error messages
      isDisabled: false, // dis/enables buttons
      submitDisabled: true,
      imgLoading: false, // loading status for return image spinner
      s3: null, // placeholder for configured aws S3 bucket object
      uploadImg: '', // user submitted image, to be displayed
      uploadFile: undefined, // user file to be uploaded;contains file information as array
      fileName: '', // file name of upload image to display
      returnAicUrl: '', // url of AIC artwork
      aicBlue: undefined, // AIC API returned blue , red, green values
      aicRed: undefined,
      aicGreen: undefined,
      userGreen: undefined, // computed dominant rgb colors from uploaded image
      userRed: undefined,
      userBlue: undefined,
    };
  }, // end data()

  mounted() {
    // set config and bucket name for AWS S3 upload app
    AWS.config.update({
      region: 'us-east-1',
      credentials: new AWS.CognitoIdentityCredentials({
        IdentityPoolId: 'us-east-1:fafe5de1-71f5-4c79-a9c8-6e09e0f650b2',
      }),
    });

    this.s3 = new AWS.S3({
      params: {
        Bucket: 'bradley-test-bucket',
      },
    }, (err) => {
      if (err) this.errMessage = `Error configuring S3 bucket: ${err}`;
    });
  }, // end mounted()

  methods: {
    fileLoad() {
      // Called when user clicks the #fileUpload button.

      // reset if there's a previous image submited
      if (this.upSuccess === true) {
        this.upSuccess = false;
        // reset any chosen file to upload, including name
        this.uploadFile = undefined;
        this.fileName = '';
        // reset progress bar
        this.upProg = 0;
        // reset data values
        this.returnAicUrl = '';
        this.aicBlue = undefined;
        this.aicRed = undefined;
        this.aicGreen = undefined;
        this.userRed = undefined;
        this.userBlue = undefined;
        this.userGreen = undefined;
        this.uploadImg = undefined;
        this.errMessage = '';
        // reenable 'Submit Image' button on new file select
        this.isDisabled = false;
        this.submitDisabled = true;
      }

      document.getElementById('fileUpload').onchange = () => {
        // read fil and display in the generated card
        const pic = document.getElementById('fileUpload').files;
        // display file name on selection
        this.fileName = pic[0].name;

        [this.uploadFile] = pic; // only upload one file

        // get info on image and display
        const reader = new FileReader();
        if (reader.onerror) {
          this.errMessage = FileReader.error;
        } else {
          reader.onload = (event) => {
            this.uploadImg = event.target.result; // loads image
          };
          reader.readAsDataURL(this.uploadFile); // shows image
          this.submitDisabled = false; // enable button to upload
        }
      };
    },

    submitFile() {
      // Called when user clicks 'Submit Image' button

      // check to see if a file has been chosen for upload; shouldn't see this at all because
      //  the check is in the ":disable" property logic
      if (!this.uploadFile) {
        this.errMessage = 'Please select an image to upload';
      } else {
        // disable button while image is uploading to prevent concurrent uploads
        this.isDisabled = true;

        // clear any previous error on new file submission
        if (this.errMessage !== '') this.errMessage = '';

        // parameters for file information for the S3 bucket upload
        const params = {
          Key: this.uploadFile.name,
          ContentType: this.uploadFile.type,
          Body: this.uploadFile,
          ACL: 'public-read',
        };

        // upload image to be save in S3 bucket
        this.s3.upload(params, (err) => {
          if (err) {
            this.errMessage = `Upload Error: ${err}`;
          } else {
            // a successful upload will trigger AWS Lambda functions watching this
            //  particular bucket
            this.upSuccess = true;
            // show spinners
            this.imgLoading = true;
            // fetch results from Lamda trigger and SQS message
            this.getResults();
          }
        })
          // show upload progress via html progress element
          .on('httpUploadProgress', (evt) => {
            this.upProg = parseInt(((evt.loaded * 100) / evt.total), 10);
          });
      }
    },

    getResults() {
      // method called by submitFile() to fetch results via AWS SQS

      const sqs = new AWS.SQS({
        apiVersion: '2012-11-05',
        maxRetries: 3,
      }, (err) => {
        if (err) this.errMessage = `Error in sending SQS request: ${err}`;
      });
      const params = {
        QueueUrl: 'https://sqs.us-east-1.amazonaws.com/145918816538/AIC_SNS',
        AttributeNames: ['All'],
        MaxNumberOfMessages: '1',
        MessageAttributeNames: ['*'],
        VisibilityTimeout: 60, // in seconds
        WaitTimeSeconds: 20, // in seconds, max 20, returns sooner if available
      };

      sqs.receiveMessage(params, (err, data) => {
        if (err) {
          this.errMessage = `Error in retrieving data from SQS: ${err}`;
        } else if (data.Messages.length !== 0) {
          const result = JSON.parse(JSON.parse(data.Messages[0].Body).Message).Input;
          // stop spinner
          this.imgLoading = false;
          // set data for prop values for children:
          this.returnAicUrl = result.aic_colors.url; // url of AIC color match
          // color of match:
          this.aicRed = result.aic_colors.red;
          this.aicBlue = result.aic_colors.blue;
          this.aicGreen = result.aic_colors.green;
          // rgb computed from user uploaded image:
          this.userRed = result.user_colors.user_red;
          this.userGreen = result.user_colors.user_green;
          this.userBlue = result.user_colors.user_blue;

          // remove message from AWS SQS queue to help ensure correct message is received for next
          sqs.deleteMessage({
            QueueUrl: 'https://sqs.us-east-1.amazonaws.com/145918816538/AIC_SNS',
            ReceiptHandle: data.Messages[0].ReceiptHandle,
          }, (delErr) => {
            if (delErr) this.errMessage = 'Message in SQS queue has not been deleted!';
          });
        } else {
          // message was returned from SQS, but empty
          this.imgLoading = false;
          this.errMessage = 'Return data is empty!';
        }
        // reset buttons after data loads
        this.isDisabled = false;
        this.submitDisabled = true;
      });
    },
  }, // end methods()

};
</script>

<template>
  <div class="upload">
    <div class="interaction-flex-container">
      <div class="inputs">
        <input
          id="fileUpload"
          class="file-button"
          name="myfile"
          type="file"
          accept=".jpg, .jpeg, .png"
          :disabled="isDisabled"
          @click="fileLoad"
        >
        <label for="fileUpload">
          SELECT YOUR IMAGE
        </label>

        <div class="file-name">
          {{ fileName }}
        </div>

        <div>
          <button
            id="submitImage"
            class="submit-button"
            type="button"
            name="SUMBIT IMAGE"
            :disabled="isDisabled || submitDisabled"
            @click="submitFile"
          >
            SUBMIT IMAGE
          </button>
        </div>
      </div>
      <!-- inputs -->

      <div class="upload-indication">
        <!-- only show progress bar whilst uploading,  but keep it displayed even if error -->
        <div
          v-if="upProg > 0"
          class="progress-bar"
        >
          <ProgressBar
            id="showUpload"
            max="100"
            size="20"
            bar-color="#1E88E5"
            bar-border-radius="3"
            :val="upProg"
          />
        </div>

        <div class="message-container">
          <div
            v-if="upSuccess"
            class="success-upload"
          >
            Upload Successful
          </div>
          <!-- placeholder for all error messages -->
          <div
            v-if="errMessage"
            class="error-message"
          >
            {{ errMessage }}
          </div>
          <!-- Processing indication -->
          <div class="loader">
            <div v-if="imgLoading">
              Processing
            </div>
            <PulseLoader
              :loading="imgLoading"
              :color="'#424242'"
              :size="'4px'"
              :margin="'2px'"
            />
            <div
              v-if="aicRed"
              class="process-complete"
            >
              Processing Complete!
            </div>
          </div>
          <!-- .loader -->
        </div>
        <!-- message-container -->
      </div>
      <!-- upload-indication -->
    </div>
    <!-- interaction-flex-container -->

    <div class="card-container">
      <ImageCard
        v-if="uploadImg"
        cardtitle="Uploaded Image"
        colortitle="Dominant Color of This Image"
        :src="uploadImg"
        :red="userRed"
        :green="userGreen"
        :blue="userBlue"
      />
      <ImageCard
        v-if="returnAicUrl"
        cardtitle="AIC Match"
        colortitle="Nearest Color Matched to AIC API"
        :src="returnAicUrl"
        :red="aicRed"
        :green="aicGreen"
        :blue="aicBlue"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">

.upload {
  margin: auto;
  text-align: center;

  @media only screen and (max-width: $responsive-width) {
    width: 95%;
  }
}

.interaction-flex-container {
  align-items: space-evenly;
  border-radius: 5px;
  box-shadow: $shadow-depth-1;
  display: flex;
  flex-direction: row;
  margin: 1rem auto;
  width: 50rem;

  @media only screen and (max-width: $responsive-width) {
    flex-direction: column;
    height: 16rem;
    width: 100%;
  }
}

.inputs {
  margin: 0.5rem;
  text-align: left;
  width: 50%;

  @media only screen and (max-width: $responsive-width) {
    text-align: center;
    width: 100%;
  }
}

/*
 * file input styling per https://www.benmarshall.me/styling-file-inputs/
 * claims to be optimized, semantic, and accessible
 */
[type="file"] {
  // hides the default input UI
  border: 0;
  clip: rect(0, 0, 0, 0);
  height: 1px;
  overflow: hidden;
  padding: 0;
  position: absolute !important;
  white-space: nowrap;
  width: 1px;

  + label {
    border-radius: 5px;
    // File upload button styles
    box-shadow: $shadow-depth-1;
    color: $text-black;
    cursor: pointer;
    display: inline-block;
    font-size: 0.9rem;
    height: 2.5rem;
    margin: 0.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.7rem;
    text-align: center;
    transition: background-color 0.3s;
    width: 13rem;
  }

  &:focus + label,
  + label:hover {
    // File upload hover state button styles
    @include button-hover;
  }

  &:active + label,
  + label:active {
    // button press transition
    @include button-active;
  }

  &:focus + label {
    // File upload focus state button styles
    outline: -webkit-focus-ring-color auto 1px;
    outline: 1px dotted #000;
  }

  &:disabled + label {
    @include button-inactive;
  }
}

.file-name {
  height: 1.2rem;
  margin: 0.5rem 0 0.5rem 1rem;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 20rem;
}

.submit-button {
  border-radius: 5px;
  border-style: none;
  box-shadow: $shadow-depth-1;
  color: $text-black;
  cursor: pointer;
  font-family: Helvetica, Arial, sans-serif;
  font-size: 0.9rem;
  height: 2.5rem;
  margin: 0.5rem;
  transition: background-color 0.3s;
  width: 13rem;

  &:hover {
    @include button-hover;
  }

  &:active {
    @include button-active;
  }

  &:disabled {
    @include button-inactive;
  }
}

.upload-indication {
  margin: 0.5rem;
  text-align: left;
  width: 50%;

  @media only screen and (max-width: $responsive-width) {
    margin: 0;
    text-align: center;
    width: 100%;
  }
}

.success-upload {
  color: $success-green;
  font-weight: bold;
  margin: 0.5rem 0 0 0;
}

.error-message {
  color: $error-red;
  font-weight: bolder;
  margin-top: 0.5rem;
}

.process-complete {
  color: $success-green;
}

.progress-bar {
  margin-top: 0.5rem;
}

.loader {
  display: inline-flex;
  font-weight: bold;
  margin: 0.5rem 0 0 0;
}

.card-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
