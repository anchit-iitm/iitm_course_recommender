<template>
  <router-view />
  <vtoast ref="vtoast"/>
</template>

<script>
import vtoast from './components/vtoast.vue'
export default {
  name: 'App', //or whatever your root is
    components:{
        vtoast
    },
    mounted() {
      this.$root.vtoast = this.$refs.vtoast
    },
}
</script>
