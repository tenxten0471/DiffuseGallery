
<template>
	<div class='card'>
    <div class="edit edit_end" v-if="edit" @click="edit_completed"/>
    <favorite_button class="favorite_btn" :flag_init="favorite" v-if="item.update_date" @click="set_favorite"/>
    <div class='card_content'>
      <div class="edit edit_start" v-if="!edit" @click="edit_activate"/>
      <div v-if="edit">{{item.update_date ? isChanged ? "*editing" : "editing" : isChanged ? "*creating" : "creating"}}</div>
      <div class='date'>update : {{item.update_date || "---- -- -- --:--:--"}}</div>
      <div class="line" />
      <div class='text' v-if="!edit" v-html="md_parced_text"></div>
      <div class='tags' v-if="!edit">{{tags}}</div>
      
      <div class='input_area' v-if="edit">
        <div class="discription">text:</div>
        <custom_textarea ref='textarea' class = 'text input' v-model="text" :value="text" />
        <div class="discription">tags:</div>
        <input class = 'tags input' v-model="tags"/>
        <div class="input_length discription" v-text="'input_length : '+ text.length"/>
      </div>
      
      <div class="buttons" v-if="edit">
        <floating_button class="cancel_btn" button_text="canceled" @click="edit_canceled"/>
        <floating_button class="delete_btn" @click="call_delete" button_text="delete" v-if="item.update_date"/>
      </div>

    </div>
    
  </div>
</template>

<script>
  import floating_button from "./floating_button.vue";
  import favorite_button from "./favorite_button.vue";
  import custom_textarea from './custom_textarea.vue'
  export default {
    data() {
      return {
        text:this.item.text,
        tags:this.item.tags,
        favorite:this.item.isfavorite == "True",
        edit:this.edit_init,
        print:'',
        input_height:'20',
        // selected_text:'',
      }
    },
    props:{
        // id:{type:String,default:'-1'},
        // text_init:{type:String,default:'init'},
        // tags_init:{type:String,default:'pytorch python 機械学習'},
        item:{type:Object,default:{text:"",tags:"",favorite:false}},
        edit_complete_func:{type:Function,default:function(item,text,tags,favorite){console.log(text)}},
        set_favorite_func:{type:Function,default:function(item,text,tags,favorite){console.log(text)}},
        edit_cancel_func:{type:Function,default:function(){console.log('canceled!')}},
        delete_func:{type:Function,default:function(){console.log('delete_default!')}},
        edit_init:{type:Boolean,default:false},
    },
    computed:{
      isChanged(){
        let dropped = !this.item.update_date && this.text ? true : false
        return (this.item.text != this.text || this.item.tags != this.tags) && this.item.update_date || dropped
      },
      md_parced_text(){
        // this.text = this.to_halfwidth(this.text)
        return markdown.parse(this.text) || this.text
      },
    },
    watch:{
      item(){
        this.init()
        this.favorite = this.item.isfavorite == "True"
        this.edit = false
      },
      text(){
        this.text = this.to_halfwidth(this.text)
      },
      tags(){
        this.tags = this.to_halfwidth(this.tags)
      },
    },
    methods: {
      onInput_text(e) {
        this.text = to_halfwidth(e.target.value)
      },
      onInput_tags(e) {
        this.tags = to_halfwidth(e.target.value)
      },
      // selected(e){
      //   this.selected_text = window.getSelection().toString()
      // },
      edit_activate(){
        this.edit = true
      },
      edit_completed(){
        this.edit = false
        if(this.isChanged){
          this.edit_complete_func(this.item,this.text,this.tags,this.favorite)
        }else{
          this.edit_canceled()
        } 
      },
      edit_canceled(){
          this.edit = false
          this.init()
          this.edit_cancel_func()
      },
      call_delete(){
        this.delete_func(this.item,this.text,this.tags,this.favorite)
      },
      set_favorite(){
        this.favorite = !this.favorite
        this.set_favorite_func(this.item,this.item.text,this.item.tags,this.favorite,!this.edit)
      },
      init(){
        this.text = this.item.text
        this.tags = this.item.tags
        // this.favorite = this.item.favorite
      },
      to_halfwidth(strVal){
        // 半角変換
        var halfVal = strVal.replace(/[！-～]/g,
          function( tmpStr ) {
            // 文字コードをシフト
            return String.fromCharCode( tmpStr.charCodeAt(0) - 0xFEE0 );
          }
        );
      
        // 文字コードシフトで対応できない文字の変換
        return halfVal.replace(/”/g, "\"")
          .replace(/’/g, "'")
          .replace(/‘/g, "`")
          .replace(/￥/g, "\\")
          .replace(/　/g, " ")
          .replace(/〜/g, "~");
      },
    },
    components: {
      custom_textarea,
      floating_button,
      favorite_button,
    },
  }
</script>

<style scoped>
  .card{
    position:relative;
    z-index: v-bind(edit ? 10 : 0);
    width:95%;
    border-radius:5px;
    line-height: 1.45em;
    margin: 0 auto 15px;
    -webkit-transition: height 0.3s ease;
            transition: height 0.3s ease;
    /* -webkit-box-shadow: 1px 3px 7px -3px rgba(0, 0, 0, 0.4);
            box-shadow: 1px 3px 7px -3px rgba(0, 0, 0, 0.4); */
  }
  .card:hover {
    /* -webkit-box-shadow: 0 3px 7px -3px rgba(0, 0, 0, 0.7);
            box-shadow: 0 3px 7px -3px rgba(0, 0, 0, 0.7); */
    -webkit-box-shadow: 1px 3px 7px -3px rgba(0, 0, 0, 0.4);
            box-shadow: 1px 3px 7px -3px rgba(0, 0, 0, 0.4);
	}
  .favorite_btn{
    /* display: block; */
    position: absolute;
    /* top: 0;left: 0; */
    z-index: 25;
    margin: 10px;
    width: 25px;
    height: 25px;
    /* background: #111111; */

    /* background: v-bind(favorite ? "#ef8c22" : "#88888820");
    clip-path: polygon(50% 5%, 61% 40%, 98% 40%, 68% 62%, 79% 96%, 50% 75%, 21% 96%, 32% 62%, 2% 40%, 39% 40%); */
  }
  .card_content{
    position:relative;
    z-index: 10;
    display:block;
    border-radius:5px;
    /* border-radius: 3px; */
    overflow-x: hidden;
    overflow-wrap: break-word;
    word-break: break-word;
    background: #ffffff;
    padding:20px ;
    /* word-wrap: break-word; */
  }
  .card_content * {
  	overflow-wrap: break-word;
    display:flex;
    justify-content: flex-end;
    
  }
  .line{
    display:block;
    height:1px;
    width:100%;
    background:#88888840;
  }
  .discription{
    font-size: 12px;
    color: #88888888;
  }
  .date{
    font-size: 12px;
  }
  .text{
    flex-direction: column;
    font-size: 18px;
    justify-content: flex-start;
    min-height: 100px; 
    position: relative;;
    z-index: 25;
    cursor: text;
    /* word-break: break-word; */
  }
  .tags{
    font-size: 14px;
  }
  .input_area{
    content: "";
    position: relative;
    flex-direction:column;
    align-items: flex-start;
    /* justify-content:stretch; */
    width:100%;
    /* height: 100%; */
    /* min-height:60vh; */
    padding:0;
  }
  .input_length{
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    /* z-index: 30; */
    bottom: 40px;
    right: 0;
    /* width: 100%;
    height: 100%; */
    margin: auto;
    margin: 10px;
  }
  .text.input{
    min-height: 50vh;
  }
  .input{
    resize: vertical;
    width:100%;
    border:0;
    border-left:1px solid #888888;
    outline:0.5px;
    background:transparent;
  }
  .input:hover{
    border-left:1px solid #88ccff;
  }
  .input:focus{
    border:1px solid #88ccff;
  }
  .buttons{
    justify-content: flex-start;
    position: absolute;
    z-index: 11;
    top: 10px;
    left: 40px;
  }
  .buttons *{
    margin: 5px;
    
  }
  .edit{
    position:absolute;
  	left: 0; top: 0;
    width:100%;
    height:100%;
    background:#88888800;
  }
  .edit_start{
    z-index:20;
  }
  .edit_end{
    content: "";
    position:fixed;
    background:#88888815;
    width: 100vw;
    height: 100vh;
  }
  .edit_end:before{
    content: '';
    background: inherit;
    backdrop-filter: blur(5px);
    position: absolute;
    top: -5px;
    left: -5px;
    right: -5px;
    bottom: -5px;
    z-index: -1;
  }
</style>