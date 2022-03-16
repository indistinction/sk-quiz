import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.config.productionTip = false;

Number.prototype.pad = function(size) {
  var s = String(this);
  while (s.length < (size || 2)) {s = "0" + s;}
  return s;
}

Vue.prototype.$sec2min = function(seconds) {
  if (seconds <= 0) {return "0:00"}
  else {
    let minutes = Math.floor(seconds / 60)
    let remainder = (seconds - (minutes * 60)).pad(2)
    return minutes.toString() + ":" + remainder
  }
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
