import datetime


def last_year(years=1):
    return datetime.datetime.now() - datetime.timedelta(days=365*years)