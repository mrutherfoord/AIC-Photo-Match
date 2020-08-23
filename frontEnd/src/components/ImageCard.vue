<script>
import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';

export default {
  name: 'ImageCard',

  components: {
    ClipLoader,
    PulseLoader,
  },

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
    imgloading: {
      type: Boolean,
      default: false,
    },
    rgbloading: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      spinnerColor: '#2c3e50', // color for all loading spinners
    };
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
      <div v-if="imgloading">
        <div class="bounce-loader">
          <ClipLoader
            :loading="imgloading"
            :color="spinnerColor"
          />
        </div>
      </div>
      <div v-else>
        <img
          :src="src"
          class="photo"
        />
      </div>
    </div>
    <div class="color-title">
      {{ colortitle }}
    </div>
    <div v-if="red">
      <!-- only need to test for one color value since all are computed simultaneously;
         - only show if values so that old color swatches aren't present while a new one
         - is being loaded
         -->
      <div
        class="color-swatch"
        :style="computedColor"
      >
      </div>
    </div>
    <div v-if="rgbloading">
      <PulseLoader
        :loading="rgbloading"
        :color="spinnerColor"
        :size="'10px'"
      />
    </div>
    <div v-else-if="red">
      <!-- only need to test for one color value since all are computed simultaneously -->
      <div class="rgb-value">
        rgb({{ red }}, {{ green }}, {{ blue }})
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
$responsive-width: 599px;

.user-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
  margin: 0.5rem 1rem 0.5rem 1rem;
  max-height: 800px;
  min-height: 500px;
  min-width: 400px;

  @media only screen and (max-width: $responsive-width) {
    min-width: 100%;
  }
}

.card-title {
  font-weight: 300;
}

.img-container {
  min-height: 300px;
}

.bounce-loader {
  align-items: center;
  display: flex;
  height: 300px;
  justify-content: center;
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
