import datetime
from datetime import timedelta, date

def n_days_ago(n):
    today = datetime.date.today()
    return today - datetime.timedelta(days=n)


def today():
    return datetime.datetime.date(datetime.datetime.now())


def yesterday():
    one_days_age= n_days_ago(1)
    return one_days_age


def last_seven_days():
    seven_days_ago= n_days_ago(7)
    return seven_days_ago


def last_thirty_days():
    thirty_days_ago=n_days_ago(30)
    return thirty_days_ago


def current_month():
    month = datetime.datetime.now().month
    return month


def last_month_year():
    today = date.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    print(last_month.strftime("%Y"))
    return last_month.strftime("%Y")


def last_month():
    today = date.today()
    first = today.replace(day=1)
    lastMonth = first - timedelta(days=1)
    print(lastMonth.strftime("%m"))
    return lastMonth.strftime("%m")


def current_year():
    today = datetime.datetime.today()
    return today.year


def last_year():
    now = datetime.datetime.now()
    return now.year - 1