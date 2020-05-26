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
      IdentityPoolId: 'us-east-1:fafe5de1-71f5-4c79-a9c8-6e09e0f650b2',
      s3: null, // placeholder for configured aws bucket
    };
  },

  methods: {
    submitFile() {
      const pic = document.getElementById('fileUpload').files;

      if (!pic.length) {
        console.log('no file selected');
      } else {
        const file = pic[0];
        const fileName = `${file.name}`;
        const params = {
          Key: fileName,
          ContentType: file.type,
          Body: file,
          ACL: 'public-read',
        };

        this.s3.putObject(params, (err, data) => {
          if (err) {
            console.log(`There is an error: ${err}`);
          } else {
            console.log(data); // success!
          }
        });
      }
    },

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
