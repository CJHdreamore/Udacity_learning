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

    def __init__(self,dir_path,date):
        self.date = date
        self.tfile = 'T'+date

        self.files = os.listdir(dir_path)


    #def search_file(self,file_name):
    #    for file in self.files:
    #        if file == file_name:
    #            return file
    #    return None


    def get_all_site_ZPD(self):

        if self.tfile in self.files:
            with open(self.tfile)as obs_file:
                lines = obs_file.readlines()
                row_number = 0
                for line in lines:
                    line = line.rstrip()              # delete all space in the right place
                    row_number += 1
                    #index = row_number - 1
                    if line == '+TROP/SOLUTION':    # start of a chunk
                        ZPD_dic = {}

                        #skip header

                        row_number = row_number + 2     #302
                        index = row_number - 1
                        #print (row_number)
                        #print (index)
                        total_row = len(lines)          #3514

                        while (row_number + 11) <= (total_row - 2):   #3501 + 11 = 3512
                            one_site = []
                            for i in range(1, 13):

                                pointer = index + i

                                value = lines[pointer]

                                zpd = float(value[18:25].lstrip())
                                std = float(value[29:32])
                                one_site.append([zpd,std])
                                site_name = value[1:5]
                                ZPD_dic[site_name] = one_site

                            index = pointer

                            row_number = index + 1
                        return ZPD_dic
        else:
            return None

#------------------------------------------------------------------------
    def look_up_site_zpd(self,site_name):
        ZPD_dic = self.get_all_site_ZPD()

        if site_name in ZPD_dic.keys():
            zpd_value = []
            zpd_data = ZPD_dic.get(site_name)
            for i in zpd_data:
                zpd_value.append(i[0])
            #print (zpd_value)

            return zpd_value

#------------------------------------------------------------------------------
    def draw_site_zpd(self,site_name):
        zpd_site = self.look_up_site_zpd(site_name)
        time_axis = []
        time = datetime.datetime.strptime(self.date+ ' 01:00:00','%Y-%m-%d %H:%M:%S')
        for i in range (0,12):
            time_axis.append(time)
            time = time + datetime.timedelta(hours = 2)

        # Draw Graph Settings
        mpl.rcParams['axes.unicode_minus'] = False  # to show 'minus' correctly
        mpl.rc('xtick', labelsize=5)
        mpl.rc('ytick', labelsize=10)
        font_size = 20
        plt.style.use('ggplot')
        Fig = plt.figure(figsize=(10, 5))
        ax = Fig.add_subplot(111)
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))
        #plt.ylim(0, max(tec) + 10)
        plt.xlabel('Observe_time')
        plt.ylabel('ZPD(mm)')
        title = 'Tropospheric Zenith Path Delay at ' + site_name + ' during '+ self.date
        plt.title(title)

        # ----draw now-------------------------
        ax.plot(time_axis, zpd_site, '--b*')
        filename = 'ZPD' + '-' + site_name + '-' + self.date
        #print (filename)
        plt.savefig(filename)
        plt.show()

#------------------------------this function may be not necessary------------------------------------------
    def get_sat_dic(self,file_name):
        file = self.search_file(file_name)
        if file:
            with open(file)as obs_file:
                lines = obs_file.readlines()
                row_number = 0
                cordinate_dic = {}
                for line in lines:
                    line = line.rstrip()
                    row_number += 1
                    if line == '+TROP/STA_COORDINATES':
                        cord_start_row = row_number + 2
                        index = cord_start_row - 1
                        while index < 297:

                            site_info = lines[index]
                            name = site_info[1:5]
                            x = float(site_info[15:28].lstrip())
                            #print (x)
                            y = float(site_info[29:41])
                            #print (y)
                            z = float(site_info[42:54])
                            cordinate_dic[name] = [x,y,z]

                            index = index + 1
                return cordinate_dic
#----------------------------------------------------------------------------------------------------------
    def get_sites_alt(self,station_file):

        if station_file in self.files:

            with open(station_file) as obj_file:
                lines = obj_file.readlines()
                row_number = 0
                for line in lines:
                    row_number += 1
                    line = line.rstrip()
                    if line == '+SITE/ID':
                        sites_alt = {}
                        start_row = row_number + 2
                        index = start_row - 1
                        while (lines[index].rstrip() != '-SITE/ID'):
                            station_info = lines[index]
                            name = station_info[1:5]

                            altitude = float(station_info[-7:-1])
                            sites_alt[name] = altitude
                            index += 1
                        return sites_alt

#----------------------------------------------------------------------------------------------------------

    def look_up_site_alt(self,site_name,station_file):
        sites_alt = self.get_sites_alt(station_file)

        if site_name in sites_alt.keys():

            site_alt = sites_alt.get(site_name)
            return site_alt
        else:
            return None
#----------------------------------------------------------------------------------------------------------

    def TD_model_1(self,site_name,h_scene,inc,station_file):
        zpd_scene =[]
        h_site = self.look_up_site_alt(site_name,station_file)
        zpd_site = self.look_up_site_zpd(site_name)
        h0 = 6000
        for i in zpd_site:
            zpd_scene.append( i / math.cos(inc) * math.exp(-(h_scene - h_site)/h0))

        return (zpd_scene)
#----------------------------------------------------------------------------------------------------------
    def draw_TD(self,site_name,h_scene,inc,station_file):
        zpd_scene = self.TD_model_1(site_name,h_scene,inc,station_file)
        time_axis = []
        time = datetime.datetime.strptime(self.date + ' 01:00:00', '%Y-%m-%d %H:%M:%S')
        for i in range(0, 12):   #risk ,what if  not 12??
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
        # plt.ylim(0, max(tec) + 10)
        plt.xlabel('Observe_time')
        plt.ylabel('Slant Tropo Delay(mm)')
        title = 'Tropospheric Slant Path Delay at '+ str(h_scene) + 'm during '+ self.date
        plt.title(title)

        # ----draw now-------------------------


        ax.plot(time_axis, zpd_scene, '--b*')
        filename = 'TD' + '-' + str(h_scene) + '-' + self.date
        # print (filename)
        plt.savefig(filename)
        plt.show()









if __name__ == '__main__':
    dir_path = r'C:\Users\CJH\PycharmProjects\path_delay'
    date = '2009-04-08'
    obj = Tropofile(dir_path,date)
    site_name = 'PDEL'
    zpd_dic = obj.get_all_site_ZPD()
    site_zpd = obj.look_up_site_zpd(site_name)
    station_file = 'Site2009-04-05--04-11'
    site_alt = obj.look_up_site_alt(site_name,station_file)
    #obj.draw_site_zpd(site_name)
    inc = (41 /180) * math.pi
    h_scene = 644

    obj.draw_TD(site_name,h_scene,inc,station_file)






