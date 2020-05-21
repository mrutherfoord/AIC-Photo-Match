import Vue from 'vue';
import App from './App.vue';

// require('aws-sdk/clients/s3');

Vue.config.productionTip = false;

new Vue({
  render: (h) => h(App),
}).$mount('#app');
