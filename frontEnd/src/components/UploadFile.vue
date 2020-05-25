<template>
  <div class="upload">

      <div class="inputs">
        <label for="uploadbanner">
          Upload Your Image
        </label>
        <input id="fileUpload" name="myfile" type="file"
               accept="image/jpg, image/jpeg, image/png" />
      </div>

      <div class="inputs">
        <input type="submit" @click="submitFile" id="submit" />
      </div>

      <!-- <progress id="show" max="100" value="0"></progress> -->

  </div>
</template>

<script>
import AWS from 'aws-sdk';

export default {
  name: 'UploadFile',

  data() {
    return {
      bucketName: 'bradley-test-bucket',
      bucketRegion: 'us-east-1',
      IdentityPoolId: 'melAiApp',
      s3: null, // placeholder for configured aws bucket
    };
  },

  methods: {
    submitFile() {
      const pic = document.getElementById('fileUpload').files;

      if (!pic.length) {
        console.log('no file selected');
      } else {
        AWS.config.update({
          region: this.bucketRegion,
          credentials: new AWS.CognitoIdentityCredentials({
            IdentityPoolId: this.IdentityPoolId,
          }),
        });

        this.s3 = new AWS.S3();

        const file = pic[0];
        const fileName = file.name;
        const params = {
          Bucket: this.bucketName,
          Key: fileName,
          Body: file,
          ACL: 'public-read',
        };

        this.s3.putObject(
          params,
          (err, data) => {
            if (err) {
              console.log(`There is an error: ${err}`);
            } else {
              console.log(data);
            }
          },
        );
      }
    },

  },

};
</script>

<style scoped lang="scss">
.upload {
  margin: auto;
  text-align: left;
  width: 50%;
}

.inputs {
  padding: 10px;
}
</style>
