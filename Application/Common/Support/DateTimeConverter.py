from datetime import datetime

class DateTimeConverter:
    def ConvertDatetime(datetimeInput: str):
        year = int(datetimeInput[:4])
        month = int(datetimeInput[5:7])
        day = int(datetimeInput[8:10])
        hour = int(datetimeInput[11:13])
        minute = int(datetimeInput[14:16])
        second = int(datetimeInput[17:19])
        return datetime(year, month, day, hour, minute, second)

    def ConvertDate(dateInput : str):
        year = int(dateInput[:4])
        month = int(dateInput[5:7])
        day = int(dateInput[8:10])
        return datetime(year, month, day)