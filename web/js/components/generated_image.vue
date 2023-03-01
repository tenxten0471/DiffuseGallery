<template>
	<div>

		<div class="image_container" v-if="!is_generating">
			<p v-if="images.length == 0">no images</p>
			<div class="image_wrapper" v-for="(image, i) in images">
				<img class="image" :src="image.src">
				<div class="buttons">
					<floating_button :click="function(){image_show(i)}" button_text="show">show</floating_button>
					<floating_button :click="function(){image_save(i)}" button_text="save">save</floating_button>
				</div>
			</div>
		</div>
		
		<div class="generating_guage" v-if="is_generating">
			<a>generating...</a>
			<meter min="0" :max="meter_param.max" :value="meter_param.value"></meter>
		</div>
	</div>
</template>

<script>
	import floating_button from "./floating_button.vue";
	export default {

		data(){
			return {
				images:this.images_init,
				is_generating:false,
				meter_param:{
					max:20,
					value:0
				}
			}
		},

		methods:{
			async image_show(i){
				pywebview.api.image_show(this.images[i])
			},
			async image_save(i){
				pywebview.api.image_save(this.images[i])
			},
			update_images(images){
				this.images = images
				this.is_generating = false
			},
			set_meter(step_now, steps){
				this.is_generating = true
				this.meter_param = {
					max:steps,
					value:step_now
				}
			},
		},
        
		props: {
			images_init:{
				type:Array,
				default:[]
			},
		},
		components: {
			floating_button,
		},
		mounted() {
			generated_images_update_func = this.update_images
			set_meter_func = this.set_meter
		}

	}
</script>

<style scoped>
.buttons{
	display: flex;
	position: absolute;
	bottom: 10px;
	right: 10px;
}
.image_container{
	display: flex;
	flex-direction: column;
	align-items: center;
	/* justify-content: center; */
	width: 100%;
	height: 100%;
	gap: 20px;
	overflow: scroll;
}
.generating_guage{
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	width: 100%;
	height: 100%;

}
.generating_guage > *{
	max-width: 500px;
	width:40%
}
.image_wrapper{
	/* width: 100%; */
	display: flex;
	position: relative;
	/* margin: v-bind(images.length > 1 ? "5px" : "auto"); */
	margin: auto;
	object-fit: contain;
	
	/* max-width: 100%;
	max-height: 100%; */
}
.image {
	width: 100%;
	object-fit: contain;
	filter: drop-shadow(3px 3px 10px  #646c78);
}
</style>