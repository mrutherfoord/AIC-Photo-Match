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
    <h1 class="title">
      Art Institute of Chicago API Color Match App
    </h1>

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
  color: #2c3e50;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin-top: 20px;
  text-align: center;
}

</style>
