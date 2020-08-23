<script>
import AWS from 'aws-sdk';
// import UserImageCard from './UserImageCard.vue';
// import ResultImageCard from './ResultImageCard.vue';
import ImageCard from './ImageCard.vue';

export default {
  name: 'UploadFile',

  components: {
    ImageCard,
  },

  data() {
    return {
      upProg: 0, // update progress html element
      success: false, // status of full upload to S3 bucket
      error: false, // conditional for v-if error display
      errMessage: '', // generic placeholder for error messages
      noneSelected: false, // check value for if an image file has been selected
      bucketName: 'bradley-test-bucket',
      bucketRegion: 'us-east-1',
      IdentityPoolId: 'us-east-1:fafe5de1-71f5-4c79-a9c8-6e09e0f650b2',
      s3: null, // placeholder for configured aws S3 bucket object
      uploadImg: '', // user submitted image, to be displayed
      returnAicUrl: '', // object holding the Lamda funtion returned data, as shown below
      aicBlue: undefined, // AIC API returned blue , red, green values
      aicRed: undefined,
      aicGreen: undefined,
      userGreen: undefined, // computed dominant rgb colors from uploaded image
      userRed: undefined,
      userBlue: undefined,
      imgLoading: false, // loading status for return image spinner
      rgbLoading: false, // loading status for rgb color swatch and text
    };
  }, // end data()

  mounted() {
    // set config and bucket name for AWS S3 upload app
    AWS.config.update({
      region: this.bucketRegion,
      credentials: new AWS.CognitoIdentityCredentials({
        IdentityPoolId: this.IdentityPoolId,
      }),
    });

    this.s3 = new AWS.S3({
      params: {
        Bucket: this.bucketName,
      },
    });
  }, // end mounted()

  methods: {
    submitFile() {
      // reset if there's a previous image submited
      if (this.success === true) {
        this.success = false;
        // rest data values
        this.returnAicUrl = '';
        this.aicBlue = undefined;
        this.aicRed = undefined;
        this.aicGreen = undefined;
        this.userRed = undefined;
        this.userBlue = undefined;
        this.userGreen = undefined;
        this.uploadImg = undefined;
        this.error = false;
        this.errMessage = '';
      }

      const pic = document.getElementById('fileUpload').files;

      if (pic.length === 0) {
        this.error = true;
        this.errMessage = 'Please select an image to upload';
      } else {
        // clear any previous error on new file submission
        if (this.error) {
          this.error = false;
          this.errMessage = '';
        }

        const file = pic[0]; // only upload one file
        const reader = new FileReader();

        reader.addEventListener('load', (event) => {
          this.uploadImg = event.target.result;
        }); // loads image
        reader.readAsDataURL(file); // shows image

        const params = {
          Key: file.name,
          ContentType: file.type,
          Body: file,
          ACL: 'public-read',
        };

        // upload image to be save in S3 bucket
        this.s3.upload(params, (err) => {
          if (err) {
            this.error = true;
            this.errMessage = `Upload Error: ${err}`;
          } else {
            // a successful upload will trigger AWS Lambda functions watching this
            //  particular bucket; fetch result waiting for us from SQS
            this.success = true;
            // show spinner
            this.imgLoading = true;
            this.rgbLoading = true;
            this.getResults();
          }
        })
          // show upload progress
          .on('httpUploadProgress', (evt) => {
            this.upProg = parseInt(((evt.loaded * 100) / evt.total), 10);
          });
      }
    },

    getResults() {
      const sqs = new AWS.SQS({
        apiVersion: '2012-11-05',
        maxRetries: 3,
      });
      const params = {
        QueueUrl: 'https://sqs.us-east-1.amazonaws.com/145918816538/AIC_SNS',
        AttributeNames: ['All'],
        MaxNumberOfMessages: '1',
        MessageAttributeNames: ['*'],
        VisibilityTimeout: 60, // in seconds
        WaitTimeSeconds: 20, // in seconds
      };

      sqs.receiveMessage(params, (err, data) => {
        if (err) {
          this.error = true;
          this.errMessage = `Error is retrieving data from SQS: ${err}`;
        } else if (data.Messages.length !== 0) {
          const result = JSON.parse(JSON.parse(data.Messages[0].Body).Message).Input;
          // stop spinner
          this.imgLoading = false;
          this.rgbLoading = false;
          // console.log(result);
          // set data for prop values for children:
          // url of AIC color match
          this.returnAicUrl = result.aic_colors.url;
          // color of match
          this.aicRed = result.aic_colors.red;
          this.aicBlue = result.aic_colors.blue;
          this.aicGreen = result.aic_colors.green;
          // rgb computed from user uploaded image
          this.userRed = result.user_colors.user_red;
          this.userGreen = result.user_colors.user_green;
          this.userBlue = result.user_colors.user_blue;

          // remove message from AWS SQS queue to help ensure correct message is received for next
          sqs.deleteMessage({
            QueueUrl: 'https://sqs.us-east-1.amazonaws.com/145918816538/AIC_SNS',
            ReceiptHandle: data.Messages[0].ReceiptHandle,
          }, (delErr) => {
            if (delErr) {
              this.error = true;
              this.errMessage = 'Message in SQS queue has not been deleted!';
            }
          });
        } else {
          // message was returned from SQS, but empty
          this.imgLoading = false;
          this.rgbLoading = false;
          this.error = true;
          this.errMessage = 'Return data is empty!';
        }
      });
    },
  }, // end methods()

};
</script>

<template>
  <div class="upload">

    <p class="app-copy">
      This app will take an uploaded image, decipher the dominant color of that image, and match
      it to a painting with the Art Institute of Chicago's (AIC) API database that contains the
      dominant color of the uploaded image within the artwork's top three dominant colors.
    </p>

    <div class="interaction-flex-container">

      <div class="inputs">
        <input
          id="fileUpload"
          class="file-button"
          name="myfile"
          type="file"
          accept=".jpg, .jpeg, .png"
          required
        />
        <label for="fileUpload">
          SELECT YOUR IMAGE
        </label>

        <div>
          <input
            id="submitImage"
            class="submit-button"
            type="submit"
            value="SUMBIT IMAGE"
            @click="submitFile"
          />
        </div>
      </div><!-- inputs -->

      <div class="upload-indication">
        <!-- only show progress bar whilst uploading,  but keep it displayed even if error -->
        <div v-if="upProg > 0">
          <progress
            id="showUpload"
            max="100"
            :value="upProg"
          />
        </div>

        <div class="message-container">
          <div
            v-if="success"
            class="success-upload">
            Upload Successful
          </div>
          <!-- placeholder for all error messages -->
          <div
            v-if="error"
            class="error-message">
            {{ errMessage }}
          </div>
        </div><!-- message-container -->
      </div><!-- upload-indication -->

    </div><!-- interaction-flex-container -->

    <div class="card-container">

      <ImageCard
        cardtitle="Uploaded Image"
        colortitle="Dominant Color of This Image"
        :src="uploadImg"
        :red="userRed"
        :green="userGreen"
        :blue="userBlue"
        :rgbloading="rgbLoading"
      />
      <ImageCard
        cardtitle="AIC Match"
        colortitle="Nearest Color Matched to AIC API"
        :src="returnAicUrl"
        :red="aicRed"
        :green="aicGreen"
        :blue="aicBlue"
        :imgloading="imgLoading"
        :rgbloading="rgbLoading"
      />

    </div>

  </div>
</template>

<style scoped lang="scss">
$progress-fill: #1976d2;
$success-green: #388e3c;
$error-red: #d32f2f;
$responsive-width: 599px;

.upload {
  margin: auto;
  text-align: center;
}

.app-copy {
  font-family: 'Times New Roman', Times, Georgia, serif;
  font-size: 1.2rem;
  margin: auto;
  text-align: left;
  width: 40%;

  @media only screen and (max-width: $responsive-width) {
    width: 90%;
  }
}

.interaction-flex-container {
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
  display: flex;
  flex-direction: row;
  align-items: space-evenly;
  margin: 1rem auto;
  width: 70%;

  @media only screen and (max-width: $responsive-width) {
    width: 100%;
    flex-direction: column;
    height: 16rem;
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
 * file input sytling per https://www.benmarshall.me/styling-file-inputs/
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
    // File upload button styles
    box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    border-radius: 5px;
    display: inline-block;
    font-size: 1rem;
    height: 2.5rem;
    width: 13rem;
    text-align: center;
    padding-top: 0.7rem;
    padding-left: 1rem;
    padding-right: 1rem;
    margin: 0.5rem;
    transition: background-color 0.3s;
  }

  &:focus + label,
  + label:hover {
    // File upload hover state button styles
    background-color: white;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
  }

  &:active + label,
  + label:active {
    // button press transition
    background-color: white;
    box-shadow: none;
  }

  &:focus + label {
    // File upload focus state button styles
    outline: 1px dotted #000;
    outline: -webkit-focus-ring-color auto 1px;
  }
}

.submit-button {
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
  border-radius: 5px;
  border-style: none;
  font-size: 1rem;
  height: 2.5rem;
  width: 13rem;
  margin: 0.5rem;
  transition: background-color 0.3s;

  &:hover {
    background-color: white;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
  }

  &:active {
    background-color: white;
    box-shadow: none;
  }
}

.upload-indication {
  margin: 0.5rem;
  text-align: left;
  width: 50%;

  @media only screen and (max-width: $responsive-width) {
    text-align: center;
    width: 100%;
  }
}

progress[value] {
  /* Reset the default appearance */
  appearance: none;
  border-radius: 5px;
  margin: 0.5rem 0 0.2rem 0.4rem;
  height: 1.5rem;
  width: 80%;
}

.success-upload {
  color: $success-green;
  font-weight: bold;
  margin-left: 0.5rem;
}

.error-message {
  color: $error-red;
  font-weight: bolder;
  margin: 1rem 0 0 0.5rem;
}

.card-container {
  align-content: center;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
