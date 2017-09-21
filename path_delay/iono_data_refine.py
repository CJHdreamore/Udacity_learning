import datetime,time
import math
import numpy as np
#import pylab as pl
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import os
from PIL import Image

### Define a class-----------------------------------------------------------------------------------------

class ObsFile(object):

    def __init__(self,date):
        self.date = date
        file_name = 'I'+self.date
        self.fh = file_name
        current_path = os.getcwd()
        self.files = os.listdir(current_path)


##----------------------------------------------------------------------------------------------------------
    def get_map_numbers (self):
        if self.fh in self.files:
            with open(self.fh)as obs_file:
                lines = obs_file.readlines()
                for line in lines:
                    comment = line[60:].strip()
                    if comment == '# OF MAPS IN FILE':
                        no_space = ''.join(line[:60].split())
                        number_maps = int(no_space)  # one parameter
                return number_maps


##----------------------------------------------------------------------------------------------------------
    def get_interval(self):
        if self.fh in self.files:
            with open(self.fh)as obs_file:
                lines = obs_file.readlines()
                for line in lines:
                    comment = line[60:].strip()
                    if comment == 'INTERVAL':
                        no_space = ''.join(line[:60].split())
                        interval = int(no_space)
                        return interval
##----------------------------------------------------------------------------------------------------------
    def get_obs_time(self):
        interval = self.get_interval()
        number = self.get_map_numbers()
        obs_time = datetime.datetime.strptime(self.date, '%Y-%m-%d')
        obs_time_axis = []
        for i in range(number):
            obs_time_axis.append(obs_time)
            obs_time = obs_time + datetime.timedelta(seconds = interval)
        return (obs_time_axis)

##----------------------------------------------------------------------------------------------------------
    def get_lat_lon_info(self):
        if self.fh in self.files:
            with open(self.fh)as obs_file:
                lines = obs_file.readlines()
                for line in lines:
                    comment = line[60:].strip()
                    if comment == 'LAT1 / LAT2 / DLAT':
                        lat_info = line[:60].split()

                    elif comment =='LON1 / LON2 / DLON':
                        lon_info = line[:60].split()

                return lat_info,lon_info

##--------------------------------------------------------------------------------------------------------
    def get_lon_occp_number(self):
        if self.fh in self.files:
            with open(self.fh)as obs_file:
                lines = obs_file.readlines()
                count = 0
                row = 0
                for line in lines:
                    row += 1
                    comment = line[60:].strip()
                    if comment == 'LAT/LON1/LON2/DLON/H':
                        count += 1
                        if count == 1:
                            set_flag = row

                        if count == 2:
                            end_flag =row - 1

                            inter_row = end_flag - set_flag

                            return inter_row


##---------------------------------------------------------------------------------

    def get_tec_maps(self):
        if self.fh in self.files:
            with open(self.fh)as obs_file:
                index = 0
                tec_map = {}
                lines = obs_file.readlines()
                total_maps = self.get_map_numbers()
                lat_info,lon_info = self.get_lat_lon_info()
                start_lat,end_lat,lat_inter = float(lat_info[0]),float(lat_info[1]),float(lat_info[2])
                row = 0
                obs_time_axis = self.get_obs_time()
                # -----read each line--------------------
                for line in lines:
                    row += 1
                    comment = line[60:].strip()  # judge via comment

                    if comment == 'START OF TEC MAP':

                        index_of_map= int(line[:60].split()[0])
                        obs_time =obs_time_axis[index_of_map - 1]

                        lat_count = 0
                        fixed_time_map = {}



                    elif comment == 'LAT/LON1/LON2/DLON/H':  #prepare to collect VTEC
                        current_lat = start_lat + lat_inter * lat_count
                        next = index + 1
                        rows = self.get_lon_occp_number()
                        value = []
                        for i in range(rows):
                            pointer = next + i
                            VTEC = lines[pointer].split()
                            for ele in VTEC:
                                value.append(float(ele))

                        fixed_time_map[current_lat] = value

                        lat_count += 1


                    elif comment =='END OF TEC MAP':
                        tec_map[obs_time] = fixed_time_map
                        index_of_map = int(line[:60].split()[0])
                        if index_of_map == total_maps:
                            return tec_map

                    index += 1

##----------------------------------------------------------------------------------------------------
    def look_up_map(self,obs_time,lat,lon):
        tec_maps = self.get_tec_maps()
        if obs_time in tec_maps.keys():
            fixed_time_map = tec_maps.get(obs_time)
            if lat in fixed_time_map:
                tec_along_lon = fixed_time_map[lat]
                lon_to_index = int((lon+180) / 5)
                if lon_to_index <= len(tec_along_lon):
                    point_tec = tec_along_lon[lon_to_index]
                    return point_tec
                else:
                    return None
            else:
                return None
        else:
            return None

##----------------------------------------------------------------------------------------------
    def get_tec_along_time(self,lat,lon):
        time= []
        tec = []
        tec_maps = self.get_tec_maps()
        index = int((lon + 180) / 5)

        for keys in tec_maps.keys():

            if lat in tec_maps[keys]:

                if index <= len(tec_maps[keys][lat]):

                    tec.append(tec_maps[keys][lat][index])

                    time.append(keys)

        return (tec,time)

##-----------------------------------------------------------------------------------------------------
    def draw_time_map(self,date,lat,lon):

        tec,time = self.get_tec_along_time(lat,lon)
        lat_s,lon_s = self.lat_lon_convert_str(lat,lon)

        # Draw Graph Settings
        mpl.rcParams['axes.unicode_minus'] = False # to show 'minus' correctly
        mpl.rc('xtick',labelsize=5)
        mpl.rc('ytick', labelsize=10)
        plt.style.use('ggplot')
        Fig = plt.figure(figsize=(10,5))
        ax = Fig.add_subplot(111)
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.ylim(0,max(tec)+10)
        plt.xlabel('Observe_time')
        plt.ylabel('TEC(0.1TECU)')
        title = 'TEC during one day at '+ 'lattitude:' + lat_s+' longitude:'+ lon_s
        plt.title(title)

        #----draw now-------------------------
        ax.plot(time, tec, '--b*')

        filename = 'TEC' + '-'+ lat_s + '-'+ lon_s + '-'+date
        print (filename)
        plt.savefig(filename)
        #plt.show()
##----------------------------------------------------------------------------------------------------------
    def lat_lon_convert_str(self,lat,lon):
        if lat < 0:
            lat_name = 'S'+ str(-lat)
        else:
            lat_name = 'N'+ str(lat)
        if lon < 0:
            lon_name = 'W'+str(-lon)
        else:
            lon_name = 'E'+str(lon)
        if type(lat) != 'int':
            index = 0
            for i in lat_name:

                if i == '.':

                    lat_name = lat_name[:index] + 'dot'+lat_name[index+1:]
                index += 1
        return lat_name,lon_name
##-------------------------------------------------------------------------------------------------------
    def get_tec_with_position(self,time):
        lats = []
        lons = []
        tec = []
        these_maps = self.get_all_maps()
        for keys in these_maps:
            if time == keys:
                this_map = these_maps[keys]
                for keys in this_map:
                    for index in range(0,len(this_map[keys])):
                        longitude = float(-180 + index * 5)
                        lats.append(keys)
                        lons.append(longitude)
                        tec.append(this_map[keys][index])
        return lats,lons,tec

##--------------------------------------------------------------------------------------------------------

    def exact_path_delay(self,time,lat,lon,inc,f):
        TECU = pow(10, 16)
        point_tec = self.look_up_map(time,lat,lon) * 0.1 * TECU

        K = 40.3
        rad = math.pi * inc / 180

        point_iono_delay = K * point_tec / (pow(f,2) * math.cos(rad) )

        return point_iono_delay

##----------------------------------------------------------------------------------------------------------

    def draw_pd_withinday(self,date,lat,lon,inc,f):
        obj_day = datetime.datetime.strptime(date, '%Y-%m-%d')
        current_time = obj_day
        time_record  = []
        delay_record = []

        for i in range (0,25):
            current_delay = self.exact_path_delay(current_time,lat,lon,inc,f)
            time_record.append(current_time)
            delay_record.append(current_delay)
            current_time += datetime.timedelta(seconds=3600)

        # --------draw settings--------------
        mpl.rcParams['axes.unicode_minus'] = False  # to show 'minus' correctly
        mpl.rc('xtick', labelsize=5)
        mpl.rc('ytick', labelsize=10)

        plt.style.use('ggplot')
        Fig = plt.figure(figsize=(10, 5))
        ax = Fig.add_subplot(111)
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.ylim(0, max(delay_record) + 0.02)
        plt.xlabel('Observe_time')
        plt.ylabel('Path Delay(m)')
        title = 'Path Delay within one day at ' + 'lattitude:' + str(lat) + ' longitude:' + str(lon)
        plt.title(title)
        # --------draw now-------------------------
        print (time_record)
        print (delay_record)
        ax.plot(time_record, delay_record, '--r*')
        #filename = 'ID' +'-'+ str(lat) +'-'+ str(lon) + '-' + date

        #plt.savefig(filename)
        #plt.show()
####----------------------------------------end class-------------------------------------------------------


##----------------------------------------------------------------------------------------------------------

def search_figure(arg,lat,lon,date):
    figure_name = arg + '-'+ str(lat) +'-'+ str(lon)+'-'+ date + '.png'
    current_path = os.getcwd()
    file_names = os.listdir(current_path)
    figure_path = os.path.join(current_path,figure_name)
    if figure_name in file_names:
        img = Image.open(figure_path)
        plt.figure(figure_name)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    else:
        return None






if __name__ == '__main__':
    date = '2017-03-16'

    obj = ObsFile(date)
    #inc = 41
    #f   = 13.58 * pow(10,9)    #Ku
   # f   = 9.6 * pow(10,9)   #X
   # obj_day = datetime.datetime.strptime(date, '%Y-%m-%d')
   # spec_time = obj_day + datetime.timedelta(hours=8)

    #delay = obj.exact_path_delay(spec_time, 37.5, -25, inc, f)
    #print (delay)
    #obj.draw_time_map(date,37.5, -25)
   # obj.draw_pd_withinday(date, 0, 100, inc, f)
   # search_figure('PD',0,100,date)
    obs_time = datetime.datetime(2017,3,16,13,0,0)
    lat = 37.5
    lon = -25
    obj.draw_time_map(date,lat,lon)






















