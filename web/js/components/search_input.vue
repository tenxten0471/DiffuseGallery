<template>
    <div class="cp_iptxt">
        <input class="ef" type="text" placeholder="" @input="search_func">
            <label class="text">{{title || 'No props passed yet'}}</label>
        <span class="focus_line"><i></i></span>
    </div>
</template>

<script>
	export default {

		/* == data == リアクティブ・データ登録 */
		data(){
			return {
				// title: 'test',
			}
		},

		methods:{
		},
		/* == props == テンプレートタグの属性を登録 */
		props: {
			title: String,
			colors: {type:Object,default:{
				accent : '#da3c41'
			}},
			search_func:{type:Function,default:function(e){console.log(e.target.value)}}
		}

	}
</script>

<style scoped>
	.cp_iptxt {
		position: relative;
		/* width: 80%;
		margin: 40px 3%; */
		border-radius: 15px;
		border: 1px solid #aaaaaa00;
		overflow: hidden;
	}
	/* .cp_iptxt:hover {
		border: 1px solid #aaaaaa00;
	} */
	.cp_iptxt:focus-within, .cp_iptxt:hover{
		filter: drop-shadow(1px 1px 5px  #aa888830);
	}
	.cp_iptxt input[type='text'] {
		font: 15px/24px sans-serif;
		outline: none;
		box-sizing: border-box;
		width: 100%;
		letter-spacing: 1px;
		padding-left: 1em;
		border: 0;
		/* background: transparent; */
	}
	/* .ef:focus{
		filter: drop-shadow(3px 3px 3px #888888);
	} */
	/* .cp_iptxt input[type='text']:focus {
	} */
	.focus_line::after{
		position: absolute;
		bottom:0; left:0;
		z-index: 2;
		width: 0;
		background-color: v-bind(colors['accent']);
	}
	.cp_iptxt input[type='text']:focus ~ .focus_line::after{
		width: 100%;
		height: 1px;
	}
	.text {
		position: absolute;
		z-index: 1;
		top: 10%;
		left: 14px;
		/* width: 25%; */
		transition: 0.3s;
		letter-spacing: 0.5px;
		color: #aaaaaa;
		/* border-right: 1px solid #88888830; */
		/* background: v-bind(colors['accent']); */
	}
	.ef:not([value=""]) ~ .text{
		left: -200px;
	}

</style>