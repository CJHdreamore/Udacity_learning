# By Websten from forums
#
# Given your birthday and the current date, calculate your age in days.
# Account for leap days.
#
# Assume that the birthday and current date are correct dates (and no
# time travel).
#

def daysBetweenDates(year1, month1, day1, year2, month2, day2):
    leap_count = 0
    d_y= year2 - year1
    if year1 == year2:
        return comp(year2,month2,day2)
    while year1 <= year2:
        leap_count = leap_count + judge_leapyear(year1)
        year1 = year1 + 1
    # count out how many leap years
    d_year = leap_count * 366 + ((d_y + 1) - leap_count) * 365

    comp_year = d_year -( comp(year1,month1,day1) + (365 - comp(year2,month2,day2)+judge_leapyear(year2)))
    return comp_year

def judge_leapyear(n):
    if n % 4 == 0:
        if n % 100 != 0:
            return 1
        else:
            return 0
    else:
        if n % 400 == 0:
            return 1
        return 0

def comp(y,m,d):
    normal_month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    comp_month = 0
    n_month = m - 1
    while n_month >= 1:
        if judge_leapyear(y) == 1:
            normal_month_list[1] = 29
        comp_month = comp_month + normal_month_list[n_month - 1]
        n_month = n_month - 1

    comp_day = comp_month + d - 1
    return comp_day
# Test routine



def test():
    test_cases = [((2012,1,1,2012,2,28), 58),
                  ((2012,1,1,2012,3,1), 60),
                  ((2011,6,30,2012,6,30), 366),
                  ((2011,1,1,2012,8,8), 585 ),
                  ((1900,1,1,1999,12,31), 36523)]
    for (args, answer) in test_cases:
        result = daysBetweenDates(*args)
        print result
        if result != answer:
            print "Test with data:", args, "failed"
        else:
            print "Test case passed!"

test()