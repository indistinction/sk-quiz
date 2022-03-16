<template>
  <div id="app">
    <navbar></navbar>
    <div v-if="ie===true">
      <p class="mt-5 pt-5">Unfortunately our interview questions are not available using the Internet Explorer browser.</p>
      <p>Please use a more modern browser to complete your assessment, for example Chrome, Safari, Firefox, Opera, or Edge.</p>
    </div>
    <div v-if="ie===false">
    <router-view class="mt-5 pt-5"/>
    </div>
    <!--footer class="footer mt-auto py-3">
      <div class="container">
        <span class="text-muted">Place sticky footer content here.</span>
      </div>
    </footer-->
  </div>
</template>

<script>
  import Nav from "@/components/Nav.vue";

  export default {
    data() {
      return {
        ie: null
      };
    },
    components: {
      navbar: Nav
    },
    mounted(){
      if (window.navigator.userAgent.indexOf('MSIE ') > 0) {
        // IE 10 or older => return version number
        this.ie = true;
      } else if (window.navigator.userAgent.indexOf('Trident/') > 0) {
        // IE 11 => return version number
        this.ie = true;
      } else {
        this.ie = false;
      }
    }
  }

</script>

<style>
  #app {
    font-family: "Roboto", sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    font-weight: lighter;
    font-variant-ligatures: common-ligatures;
  }

  h1,
  h2,
  h3,
  h4,
  h5 {
    font-weight: 800 !important;
    font-family: "Roboto Slab", serif;
  }

  .bg-pale{
    background-color: #ccc;
  }

</style>
