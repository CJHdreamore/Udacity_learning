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

##---------------------------------------------------------------------------------------------------------

    def __init__(self,date,f,inc,lat,lon):
        self.lat = lat
        self.lon = lon
        self.f = f
        self.inc = inc
        self.date = date
        file_name = 'I'+self.date
        self.fh = file_name
        current_path = os.getcwd()
        self.files = os.listdir(current_path)


##----------------------------------------------------------------------------------------------------------

    def get_map_numbers (self):
        ''' how many maps in this file'''
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
        '''find out the time spacing of this file,ie : 7200s = 2 h'''
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
        '''return the obs_time_axis: a list of specific time on the day we need'''
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
        ''' In this file : the lat's and lon's coverage and their spacing '''
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

##----------------------------------------------------------------------------------------------------------

    def get_lon_occp_number(self):
        ''' How many lines we should extract at one time as a list of TEC on a fixed lattitude '''
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

##----------------------------------------------------------------------------------------------------------

    def get_tec_maps(self):
        ''' convert all the tec values in this file into several maps (according to the obs_interval
            data structure: tec_map = {'specific_time:{lattitude:[tec1,tec2,****};}
                            [tec1,tec2,***]:index of this list maps to the longitude
        '''
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

##----------------------------------------------------------------------------------------------------------

    def look_up_map(self,obs_time):
        ''' obs_time: type(datetime.datetime(2017,03,16,0,0,0)   a specific time
            return : TEC_value
        '''
        tec_maps = self.get_tec_maps()
        if obs_time in tec_maps.keys():
            fixed_time_map = tec_maps.get(obs_time)
            if self.lat in fixed_time_map:
                tec_along_lon = fixed_time_map[self.lat]
                lon_to_index = int((self.lon+180) / 5)
                if lon_to_index <= len(tec_along_lon):
                    point_tec = tec_along_lon[lon_to_index]
                    return point_tec
                else:
                    return None
            else:
                return None
        else:
            return None

##----------------------------------------------------------------------------------------------------------

    def get_tec_during_oneday(self):
        '''
        :param lat:  degreee
        :param lon:  degree
        :return: tec,obs_time   tec_value during one day on (lat,lon)
        '''
        obs_time= []
        tec = []
        tec_maps = self.get_tec_maps()
        index = int((self.lon + 180) / 5)   # this function needs modification,for now it's too coarse to map lon to index

        for keys in tec_maps.keys():

            if self.lat in tec_maps[keys]:

                if index <= len(tec_maps[keys][self.lat]):

                    tec.append(tec_maps[keys][self.lat][index])

                    obs_time.append(keys)

        return (tec,obs_time)

##---------------------------------------------------------------------------------------------------------

    def draw_tec_during_oneday(self):
        '''

        :param lat:
        :param lon:
        :return: tec-variation map on (lat,lon) during one day, a pgn figure save as : TEC-lat-lon-date;
                  float number : point represented as dot
        '''

        tec,time = self.get_tec_along_time()
        lat_s,lon_s = self.lat_lon_convert_str()

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
        title = 'TEC during one day at '+ 'lattitude:' + str(self.lat)+' longitude:'+ str(self.lon)
        plt.title(title)

        #----draw now-------------------------
        ax.plot(time, tec, '--b*')
        filename = 'TEC' + '-'+ lat_s + '-'+ lon_s + '-'+date
        print (filename)
        plt.savefig(filename)
        plt.show()

##----------------------------------------------------------------------------------------------------------

    def lat_lon_convert_str(self):
        '''change float number (lat,lon) to propriate str for saving figures'''
        if self.lat < 0:
            lat_name = 'S'+ str(-self.lat)
        else:
            lat_name = 'N'+ str(self.lat)
        if self.lon < 0:
            lon_name = 'W'+str(-self.lon)
        else:
            lon_name = 'E'+str(self.lon)
        if type(self.lat) != 'int':
            index = 0
            for i in lat_name:

                if i == '.':
                    lat_name = lat_name[:index] + 'dot'+lat_name[index+1:]

                index += 1
        return lat_name,lon_name

##----------------------------------------------------------------------------------------------------------

    def get_iono_pd_during_oneday(self):
        '''
        :param lat:  degreee
        :param lon:  degree
        :return: iono_pd,obs_time  iono_pd (m) during one day on (lat,lon)
        '''
        obs_time= []
        iono_pd = []
        tec_maps = self.get_tec_maps()
        index = int((self.lon + 180) / 5)   # this function needs modification,for now it's too coarse to map lon to index

        for keys in tec_maps.keys():

            if self.lat in tec_maps[keys]:

                if index <= len(tec_maps[keys][self.lat]):
                    tec_value = tec_maps[keys][self.lat][index]
                    pd = self.compute_iono(tec_value)
                    iono_pd.append(pd)
                    obs_time.append(keys)

        return (iono_pd,obs_time)


##--------------------------------------------------------------------------------------------------------

    def compute_iono(self,tec_value):
        '''
        :param tec_value:
        :return: pd
        '''
        TECU = pow(10, 16)
        point_tec = tec_value * 0.1 * TECU

        K = 40.3
        rad = math.pi * self.inc / 180

        pd = K * point_tec / (pow(self.f,2) * math.cos(rad) )

        return pd

##----------------------------------------------------------------------------------------------------------

    def draw_pd_during_oneday(self):
        '''
        :param lat:
        :param lon:
        :return: iono_pd-variation map on (lat,lon) during one day, a pgn figure save as : IPD-lat-lon-date;
                  float number : point represented as dot
        '''
        iono_pd, obs_time = self.get_iono_pd_during_oneday()

        lat_s, lon_s = self.lat_lon_convert_str()

        # Draw Graph Settings
        mpl.rcParams['axes.unicode_minus'] = False  # to show 'minus' correctly
        mpl.rc('xtick', labelsize=5)
        mpl.rc('ytick', labelsize=10)
        plt.style.use('ggplot')
        Fig = plt.figure(figsize=(10, 5))
        ax = Fig.add_subplot(111)
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))
        #plt.ylim(0, max(iono_pd) + 10)
        plt.xlabel('Observe_time')
        plt.ylabel('Ionospheric Path Delay (m)')
        title = 'IPD during one day at ' + 'lattitude:' + str(self.lat) + ' longitude:' + str(self.lon)
        plt.title(title)

        # ----draw now-------------------------
        ax.plot(obs_time, iono_pd, '--b*')
        filename = 'IPD' + '-' + lat_s + '-' + lon_s + '-' + date
        print(filename)
        plt.savefig(filename)
        plt.show()
####----------------------------------------end class-------------------------------------------------------


##----------------------------------------------------------------------------------------------------------

def search_figure(arg):
    figure = arg +'.png'
    current_path = os.getcwd()
    files = os.listdir(current_path)
    if figure in files:
        figure_path = current_path+ '/'+ figure
        img = Image.open(figure_path)
        img.show()
       # plt.figure('IPD')
       # plt.imshow(img)
       # plt.axis('off')
       # plt.show()


if __name__ == '__main__':
    date = '2009-07-16'
    f    = 9.6 * pow(10,9)   #X
    inc  = 41
    lat = 37.5
    lon = -25
    obj = ObsFile(date,f,inc,lat,lon)
    #obj.draw_pd_during_oneday()
    figure = 'IPD-N37dot5-W25-2009-04-08'
    search_figure(figure)





















