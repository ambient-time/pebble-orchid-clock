// Copyright 2026 Luke Steuber. MIT License.
#pragma once
// Private to this standalone face; keys remain stable across updates.
static bool s_digital=DEFAULT_DIGITAL, s_calm=false;
static void settings_changed(void);
static void settings_receive(DictionaryIterator *iter,void *context){
  (void)context;
  Tuple *value=dict_find(iter,1);
  if(value && value->length==4 && (value->type==TUPLE_INT || value->type==TUPLE_UINT) && value->value->int32>=0 && value->value->int32<=1){
    s_digital=value->value->int32;persist_write_bool(1,s_digital);
  }
  value=dict_find(iter,2);
  if(value && value->length==4 && (value->type==TUPLE_INT || value->type==TUPLE_UINT) && value->value->int32>=0 && value->value->int32<=1){
    s_calm=value->value->int32;persist_write_bool(2,s_calm);
  }
  APP_LOG(APP_LOG_LEVEL_INFO,"Face settings digital=%d calm=%d",s_digital,s_calm);
  settings_changed();
}
static void settings_init(void){
  if(persist_exists(1))s_digital=persist_read_bool(1);
  if(persist_exists(2))s_calm=persist_read_bool(2);
  app_message_register_inbox_received(settings_receive);
  app_message_open(64,64);
  APP_LOG(APP_LOG_LEVEL_INFO,"Face settings digital=%d calm=%d",s_digital,s_calm);
}
static void digital_draw(GContext *ctx,GRect bounds,struct tm *now,GColor color){
  if(!s_digital)return;
  char text[8];strftime(text,sizeof(text),clock_is_24h_style()?"%H:%M":"%I:%M",now);
  if(!clock_is_24h_style() && text[0]=='0')memmove(text,text+1,strlen(text));
  int height=bounds.size.w>=200?34:28;
  int bottom=PBL_IF_ROUND_ELSE(bounds.size.h*91/100,bounds.size.h-3);
  graphics_context_set_text_color(ctx,color);
  graphics_draw_text(ctx,text,fonts_get_system_font(bounds.size.w>=200?FONT_KEY_GOTHIC_28_BOLD:FONT_KEY_GOTHIC_24_BOLD),
    GRect(0,bottom-height,bounds.size.w,height),GTextOverflowModeTrailingEllipsis,GTextAlignmentCenter,NULL);
}
