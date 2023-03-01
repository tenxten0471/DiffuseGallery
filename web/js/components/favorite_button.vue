<template>
	<div class="favorite_btn" @click="click"/>
</template>

<script>
	export default {

		data(){
			return {
				flag:this.flag_init,
			}
		},

		methods:{
		},
        
		props: {
        flag_init:{type:Boolean,default:false},
        click:{type:Function,default:function(){console.log(this.flag)}},
		},
		watch:{
			flag_init(){
				console.log('flagChange')
				this.flag = this.flag_init
			}
		},

	}
</script>

<style scoped>

.favorite_btn{
    display: block;
    background: v-bind(flag ? "#ef8c22" : "#88888820");
    clip-path: polygon(50% 5%, 61% 40%, 98% 40%, 68% 62%, 79% 96%, 50% 75%, 21% 96%, 32% 62%, 2% 40%, 39% 40%);
  }
</style>