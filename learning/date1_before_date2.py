def date1_before_date2(year1,month1,day1,year2,month2,day2):
    if year1 < year2:
        return True
    else:
        if year1 == year2:
            if month1 < month2:
                return True
            else:
               if month1 == month2:
                   if day1 < day2:
                      return True






print date1_before_date2(2013,5,2,2012,6,2)