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
      type: Number,
      default: undefined,
    },
    green: {
      type: Number,
      default: undefined,
    },
    blue: {
      type: Number,
      default: undefined,
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
      <div>
        <img
          :src="src"
          class="photo"
        />
      </div>
    </div>
    <!-- only need to test for one color value since all are computed simultaneously;
      - only show if values so that old color swatches aren't present while a new one
      - is being loaded
    -->
    <div v-if="red">
      <div class="color-title">
        {{ colortitle }}
      </div>
      <div
        class="color-swatch"
        :style="computedColor"
      >
      </div>
      <div class="rgb-value">
        rgb({{ red }}, {{ green }}, {{ blue }})
      </div>
    </div><!-- v-if red -->
  </div>
</template>

<style scoped lang="scss">

.user-card {
  animation: fadein 1.5s;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: $shadow-depth-2;
  margin: 0.5rem 1rem 0.5rem 1rem;
  max-height: 800px;
  min-height: 500px;
  min-width: 400px;

  @keyframes fadein {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @media only screen and (max-width: $responsive-width) {
    min-width: 100%;
  }
}

.card-title {
  font-weight: 400;
}

.img-container {
  min-height: 300px;
}

.photo {
  height: 300px;
  max-width: 100%;
  object-fit: contain;
  text-align: center;
}

.color-title {
  margin: 1rem 0;
}

.rgb-value {
  font-size: 1.25rem;
  margin: 0.5rem 0;
}
</style>
