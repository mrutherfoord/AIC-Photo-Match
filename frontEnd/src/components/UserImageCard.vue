<script>
export default {
  name: 'UserImageCard',

};
</script>

<template>
  <div class="userCard">
    <img
      id=uploadImg
      class=photo
    />
  </div>
</template>

<style lang="scss" scoped>
.userCard {
  border: 2px solid black;
  max-height: 800px;
  min-height: 400px;
  min-width: 300px;
}

.photo {
  max-height: 200px;
  text-align: center;
}
</style>
