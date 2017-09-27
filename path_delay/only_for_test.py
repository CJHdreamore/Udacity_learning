import datetime
import math
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


##---------------------------------------------------------------------------------------------------------
start_date = datetime.datetime(2009,1,1,0,0,0)

current_date = datetime.datetime(2009,4,30,0,0,0)
inter_days = current_date - start_date

#real_days = inter_days + 1
#print (inter_days)




#-----------for tropo file-------------------------------------------------------------------------------
days = datetime.datetime(2017,3,16) - datetime.datetime(1980,1,6)
#print (days)
hours = 13584 * 24
day_of_week = hours % 168 / 24
gps_week = (hours - day_of_week * 24)/ 168
print (gps_week)
print (day_of_week)

##-----------------Model-TPD-2--------------------------------------------------------------------------
h_scene = 644
inc = 41 / 180 * math.pi
ZPD = math.pow(h_scene,2) / (8.55 * pow(10,7)) - h_scene/3411 + 2.41
TPD = ZPD/math.cos(inc)
#print (TPD)

##--------------------------------------------------------------------------------------------------------

