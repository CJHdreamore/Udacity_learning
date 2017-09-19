import  os
import shutil
import time,datetime
import calendar

#-----what a pity when I finished coding, I realized that this function may not be useful--------
def organize_file(rootdir,new_dir_name):
    dir_names = os.listdir(rootdir)  # get all dirs under the rootdir
    current_workpath = os.getcwd()
    new_dir = os.path.join(current_workpath, new_dir_name)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    for entry in dir_names:

        dir_path = os.path.join(rootdir, entry)

        file_name = os.listdir(dir_path)

        file_path = os.path.join(dir_path, file_name[0])

        if os.path.isfile(file_path):

            new_file_path = os.path.join(new_dir, file_name[0])

            if not os.path.exists(new_file_path):

                shutil.move(file_path, new_dir)

        os.rmdir(dir_path)
    return new_dir


#---------remodify files with regular name----------
def modify_name(dir_path):
    files = os.listdir(dir_path)

    for old_name in files:

        if old_name[0:4]== 'CODG':        # modify file name of iono to standard format I2017-3-16

            ddd = int(old_name[4:7])
            yy = "20" + old_name[9:11]
            year = int(yy)
            print(year)
            d1 = datetime.datetime(year, 1, 1)
            print(d1)
            d2 = d1 + datetime.timedelta(days=ddd - 1)
            print(d2)
            new_name = 'I' + d2.strftime("%Y-%m-%d")
            print(new_name)
            if not os.path.exists(dir_path + '/' + new_name):
                print("yes")
                os.rename(dir_path + '/' + old_name, dir_path + '/' + new_name)


        elif old_name[-3:] == 'TRO':    #modify file name of tropo to standard format such as T2017-3-16

            gps_week = int(old_name[3:7])
            day_of_week = int(old_name[7])
            start_date = datetime.datetime(1980,1,6,0,0,0)
            delta_hours = gps_week * 168 + day_of_week * 24
            current_date = start_date + datetime.timedelta(hours = delta_hours)
            new_name = 'T' + current_date.strftime('%Y-%m-%d')
            #print (new_name)
            if not os.path.exists(dir_path + '/' + new_name):
                os.rename(dir_path + '/' + old_name,dir_path + '/' + new_name)



rootdir = r'C:\Users\CJH\PycharmProjects\path_delay'
modify_name(rootdir)







