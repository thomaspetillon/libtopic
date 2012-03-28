#!/usr/bin/env python
import datetime
import calendar
from libtopic.dates import is_today
from libtopic.dates import get_date_from_datetime

class AgendaDay:
    def __init__(self,day,agenda_dict):
        self.day = day
        self.events = agenda_dict.get(day,[])

def get_agenda_dict(events,event_date_field,event_text_field):    
    dict = {}
    for event in events:        
        if dict.has_key(getattr(event,event_date_field)):
            dict[getattr(event,event_date_field)].append(event)
        else :
            dict[getattr(event,event_date_field)] = [event]
    # For each day, display only places
    for key in dict.keys():
        dict[key] = [getattr(event,event_text_field) for event in dict[key]]
    return dict
    
def get_monthly_agenda(year,month,event_list,event_date_field,event_text_field):    
    agenda_dict = get_agenda_dict(event_list,event_date_field,event_text_field)
    cal =  calendar.Calendar(0).monthdatescalendar(year,month)
    cal2 = []
    for line in cal:
        line2 = []
        for day in line:
            agenda_day = AgendaDay(day,agenda_dict)
            if is_today(day):
                agenda_day.is_current_day = True
            if day.month==month:
                agenda_day.in_current_month = True
            if day < get_date_from_datetime(datetime.datetime.now()):
                agenda_day.is_in_past = True            
            line2.append(agenda_day)
        cal2.append(line2)
    return cal2
