// Copyright 2026 Luke Steuber. MIT License.
#include <pebble.h>
#include "orchid.h"
#include "geometry.h"
static Window *s_window;
static Layer *s_layer;
static bool s_focused;
static ResHandle s_art;
static uint8_t s_row[260];
typedef char RowBufferMustFitArtwork[ART_WIDTH<=sizeof(s_row)?1:-1];
static uint32_t s_frames;

static bool background(GContext *ctx,OrchidTime t){
 if(resource_size(s_art)!=(size_t)(ART_WIDTH*ART_HEIGHT))return false;
 GBitmap *buffer=graphics_capture_frame_buffer(ctx);if(!buffer)return false;
 GRect screen=gbitmap_get_bounds(buffer);
 GPoint origin=layer_get_frame(window_get_root_layer(s_window)).origin;
 int end=orchid_nectar_end(THROAT_Y,FLOWER_R,t.second);
 for(int y=0;y<ART_HEIGHT;y++){
  if(resource_load_byte_range(s_art,y*ART_WIDTH,s_row,ART_WIDTH)!=(size_t)ART_WIDTH){graphics_release_frame_buffer(ctx,buffer);return false;}
  int sy=y+origin.y;if(sy<0||sy>=screen.size.h)continue;
  GBitmapDataRowInfo row=gbitmap_get_data_row_info(buffer,sy);
  for(int x=0;x<ART_WIDTH;x++){
   int sx=x+origin.x;if(sx<row.min_x||sx>row.max_x||sx<0||sx>=screen.size.w)continue;
   uint8_t pixel=s_row[x];
   bool nectar=(x>=THROAT[y][0]&&x<=THROAT[y][1])||(x>=THROAT[y][2]&&x<=THROAT[y][3]);
   if(t.second>0&&y<=end&&nectar){
#ifdef PBL_COLOR
    int fraction=100*(y-THROAT_Y)/(end-THROAT_Y);
    pixel=fraction<45?GColorRoseVale.argb:fraction<75?GColorMelon.argb:GColorIcterine.argb;
#else
    pixel=(x+y)%3!=0;
#endif
   }
#ifdef PBL_COLOR
   row.data[sx]=pixel;
#else
   uint8_t bit=1<<(sx&7);if(pixel)row.data[sx>>3]|=bit;else row.data[sx>>3]&=~bit;
#endif
  }
 }
 graphics_release_frame_buffer(ctx,buffer);return true;
}
static void draw(Layer *layer,GContext *ctx){
 time_t epoch;uint16_t start,end;time_ms(&epoch,&start);struct tm local=*localtime(&epoch);
 OrchidTime t=orchid_time(&local);GRect bounds=layer_get_bounds(layer);
 if(!background(ctx,t)){APP_LOG(APP_LOG_LEVEL_ERROR,"Orchid artwork unavailable");return;}
 graphics_context_set_antialiased(ctx,true);
 for(int i=0;i<12;i++){
  GPoint p=GPoint(HOURS[i][0],HOURS[i][1]);int r=HOURS[i][2];
  if(i<t.hour_spots){
   graphics_context_set_fill_color(ctx,PBL_IF_COLOR_ELSE(GColorRoseVale,GColorBlack));graphics_fill_circle(ctx,p,r);
  }else{
   graphics_context_set_stroke_color(ctx,PBL_IF_COLOR_ELSE(GColorMelon,GColorBlack));graphics_context_set_stroke_width(ctx,1);graphics_draw_circle(ctx,p,r);
  }
 }
 for(int i=0;i<60;i++){
  GPoint p=GPoint(MINUTES[i][0],MINUTES[i][1]);
  graphics_context_set_stroke_color(ctx,PBL_IF_COLOR_ELSE(i<t.minute_spots?GColorBulgarianRose:GColorPastelYellow,GColorBlack));
  if(i<t.minute_spots){graphics_draw_pixel(ctx,p);if(ART_WIDTH>=200)graphics_draw_pixel(ctx,GPoint(p.x+1,p.y));}
  else if(i==t.minute_spots){graphics_context_set_stroke_color(ctx,PBL_IF_COLOR_ELSE(GColorRoseVale,GColorBlack));graphics_draw_circle(ctx,p,1);}
#ifdef PBL_COLOR
  else graphics_draw_pixel(ctx,p);
#endif
 }
 char exact[8];strftime(exact,sizeof(exact),clock_is_24h_style()?"%H:%M":"%I:%M",&local);
 graphics_context_set_text_color(ctx,PBL_IF_COLOR_ELSE(GColorBulgarianRose,GColorWhite));
 GFont font=fonts_get_system_font(ART_WIDTH>=200?FONT_KEY_GOTHIC_28_BOLD:FONT_KEY_GOTHIC_18_BOLD);
 graphics_draw_text(ctx,exact,font,GRect(0,CAPTION_Y-(ART_WIDTH>=200?15:10),bounds.size.w,32),GTextOverflowModeTrailingEllipsis,GTextAlignmentCenter,NULL);
 s_frames++;time_ms(NULL,&end);
 APP_LOG(APP_LOG_LEVEL_INFO,"Orchid time=%02d:%02d:%02d ms=%u heap=%lu frames=%lu",local.tm_hour,local.tm_min,local.tm_sec,(end+1000-start)%1000,(unsigned long)heap_bytes_free(),(unsigned long)s_frames);
}
static void tick(struct tm *t,TimeUnits units){if(s_focused&&s_layer)layer_mark_dirty(s_layer);}
static void focus(bool focused){s_focused=focused;if(focused&&s_layer)layer_mark_dirty(s_layer);}
static void load(Window *window){
 s_art=resource_get_handle(RESOURCE_ID_ART);s_layer=layer_create(layer_get_bounds(window_get_root_layer(window)));
 layer_set_update_proc(s_layer,draw);layer_add_child(window_get_root_layer(window),s_layer);
}
static void unload(Window *window){layer_destroy(s_layer);s_layer=NULL;}
int main(void){
 s_window=window_create();window_set_background_color(s_window,GColorBlack);
 window_set_window_handlers(s_window,(WindowHandlers){.load=load,.unload=unload});s_focused=true;window_stack_push(s_window,false);
 tick_timer_service_subscribe(SECOND_UNIT,tick);app_focus_service_subscribe(focus);app_event_loop();
 tick_timer_service_unsubscribe();app_focus_service_unsubscribe();window_destroy(s_window);
}
