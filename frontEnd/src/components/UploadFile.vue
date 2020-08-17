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
      success: false,
      error: false, // conditional for v-if error display
      errMessage: '', // generic placeholder for error messages
      noneSelected: false, // check value for if an image file has been selected
      bucketName: 'bradley-test-bucket',
      bucketRegion: 'us-east-1',
      IdentityPoolId: 'us-east-1:fafe5de1-71f5-4c79-a9c8-6e09e0f650b2',
      s3: null, // placeholder for configured aws S3 bucket
      uploadImg: '', // user submitted image, to be displayed
      returnAicUrl: '', // object holding the Lamda funtion returned data, as shown below
      aicBlue: '', // AIC API returned blue , red, green values
      aicRed: '',
      aicGreen: '',
      userGreen: '', // computed dominant color from uploaded image
      userRed: '',
      userBlue: '',
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
        this.aicBlue = '';
        this.aicRed = '';
        this.aicGreen = '';
        this.userRed = '';
        this.userBlue = '';
        this.userGreen = '';
        this.uploadImg = '';
        this.error = false;
        this.errMessage = '';
      }

      const pic = document.getElementById('fileUpload').files;

      if (pic.length === 0 || pic.length > 1) {
        this.noneSelected = true; // for resetting
      } else {
        this.noneSelected = false;
        const file = pic[0]; // only upload one file
        // TODO: fix upload preview
        const reader = new FileReader();
        // const output = document.getElementById('userImage');

        // loads image
        reader.addEventListener('load', (event) => {
          this.uploadImg = event.target.result;
        });
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
          this.returnAicUrl = result['aic colors'].url;
          // color of match
          this.aicRed = result['aic colors'].red;
          this.aicBlue = result['aic colors'].blue;
          this.aicGreen = result['aic colors'].green;
          // rgb computed from user uploaded image
          this.userRed = result['user colors'].user_red;
          this.userGreen = result['user colors'].user_green;
          this.userBlue = result['user colors'].user_blue;

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

    <div class="inputs">
      <label for="uploadbanner">
        Upload Your Image
      </label>
      <input
        id="fileUpload"
        name="myfile"
        type="file"
        accept=".jpg, .jpeg, .png"
        required
      />
    </div>

    <div class="inputs">
      <input
        id="submitImage"
        type="submit"
        value="Submit Image"
        @click="submitFile"
      />
    </div>

    <div class="upload-indication">
      <!-- only show progress bar whilst uploading -->
      <div v-if="upProg >0 && upProg < 100">
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
        <div
          v-else-if="noneSelected"
          class="error">
          Please select an image to upload.
        </div>
        <!-- placeholder for all error messages -->
        <div
          v-if="error"
          class="error">
          {{ errMessage }}
        </div>
      </div>
    </div>

    <div class="photo-container">

      <ImageCard
        cardtitle="Uploaded Image"
        :src="uploadImg"
        colortitle="Dominant Color of This Image"
        :red="userRed"
        :green="userGreen"
        :blue="userBlue"
        :rgbloading="rgbLoading"
      />
      <ImageCard
        cardtitle="AIC Match"
        :src="returnAicUrl"
        colortitle="Nearest Color Matched to AIC API"
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
.upload {
  margin: auto;
  text-align: center;
}

.inputs {
  padding: 10px;
}

.upload-indication {
  min-height: 3rem;
}

progress[value] {
  /* Reset the default appearance */
  appearance: none;
  height: 20px;
  width: 250px;
}

.message-container {
  margin: 0.5rem;
}

.success-upload {
  color: green;
  font-weight: bold;
}

.error {
  color: red;
  font-weight: bolder;
}

.photo-container {
  align-content: center;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  margin: auto;
  max-width: 100%;
  min-width: 80%;
}
</style>
