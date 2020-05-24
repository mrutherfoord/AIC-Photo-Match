<template>
  <div id="app" role="main">
    <div class="pageLay">
      <h1 class="title">Welcome to this awesome AI Machine-Learning app of awesomeness!</h1>

      <UploadFile />

    </div><!-- pageLay -->
  </div>
</template>

<script>
import UploadFile from './components/UploadFile.vue';

export default {
  name: 'App',
  components: {
    UploadFile,
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.pageLay {
  margin: auto;
  width: 60%;
}
</style>
