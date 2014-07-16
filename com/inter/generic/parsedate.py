import datetime

def dateConvert(_date):
    sDate = _date
    format2 = "%Y-%m-%d"
    return datetime.datetime.strptime(sDate,"%m/%d/%Y %H:%M:%S %p").strftime(format2)
