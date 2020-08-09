<script>
export default {
  name: 'ResultImageCard',
  props: ['aicimgurl'],

};
</script>

<template>
  <div class="userCard">
    <img
      :src="aicimgurl"
      class="photo"
      />
  </div>
</template>

<style lang="scss" scoped>
.userCard {
  border: 2px solid black;
  max-height: 800px;
  min-height: 500px;
  min-width: 400px;
}

.photo {
  margin: 1rem 0;
  max-height: 300px;
  text-align: center;
}
</style>
