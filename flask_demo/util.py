# coding=utf-8
from dateutil import rrule
from datetime import datetime

def GetBetweenMonth(start, end):
    '''获取从start开始到end之间的所有的月份；start传入的是datetime类型，返回的是datetime的list'''
    res = []
    for dt in rrule.rrule(rrule.MONTHLY,
                      dtstart=start,
                      until=end):
        res.append(dt.strftime('%Y-%m'))
    # print(res)
    return res

def GetMonth2Quarter(monthlist):
    '''获取monthlist中month到quarter字串的映射'''
    pass

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
    GetBetweenYear(a,b)