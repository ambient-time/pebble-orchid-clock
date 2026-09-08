// Copyright 2026 Luke Steuber. MIT License.
'use strict';
var saved = {DIGITAL: 1, CALM: 0};
try { var cached=JSON.parse(localStorage.getItem('face-settings-v1')); if(cached && (cached.DIGITAL===0 || cached.DIGITAL===1)) saved=cached; } catch(e) {}
// Only an explicit Save changes the watch; a phone reconnect never resets it.
Pebble.addEventListener('showConfiguration',function(){
  function select(id,label,value){return '<label for="'+id+'">'+label+'</label><select id="'+id+'"><option value="1"'+(value?' selected':'')+'>On</option><option value="0"'+(!value?' selected':'')+'>Off</option></select>';}
  var html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Orchid Clock</title><style>body{font:18px system-ui;background:#f4f2ed;color:#202020;margin:24px auto;padding:0 20px;max-width:32rem}label{display:block;margin-top:24px}select,button{font:inherit;width:100%;min-height:48px;margin:10px 0}a{display:block;padding:16px 0;color:#23496a}</style><h1>Orchid Clock</h1>'+select('DIGITAL','Bottom digital clock',saved.DIGITAL)+''+'<button id="save">Save to watch</button><a href="pebblejs://close">Cancel</a><script>document.getElementById("save").onclick=function(){var v={DIGITAL:Number(document.getElementById("DIGITAL").value),CALM:document.getElementById("CALM")?Number(document.getElementById("CALM").value):0};location.href="pebblejs://close#"+encodeURIComponent(JSON.stringify(v));};<\/script></html>';
  Pebble.openURL('data:text/html;charset=utf-8,'+encodeURIComponent(html));
});
Pebble.addEventListener('webviewclosed',function(event){
  if(!event || !event.response)return;
  try{
    var value=JSON.parse(event.response.charAt(0)==='{'?event.response:decodeURIComponent(event.response));
    if(!value || (value.DIGITAL!==0 && value.DIGITAL!==1) || (value.CALM!==0 && value.CALM!==1))return;
    Pebble.sendAppMessage(value,function(){saved=value;localStorage.setItem('face-settings-v1',JSON.stringify(value));},function(){console.log('Settings not delivered. Open settings and save again.');});
  }catch(e){console.log('Settings unchanged.');}
});
