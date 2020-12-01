import requests
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from datetime import datetime, timedelta


def WeeklyAverage(countries):
    data = requests.get('https://pomber.github.io/covid19/timeseries.json').json()
    date_format = mpl_dates.DateFormatter('%b %d')
    last_day = datetime.today()
    week = timedelta(days=7)
    plt.style.use('seaborn')
    plt.figure(figsize=(10,5))

    for country in countries:
        if country in data.keys():
            pass
        else:
            return (country + ' is not a valid country name. Please try again.\nNote : Countries entered are case sensitive. That means US is accepted, but Us is not. Please type "/country" without the quotes to view the available countries')
    for country in countries:
        total = 0
        week_day = 0
        prev = 0
        last_day = datetime.today()
        cases = []
        dates = []
        for num in data[country]:
            week_day+=1
            total += num['confirmed']-prev
            last_day = datetime.strptime(num['date'], '%Y-%m-%d')
            if week_day==7:
                cases.append(round(total/7, 2))
                total = 0
                week_day = 0
                dates.append(datetime.strptime(num['date'], '%Y-%m-%d')-week)
            prev = num['confirmed']
        if week_day!=0:
            cases.append(round(total/week_day, 2))
            dates.append(last_day-timedelta(days=week_day))
        plt.plot_date(dates, cases, label=country,linestyle='solid', marker=None)
    plt.title('7 Day moving average - Daily New cases')
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.savefig('WeeklyAverage.png')
    return 'OK'

def DailyCases(countries):
    data = requests.get('https://pomber.github.io/covid19/timeseries.json').json()
    date_format = mpl_dates.DateFormatter('%b %d')
    plt.style.use('seaborn')
    plt.figure(figsize=(10,5))

    for country in countries:
        if country in data.keys():
            pass
        else:
            return (country + ' is not a valid country name. Please try again.\nNote : Countries entered are case sensitive. That means US is accepted, but Us is not. Please type "/country" without the quotes to view the available countries')
    for country in countries:
        cases = []
        dates = []
        prev = 0
        for num in data[country]:
            cases.append(num['confirmed']-prev)
            dates.append(datetime.strptime(num['date'], '%Y-%m-%d'))
            prev = num['confirmed']
        plt.plot_date(dates, cases, label=country,linestyle='solid', marker=None)
    plt.title('Daily New cases')
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.savefig('DailyCasesWorld.png')
    return 'OK'

def CumulativeCases(countries):
    plt.style.use('seaborn')
    data = requests.get('https://pomber.github.io/covid19/timeseries.json').json()
    date_format = mpl_dates.DateFormatter('%b %d')
    plt.figure(figsize=(10,5))
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    for country in countries:
        if country in data.keys():
            pass
        else:
            return (country + ' is not a valid country name. Please try again.\nNote : Countries entered are case sensitive. That means US is accepted, but Us is not. Please type "/country" without the quotes to view the available countries')
    for country in countries:
        cases = []
        dates = []
        for num in data[country]:
            cases.append(num['confirmed'])
            dates.append(datetime.strptime(num['date'], '%Y-%m-%d'))
        plt.plot_date(dates, cases, label=country,linestyle='solid', marker=None)
    plt.title('Daily New cases')
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.savefig('DailyCasesWorld.png')
    return 'OK'
