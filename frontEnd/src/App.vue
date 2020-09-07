<script>
import UploadFile from './components/UploadFile.vue';
import AppFooter from './components/Footer.vue';

export default {
  name: 'App',
  components: {
    UploadFile,
    AppFooter,
  },
};
</script>

<template>
  <div
    id="app"
    role="main"
  >
    <div class="content">
      <h1 class="title">
        Art Institute of Chicago API Color Match App
      </h1>

      <p class="app-copy">
        This app will take an uploaded image, calculate the dominant color of that image, and then
        match it to a painting with the Art Institute of Chicago's (AIC) API database which contains
        the dominant color of the uploaded image within the artwork's top three dominant colors.
      </p>

      <UploadFile />
    </div>

    <footer>
      <AppFooter />
    </footer>

  </div><!-- main -->
</template>

<style lang="scss">
* {
  box-sizing: border-box;
}

body {
  background-color: #eee;
  margin: 0;
}

#app {
  color: #424242;
  display: flex; // boilerplate to keep footer down below
  flex-direction: column; // footer at the botom ;)
  font-family: Helvetica, Arial, sans-serif;
  height: 100vh; // needed to stick the footer to bottom
  text-align: center;
}

.content {
  flex: 1 0 auto; // grow page space to content
}

footer {
  /* Prevent Chrome, Opera, and Safari from letting these items shrink to smaller than their
  content's default minimum size. */
  flex-shrink: 0;
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
