<script>
export default {
  name: 'ImageCard',

  props: {
    src: {
      type: String,
      default: '',
    },
    cardtitle: {
      type: String,
      default: '',
    },
    colortitle: {
      type: String,
      default: '',
    },
    red: {
      type: String,
      default: '',
    },
    green: {
      type: String,
      default: '',
    },
    blue: {
      type: String,
      default: '',
    },
  },

  computed: {
    computedColor() {
      return {
        'background-color': `rgb(${this.red}, ${this.green}, ${this.blue})`,
        height: '40px',
      };
    },
  },

};
</script>

<template>
  <div class="user-card">
    <h2 class="card-title">
      {{ cardtitle }}
    </h2>
    <div class="img-container">
      <img
        :src="src"
        class="photo"
      />
    </div>
    <div class="color-title">
      {{ colortitle }}
    </div>
    <div
      class="color-swatch"
      :style="computedColor"
    >
    </div>
  </div>
</template>

<style lang="scss" scoped>
.user-card {
  background-color: #fff;
  border-radius: 10px;
  max-height: 800px;
  min-height: 500px;
  min-width: 400px;
}

.img-container {
  height: 300px;
}

.photo {
  max-height: 300px;
  text-align: center;
}

.color-title {
  margin: 1rem 0;
}
</style>
