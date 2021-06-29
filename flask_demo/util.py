# coding=utf-8
from dateutil import rrule
from datetime import datetime

def GetBetweenMonth(start, end):
    '''获取从start开始到end之间的所有的年份-月份；start传入的是datetime类型，返回的是datetime的list'''
    res = []
    for dt in rrule.rrule(rrule.MONTHLY,
                      dtstart=start,
                      until=end):
        res.append(dt.strftime('%Y-%m'))
    # print(res)
    return res

def GetBetweenQuarter(start, end):
    '''获取从start开始到end之间的所有的年份-季度；start传入的是datetime类型，返回的是datetime的list'''
    months = GetBetweenMonth(start, end)
    res = []
    for month in months:
        mon_date = datetime.strptime(month, '%Y-%m')
        quarter = (mon_date.month-1) / 3 + 1
        re = str(mon_date.year) + '-' + str(quarter)
        if len(res)==0 or res[len(res)-1]!=re:
            res.append(re)
    # print(res)
    return res

def GetBetweenYear(start, end):
    '''获取从start开始到end之间的所有的年份；start传入的是datetime类型，返回的是datetime的list'''
    res = []
    for dt in rrule.rrule(rrule.YEARLY,
                      dtstart=start,
                      until=end):
        res.append(dt.strftime('%Y'))
    # print(res)
    return res

if __name__ == "__main__":
    a = '2012-05-25'
    b = '2012-06-27'
    a = datetime.strptime(a, '%Y-%m-%d')
    b = datetime.strptime(b, '%Y-%m-%d')

    GetBetweenMonth(a,b)
    GetBetweenQuarter(a,b)
    GetBetweenYear(a,b)