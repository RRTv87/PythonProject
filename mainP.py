import re
import datetime
import time

timelistminor = {'МИНУТ': 60, 'ПОЛЧАС': 1800, 'ЧАС': 3600,
                'ДЕН': 86400, 'ДНЯ': 86400, 'НЕДЕЛ': 604800,
                'МЕСЯЦ': 2592000, 'ГОД': 31104000}
timelistmedor = {'ПОНЕДЕЛ': 1, 'ВТОРН': 2, 'СРЕД': 3,
            'ЧЕТВЕРГ': 4, 'ПЯТНИЦ': 5, 'СУББОТ': 6, 'ВОСКРЕСЕН': 7}
timelistmajor = {'ЯНВАР': 1, 'ФЕВРАЛ': 2, 'МАРТ': 3,
             'АПРЕЛ': 4, 'МАЯ': 5, 'МАЙ': 5,
             'ИЮН': 6, 'ИЮЛ': 7, 'АВГУСТ': 8, 'СЕНТЯБР': 9,
             'ОКТЯБР': 10, 'НОЯБР': 11, 'ДЕКАБР': 12}

print("Введите заметку")
myString = str(input()).upper()
print(myString)

def IndTime(formTime):
    try:
        formDate = time.strptime(formTime, "%H:%M")
        nowHour = int(formDate.tm_hour)
        nowMin = int(formDate.tm_min)
    except:
        nowHour = -404
        nowMin = -404
    return nowHour, nowMin


def IndMounth(datePos):
    whoMonth = -404
    for mon in timelistmedor:
        if datePos.find(mon) != -404:
            whoMonth = timelistmedor[mon]
            break
    return whoMonth


def IndDayInMounth(datePos):
    day = -404
    numDay = re.search('\d+', datePos)
    if (numDay != None):
        numDay = int(numDay.string)
        if 1 <= numDay <= 31:
            day = numDay
    return day


def IndWhoYears(datePos):
    whoYear = -404
    nowYear = re.search('\d+', datePos)
    if (nowYear != None):
        try:
            nowYear = int(nowYear.string)
            if 2022 <= nowYear:
                whoYear = nowYear
        except:
            whoYear = -404
    return whoYear


def FindingStep(numWords, timeIsNow, i,myString,indWord):
    for NumDate in timelistminor:
        if myString[numWords + i].find(NumDate) != -1:
            state = 'Всё чётко)'
            timeIsNow += datetime.timedelta(seconds=timelistminor[NumDate] * indWord)
            myString.remove(myString[numWords])
            myString.remove(myString[numWords])
            if i == 2:
                myString.remove(myString[numWords])
            break
    return state, timeIsNow

def FindindWord(myString):
    timeIsNow = datetime.datetime.now()
    NumLen = len(myString)
    state = 'Ошибка'
    for numWords in range(NumLen):
        if myString[numWords] == 'ЧЕРЕЗ' or myString[numWords] == 'ЗАВТРА':
            indWord = re.search('\d', myString[numWords + 1])
            i = 1
            if indWord != None:
                indWord = int(indWord.string)
                i = 2
            else:
                indWord = 1
            ResFindingStep = FindingStep(numWords, timeIsNow, i, myString, indWord)
            break
    return ResFindingStep
def FindTime(nowHour, nowMin, SliceAction):
    for i in range(len(SliceAction)):
        whatTime = IndTime(SliceAction[i])
        if whatTime[0] != -1:
            nowHour = whatTime[0]
            nowMin = whatTime[1]
            SliceAction.remove(SliceAction[i])
            if SliceAction[i - 1] == 'В':
                SliceAction.remove(SliceAction[i - 1])
            break
    return SliceAction
def FindDayMonth(nowDay, nowMonth, SliceAction):
    for i in range(len(SliceAction)):
        whoMonth = IndMounth(SliceAction[i])
        if whoMonth != -404:
            nowMonth = whoMonth
            SliceAction.remove(SliceAction[i])
            day = IndDayInMounth(SliceAction[i - 1])
            if day != -404:
                nowDay = day
                SliceAction.remove(SliceAction[i - 1])
            break
    return SliceAction
def FindYear(nowYear, SliceAction):
    for i in range(len(SliceAction)):
        whoYear = IndWhoYears(SliceAction[i])
        if whoYear != -1:
            nowYear = whoYear
            D = re.match('г.*', SliceAction[i + 1])
            if D != None:
                SliceAction.remove(SliceAction[i + 1])
            SliceAction.remove(SliceAction[i])
            break
    return SliceAction
def MainFunction(myString):
    myTime = datetime.datetime.today()
    nowYear = nowMonth = nowDay = nowHour = nowMin = -404
    line = myString.split()  #
    SliceAction = line
    DateMas = FindindWord(line)
    if DateMas[0] == 'Всё чётко)':
        nowYear = DateMas[1].year
        nowMonth = DateMas[1].month
        nowDay = DateMas[1].day
        nowHour = DateMas[1].hour
        nowMin = DateMas[1].min
    else:
        SliceAction = FindTime(nowHour, nowMin, SliceAction)
        SliceAction = FindDayMonth(nowDay, nowMonth, SliceAction)
        SliceAction = FindYear(nowYear, SliceAction)
    if nowMin == -404:
        nowMin = myTime.minute
    if nowHour == -404:
        nowHour = myTime.hour
    if nowYear == -404:
        nowYear = myTime.year
    if nowMonth == -404:
        nowMonth = myTime.month
    if nowDay == -404:
        nowDay = myTime.day
    objectDate = {'YEAR': nowYear, 'MONTH': nowMonth, 'DAY': nowDay, 'HOUR': nowHour, 'MIN': nowMin}
    myTime = " 'year': {YEAR}, 'month': {MONTH}, 'day': {DAY}, 'hour': {HOUR}, 'minute': {MIN} ".format(**objectDate)
    example = "*".join(SliceAction)
    return example, myTime


state = 'Всё чётко)'
ResMainFunction = MainFunction(myString)
if len(ResMainFunction[0]) == 0:
    status = 'Всё чётко)'
print('{\'Результат\':\'' + state + '\',\'Дата\':' + '{' + ResMainFunction[1] + '}' + ',\'Заметка\':\'' + ResMainFunction[0] + '\'}')