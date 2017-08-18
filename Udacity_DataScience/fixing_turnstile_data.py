import csv
import re
import pandas
import datetime
import math

def fix_turnstile_data(filename,newfilename):
    with open(filename,'rb') as f:
        with open(newfilename, 'w') as o:
           o.write('C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn\n')

           filenames = csv.reader(f,delimiter = ',')
           for name in filenames:
               for i in range(3,len(name),5):

                   writer = csv.writer(o,delimiter = ',')
                   writer.writerow(name[0:3] + name[i:i+5])

#fix_turnstile_data(r'C:\Users\CJH\PycharmProjects\Udacity_DataScience\turnstile-110528.txt',r'C:\Users\CJH\PycharmProjects\Udacity_DataScience\Updated_turnstile-110528.txt')
def filter_by_regular(filename):

    df = pandas.read_csv(filename)
    turnstile_data = df.loc[df['DESCn'] == 'REGULAR']
    return  turnstile_data

def get_hourly(df):
    '''
        The data in the MTA Subway Turnstile data reports on the cumulative
        number of entries and exits per row.  Assume that you have a dataframe
        called df that contains only the rows for a particular turnstile machine
        (i.e., unique SCP, C/A, and UNIT).  This function should change
        these cumulative entry numbers to a count of entries since the last reading
        (i.e., entries since the last row in the dataframe).

        More specifically, you want to do two things:
           1) Create a new column called ENTRIESn_hourly
           2) Assign to the column the difference between ENTRIESn of the current row
              and the previous row. If there is any NaN, fill/replace it with 1.

        You may find the pandas functions shift() and fillna() to be helpful in this exercise.

        Examples of what your dataframe should look like at the end of this exercise:

               C/A  UNIT       SCP     DATEn     TIMEn    DESCn  ENTRIESn    EXITSn  ENTRIESn_hourly
        0     A002  R051  02-00-00  05-01-11  00:00:00  REGULAR   3144312   1088151                1
        1     A002  R051  02-00-00  05-01-11  04:00:00  REGULAR   3144335   1088159               23
        2     A002  R051  02-00-00  05-01-11  08:00:00  REGULAR   3144353   1088177               18
        3     A002  R051  02-00-00  05-01-11  12:00:00  REGULAR   3144424   1088231               71
        4     A002  R051  02-00-00  05-01-11  16:00:00  REGULAR   3144594   1088275              170
        5     A002  R051  02-00-00  05-01-11  20:00:00  REGULAR   3144808   1088317              214
        6     A002  R051  02-00-00  05-02-11  00:00:00  REGULAR   3144895   1088328               87
        7     A002  R051  02-00-00  05-02-11  04:00:00  REGULAR   3144905   1088331               10
        8     A002  R051  02-00-00  05-02-11  08:00:00  REGULAR   3144941   1088420               36
        9     A002  R051  02-00-00  05-02-11  12:00:00  REGULAR   3145094   1088753              153
        10    A002  R051  02-00-00  05-02-11  16:00:00  REGULAR   3145337   1088823              243
        ...
        ...

        '''

    pre_df = df.shift(periods=1,axis=0)
    df['ENTRIESn_hourly'] = (df['ENTRIESn']  -  pre_df['ENTRIESn']).fillna(0)
    df['EXITSn_hourly'] = (df['EXITSn']  -  pre_df['EXITSn']).fillna(0)
    print df
    return df


#turnstile_data = filter_by_regular('C:\Users\CJH\PycharmProjects\Udacity_DataScience\Updated_turnstile-110528.txt')
#get_hourly(turnstile_data)
u1 = 0.299
u2 = 0.307
n1 = 150
n2 =165
sigma1 = 0.05
sigma2 = 0.08
t = (u2 - u1) / math.sqrt(sigma1/n1 + sigma2/n2)
v1 = (sigma1/n1 + sigma2/n2) ** 2
v2 =  (sigma1 ** 2) / ((n1**2) * (n1 - 1) )
v3 =  (sigma2 ** 2) / ((n2**2) * (n2 - 1))

print v1/(v2+v3)
