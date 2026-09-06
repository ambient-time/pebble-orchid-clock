// Copyright 2026 Luke Steuber. MIT License.
#include "../src/c/orchid.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
int main(void){
 for(int second=0;second<86400;second++){
  struct tm t={.tm_hour=second/3600,.tm_min=second/60%60,.tm_sec=second%60};OrchidTime o=orchid_time(&t);
  assert(o.hour_spots==(t.tm_hour%12?t.tm_hour%12:12));assert(o.minute_spots==t.tm_min);assert(o.second==t.tm_sec);
  for(int r=45;r<=85;r++){
   double source=12+r*(.1+(t.tm_sec/60.0)*.72);
   assert(fabs(orchid_nectar_end(12,r,o.second)-source)<=.500001);
  }
 }
 puts("86400 local-time states; nectar agrees with source within half a pixel at every native scale.");
}
