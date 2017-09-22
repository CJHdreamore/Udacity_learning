import datetime,time
import math
import numpy as np
#import pylab as pl
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import os
from PIL import Image

class Tropofile(object):

##----------------------------------------------------------------------------------------------------------

    def __init__(self,date,station_file,site_name,h_scene,inc):
        self.site_name = site_name
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






##----------------------------------------------------------------------------------------------------------

    def look_up_site_zpd(self):
        '''
        :param site_name:
        :return: zpd of this site
        '''
        ZPD_value,ZPD_std = self.get_all_sites_ZPD()

        if self.site_name in ZPD_value.keys():
           zpd_one_site = ZPD_value.get(self.site_name)

        return zpd_one_site

#------------------------------------------------------------------------------
    def draw_site_zpd(self,site_name):
        zpd_one_site = self.look_up_site_zpd(site_name)
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
        sites_alt = self.get_sites_alt()
        if self.site_name in sites_alt.keys():
            site_alt = sites_alt.get(self.site_name)
            return site_alt
        else:
            return None

#----------------------------------------------------------------------------------------------------------
    def TD_model_1(self):
        '''
        :return: TPD of h_scene at a fixed radar_inc during one day （slant range)
        '''
        zpd_scene_oneday =[]
        h_site = self.look_up_site_alt()       #altitude of the IGS station
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
    station_file = 'Site2009-08-02--08-08'
    date = '2009-08-07'
    site_name = 'PDEL'
    inc = 41
    h_scene = 644
    obj = Tropofile(date,station_file,site_name,h_scene,inc)
    obj.draw_TD()








