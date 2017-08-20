import ggplot
from ggplot import *
from pandas import *


df = pandas.read_csv(r'C:\Users\CJH\PycharmProjects\Data_Science_Anaconda\turnstile_data_master_with_weather.csv')

def plot_weather_data(df):
    '''
    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time of day or day of week
     * How ridership varies based on Subway station (UNIT)
     * Which stations have more exits or entries at different times of day
    (You can use UNIT as a proxy for subway station.)
    :param df:
    :return:
    '''
    # Ridership by time of day
    p1 = ggplot(df,aes(x = 'Hour',y = 'ENTRIESn_hourly')) + geom_bar()+\
        ggtitle(' Ridership by time of day')
    # Ridership varies based on Unit
    p2 = ggplot(df,aes(x = 'Hour',y = 'ENTRIESn_hourly',color = 'UNIT')) + geom_point()+\
        scale_color_gradient(low = 'black',high = 'red') +\
         ggtitle(' Ridership by time of day in different stations')
    p3 = ggplot(df,aes(x = 'Hour',y = 'ENTRIESn_hourly')) + geom_point() + stat_smooth
    return p3
print plot_weather_data(df)