import datetime,time
import math
import numpy as np
import pylab as pl
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.ticker as mtick


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



    def get_base_radius(self):
        with open(self.fh)as obs_file:
            lines = obs_file.readlines()
            for line in lines:
                comment = line[60:].strip()
                if comment == 'BASE RADIUS':
                    no_space = ''.join(line[:60].split())  # second
                    base_radius = float(no_space)
            return base_radius


    def get_all_maps(self):
        with open(self.fh)as obs_file:
            row_number = 0
            lines = obs_file.readlines()
            create_maps = {}
            count = 0
            value = {}
            map1_flag = 0
            date_record = []
            for line in lines:
                fixed_lat_data = []

                comment = line[60:].strip()
                if comment == 'EPOCH OF CURRENT MAP':

                    time_str = '-'.join(line[:60].split())
                    date = time.strptime(time_str, '%Y-%m-%d-%H-%M-%S')  # third: record map epoch
                    y, m, d, h = date[0:4]
                    date = datetime.datetime(y, m, d, h)
                    date_record.append(date)
                    if map1_flag == 71:
                        map1_date = date_record.pop(0)
                        create_maps[map1_date] = value
                        value = {}

                    if count == 71:
                        # print ('yes')
                        create_maps[date] = value
                        value = {}
                        count = 0

                    initial_lat = 87.5

                if comment == 'LAT/LON1/LON2/DLON/H':
                    '''it's time to access TEC data,stick the next 5 lines together'''

                    for next in range(1, 6):
                        raw_data = lines[row_number + next].split()
                        for ele in raw_data:
                            fixed_lat_data.append(float(ele))

                    value[initial_lat] = fixed_lat_data

                    # print (value)
                    initial_lat -= 2.5
                    count += 1
                    map1_flag += 1

                row_number += 1

        return create_maps


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


    def draw_time_map(self,lat,log):
        latt = lat
        logg = log
        tec,time = self.get_tec_along_time(latt,logg)

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
        title = 'TEC during one day at '+ 'lattitude:' + str(latt)+' longitude:'+ str(log)
        plt.title(title)


        ax.plot(time, tec, '--b*')
        filename = 'TEC at ' + str(latt) + str(log)
        plt.savefig(filename)
        plt.show()

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



    def draw_position_map(self,time):
        lats,lons,tec = self.get_tec_with_position(time)
        # set up map projection
        # use low resolution coastlines
        map = Basemap(projection = 'ortho',lat_0 = 35,lon_0 = 120,resolution = '1')

        # draw lat/lon grid lines scales
        map.drawmeridians(np.arange(-180,180,5))
        map.drawparallels(np.arange(-87.5,87.5,2.5))

        #compute native map projection coordinates of lat/lon grid
        x,y = map(lons,lats)

        max_tec = max(tec)

        #set some parameters about the graph
        y_offset    =15.0
        rotation    =30
        for i,j,k in zip(x,y,tec):
            cs = map.scatter(i,j,tec,marker = 'o',color = '#FF5600')
            plt.text(i,j+y_offset,rotation = rotation,fontdict=10)

        plt.title('Global Tec at'+ str(time))
        plt.show()


    def exact_path_delay(self,time,lat,lon,inc,f):
        TECU = pow(10, 16)
        point_tec = self.look_up_map(time,lat,lon) * 0.1 * TECU

        K = 40.3
        rad = math.pi * inc / 180

        point_iono_delay = K * point_tec / (pow(f,2) * math.cos(rad) )

        return point_iono_delay




if __name__ == '__main__':
    file = 'CKMG0010.16I'
    obj = ObsFile(file)
    #print(obj.look_up_map(datetime.datetime(2016,1,1,19),0,90))
    #obj.draw_time_map(0,90)
    #obj.get_tec_with_position(datetime.datetime(2016,1,1,20))
    delay = obj.exact_path_delay(datetime.datetime(2016,1,1,18,0),0,90,10,13.58 * pow(10,9))
    print (delay)











