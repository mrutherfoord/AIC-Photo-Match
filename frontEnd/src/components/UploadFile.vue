<script>
import AWS from 'aws-sdk';

export default {
  name: 'UploadFile',

  data() {
    return {
      upProg: 0, // update progress html element
      success: false,
      error: false,
      noneSelected: false,
      uploadErrMessage: '',
      bucketName: 'bradley-test-bucket',
      bucketRegion: 'us-east-1',
      IdentityPoolId: 'us-east-1:fafe5de1-71f5-4c79-a9c8-6e09e0f650b2',
      s3: null, // placeholder for configured aws S3 bucket
      uploadImg: '', // user submitted image
      returnImgUrl: '', // aic generated image
    };
  },

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
  },

  methods: {
    submitFile() {
      // reset if there's an image
      if (this.uploadImg !== '') {
        this.uploadImg = '';
      }

      const pic = document.getElementById('fileUpload').files;

      if (pic.length === 0 || pic.length > 1) {
        this.noneSelected = true;
      } else {
        this.noneSelected = false;
        const reader = new FileReader();
        const file = pic[0]; // only upload one file
        const output = document.getElementById('uploadImg');

        reader.addEventListener('load', (event) => {
          output.src = event.target.result;
        });
        reader.readAsDataURL(file);

        const params = {
          Key: file.name,
          ContentType: file.type,
          Body: file,
          ACL: 'public-read',
        };

        this.s3.upload(params, (err) => {
          if (err) {
            this.error = true;
            this.uploadErrMessage = `Upload Error: ${err}`;
          } else {
            this.success = true;
            this.getResults();
          }
        })
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
          console.log(err, err.stack);
        } else {
          let result = JSON.parse(data.Messages[0].Body).Message;
          result = JSON.parse(result).Input['aic colors'].url;

          this.returnImgUrl = result;

          sqs.deleteMessage({
            QueueUrl: 'https://sqs.us-east-1.amazonaws.com/145918816538/AIC_SNS',
            ReceiptHandle: data.Messages[0].ReceiptHandle,
          }, (delErr, delData) => {
            if (delErr) {
              console.log(delErr);
            } else {
              console.log(delData);
            }
          });
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
        id="submit"
        type="submit"
        @click="submitFile"
      />
    </div>

    <progress
      id="showUpload"
      max="100"
      :value="upProg"
    />

    <div class="uploadStatus">
      <p
        v-if="success"
        class="success-upload">
        Upload Successful
      </p>
      <p
        v-else-if="error"
        class="error">
        {{ uploadErrMessage }}
      </p>
      <p
        v-else-if="noneSelected"
        class="error">
        Please select an image to upload
      </p>
    </div>

    <div class="photoConatiner">
      <img
        id="uploadImg"
        class="photo"
      />
      <img
        :src="returnImgUrl"
        class="photo"
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

progress[value] {
  /* Reset the default appearance */
  -webkit-appearance: none;
     -moz-appearance: none;
          appearance: none;

  width: 250px;
  height: 20px;
}

.success-upload {
  color: green;
}

.error {
  color: red;
}

.photoConatiner {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-content: center;
  width: 100%;
  max-height: 600px;
}

.photo {
  margin: 0 2rem 0 2rem;
  object-fit: contain;
}
</style>
