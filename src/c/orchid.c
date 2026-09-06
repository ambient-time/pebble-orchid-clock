// Copyright 2026 Luke Steuber. MIT License.
#include "orchid.h"
OrchidTime orchid_time(const struct tm *local){
 int h=local->tm_hour%12;
 return (OrchidTime){h?h:12,local->tm_min,local->tm_sec};
}
int orchid_nectar_end(int origin,int radius,int second){
 return origin+(radius*(600+72*second)+3000)/6000;
}
