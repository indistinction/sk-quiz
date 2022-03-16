<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <h1 class="pt-5">PGCE Science Interviews</h1>
        <h3 class="text-muted pb-5">Subject Knowledge Assessment</h3>
        <div class="alert alert-danger" role="alert" v-if="errorAlert">
          {{ errorAlert }}
        </div>
      </div>
    </div>
    <div class="row" v-if="started">
      <div class="col-12 text-left bg-white rounded border py-3">
        <p>{{ currentQ + 1 }}. {{ questions[currentQ]["Q"] }}</p>
        <div class="alert alert-danger text-center mb-1" style="min-height: 180px;" v-if="cheated.includes(currentQ)" role="alert">
          <div class="pt-3 mt-4">These answers have been locked as the window was exited. You may continue to answer other questions.</div>
        </div>
        <div class="p-2 w-100 pointer my-1 rounded border"
             :class='{"bg-primary": answers[key]}'
             v-for="(text, key) in questions[currentQ]['As']"
             :key="key"
             @click="answer(questions[currentQ]['qid'].toString() + '#' + text, key)"
             v-else
        >
          <div>
            {{ text }}
          </div>
        </div>
      </div>
      <div class="col-12">
        <button class="btn btn-primary mr-2 px-4 py-4 mt-3" @click="back" v-if="!hideback">&lt; Back</button>
        <button class="btn btn-primary ml-2 px-4 py-4 mt-3" @click="next" v-if="!hidenext">Next &gt;</button>
      </div>
    </div>
    <div class="row" v-else>
      <div class="col-12 text-left">
        <p>
          Please answer the questions below. They are a random selection of 60
          multiple choice questions based on the Key Stage 3 Science National
          Curriculum programmes of study.
        </p>
        <p>
          As all PGCE Science students are required to teach all three sciences
          up to KS3, these questions are a combination of biology, chemistry,
          and physics.
        </p>
        <p>
          You do not need to save your answers, they will be saved
          automatically.
        </p>
        <p>
          Your time limit is shown in the above. <em>Please do not leave this page
          or refresh your browser as you may lose access to your answers</em>.
        </p>
        <p>When you are ready to begin, please click the button below.</p>
      </div>
      <button
        type="button"
        class="btn btn-success btn-block p-3"
        @click="start"
      >
        Click to begin
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Main",
  data() {
    return {
      started: false,
      interval: null,
      questions: [],
      errorAlert: null,
      currentQ: 0,
      answers: {},
      hidenext: false,
      hideback: true,
      cheated: []
    };
  },
  watch: {
    currentQ: function (){
        if (this.currentQ === 0) {
        this.hideback = true;
        } else {
        this.hideback = false;
        }


if (this.currentQ === this.questions.length - 1) {
this.errorAlert = "You have completed the final question. You may close this window or click 'End Assessment' above."
        this.hidenext = true
      } else {
               this.hidenext = false;
               }

    }
  },
  methods: {
    start() {
      this.started = true;
      this.$store.commit("begin");
    },
    next() {
      if (this.currentQ < this.questions.length - 1) {
        this.currentQ++;
      }
    },
    back() {
      if (this.currentQ > 0) {
        this.currentQ--;
      }
    },
    answer(text, key) {
      const self = this
      let qid = key.split(".")[0]
      axios
        .post(
          "https://backend/a",
          {
            a: text
          },
          {
            headers: {
              "x-token": self.$store.getters.getUser
            }
          }
        )
        .then(() => {
          self.answers[qid + ".1"] = false
          self.answers[qid + ".2"] = false
          self.answers[qid + ".3"] = false
          self.answers[qid + ".4"] = false
          self.answers[key] = true
          self.next()
          self.$forceUpdate()
        })
        .catch(err => {
          if (err.response.status < 500) {
            self.errorAlert = err.response.data
          }
        });
    },
    tickover() {
      this.$store.dispatch("timerTick");
    },
    windowBlur (){
    if (this.currentQ !== 0){
      this.cheated.push(this.currentQ)
      this.$forceUpdate()
      }
    }
  },
  created() {
    const self = this;
    self.interval = setInterval(self.tickover, 1000);

    window.addEventListener('blur', this.windowBlur)

    axios
      .get("https://backend/qs", {
        headers: {
          "x-token": self.$store.getters.getUser
        }
      })
      .then(response => {
        self.questions = response.data;
      })
      .catch(() => {
        self.errorAlert =
          "Error getting questions. Please inform your interviewer.";
      });
  },
  destroyed() {
    clearInterval(this.interval);
    window.removeEventListener('blur', this.windowBlur)
  }
};
</script>

<style scoped>
  .pointer {cursor: pointer;}


</style>
