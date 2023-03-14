

<template>
    <div class="root" >
		<div class="generate_area">
			<div class="side_bar">
				<generate_setting></generate_setting>
				
			</div>
			
			<generated_image class="generated_image"></generated_image>
		</div>
		<switch_components class="menu">
			<template #switch>
				<floating_button class="menu_button" button_text="="></floating_button>
			</template>
			<template #components>
				<div class="menu_components">
					<!-- <floating_button button_text="history viewer" @click="switch_history"></floating_button> -->
					<floating_button button_text="delete_history" @click="delete_history"></floating_button>
				</div>
			</template>
			
		</switch_components>
		
    </div>
</template>

<script>
import floating_button from "./floating_button.vue";
import generate_setting from "./generate_setting.vue";
import generated_image from "./generated_image.vue";
import switch_components from "./switch_components.vue";

	export default {

		data(){
			return {
				
			}
		},

		methods:{
			print(data='notdata'){
				console.log(data);
				// eel.print_eel(data)
			},
			delete_history(){
				pywebview.api.delete_history()
			},


		},
        
		computed: {
		},
		props: {
			items_init:{type:Array,default:[]},
			colors: {type:Object,default:{
				accent : '#da3c41'
			}},
		},
		components: {
			floating_button,
			generate_setting,
			generated_image,
			switch_components,
		},
		mounted(){
			
		},
		watch:{
		},

	}
</script>
<style scoped>
/* html	{
} */
.root{
	display: flex;
	content: "";
	position: absolute;
	top: 0;left: 0;
	width: 100%;
	height: 100%;
	min-height: 100%;
	background: #f8f8fa;
	/* font-size: 5.46875%; */
}
.generate_area{
	display: flex;
	/* flex-direction: column; */
	width: 100%;
	height: 100%;
	min-height: 100%;
}
/* .generate_area > *{
	width: 100%;
	height: 100%;
} */
.side_bar{
	/* background-color: #151518; */
	width: 30%;
	min-width: 380px;
	height: 100%;
	filter: drop-shadow(3px 3px 5px  #5f5b7a97);
}
.side_bar > *{
	margin: 20px 0px 0px 10%;
}
.generated_image{
	width: 100%;
}
.menu{
	position: fixed;
	top: 20px;
	left: 20px;
}
.menu_button{
	width: 50px;
	height: 50px;
}
.menu_components{
	display: flex;
	flex-direction: column;
	justify-content: left;
	gap: 10px;
	margin: 10px;
}
.menu_components > *{
	width: 150px;
	height: 30px;
	transition: 0.2s;
}
.menu_components > *:hover{
	width: 300px;
}
</style>