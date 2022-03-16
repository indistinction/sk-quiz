<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <h1 class="pt-5">Interviews</h1>
        <h3 class="text-muted pb-5">Staff Page</h3>
      </div>
    </div>
    <div class="row" v-if="results">
      <div class="col-12 text-left">
        <h3 class="text-muted pb-3">Recent Results</h3>
          <div class="row">
        <div v-for="result in results" :key="result.id" class="col-md-3 border bg-white rounded p-3 m-3">
            <h5>{{ result.name }}</h5>
            <div>Time taken: {{ $sec2min(result.timetaken) }}</div>
            <div>Biology: {{ result.B.toFixed(0) }}%</div>
            <div>Chemistry: {{ result.C.toFixed(0) }}%</div>
            <div>Physics: {{ result.P.toFixed(0) }}%</div>
        </div>
          </div>
      </div>
    </div>
    <div class="row" v-else>
        <div class="col-12">
      <div class="alert alert-danger" role="alert" v-if="errorAlert">
        {{ errorAlert }}
      </div>
      <div class="form-group">
        <label for="passwordInput">Enter staff passcode</label>
        <input
          type="password"
          class="form-control"
          id="passwordInput"
          placeholder="Enter passcode"
          v-model="pass"
        />
      </div>
      <button
        type="button"
        class="btn btn-primary btn-block mt-4 p-3"
        @click="login"
      >
        Submit
      </button>
        </div>
    </div>
  </div>
</template>

<script>
    import axios from 'axios'
export default {
  name: "Staff",
  data() {
    return {
      pass: null,
      results: null,
        errorAlert: null
    };
  },
  methods: {
    login() {
        var self=this
        axios.post("https://backend/res", {pass:self.pass})
                .then(r => {
            self.results = r.data
        })
                .catch(() => {self.errorAlert = "Error logging in - please try again."})
    }
  }
};
</script>

<style scoped></style>
