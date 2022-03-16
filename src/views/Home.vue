<template>
    <div class="container">
  <div class="row">
    <div class="col">
        <h1 class="pt-5">Interviews</h1>
        <h3 class="text-muted pb-5">Subject Knowledge Assessment</h3>
        <form>
            <div class="form-group">
                <label for="nameInput">Your name</label>
                <input type="text" class="form-control" id="nameInput" placeholder="Your Name" v-model="name">
            </div>
            <div class="form-group">
                <label for="passwordInput">Passcode provider by interviewer</label>
                <input type="password" class="form-control" id="passwordInput" placeholder="Enter passcode" v-model="pass">
            </div>
            <div class="alert alert-danger" role="alert" v-if="errorAlert">
                {{errorAlert}}
            </div>
            <button type="button" class="btn btn-primary btn-block mt-4 p-3" @click="login">Enter</button>
        </form>
    </div>
  </div></div>
</template>

<script>
import axios from 'axios'

export default {
  name: "Home",
    data() {
      return {
          name: "",
          pass: "",
          errorAlert: null
      }
    },
  methods: {
      login(){
          const self = this
          self.errorAlert = null
          axios.post("https://backend-address/login", {
              name: self.name,
              pass: self.pass
          }).then(r => {
              self.$store.commit("setUser", r.data.uid)
              self.$store.commit("setTimeout", r.data.to)
              self.$store.commit("setTimer", r.data.tn)
              self.$router.push("/assess")
          }).catch(() => {
              self.errorAlert = "Unable to login. Are you sure that you entered the passcode correctly?"
          })
      }
  }
};
</script>
