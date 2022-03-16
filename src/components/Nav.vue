<template>
  <nav class="navbar navbar-dark fixed-top bg-dark">
    <div class="navbar-brand">
      <img
        src="/logo.png"
        class="img-fluid d-none d-sm-block"
        style="max-height:60px;"
      />
    </div>
    <div
      class="text-white mr-auto ml-sm-auto"
      v-if="$store.getters.getLoginStatus"
    >
      <strong>Time remaining:</strong> <span :class='{"text-danger": lowtime}'>{{ $sec2min(timer) }}</span>
    </div>
    <form class="form-inline ml-2">
      <button class="btn btn-primary" type="button" @click="logout" v-if="$store.getters.getLoginStatus">
        End Assessment
      </button>
    </form>
  </nav>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "Nav",
  data(){
    return{
      lowtime: false
    }
  },
  computed: {
    ...mapGetters({
      timer: "getRemaining"
    })
  },
  watch: {
    timer: function() {
      if (this.timer < 180) {
        this.lowtime = true
      } else {
        this.lowtime = false
      }
    }
  },
  methods: {
    logout() {
      this.$store.commit("stop");
      this.$store.commit("clearTimers");
      this.$store.commit("removeUser");
      this.$router.push("/");
    }
  }
};
</script>

<style scoped></style>
