import numpy as np
import scipy
import scipy.stats
import pandas as pd

def mann_whitney_plus_means(turnstile_weather):
    '''
    This function will consume the turnstile_weather dataframe containing
    our final turnstile weather data.

    You will want to take the means and run the Mann Whitney U-test on the
    ENTRIESn_hourly column in the turnstile_weather dataframe.

    This function should return:
        1) the mean of entries with rain
        2) the mean of entries without rain
        3) the Mann-Whitney U-statistic and p-value comparing the number of entries
           with rain and the number of entries without rain

    You should feel free to use scipy's Mann-Whitney implementation, and you
    might also find it useful to use numpy's mean function.
    '''
    df = pd.read_csv(turnstile_weather)
    rain_record = df.loc[df['rain'] == 1]['ENTRIESn_hourly']
    without_rain_record = df[(df.rain == 0)]['ENTRIESn_hourly']
    with_rain_mean = np.mean(rain_record)
    without_rain_mean = np.mean(without_rain_record)
    q = scipy.stats.mannwhitneyu(rain_record,without_rain_record)
    U = q[0]
    p = q[1]




    return with_rain_mean, without_rain_mean, U, p  # leave this line for the grader

print mann_whitney_plus_means(r'C:\Users\CJH\PycharmProjects\Data_Science_Anaconda\turnstile_data_master_with_weather.csv')
