<template>
    <div class="cp_iptxt">
        <input class="ef" type="text" placeholder="" @input="search_func">
            <label>{{title || 'No props passed yet'}}</label>
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
	}
	.cp_iptxt input[type='text'] {
		font: 15px/24px sans-serif;
		box-sizing: border-box;
		width: 100%;
		letter-spacing: 1px;
		padding-left: 4em;
	}
	.cp_iptxt input[type='text']:focus {
		outline: none;
	}
	.ef {
		padding: 7px 14px;
		transition: 0.4s;
		border: 1px solid #121a2739;
		background: #ffffff;
	}
	.ef ~ .focus_line:before,
	.ef ~ .focus_line:after {
		position: absolute;
		top: 0;
		left: 0;
		width: 0;
		height: 2px;
		content: '';
		transition: 0.3s;
		background-color: v-bind(colors['accent']);
	}
	.ef ~ .focus_line:after {
		top: auto;
		right: 0;
		bottom: 0;
		left: auto;
	}
	.ef ~ .focus_line i:before,
	.ef ~ .focus_line i:after {
		position: absolute;
		top: 0;
		left: 0;
		width: 2px;
		height: 0;
		content: '';
		transition: 0.4s;
		background-color: v-bind(colors['accent']);;
	}
	.ef ~ .focus_line i:after {
		top: auto;
		right: 0;
		bottom: 0;
		left: auto;
	}
	.ef:focus ~ .focus_line:before,
	.ef:focus ~ .focus_line:after,
	.cp_iptxt.ef ~ .focus_line:before,
	.cp_iptxt.ef ~ .focus_line:after {
		width: 100%;
		transition: 0.3s;
	}
	.ef:focus ~ .focus_line i:before,
	.ef:focus ~ .focus_line i:after,
	.cp_iptxt.ef ~ .focus_line i:before,
	.cp_iptxt.ef ~ .focus_line i:after {
		height: 100%;
		transition: 0.4s;
	}
	.ef ~ label {
		position: absolute;
		z-index: -1;
		top: 10px;
		left: 14px;
		width: 100%;
		transition: 0.3s;
		letter-spacing: 0.5px;
		color: #aaaaaa;
	}
	.ef:focus ~ label,
	.cp_iptxt.ef ~ label {
		font-size: 12px;
		top: -18px;
		left: 0;
		transition: 0.3s;
		color: v-bind(colors['accent']);;
	}
</style>