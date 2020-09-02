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
    role="main"
  >
    <h1 class="title">
      Art Institute of Chicago API Color Match App
    </h1>

    <p class="app-copy">
      This app will take an uploaded image, calculate the dominant color of that image, and then
      match it to a painting with the Art Institute of Chicago's (AIC) API database which contains
      the dominant color of the uploaded image within the artwork's top three dominant colors.
    </p>

    <UploadFile />

  </div><!-- main -->
</template>

<style lang="scss">
* {
  box-sizing: border-box;
}

body {
  background-color: #f0f0f0;
}

#app {
  color: #424242;
  font-family: Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin-top: 20px;
  text-align: center;
}

.title {
  color: #b50938; // AIC's logo color
  font-weight: lighter;
}

.app-copy {
  font-family: 'Times New Roman', Times, Georgia, serif;
  font-size: 1.2rem;
  margin: auto;
  text-align: left;
  width: 40rem;

  @media only screen and (max-width: $responsive-width) {
    width: 90%;
  }
}
</style>
