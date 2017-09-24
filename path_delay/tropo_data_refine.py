import datetime,time
import math
import numpy as np
#import pylab as pl
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from matplotlib.ticker import MultipleLocator,FormatStrFormatter
import os
from PIL import Image


class Tropofile(object):

##----------------------------------------------------------------------------------------------------------

    def __init__(self,date,station_file,lat,lon,h_scene,inc):
        self.lat = lat
        self.lon = lon
        self.h_scene = h_scene
        self.inc = (inc / 180) * math.pi   # degree to rad
        self.date = date
        self.tfile = 'T'+date
        self.sfile = station_file
        current_path = os.getcwd()
        self.files = os.listdir(current_path)

##----------------------------------------------------------------------------------------------------------
    def get_sites(self):
        '''

        :return: all_used sites in this Tropo-data file
        '''
        if self.tfile in self.files:
            with open(self.tfile) as obj_file:
                sites_list = []
                lines = obj_file.readlines()
                row = 0
                for line in lines:
                    row += 1
                    line = line.rstrip()
                    if line == '+TROP/STA_COORDINATES':
                        start_row = row + 1                    #skip header
                    elif line == '-TROP/STA_COORDINATES':
                        end_row = row
                sites_lines = lines[start_row:end_row - 1]
                for row in sites_lines:
                    row = row.rstrip().split()
                    site = row[0]
                    sites_list.append(site)
                return sites_list

##----------------------------------------------------------------------------------------------------------

    def get_sites_alt(self):
        '''

        :return: a dictionary: key = site_name; value:site_altitude
        '''
        if self.sfile in self.files:
            with open(self.sfile) as obj_file:
                lines = obj_file.readlines()
                row = 0
                for line in lines:
                    row += 1
                    line = line.rstrip()
                    if line == '+SITE/ID':
                        sites_alt = {}
                        start_row = row   # don't skip header
                    elif line == '-SITE/ID':
                        end_row = row
                sites_info = lines[start_row:end_row -1]
                header = sites_info[0].split()
                index = 0

                for ele in header:
                    if ele =='_APP_H_':
                        h_index = index

                    if ele == '*CODE':
                        s_index = index
                    index += 1

                for row in sites_info[1:]:
                    row = row.split()
                    site_name = row[s_index]
                    site_alt = float(row[h_index])
                    sites_alt[site_name] = site_alt
                return sites_alt

##----------------------------------------------------------------------------------------------------------
    def get_sites_pos(self):
        '''

        :return: lat,lon of sites
        '''
        if self.sfile in self.files:
            with open(self.sfile) as obj_file:
                lines = obj_file.readlines()
                row = 0
                for line in lines:
                    row += 1
                    line = line.rstrip()
                    if line == '+SITE/ID':
                       # sites_pos = {}
                        sites_name = []
                        sites_lon = []
                        sites_lat = []
                        start_row = row  # don't skip header
                    elif line == '-SITE/ID':
                        end_row = row
                sites_info = lines[start_row:end_row - 1]
                header = sites_info[0].rstrip()
                len_h = len(header)
                i = 0
                while (i < len_h - 10):
                    h_pos = header[i:i+11]
                    h_name = header[i:i+4]

                    if h_pos == 'APPROX_LAT_':
                        lat_index = i
                    elif h_pos == 'APPROX_LON_':
                        lon_index = i

                    if h_name == 'CODE':
                        name_index = i
                    i += 1
                for row in sites_info[1:]:
                    row = row.rstrip()
                    site_name = row[name_index:name_index+4]
                    sites_name.append(site_name)

                    site_lat = row[lat_index:lat_index+6]
                    site_lat = '.'.join(site_lat.split())
                    site_lat = float(site_lat)
                    sites_lat.append(site_lat)

                    site_lon = row[lon_index:lon_index+6]
                    site_lon = '.'.join(site_lon.split())
                    site_lon = float(site_lon)
                    sites_lon.append(site_lon)

                    #sites_pos[site_name] = [site_lat,site_lon]



                return (sites_name,sites_lat,sites_lon)

##----------------------------------------------------------------------------------------------------------

    def get_all_sites_ZPD(self):
        '''

        :return:  ZPD_value: 'key' = site_name, value = {'specific_time':zpd_value}
                  or value = [ zpd_value],index of the list maps the obs_time
                  ZPD_std: 'key' = site_name, value = std
        '''
        if self.tfile in self.files:
            with open(self.tfile)as obs_file:
                lines = obs_file.readlines()
                row = 0
                for line in lines:
                    row += 1
                    line = line.rstrip()              # delete all space in the right place

                    if line == '+TROP/SOLUTION':    # start of a chunk
                        ZPD_value = {}
                        ZPD_std = {}
                        header_row = row + 1
                        start_row = header_row + 1
                    if line == '-TROP/SOLUTION':
                        end_row = row
                #------------read header-------------------
                header = lines[header_row -1].split()
                index = 0
                for ele in header:
                    if ele == '*SITE':
                        s_index = index
                    elif ele =='____EPOCH___':
                        t_index = index
                    elif ele =='TROTOT':
                        tropo_index = index
                    elif ele =='STDDEV':
                        std_index = index
                    index += 1
                #--------------------------------------------
                solution = lines[start_row-1:end_row -1]
                for row in solution:
                    row = row.split()
                    site_name = row[s_index]
                    tropo_value =float(row[tropo_index])
                    std_value = float(row[std_index])
                    ZPD_value.setdefault(site_name,[]).append(tropo_value)
                    ZPD_std.setdefault(site_name,[]).append(std_value)
                return ZPD_value,ZPD_std

        else:
            return None
##----------------------------------------------------------------------------------------------------------
    def draw_sites_pos(self):
        sites_name,sites_lat,sites_lon = self.get_sites_pos()

        # Draw Graph Settings
        mpl.rcParams['axes.unicode_minus'] = False  # to show 'minus' correctly
        mpl.rc('xtick', labelsize=5)
        mpl.rc('ytick', labelsize=5)
        plt.style.use('ggplot')
        Fig = plt.figure(figsize=(10, 5))
        ax = Fig.add_subplot(111)

        plt.xlim(-90.00,90.00,2.5)
        plt.ylim(0.00,365.00,5.0)
        xmajorlocator = MultipleLocator(10)
        xmajorformatter = FormatStrFormatter('%1.1f')
        xminorlocator = MultipleLocator(2.5)

        ymajorlocator = MultipleLocator(10)
        ymajorformatter = FormatStrFormatter('%1.1f')
        yminorlocator = MultipleLocator(5.0)

        ax.xaxis.set_major_locator(xmajorlocator)
        ax.xaxis.set_major_formatter(xmajorformatter)

        ax.yaxis.set_major_locator(ymajorlocator)
        ax.yaxis.set_major_formatter(ymajorformatter)

        ax.xaxis.set_minor_locator(xminorlocator)
        ax.yaxis.set_minor_locator(yminorlocator)

        ax.xaxis.grid(True,which = 'minor')
        ax.yaxis.grid(True, which='major')

        plt.xlabel('lattitude')
        plt.ylabel('longitude')
        title = 'IGS station distribution ' + ' on ' + self.date
        plt.title(title)

        # ----draw now-------------------------
        #ax.plot(sites_lat, sites_lon, '--b*')
        T = np.arctan2(sites_lat,sites_lon) # for color setting
        plt.scatter(sites_lat,sites_lon,c = T,s=25,alpha=0.4,marker='o')  # c = color; s =size; alpha = transparency
        plt.show()
##----------------------------------------------------------------------------------------------------------
    def find_nearest_sites(self):
        sites_name,sites_lat,sites_lon = self.get_sites_pos()
        pos_errors =[]
        for i in range (len(sites_name)):
            lat_error = abs(sites_lat[i] - self.lat)
            lon_error = abs(sites_lon[i] - self.lon)
            total_error = lat_error + lon_error / 2
            pos_errors.append(total_error)

        for i in range (len(pos_errors)):
            if pos_errors[i] == min(pos_errors):
                nearest_site = sites_name[i]

        return (nearest_site)


##----------------------------------------------------------------------------------------------------------
    def look_up_site_zpd(self):
        '''
        :param site_name:
        :return: zpd of this site
        '''
        site_name = self.find_nearest_sites()

        ZPD_value,ZPD_std = self.get_all_sites_ZPD()

        if site_name in ZPD_value.keys():
           zpd_one_site = ZPD_value.get(site_name)

        return zpd_one_site

#------------------------------------------------------------------------------
    def draw_site_zpd(self):
        site_name = self.find_nearest_sites()
        zpd_one_site = self.look_up_site_zpd()
        time_axis = []
        time = datetime.datetime.strptime(self.date+ ' 01:00:00','%Y-%m-%d %H:%M:%S')
        for i in range (0,12):
            time_axis.append(time)
            time = time + datetime.timedelta(hours = 2)

        # Draw Graph Settings
        mpl.rcParams['axes.unicode_minus'] = False  # to show 'minus' correctly
        mpl.rc('xtick', labelsize=5)
        mpl.rc('ytick', labelsize=10)
        plt.style.use('ggplot')
        Fig = plt.figure(figsize=(10, 5))
        ax = Fig.add_subplot(111)
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.xlabel('Observe_time')
        plt.ylabel('ZPD(mm)')
        title = 'Tropospheric Zenith Path Delay at ' + site_name + ' during '+ self.date
        plt.title(title)

        # ----draw now-------------------------
        ax.plot(time_axis, zpd_one_site, '--b*')
        filename = 'ZPD' + '-' + site_name + '-' + self.date
        #print (filename)
        plt.savefig(filename)
        plt.show()

##---------------------------------------------------------------------------------------------------------

    def look_up_site_alt(self):
        '''
        :return: site_altitude
        '''
        site_name = self.find_nearest_sites()
        sites_alt = self.get_sites_alt()
        if site_name in sites_alt.keys():
            site_alt = sites_alt.get(site_name)
            return site_alt
        else:
            return None

#----------------------------------------------------------------------------------------------------------
    def TD_model_1(self):
        '''
        :return: TPD of h_scene at a fixed radar_inc during one day （slant range)
        '''
        zpd_scene_oneday =[]
        h_site = self.look_up_site_alt()        #altitude of the IGS station
        zpd_one_site = self.look_up_site_zpd()     #zpd of the IGS station
        h0 = 6000                              #atomospheric thickness constant
        for i in zpd_one_site:

            zpd_scene = i / math.cos(self.inc) * math.exp(-(self.h_scene - h_site)/h0)

            zpd_scene_oneday.append(zpd_scene)
        return (zpd_scene_oneday)

#----------------------------------------------------------------------------------------------------------
    def draw_TD(self):
        zpd_scene_oneday = self.TD_model_1()
        time_axis = []
        time = datetime.datetime.strptime(self.date + ' 01:00:00', '%Y-%m-%d %H:%M:%S')
        for i in range(0, 12):
            time_axis.append(time)
            time = time + datetime.timedelta(hours=2)

        # Draw Graph Settings
        mpl.rcParams['axes.unicode_minus'] = False  # to show 'minus' correctly
        mpl.rc('xtick', labelsize=5)
        mpl.rc('ytick', labelsize=10)
        plt.style.use('ggplot')
        Fig = plt.figure(figsize=(10, 5))
        ax = Fig.add_subplot(111)
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.xlabel('Observe_time')
        plt.ylabel('Slant Tropo Delay(mm)')
        title = 'Tropospheric Slant Path Delay at '+ str(self.h_scene) + 'm during '+ self.date
        plt.title(title)

        # ----draw now-------------------------
        ax.plot(time_axis, zpd_scene_oneday, '--b*')
        filename = 'TD' + '-' + str(self.h_scene) + '-' + self.date

        plt.savefig(filename)
        plt.show()


if __name__ == '__main__':
    station_file = 'Site2008-04-27--05-03'
    date = '2008-04-28'
    lat = 46.43
    lon = 8.11
    inc = 31.2
    h_scene = 2163
    obj = Tropofile(date,station_file,lat,lon,h_scene,inc)
    obj.draw_TD()
    td = obj.draw_TD()









