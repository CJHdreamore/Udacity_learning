import numpy as np
import pandas
import matplotlib.pyplot as plt
from pandas import Series
import pylab

def entries_histogram(filename):
   turnstile_weather = pandas.read_csv(filename)
   df = pandas.DataFrame({'Rain':Series(turnstile_weather[(turnstile_weather.rain == 1)]['ENTRIESn_hourly']),
                         'No Rain':Series(turnstile_weather[(turnstile_weather.rain == 0)]['ENTRIESn_hourly'])
                          },index= turnstile_weather.index,columns=['Rain','No Rain'])

   df.plot.hist(stacked=True,bins=100)
   pylab.xlim(0,6000)
   pylab.xlabel('ENTRIESn_hourly')
   pylab.title('Histogram of ENTRIESn_hourly ')
   plt.show()


entries_histogram(r'C:\Users\CJH\PycharmProjects\Data_Science_Anaconda\turnstile_data_master_with_weather.csv')