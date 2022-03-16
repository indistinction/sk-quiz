import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {},
  state: {
    uid: null,
    timeout: null,
    running: false,
    timer: null
  },
  mutations: {
    setUser(state, payload) {
      state.uid = payload;
    },
    removeUser(state) {
      state.uid = null;
    },
    setTimeout(state, payload) {
      state.timeout = payload;
    },
    setTimer(state, payload) {
      state.timer = payload;
    },
    begin(state){
      state.running = true
    },
    stop(state){
      state.running = false
    },
    timerTick(state){
      if (state.running){
        if(state.timeout - state.timer){
          state.timer++
        } else {
          state.timeout = state.timer
        }
      }
    },
    clearTimers(state){
      state.timer = null
      state.timeout = null
    }
  },
  actions: {
    timerTick (context) {
      context.commit("timerTick");
    }
  },
  getters: {
    getUser(state){return state.uid},
    getRemaining(state){
      if (state.timer && state.timeout){
        return state.timeout - state.timer
      } else {
        return null
      }
    },
    getLoginStatus(state){
      if (state.uid){return true}
      else {return false}
    },
    isRunning(state){
      return state.running
    }
  }
});
