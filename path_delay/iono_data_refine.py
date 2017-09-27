import datetime,time
import math
import numpy as np
#import pylab as pl

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import os
from PIL import Image
from scipy import interpolate

### Define a class-----------------------------------------------------------------------------------------

class ObsFile(object):

##---------------------------------------------------------------------------------------------------------

    def __init__(self,date,time,f,inc,lat,lon):
        self.lat = lat
        self.lon = lon
        self.f = f
        self.inc = inc
        self.date = date
        file_name = 'I'+self.date
        self.fh = file_name
        current_path = os.getcwd()
        self.files = os.listdir(current_path)
        self.time = datetime.datetime.strptime(self.date+':'+time,'%Y-%m-%d:%H:%M:%S')


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
        '''  get global tec_maps of one day, the number of maps depends on observing interval
             :return
                     tec_map = {'specific_time:{lattitude:[tec1,tec2,****};}
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
    def inter_latlon_vtec(self):
        tec_maps = self.get_tec_maps()
        latt = []
        long = []
        vtec = []

        if self.time in tec_maps.keys():
            tec_map = tec_maps[self.time]

            for lat in tec_map:
                latt.append(lat)
                lons = tec_map[lat]
                for i in range(len(lons)):
                    vtec.append(lons[i])    #create lattitude axies & vtec list

            for i in range (-180,185,5):
                long.append(i)              #create longitude axies

            fig = plt.figure(figsize = (9,6))
            #ax = plt.subplot(1,1,1,projection = '3d')
            ax = Axes3D(fig)
            x,y= np.meshgrid(long,latt)
            col = len(x[0])
            row = len(x)
            count = 0
            one_row = []
            v = []
            for ele in vtec:
                count += 1
                one_row.append(ele)
                if count == col:
                    v.append(one_row)
                    count = 0
                    one_row = []
            surf = ax.plot_surface(x,y,v,cmap=cm.coolwarm,linewidth=0.5, antialiased=True)
            ax.set_xlabel('lon')
            ax.set_ylabel('lat')
            ax.set_zlabel('vtec')
            plt.colorbar(surf, shrink=0.5, aspect=5)  # 标注


            # 二维插值
            newfunc = interpolate.interp2d(x, y, v, kind='linear')
            solution = 180/1.5
            latt_new = np.linspace(87.5,-87.5,solution)

            lon_new = np.linspace(-180.0,180.0,solution)
            v_insert = newfunc(lon_new,latt_new)
            vnew = []
            row_one = []
            for i in range(len(v_insert)):
                row = v_insert[i]
                for k in range(len(row)):
                    element = row[k]
                    if element < 0:
                        element = 0
                    row_one.append(element)
                vnew.append(row_one)
                row_one = []

            xnew,ynew = np.meshgrid(lon_new,latt_new)
            fig = plt.figure(figsize=(9, 6))
            ax2 = Axes3D(fig)
            surf2 = ax2.plot_surface(xnew,ynew,vnew,rstride=2, cstride=2, cmap=cm.coolwarm,linewidth=0.5, antialiased=True)
            ax2.set_xlabel('lon')
            ax2.set_ylabel('lat')
            ax2.set_zlabel('vtec')
            plt.colorbar(surf2, shrink=0.5, aspect=5)  # 标注

            plt.show()

##---------------------------------------------------------------------------------------------------------
    def bilinear_interpo(self):
        '''
        x,y:array_like 1-D arrays of coordinates in strictly ascending order
        z: array_like 2-D array of data with shape(xsize,ysize)
        :return:
        '''
        lon_solution = int(360/5)
        lat_solution = int(87.5*2/2.5)
        lon = np.linspace(-180.0,180.0,lon_solution+1)
        lat = np.linspace(-87.5,87.5,lat_solution+1)
        vtec = []
        tec_maps = self.get_tec_maps()
        if self.time in tec_maps.keys():
            this_map = tec_maps[self.time]
            for i in lat:
                vtec.append(this_map[i])

        vtec = np.array(vtec)

        newfuc = interpolate.RectBivariateSpline(lat,lon,vtec)
        nvtec = newfuc.ev(self.lat,self.lon)
        return nvtec


##----------------------------------------------------------------------------------------------------------


##----------------------------------------------------------------------------------------------------------

    def interpolate_vtec(self):
        tec_maps = self.get_tec_maps()
        if self.time in tec_maps.keys():
            tec_map = tec_maps[self.time]
            vtec = []

            for lat in tec_map:
                lons = tec_map[lat]
                for i in range(len(lons)):
                    vtec.append(lons[i])  # create vtec list

            lon_solution = 360 / 5.0

            lat_solution = 87.5 * 2/2.5

            lon = np.linspace(-180.0,180.0,int(lon_solution + 1))
            lat = np.linspace(87.5,-87.5,int(lat_solution + 1))
            long, latt = np.meshgrid(lon, lat)

            col = len(long[0])
            v = []
            one_row = []
            count = 0

            for ele in vtec:
                count += 1
                one_row.append(ele)
                if count == col:
                    v.append(one_row)
                    one_row = []
                    count = 0

            #interpolation:
            kind_list = ['linear','quintic','cubic']

            f = interpolate.interp2d(long,latt,v,kind = kind_list[1])
            lon_new_sol = int(360 / 2.5)

            lat_new_sol = int(87.5 * 2 / 1.5)

            lon_new = np.linspace(-180.0,180.0,lon_new_sol+1)
            lat_new = np.linspace(87.5,-87.5,lat_new_sol+1)


            v_insert = f(lon_new,lat_new)
            vnew = []
            row_one = []
            for i in range(len(v_insert)):
                row = v_insert[i]
                for k in range(len(row)):
                    element = row[k]
                    if element < 0:
                        element = 0
                    row_one.append(element)
                vnew.append(row_one)
                row_one = []
            #lon_new, lat_new = np.meshgrid(lon_new, lat_new)

            return lon_new,lat_new, vnew

##----------------------------------------------------------------------------------------------------------
    def look_up_inter_vtec(self):

        lon,lat,vtec = self.interpolate_vtec()
        lon_error_store = []
        lat_error_store = []
        for i in range(len(lon)):
            lon_error = abs(lon[i] - self.lon)
            lon_error_store.append(lon_error)
        for k in range(len(lat)):
            lat_error = abs(lat[k] - self.lat)
            lat_error_store.append(lat_error)
        lon_index = lon_error_store.index(min(lon_error_store))
        lat_index = lat_error_store.index(min(lat_error_store))
        inter_vtec = vtec[lon_index][lat_index]
        return (inter_vtec)


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
##----------------------------------------------------------------------------------------------------------



##----------------------------------------------------------------------------------------------------------

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
    def processing_IPD_1(self):
        '''

        :return: interpolated global_slant_iono_pd at obs_time (interpolate over time)

                {lat:array[slant_path_delay]}
        '''
        #step 1: get global tec_map associated with input date (self.date)
        tec_maps_oneday = self.get_tec_maps()
        #step 2: find time before & after the obs_time
        obs_time_line = []
        for key in tec_maps_oneday.keys():
            obs_time_line.append(key)

        for i in range(len(obs_time_line) - 1):
            if obs_time_line[i] < self.time and obs_time_line[i+1] > self.time:
                obs_time_before = obs_time_line[i]
                obs_time_after = obs_time_line[i+1]

        tec_map_before = tec_maps_oneday[obs_time_before]
        tec_map_after = tec_maps_oneday[obs_time_after]

        #step3 :linear interpolation for specific obs_time
        interptime_pd_map = {}
        lat = np.linspace(87.5,-87.5,71)
        for i in lat:
            tec_before = np.array(tec_map_before[i])
            tec_after = np.array(tec_map_after[i])
            time_interval = (obs_time_after - obs_time_before).seconds
            interp_tec = (obs_time_after - self.time).seconds / time_interval * tec_before +\
                         (self.time - obs_time_before).seconds /time_interval * tec_after
            # vtec converts to iono slant path delay
            TECU = pow(10, 16)
            interptime_tec = interp_tec * 0.1 * TECU

            K = 40.3
            rad = math.pi * self.inc / 180

            interptime_pd = K * interptime_tec / (pow(self.f, 2) * math.cos(rad))

            interptime_pd_map[i] = interptime_pd

        return (interptime_pd_map)


##----------------------------------------------------------------------------------------------------------
    def processing_IPD_2(self):
        '''
        According to (lat,lon) of  the target scene, impolying bilinear interpolation on retangular grids
        :return: the desire ionon path delay for target scene on a specific observe_time
        '''
        interptime_pd_map = self.processing_IPD_1()
        #step 1: According to self.lat & self.lon ,find four retangular coordinates around target scene
        lat = np.linspace(87.5,-87.5,71)
        lon = np.linspace(-180,180,73)
        for i in range(lat.size - 1):
            if lat[i] >= self.lat and lat[i+1] <= self.lat:
                lat_larger = lat[i]
                lat_smaller = lat[i+1]
        lat_grid = [lat_smaller,lat_larger]
        for i in range(lon.size - 1):
            if lon[i] <= self.lon and lon[i + 1] <= self.lon:
                lon_larger = lon[i+1]
                lon_smaller = lon[i]
        lon_grid = [lon_smaller,lon_larger]

        lon_smaller_index = int((lon_smaller + 180) / 5)
        lon_larger_index = int((lon_larger + 180) /5)

        point_1 = interptime_pd_map[lat_smaller][lon_smaller_index]
        point_2 = interptime_pd_map[lat_smaller][lon_larger_index]
        point_3 = interptime_pd_map[lat_larger][lon_smaller_index]
        point_4 = interptime_pd_map[lat_larger][lon_larger_index]

        # compute interpolated value -- bilinear
        pd_array =np.array([[point_1,point_2],[point_3,point_4]])
        lat_array = np.array([lat_larger - self.lat,self.lat - lat_smaller])
        lon_array = np.array([[lon_larger - self.lon],[self.lon - lon_smaller]])
        coe = 1/((lat_larger - lat_smaller)*(lon_larger - lon_smaller))

        result = np.dot(lat_array,pd_array)
        result = coe * np.dot(result,lon_array)[0]

        return (result)


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
##----------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    date = '2009-07-16'
    time = '07:47:00'
    f    = 9.6 * pow(10,9)   #Ku
    #inc_near = 2.5
    inc_far = 41
    lat  = 37.76
    lon  = -25.47
    obj = ObsFile(date,time,f,inc_far,lat,lon)
    ipd = obj.processing_IPD_2()
    print (ipd)


























