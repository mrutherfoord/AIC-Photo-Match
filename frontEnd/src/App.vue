<script>
import UploadFile from './components/UploadFile.vue';

export default {
  name: 'App',
  components: {
    UploadFile,
  },
};
</script>

<template>
  <div
    id="app"
    role="main">
    <div class="page-lay">
      <h1 class="title">
        Art Institute of Chicago API Color Match App
      </h1>
      <p class="app-copy">
        This app will take an uploaded image, decipher the dominant color of that image, and match
        it to a painting with the Art Institute of Chicago's API database that contains the dominant
        color of the uploaded image within the artwork's top three dominant colors.
      </p>

      <UploadFile />

    </div><!-- pageLay -->
  </div><!-- main -->
</template>

<style lang="scss">
body {
  background-color: #f0f0f0;
}

#app {
  color: #2c3e50;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin-top: 60px;
  text-align: center;
}

.app-copy {
  margin: auto;
  width: 50%;
}

.page-lay {
  margin: auto;
}
</style>
