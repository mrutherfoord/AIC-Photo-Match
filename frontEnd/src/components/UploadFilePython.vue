<script>
export default {
  name: 'UploadFilePython',

  data() {
    return {
      upProg: 0, // update progress html element
      success: false,
      error: false,
      noneSelected: false,
      uploadErrMessage: '',
      uploadImg: '', // user submitted image
      returnImgUrl: '', // aic generated image
    };
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
      }
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

<style scoped>
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
</style>>
