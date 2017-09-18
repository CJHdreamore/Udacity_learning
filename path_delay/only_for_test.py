from data_refine import *
from remodify_filename import modify_name
import os
def search_file(date):

    dir_path = os.getcwd()
    files = os.listdir(dir_path)
    for file in files:
        if file[1:] == date:
            return (file)

date = '2017-03-21'
obj_file = search_file(date)
obj = ObsFile(obj_file)

inc = 8.0
f   = 13.58 * pow(10,9)
obj_day = datetime.datetime.strptime(date,'%Y-%m-%d')
spec_time = obj_day + datetime.timedelta(hours = 7)
delay = obj.exact_path_delay(spec_time,0,95,inc,f)
#print (delay)
obj.draw_time_map(0,95)
obj.draw_pd_withinday(obj_day,0,100,inc,f)