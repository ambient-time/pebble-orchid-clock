// Copyright 2026 Luke Steuber. MIT License.
#pragma once
#ifdef ORCHID_HOST
#include <time.h>
#else
#include <pebble.h>
#endif
typedef struct {int hour_spots,minute_spots,second;} OrchidTime;
OrchidTime orchid_time(const struct tm *local);
int orchid_nectar_end(int origin,int radius,int second);
