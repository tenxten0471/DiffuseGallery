<template>
	<div id="input_area">

		<div class="container">
			<a>model :  </a>
			<select v-model="models.selected">
				<option v-for="v,k in models.models" :value="k">{{ k }}</option>
			</select>
		</div>
		<div class="container">
			<a>scheduler :  </a>
			<select v-model="schedulers.selected">
				<option v-for="k in schedulers.schedulers" :value="k">{{ k }}</option>
			</select>
		</div>
		<div class="container">
			<floating_button button_text="model_load" @click="set_model"></floating_button>
		</div>

		<hr>

		<div class="container">
			<a>generate_config :  </a>
			<select v-model="configs.selected">
				<option v-for="v,k in configs.configs" :value="k">{{ k }}</option>
			</select>
			<floating_button button_text="load" @click="load_generate_config"></floating_button>
			<floating_button button_text="delete" @click="delete_generate_config"></floating_button>
		</div>

		<hr>

		<div class="container prompt">
			<a>prompt :  </a>
			<textarea id="prompt" class="textarea" v-model="generate_config.prompt" />
		</div>

		<div class="container prompt">
			<a>negative_prompt :  </a>
			<textarea id="negative_prompt" class="textarea" v-model="generate_config.negative_prompt" />
		</div>

		<div class="container">
			<a>num_steps :  </a>
			<input type="number" class="num" v-model="generate_config.num_inference_steps">
			<input type="range" id="num_inference_steps" min="0" max="100" v-model="generate_config.num_inference_steps">
		</div>

		<div class="container">
			<a>num_images :  </a>
			<input type="number" class="num" v-model="generate_config.num_images_per_prompt">
			<input type="range" id="num_inference_steps" min="0" max="100" v-model="generate_config.num_images_per_prompt">
		</div>

		<div class="container">
			<a>width :  </a>
			<input type="number" class="num" v-model="generate_config.width">
			<input type="range" id="width" min="0" max="2048" step="64" v-model="generate_config.width">
		</div>

		<div class="container">
			<a>height :  </a>
			<input type="number" class="num" v-model="generate_config.height">
			<input type="range" id="height" min="0" max="2048" step="64" v-model="generate_config.height">
		</div>
		
			

		<div class="container">
			<floating_button class="button" button_text="generate" @click="generate"></floating_button>
			<floating_button button_text="save_config" @click="save_generate_config"></floating_button>
		</div>
		

	</div>
</template>

<script>
	import floating_button from "./floating_button.vue";
	export default {

		data(){
			return {
				models : this.models_init,
				configs:this.configs_init,
				generate_config : this.generate_config_init,
				schedulers:{},
			}
		},

		methods:{
			generate(){
				pywebview.api.image_generate(this.generate_config)
			},
			set_model(){
				pywebview.api.set_model(this.models.selected, this.schedulers.selected)
			},
			async load_generate_config(){
				this.generate_config = await pywebview.api.get_generate_config(this.configs.selected)
			},
			delete_generate_config(){
				if (window.confirm('Delete generate_config, are you sure?')){
					pywebview.api.delete_generate_config(this.configs.selected)
				}
			},
			save_generate_config(){
				var name = window.prompt("Please config name", "")
				if (name){
					pywebview.api.save_generate_config(name,this.generate_config)
					this.init_load()
				}
				
				
			},
			async init_load(){

				this.models = await pywebview.api.get_model_data()
				this.configs = await pywebview.api.get_config_data()
				this.generate_config = await pywebview.api.get_generate_config()
				this.schedulers = await pywebview.api.get_schedulers()
			},
		},
        
		props: {
			models_init:{
				type:Object,
				default:{
				}
			},
			configs_init:{
				type:Object,
				default:{
				}
			},
			generate_config_init:{
				type:Object,
				default:{
					prompt:'',
					negative_prompt:'',
					num_inference_steps:20,
					num_images_per_prompt:1,
					width:448,
					height:768,
				}
			},
		},
		components: {
			floating_button,
		},
		mounted(){
			this.init_load()
			// pywebview.api.get_model_data().then(function(r){this.models = r.message})
			// pywebview.api.get_config_data().then(function(r){this.configs = r.message})
			// pywebview.api.get_generate_config().then(function(r){this.generate_config = r.message})
		},

	}
</script>

<style scoped>
	#input_area{
		display: flex;
		flex-direction: column;
		justify-content: center;
	}
	#input_area > *{
		margin: 10px 0px;
	}
	/* #input_area *{
		width: 100%;
	} */
	.textarea{
		border: 0px;
		height: 60px;
		max-width: 100%;
		min-width: 100%;
	}
	.container{
		display: flex;
		justify-content: end;
		width: 100%;
		gap: 10px;

	}
	.prompt{
		flex-direction: column;
		justify-content: start;
	}
	.num{
		background-color: transparent;
		width: 40px;
		border: 0px;
		border-bottom: 1px solid #3a4d6c;
	}
	.button{
		width: 30%;
	}
</style>