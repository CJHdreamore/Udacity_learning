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

    def __init__(self,dir_path):
        self.dir = dir_path
        self.files = os.listdir(dir_path)


    def search_file(self,date):
        for file in self.files:
            if file == date:
                return file
        return None


    def get_all_site_ZPD(self,date):
        file = self.search_file(date)
        if file:
            with open(file)as obs_file:
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


    def look_up_site(self,date,site):
        ZPD_dic = self.get_all_site_ZPD(date)
        if site in ZPD_dic.keys():
            zpd_value = []
            zpd_data = ZPD_dic.get(site)
            for i in zpd_data:
                zpd_value.append(i[0])
            #print (zpd_value)
            return zpd_value

    def draw_zpd(self,date,site):
        file_name = 'T'+ date
        zpd_value = self.look_up_site(file_name,site)
        time_axis = []
        time = datetime.datetime.strptime(date+ ' 01:00:00','%Y-%m-%d %H:%M:%S')
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
        title = 'Tropospheric Zenith Path Delay at ' + site + ' during '+ date
        plt.title(title)

        # ----draw now-------------------------
        ax.plot(time_axis, zpd_value, '--b*')
        filename = 'ZPD' + '-' + site + '-' + date
        #print (filename)
        plt.savefig(filename)
        plt.show()


    def look_up_site(self,site_name,file_name):
        file = self.search_file(file_name)
        if file:
            with open(file)as obs_file:
                lines = obs_file.readlines()
                row_number = 0
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

                            index = index + 1

























if __name__ == '__main__':
    dir_path = r'C:\Users\CJH\PycharmProjects\path_delay'
    date = 'T2017-03-16'
    obj = Tropofile(dir_path)
    #ZPD = obj.get_all_site_ZPD(date)
    #print (file_name)
    #zpd_value = obj.look_up_site('T2017-03-16','BJCO')
    #obj.draw_zpd('2017-03-16','BJCO')
    obj.look_up_site('BJCO','T2017-03-16')


