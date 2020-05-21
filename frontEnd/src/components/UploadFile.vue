<template>
  <div class="upload">
    <form id="uploadbanner" enctype="multipart/form-data" method="post">

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

      <div id="show"></div>

    </form>
  </div>
</template>

<script>
import AWS from 'aws-sdk';

export default {
  name: 'UploadFile',

  data() {
    return {
      bucketName: 'mrutherfoordtestbucket',
      bucketRegion: 'US East (N. Virginia) us-east-1',
      IdentityPoolId: 'melAiApp',
      s3: null, // placeholder for configured aws bucket
    };
  },

  methods: {
    submitFile() {
      const pic = document.getElementById('fileUpload').files;

      if (pic) {
        const file = pic[0];
        const fileName = file.name;
        const filePath = `${this.bucketName}/${fileName}`;
        // change to bucket name
        // const fileUrl = `https://${this.bucketRegion}.amazonaws.com/my-first-bucket/${filePath}`;

        this.s3
          .upload({
            Key: filePath,
            Body: file,
            ACL: 'public-read',
          }, (err, data) => {
            if (err) {
              throw err;
            }
            console.log(data);
            alert('Successfully Uploaded!');
          });
        /*
         * .on('httpUploadProgress', (progress) => {
         *   let uploaded = parseInt((progress.loaded * 100) / progress.total);
         *   $('progress').attr('value', uploaded);
         * });
         */
      }
    },
  },

  mounted() {
    // configure the aws bucket
    AWS.config.update({
      region: this.bucketRegion,
      credentials: new AWS.CognitoIdentityCredentials({
        IdentityPoolId: this.IdentityPoolId,
      }),
    });

    this.s3 = new AWS.S3({
      apiVersion: '2006-03-01',
      params: { Bucket: this.bucketName },
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
