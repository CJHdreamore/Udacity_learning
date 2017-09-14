import datetime,time
with open('CKMG0010.16I')as obs_file:
    row_number = 0
    one_lat = 0
    lines = obs_file.readlines()
    create_maps = {}
    count = 0
    value={}
    map1_flag = 0
    date_record = []
    for line in lines:
        fixed_lat_data = []

        comment = line[60:].strip()

        #print (comment)
        if comment == '# OF MAPS IN FILE':
            no_space =''.join(line[:60].split())
            number_maps = int(no_space)           # one parameter

        if comment == 'BASE RADIUS':
            no_space = ''.join(line[:60].split())    #second
            base_radius = float(no_space)
            #print (base_radius)

        if comment == 'EPOCH OF CURRENT MAP':

            time_str = '-'.join(line[:60].split())
            date = time.strptime(time_str,'%Y-%m-%d-%H-%M-%S')   # third: record map epoch
            y, m, d, h = date[0:4]
            date = datetime.datetime(y,m,d,h)
            date_record.append(date)
            if map1_flag == 71:

                map1_date = date_record.pop(0)
                create_maps[map1_date] = value
                value = {}

            if count == 71:
               # print ('yes')
                create_maps[date] = value
                value ={}
                count = 0

            initial_lat = 87.5


        if comment == 'LAT/LON1/LON2/DLON/H':
            '''it's time to access TEC data,stick the next 5 lines together'''

            for next in range(1,6):
                raw_data = lines[row_number+next].split()
                for ele in raw_data:
                    fixed_lat_data.append(float(ele))

            value[initial_lat] = fixed_lat_data

            #print (value)
            initial_lat -= 2.5
            count += 1
            map1_flag += 1





        row_number += 1
print (create_maps[datetime.datetime(2016, 1, 1, 0, 0)])
print (create_maps[datetime.datetime(2016, 1, 1, 12, 0)])



















