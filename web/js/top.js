const options = {
    moduleCache: {
      vue: Vue
    },
    async getFile(url) {
      
      const res = await fetch(url);
      if ( !res.ok )
        throw Object.assign(new Error(res.statusText + ' ' + url), { res });
      return {
        getContentData: asBinary => asBinary ? res.arrayBuffer() : res.text(),
      }
    },
    addStyle(textContent) {

      const style = Object.assign(document.createElement('style'), { textContent });
      const ref = document.head.getElementsByTagName('style')[0] || null;
      document.head.insertBefore(style, ref);
    },
  }
const { loadModule } = window['vue3-sfc-loader'];
console.log(location);
var app = {
    el: '#app',

    /* == data == リアクティブなデータを登録 */
    data(){
        return{
            searchtitle:'title',
            searchtext: '',
            colors:{
                bg : '#fefefeff',
                accent : '#ffffff'
            }
        };
    },
    methods:{
        search(e){
            eel.print()
        },
        add_data(){
            eel.add_data()
        }
    },
    /* ==== components ==== */
    // -- 単一ファイルコンポーネントの登録
    components: {
        // 'searchinput': httpVueLoader("./js/components/searchinput.vue"),
        // 'search_input': Vue.defineAsyncComponent( () => loadModule("./js/components/search_input.vue", options) ),
        // 'add_button': Vue.defineAsyncComponent( () => loadModule("./js/components/add_button.vue", options) ),
        'app_ui': Vue.defineAsyncComponent( () => loadModule("./js/components/main.vue", options) ),
    },

}

var generated_images_update_func = function(images){console.log(images)}
var set_meter_func = function(step_now,steps){console.log(step_now)}

Vue.createApp(app).mount('#app')