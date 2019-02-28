import datetime

def addZero(num):
    if num < 10:
        num = "0" + str(num)
    return num

def getTime(dt, hour = True, minute = True, second = False):
    tm = dt.time()
    timeString = "{}".format(addZero(tm.hour))
    if minute:
        timeString += ":{}".format(addZero(tm.minute))
    if second:
        timeString += ":{}".format(addZero(tm.second))
    return timeString

def getDate(dt, day = True, month = True, year = True, sep="."):
    date = []
    dateString = sep
    if day:
        date.append(str(addZero(dt.day)))
    if month:
        date.append(str(addZero(dt.month)))
    if year:
        date.append(str(dt.year))
    return sep.join(date)

def getDateAndTime(dt):
    dateValue = getDate(dt)
    timeValue = getTime(dt, hour = True, minute = True, second = True)
    return timeValue + " | " + dateValue

def getDateAndTimeShort(dt):
    dV = getDate(dt, day = True, month = True, year = False, sep=".")
    tV = getTime(dt, hour = True, minute = True, second = False)
    return dV + "., " + tV

def nowToWeekNumYear(passedWeeks = 0):
    now = datetime.datetime.utcnow()
    string = datetimeToWeekNumYear(now, passedWeeks)
    return string

def datetimeToWeekNumYear(unixTime, passedWeeks = 0):
    weekAndYear = unixTime.isocalendar()
    yearNum = weekAndYear[0]
    weekNum = weekAndYear[1]
    if passedWeeks >= weekNum:
        yearNum -=1
        weekNum = weekNum-passedWeeks + 52
    else:
        weekNum = weekNum - passedWeeks
    return "{}-{}".format(yearNum, weekNum)

def getNextWeekday(weekday, hour = 0, minute = 0, second = 0):
    d = datetime.datetime.utcnow()
    t = datetime.timedelta((7 + weekday - d.weekday()) % 7)
    newD = (d + t).replace(hour=hour, minute=minute, second=second)
    return newD

def isoToDates(isoDates):
    dates = [datetime.datetime.fromisoformat(date) for date in isoDates]
    return dates

def passedTimeInDays(startDate, endDate):
    passedTime = endDate - startDate
    passedDays = passedTime.total_seconds()//(60*60*24)
    return int(passedDays)

def getLastNWeeksFromArray(weeks, array):
    today=datetime.datetime.utcnow()
    passedDays = weeks * 7
    interval = datetime.timedelta(days=passedDays)
    beginningDay = today-interval
    return [day for day in array if day > beginningDay]
