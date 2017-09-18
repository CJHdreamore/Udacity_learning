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

    def __init__(self,file):
        self.fh = file

    def get_map_numbers (self):
        with open(self.fh)as obs_file:
            lines = obs_file.readlines()
            for line in lines:
                comment = line[60:].strip()
                if comment == '# OF MAPS IN FILE':
                    no_space = ''.join(line[:60].split())
                    number_maps = int(no_space)           # one parameter
            return number_maps

##------------------------------------------------------------------------------

    def get_base_radius(self):
        with open(self.fh)as obs_file:
            lines = obs_file.readlines()
            for line in lines:
                comment = line[60:].strip()
                if comment == 'BASE RADIUS':
                    no_space = ''.join(line[:60].split())  # second
                    base_radius = float(no_space)
            return base_radius

##---------------------------------------------------------------------------------

    def get_all_maps(self):
        with open(self.fh)as obs_file:

            lines = obs_file.readlines()
            create_maps = {}                  #final format of this file
            current_row = 0
            date_record = []                  #store 25 dates
            tec_matrix_sets = []              #store 25 matrices
            initial_lat = 87.5

            #-----read each line--------------------
            for line in lines:
                comment = line[60:].strip()           # judge via comment

                if comment == 'EPOCH OF CURRENT MAP':
                    count_lat = 0                     # initialize the number of recorded_lattitude
                    value = {}
                    current_lat = initial_lat
                    #----------extract date from str-----------------
                    time_str = '-'.join(line[:60].split())
                    date = time.strptime(time_str, '%Y-%m-%d-%H-%M-%S')
                    y, m, d, h, M ,s = date[0:6]
                    date = datetime.datetime(y, m, d, h,M,s)
                    date_record.append(date)

                elif comment == 'LAT/LON1/LON2/DLON/H':
                    '''it's time to access TEC data,stick the next 5 lines together'''

                    #print (current_lat)
                    fixed_lat_data = []           # initilize a 1-D list to store tec along index [73 longitudes]
                    count_lat += 1

                    #----------extract next 5 rows-----------
                    for i in range(1, 6):
                        raw_data = lines[current_row + i].split()
                        for ele in raw_data:
                            fixed_lat_data.append(float(ele))

                    #----------------------------------------

                    value[current_lat] = fixed_lat_data       #store longitude-tec list into a dictionary with key=latitude

                    if count_lat == 71 :                      # 71 lattitudes refer to one tec_matrix
                        tec_matrix_sets.append(value)
                        #count_lat = 0
                       # value = {}

                    current_lat -= 2.5

                current_row += 1                              # count row number of the whole file


            #---------after juding all lines in this file--------------------
            for i in range (0,25):
                create_maps[date_record[i]] = tec_matrix_sets[i]
            return create_maps

##----------------------------------------------------------------------------------------------------
    def look_up_map(self,time,lat,log):
        these_maps = self.get_all_maps()
        if time in these_maps:
            this_map = these_maps[time]
            if lat in this_map:
                this_map_fixed_lat = this_map[lat]
                log_to_index = int((log+180) / 5)
                if log_to_index <= len(this_map_fixed_lat):
                    point_tec = this_map_fixed_lat[log_to_index]
                    return point_tec
                else:
                    return None
            else:
                return None
        else:
            return None

##----------------------------------------------------------------------------------------------
    def get_tec_along_time(self,lat,log):
        time= []
        tec = []
        these_maps = self.get_all_maps()
        index = int((log + 180) / 5)

        for keys in these_maps.keys():

            if lat in these_maps[keys]:

                if index <= len(these_maps[keys][lat]):


                    tec.append(these_maps[keys][lat][index])

                    time.append(keys)


        return (tec,time)

##-----------------------------------------------------------------------------------------------------
    def draw_time_map(self,date,lat,lon):
        latt = lat
        long = lon
        tec,time = self.get_tec_along_time(latt,long)


        # Draw Graph Settings
        mpl.rcParams['axes.unicode_minus'] = False # to show 'minus' correctly
        mpl.rc('xtick',labelsize=5)
        mpl.rc('ytick', labelsize=10)
        font_size = 20
        plt.style.use('ggplot')
        Fig = plt.figure(figsize=(10,5))
        ax = Fig.add_subplot(111)
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.ylim(0,max(tec)+10)
        plt.xlabel('Observe_time')
        plt.ylabel('TEC(0.1TECU)')
        title = 'TEC during one day at '+ 'lattitude:' + str(latt)+' longitude:'+ str(long)
        plt.title(title)

        #----draw now-------------------------
        ax.plot(time, tec, '--b*')
        filename = 'TEC' + '-'+ str(latt) + '-'+ str(long) + '-'+date
        plt.savefig(filename)
       # plt.show()


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
        ax.plot(time_record, delay_record, '--r*')
        filename = 'PD' +'-'+ str(lat) +'-'+ str(lon) + '-' + date
        plt.savefig(filename)
        #plt.show()
####----------------------------------------end class-------------------------------------------------------


def search_file(date):

    dir_path = os.getcwd()
    files = os.listdir(dir_path)
    for file in files:
        if file[1:] == date:
            return (file)
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
    date = '2017-03-21'
    obj_file = search_file(date)
    obj = ObsFile(obj_file)
    inc = 8.0
    f   = 13.58 * pow(10,9)
    obj_day = datetime.datetime.strptime(date, '%Y-%m-%d')
    spec_time = obj_day + datetime.timedelta(hours=7)
    #delay = obj.exact_path_delay(spec_time, 0, 95, inc, f)
    # print (delay)
    #obj.draw_time_map(date,0, 95)
    #obj.draw_pd_withinday(date, 0, 100, inc, f)
    search_figure('PD',0,100,date)
















