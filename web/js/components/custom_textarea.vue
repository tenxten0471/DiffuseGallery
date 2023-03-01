<template>
    <textarea v-model="tweet" ref="area" :style="styles"></textarea>
  </template>
  <script>
  export default {
      data() {
        return {
          tweet: this.value,
          height:"60px",
        };
      },
        props:{
        value:{type:String,default:'test'},
        // selectionChange_func:{type:Function,default:function(selected_text){console.log(selected_text)}},
      },
      computed:{
        styles(){
          return {
            "height": this.height,
          }
        }
      },
      watch:{
        tweet(){
            this.resize();
        },
        select_e(){
            console.log(this.select_e)
        }
      },
      methods:{
        resize(){
          this.height = "auto";
          this.$nextTick(()=>{
            this.height = this.$refs.area.scrollHeight + 'px';
          })
        }
      },
      mounted(){
        this.resize();
      }
    }
  </script>