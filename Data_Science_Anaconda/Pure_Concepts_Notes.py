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
def parse_maybe_float(minutes):
    if minutes == '':
        return None
    else:
        return float(minutes)



# Question Phase  Let's brain storming !
# 1.the average num-course-visited
# 2.the average minutes students spent
# 3.which course does most students take?
# 4.the average time students spend on finishing a course
# 5.what's the trend of spending time based on different course?

# Next challenge:Find the number of rows in each table and the num of unique students

enrollment_num_rows = len(enrollment)
unique_students_enrollment =[]
for element in enrollment:
    element['cancel_date'] = parse_date(element['cancel_date'])
    element['days_to_cancel'] = parse_maybe_int(element['days_to_cancel'])
    element['is_canceled'] = element['is_canceled'] == 'True'
    element['is_udacity'] = element['is_udacity'] == 'True'
    element['join_date'] = parse_date(element['join_date'])
    if element['account_key'] not in unique_students_enrollment:
        unique_students_enrollment.append(element['account_key'])
enrollment_num_unique_students = len(unique_students_enrollment)
#print enrollment_num_unique_students
#print enrollment_num_rows

engagement_num_rows = len(daily_engagement)
unique_students_engagement =[]
for element in daily_engagement:
    element['utc_date'] = parse_date(element['utc_date'])
    element['num_courses_visited'] = int(float(element['num_courses_visited']))
    element['total_minutes_visited'] = parse_maybe_float(element['total_minutes_visited'])
    element['lessons_completed'] = int(float(element['lessons_completed']))
    element['projects_completed'] = int(float(element['projects_completed']))
    if element['acct'] not in unique_students_engagement:
        unique_students_engagement.append(element['acct'])
engagement_num_unique_students = len(unique_students_engagement)
#print engagement_num_unique_students
#print engagement_num_rows

submission_num_rows = len(project_submission)
unique_students = []
for element in project_submission:
    element['creation_date'] = parse_date(element['creation_date'])
    element['completion_date'] = parse_date(element['completion_date'])
    if element['account_key'] not in unique_students:
        unique_students.append(element['account_key'])
submission_num_unique_students = len(unique_students)
#print submission_num_rows
#print submission_num_unique_students

# From the results below, there are some questions:
# 1.Why the number of unique students in enrollment is different from engagement?
# 2.Column named account_key in the second table while named "acct" in the third one.

# Next Task: Rename "acct" column to "account_key" in daily_engagement table

for element in daily_engagement:
    element['account_key'] = element.pop('acct')
    #another choice
    #element['account_key'] = element['acct']
    #del element['acct']
#print daily_engagement[0]['account_key']

# Next Task: Find out why there are some students missing in engagement file,print out the abnormality.
num = 0
for element in enrollment:
    if element['account_key'] not in unique_students_engagement:
        if element['join_date'] != element['cancel_date']:
            num += 1

# Find out all the test_accounts in enrollment
udacity_test_accounts = set()
for element in enrollment:
    if element['is_udacity']:
        udacity_test_accounts.add(element['account_key'])
#print len(udacity_test_accounts)

# Create a new dictionary which doesn't involve udacity_test_enrollment
def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data

non_udacity_enrollments = remove_udacity_accounts(enrollment)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submission)

#print len(non_udacity_enrollments)
#print len(non_udacity_engagement)
#print len(non_udacity_submissions)


#Create a dictionary of students in non_udacity_engagement who either:
# 1. haven't canceld yet
# 2. stayed enrolled more than 7 days.
# keys : account keys ; values: enrollment date
# dictionary name : paid_students

paid_students = {}
for element in non_udacity_enrollments:
    if element['days_to_cancel'] == 'None' or element['days_to_cancel'] > 7:
        account_key = element['account_key']
        join_date = element['join_date']
        if account_key not in paid_students or join_date > paid_students[account_key]:
            paid_students[account_key] = join_date

#print paid_students
print len(paid_students)
















