window.$ = window.jQuery = require('jquery');
import 'startbootstrap-sb-admin-2/js/sb-admin-2'
import Vue from 'vue';
import axios from 'axios';

import '../scss/main.scss'

window.Vue = Vue

Vue.component('create-product', require('./components/product/CreateProduct.vue').default)

document.addEventListener('DOMContentLoaded', () => {
    axios.defaults.xsrfCookieName = 'csrftoken';  
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
  
    Vue.prototype.$axios = axios;
  
    const main = new Vue({
        el: '#app',
    })
  });
  
  
  
  
  