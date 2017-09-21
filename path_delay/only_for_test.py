import datetime
start_date = datetime.datetime(2009,1,1,0,0,0)

current_date = datetime.datetime(2009,4,8,0,0,0)
inter_days = current_date - start_date
# real_days = inter_days + 1
#print (inter_days)





days = datetime.datetime(2009,4,8) - datetime.datetime(1980,1,6)
#print (days)
hours = 10685 * 24
day_of_week = hours % 168 / 24
gps_week = (hours - day_of_week * 24)/ 168
#print (gps_week)
#print (day_of_week)
for i in range(-180,180,5):
    print (i)
