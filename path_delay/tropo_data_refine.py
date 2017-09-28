#coding = utf-8
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
from scipy import interpolate

class Tropofile(object):

##----------------------------------------------------------------------------------------------------------

    def __init__(self,date,time,station_file,lat,lon,h_scene,inc):
        self.lat = lat
        self.lon = lon
        self.h_scene = h_scene
        self.inc = (inc / 180) * math.pi     # degree to rad
        self.date = date
        self.tfile = 'T'+date
        self.sfile = station_file
        current_path = os.getcwd()
        self.files = os.listdir(current_path)
        self.time = datetime.datetime.strptime(self.date + ':' + time, '%Y-%m-%d:%H:%M:%S')

##----------------------------------------------------------------------------------------------------------
    def get_sites(self):
        '''
        Acquire all the existing sites' name in today's Tropo delay data
        :return: site_list = [site_name]
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
        Using SiteFile to acquire all existing sites' alt
        :return: dictionary : {site_name:site_altitude}
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

    def get_all_sites_ZPD(self):
        '''
        Acquire all the existing sites' zenith tropo path delay during that day

        Attention: these sites may be working abnormally!!!!!

        :return:  a nest dictionary.{'site_name':{specific_time:[zpd_value]}}
                  'key' = site_name, value = {'specific_time':zpd_value}

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
                return ZPD_value

        else:
            return None


##----------------------------------------------------------------------------------------------------------
    def elim_abnormal_site(self):
        '''
        find abnormally working sites: their observing time is less than usual one
        :return: abnormal_sites = [site_name]
        '''
        site_list = self.get_sites()
        elim_sites = []
        ZPD_value= self.get_all_sites_ZPD()   # a ZPD dic
        for each_site in site_list:
            if each_site in ZPD_value.keys():
                zpd_one_site = ZPD_value.get(each_site)
                if len(zpd_one_site)!= 12:
                    ZPD_value.pop(each_site)
                    elim_sites.append(each_site)


        update_ZPD_value = ZPD_value
        return update_ZPD_value,elim_sites


##----------------------------------------------------------------------------------------------------------
    def get_working_sites_info(self):
        '''
        from 'site' file to get pos info about today's existing sites
        (Attention: but these sites can be fake sites!!!!!)
        :return: {site_name:[lat,lon]}
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
                        sites_pos = {}
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


                    site_lat = row[lat_index:lat_index+6]
                    site_lat = '.'.join(site_lat.split())
                    site_lat = float(site_lat)


                    site_lon = row[lon_index:lon_index+6]
                    site_lon = '.'.join(site_lon.split())
                    site_lon = float(site_lon)


                    sites_pos[site_name] = [site_lat,site_lon]



                return sites_pos
##----------------------------------------------------------------------------------------------------------
    def TPD_processing(self):
        '''
        main_function
        :return: target scene's tropospheric slant range path delay (m)
        '''

        #step_1: According to self.date,get all working sites' Zenith Path delay

        # today's working sites info
        existing_sites_pos = self.get_working_sites_info()
        ## A big fake!!!!!!!!!!!!!!Gosh!!!!!!!!!!!!!!!



        existing_sites_zpd = self.get_all_sites_ZPD()   #{site_name:[zpd_value]}

        real_existing_sites = []
        for key in existing_sites_zpd.keys():
            real_existing_sites.append(key)



        #step_2: find abnormal working sites and remove it from working_sites_zpd
        abn_sites = []

        for site in existing_sites_zpd:
            if len(existing_sites_zpd[site]) < 12:
                abn_sites.append(site)

        print ('abnormal sites')
        print (abn_sites)
        for site in abn_sites:
            if site in existing_sites_zpd:
                existing_sites_zpd.pop(site)
            if site in existing_sites_pos:
                existing_sites_pos.pop(site)

        fake_site = []
        for site in existing_sites_pos.keys():
            if site not in real_existing_sites:
                fake_site.append(site)

        print ('fake sites:')
        print (fake_site)
        for site in fake_site:
            if site in existing_sites_pos:
                existing_sites_pos.pop(site)

        working_sites_zpd = existing_sites_zpd
        working_sites_pos = existing_sites_pos


        #step3: find two normal working sites around target scene

        pos_errors = {}
        error_record = []
        for site in working_sites_pos:
            lat,lon = working_sites_pos[site][0],working_sites_pos[site][1]

            lat_error = lat - self.lat
            lon_error = lon - self.lon
            pos_error = math.sqrt(lat_error**2 + lon_error**2)
            pos_errors[site] = pos_error
            error_record.append(pos_error)

        nearest_site = []
        for site in pos_errors:
            if pos_errors[site] == min(error_record):
                nearest_site.append(site)

        if len(nearest_site) < 2:
            error_record.remove(min(error_record))
            for site in pos_errors:
                if pos_errors[site] == min(error_record):
                    nearest_site.append(site)

        if len(nearest_site) >2:
            nearest_site.pop()

        first_site = nearest_site[0]
        print ('first_nearest_site')
        print (first_site)
        second_site = nearest_site[1]
        print ('second_nearest_site')
        print (second_site)

        first_site_pos_error = pos_errors[first_site]
        second_site_pos_error = pos_errors[second_site]
        w1 = first_site_pos_error/(first_site_pos_error+second_site_pos_error)
        w2 = second_site_pos_error /(first_site_pos_error+second_site_pos_error)
        first_site_zpd = np.array(working_sites_zpd[first_site])

        second_site_zpd = np.array(working_sites_zpd[second_site])


        # step 4 : link GPS data with the altitude of targeted scene &convert zpd to slant range path delay

        h_first_site = self.look_up_site_alt(first_site)
        h_second_site = self.look_up_site_alt(second_site)
        h0 = 6000
        first_tpd_scene = first_site_zpd / math.cos(self.inc) * math.exp(-(self.h_scene - h_first_site) / h0)
        second_tpd_scene = second_site_zpd / math.cos(self.inc) * math.exp(-(self.h_scene - h_second_site) / h0)
        first_tpd_scene = np.array(first_tpd_scene)
        second_tpd_scene = np.array(second_tpd_scene)

        interp_site_tpd = w1 *first_tpd_scene + w2 * second_tpd_scene  # array



        #step_5: linear interpolating over obs_time

        obs_time = datetime.datetime.strptime(self.date + ':01:00:00','%Y-%m-%d:%H:%M:%S')
        obs_time_axis = []
        for i in range(12):
            obs_time_axis.append((obs_time))
            obs_time = obs_time + datetime.timedelta(seconds=7200)

        for i in range(len(obs_time_axis) - 1):

            if self.time >= obs_time_axis[i] and self.time < obs_time_axis[i+1]:
                time_before_index = i
                time_after_index = i+1
                time_before = obs_time_axis[i]
                time_after = obs_time_axis[i+1]

                time_before_tpd = interp_site_tpd[time_before_index]

                time_after_tpd = interp_site_tpd[time_after_index]

                coe1 = (time_after - self.time).seconds / (time_after - time_before).seconds

                coe2 = (self.time - time_before).seconds / (time_after - time_before).seconds

                interp_time_site_tpd = coe1 * time_before_tpd + coe2 * time_after_tpd
                break

        interp_time_site_tpd = interp_time_site_tpd / 1000

        return (interp_time_site_tpd)


####################These functions may be not necessary in TG processing###################################
##----------------------------------------------------------------------------------------------------------
    def one_site_zpd_interp_fortime(self,site_name):
        '''

        :param site_name:
        :return: IGS_zpd over a interp time
        '''
        time_line = np.linspace(1,23,12)
        interp_time = self.time
        sites_zpd,sites_std = self.get_all_sites_ZPD()
        if site_name in sites_zpd:
            site_zpd_oneday = sites_zpd.get(site_name)

        for index in range(len(time_line) - 1):
            if interp_time > time_line[index] and interp_time < time_line[index + 1]:
                time_before = (time_line[index])
                time_after = (time_line[index+1])
                time_before_index =int(time_before / 2 )
                time_after_index = int(time_after /2 )
                time_before_zpd = site_zpd_oneday[time_before_index]
                time_after_zpd = site_zpd_oneday[time_after_index]
                break
        interp_zpd = (time_after - interp_time)/(time_after - time_before) *time_before_zpd +\
                    (interp_time - time_before)/(time_after - time_before) * time_after_zpd

        return interp_zpd
##----------------------------------------------------------------------------------------------------------
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
##----------------------------------------------------------------------------------------------------------
    def find_nearest_sites(self):
        '''
        Find the nearest site from target scene
        :return: type:str,nearest_site_name
        '''
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
##---------------------------------------------------------------------------------------------------------

    def look_up_site_alt(self,site_name):
        '''
        :site_name : the name of a site
        :return: site_altitude
        '''

        sites_alt = self.get_sites_alt()
        if site_name in sites_alt.keys():
            site_alt = sites_alt.get(site_name)
            return site_alt
        else:
            return None

##----------------------------------------------------------------------------------------------------------
    def look_up_site_pos(self,site_name):
        '''

        :param site_name:
        :return: the lat,lon of a site
        '''
        sites_name,sites_lat,sites_lon = self.get_sites_pos()
        for k in range(len(sites_name)):
            if site_name == sites_name[k]:
                site_lat = sites_lat[k]
                site_lon = sites_lon[k]
        return site_lat,site_lon

##----------------------------------------------------------------------------------------------------------

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
        #plt.show()
##---------------------------------------------------------------------------------------------------------
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

##----------------------------------------------------------------------------------------------------------

    def TD_model_for_onesite(self,site_name):
        h_one_site = self.look_up_site_alt(site_name)
        zpd_one_site = self.one_site_zpd_interp_fortime(site_name)
        h0 = 6000
        zpd_scene = zpd_one_site / math.cos(self.inc) * math.exp(-(self.h_scene - h_one_site) / h0)
        return zpd_scene

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



############################################################################################################

if __name__ == '__main__':
    station_file = 'Site2017-03-12--03-18'
    date = '2017-03-16'
    time = '01:05:09'
    lat = 40.8487
    lon = 109.6328
    inc = 2.5
    h_scene = 1273
    obj = Tropofile(date,time,station_file,lat,lon,h_scene,inc)
    sites = obj.get_sites()

    obj.TPD_processing()








