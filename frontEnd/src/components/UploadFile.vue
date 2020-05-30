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
      // IdentityPoolId: 'farts',
      IdentityPoolId: 'us-east-1:fafe5de1-71f5-4c79-a9c8-6e09e0f650b2',
      s3: null, // placeholder for configured aws S3 bucket
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
      const pic = document.getElementById('fileUpload').files;

      if (pic.length === 0 || pic.length > 1) {
        this.noneSelected = true;
      } else {
        this.noneSelected = false;

        const file = pic[0]; // only upload one file
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
      const params = {
        apiVersion: '2010-03-31',
        endpoint: 'https://sqs.us-east-1.amazonaws.com/145918816538/AIC_SNS',
      };
      const sqs = new AWS.SNS(params);

      console.log(sqs);
    },
  },

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

  </div>
</template>


<style scoped lang="scss">
.upload {
  margin: auto;
  text-align: left;
  width: 50%;
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

</style>
