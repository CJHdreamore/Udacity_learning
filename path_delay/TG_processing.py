import numpy as np
from iono_data_refine import *
from tropo_data_refine import *


cr_lon = np.array([109.6316,
  109.6328,
  109.5894,
  109.5935,
  109.5681,
  109.5667,
  109.5648,
  109.5689,
  109.5697,
  109.5914,
  109.5666])
cr_lat = np.array([40.8487,
   40.8436,
   40.8732,
   40.8609,
   40.8763,
   40.8735,
   40.8664,
   40.8797,
   40.8823,
   40.8685,
   40.8697])
cr_alt = [1.2776,
    1.2862,
    1.2809,
    1.2757,
    1.2785,
    1.2735,
    1.2677,
    1.2824,
    1.2852,
    1.2733,
    1.2730]
cr_alt = np.array(cr_alt)*(10**3)

date = '2017-03-16'
time = '01:05:09'
station_file = 'Site2017-03-12--03-18'
f    = 13.58 * pow(10,9)   #Ku
#inc_near = 2.5
inc_far = 8.0
ipd = []
tpd = []
for i in range(len(cr_lat)):
    lat = cr_lat[i]
    lon = cr_lon[i]
    alt = cr_alt[i]
    obj_1 = IonoFile(date,time,f,inc_far,lat,lon)
    ipd.append(obj_1.processing_IPD_2())
    obj_2 = Tropofile(date,time,station_file,lat,lon,alt,inc_far)
    tpd.append(obj_2.TPD_processing())

tpd = np.asarray(tpd)
ipd = np.asarray(ipd)
print ('tpd far-range inc')
print (tpd)
print ('ipd far-range inc')
print (ipd)


#f = open(r'C:\Users\CJH\PycharmProjects\path_delay\TG_data_record.txt','a')
#file_name_1 ='Iono_Path_delay.txt'
#file_name_2 ='Tropo_Path_delay.txt'
#np.savetxt(file_name_1,ipd,delimiter=';',newline='\n',fmt='%-10.5f',header=u'Ionospheric Path Delay for CR with near inc (m)\n')
#np.savetxt(file_name_2,tpd,delimiter=';',newline='\n',fmt='%-10.5f',header=u'Tropospheric Path Delay for CR (m) with near inc\n')

