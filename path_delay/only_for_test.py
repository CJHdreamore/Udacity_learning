import datetime
start_date = datetime.datetime(1980,1,6,0,0,0)
current_date = start_date + datetime.timedelta(hours= (1616 * 168 + 5 * 24))
another_date = current_date + datetime.timedelta(days = 230)
print (current_date)
#print (another_date)

print ( 23* 3600)

days = datetime.datetime(2017,3,16) - datetime.datetime(1980,1,6)
#print (days)
hours = 13584 * 24
day_of_week = hours % 168 / 24
gps_week = (hours - day_of_week * 24)/ 168
print (gps_week)
print (day_of_week)
