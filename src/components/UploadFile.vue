<template>
  <div class="upload">
    <form id="uploadbanner" enctype="multipart/form-data" method="post" action="#">
      <div class="inputs">
      <label for="uploadbanner">
        Upload your photo
      </label>
      <input id="fileupload" name="myfile" type="file" />
      </div>
      <div class="inputs">
      <input type="submit" value="submit" id="submit" />
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'UploadFile',
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.upload {
  text-align: center;
}

.inputs {
  padding: 10px;
}
</style>
