# coding=utf8
#!/usr/bin/env python
import time
import datetime
import calendar

def is_yesterday(the_datetime):
    today_dt    = datetime.datetime.today()
    the_date = datetime.date(the_datetime.year,the_datetime.month,the_datetime.day)
    today    = datetime.date(today_dt.year,today_dt.month,today_dt.day)
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return (the_date==yesterday)

def is_today(the_datetime):
    today_dt = datetime.datetime.today()
    the_date = datetime.date(the_datetime.year,the_datetime.month,the_datetime.day)
    today    = datetime.date(today_dt.year,today_dt.month,today_dt.day)
    return (the_date==today)
    
def is_same_day(day1,day2):    
    day1 = datetime.date(day1.year,day1.month,day1.day)
    day2 = datetime.date(day2.year,day2.month,day2.day)
    return (day1==day2)

def get_today():
    return datetime.datetime.today() 

def get_date_from_datetime(the_datetime):
    return datetime.date(the_datetime.year,the_datetime.month,the_datetime.day)

def get_month_name(month_number):
    month_index = month_number -1
    months = [u"janvier",u"février",u"mars",u"avril",u"mai",u"juin",u"juillet",u"août",u"septembre",u"octobre",u"novembre",u"décembre"]
    return months[month_index]
    
def get_month_name_abbr(month_number):
    month_index = month_number -1
    months = [u"jan",u"fév",u"mar",u"avr",u"mai",u"juin",u"juil",u"août",u"sept",u"oct",u"nov",u"déc"]
    return months[month_index]
    
def get_weekdays():
    return [u"lundi",u"mardi",u"mercredi",u"jeudi",u"vendredi",u"samedi",u"dimanche"]
    
def get_weekdays_abbr():
    return ["L","M","Me","J","V","S","D"]
    
def get_weekday_name(week_day):    
    return get_weekdays()[week_day]
    
def get_period_name(first_day,last_day):
    if first_day.year == last_day.year:
        if first_day.month == last_day.month:
            # Nous sommes au sein d'un même mois
            return u"du %s au %s %s %s" % (get_day_str(first_day.day),get_day_str(last_day.day),get_month_name(first_day.month),first_day.year)
        else:
            # A cheval sur deux mois dans la même année
            return u"du %s %s au %s %s %s" % (get_day_str(first_day.day),get_month_name(first_day.month),get_day_str(last_day.day),get_month_name(last_day.month),first_day.year)
    else:
        # A cheval sur deux années
        return u"du %s %s %s au %s %s %s" % (get_day_str(first_day.day),get_month_name(first_day.month),first_day.year,get_day_str(last_day.day),get_month_name(last_day.month),first_day.year)    
    
def get_day_str(day):
        day_str = str(day)
        if day==1:
            day_str = "1er"        
        return day_str        
    
def get_day_name(day):
        day_str = str(day.day)
        if day.day==1:
            day_str = "1er"
        return day_str + " " + get_month_name(day.month) + " " + str(day.year)
    
def get_full_day_name(day):
        return get_weekday_name(day.weekday()) + " " + get_day_name(day)

def get_first_day_of_month(dt, d_years=0, d_months=0):
    # d_years, d_months are "deltas" to apply to dt
    y, m = dt.year + d_years, dt.month + d_months
    a, m = divmod(m-1, 12)
    return datetime.date(y+a, m+1, 1)
    
def get_last_day_of_month(dt):
    return get_first_day_of_month(dt, 0, 1) + datetime.timedelta(-1)
    
# Calendar day type, ex : calendar.MONDAY
def get_next_day_of_specified_type(start_date,calendar_day_type):    
    if start_date.weekday()==calendar_day_type:
        return start_date    
    one_day = datetime.timedelta(days=1)
    stop = False
    current_date = start_date    
    while not stop:        
        current_date += one_day
        if current_date.weekday() == calendar_day_type:
            stop = True
    return current_date

# Calendar day type, ex : calendar.MONDAY
def get_previous_day_of_specified_type(start_date,calendar_day_type):
    if start_date.weekday()==calendar_day_type:
        return start_date    
    one_day = datetime.timedelta(days=1)
    stop = False
    current_date = start_date 
    while not stop:        
        current_date -= one_day
        if current_date.weekday() == calendar_day_type:
            stop = True
    return current_date

def get_next_thursday():
    return get_next_day_of_specified_type(datetime.datetime.today(),calendar.THURSDAY)
    
def get_next_wednesday():
    return get_next_day_of_specified_type(datetime.datetime.today(),calendar.WEDNESDAY)
    
def get_next_monday():
    return get_next_day_of_specified_type(datetime.datetime.today(),calendar.MONDAY)
    
def get_next_friday():
    return get_next_day_of_specified_type(datetime.datetime.today(),calendar.FRIDAY)
    
def get_next_saturday():
    return get_next_day_of_specified_type(datetime.datetime.today(),calendar.SATURDAY)
    
def get_next_sunday():
    return get_next_day_of_specified_type(datetime.datetime.today(),calendar.SUNDAY)
    
def get_first_day_of_week(the_day):
    return get_previous_day_of_specified_type(the_day,calendar.MONDAY)

def get_last_day_of_week(the_day):
    return get_next_day_of_specified_type(the_day,calendar.SUNDAY)
        
def get_django_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
def get_django_date_from_time(time):
    year   = time[0]
    month  = time[1]
    day    = time[2]
    hour   = time[3]
    minute = time[4]
    second = time[5]
    result = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(second)
    return result

def get_first_day_of_week_from_week_number(year,week_number):
    return datetime.datetime(*time.strptime('%s %s 1' % (year,week_number), '%Y %W %w')[0:5])

