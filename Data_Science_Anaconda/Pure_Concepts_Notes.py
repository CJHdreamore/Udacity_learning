# Hey,this is another course in Udacity about DataScience!
# It's taught by the same teacher in the course of "The beginning of Github".
# So,I can't wait to follow her to take a second(cause I have enrolled another DS course) step
# in DataScience!!

#------Start From Here!-------------------
# How to represent a CSV file in python?
# Option 1: Each row is a list, so a csv file is list of list!
csv = [['a1','a2','a3'],
       ['b2','b3','b3']]
#Option 2: Each row is a dictionary
# This is helpful when our csv file has a header.
# Because each key can be column name.
# The overall will be a list of dictionaries

csv = [{'name1':'a1','name2': 'a2','name3':'a3'},
       {'name1':'b1','name2':'b2','name3':'b3'}]

import unicodecsv
def read_csvfile(filename):
    with open(filename,'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

daily_engagement = read_csvfile(r'C:\Users\CJH\PycharmProjects\Data_Science_Anaconda\daily-engagement.csv')
enrollment = read_csvfile(r'C:\Users\CJH\PycharmProjects\Data_Science_Anaconda\enrollments.csv')
project_submission = read_csvfile(r'C:\Users\CJH\PycharmProjects\Data_Science_Anaconda\project-submissions.csv')


# According to the code below, there is a problem that all outcome is presented as a string! so we should modify their data type!
from datetime import datetime as dt

def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date,'%Y-%m-%d')

def parse_maybe_int(days):
    if days == '':
        return None
    else:
        return int(days)

for element in enrollment:
    element['cancel_date'] = parse_date(element['cancel_date'])
    element['days_to_cancel'] =parse_maybe_int(element['days_to_cancel'])
    element['is_canceled'] = element['is_canceled'] == 'True'
    element['is_udacity'] = element['is_udacity'] == 'True'
    element['join_date'] = parse_date(element['join_date'])

#print enrollment[1]
#print daily_engagement[0]
#print project_submission[0]

# Question Phase  Let's brain storming !
# 1.the average num-course-visited
# 2.the average minutes students spent
# 3.which course does most students take?
# 4.the average time students spend on finishing a course
# 5.what's the trend of spending time based on different course?

# Next challenge:Find the number of rows in each table


