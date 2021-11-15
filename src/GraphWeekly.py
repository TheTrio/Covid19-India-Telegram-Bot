import json
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta,datetime
import matplotlib.dates as mpl_dates
import sys

def update():

    with open('Last.txt', 'r') as f:
        last = int(f.read().replace('\n', ''))
    jsonurl = urllib.request.urlopen('https://api.covid19india.org/states_daily.json')
    data = json.load(jsonurl)
    if last==len(data['states_daily']):
        return
    fig, ax = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(10)
    plt.style.use('fivethirtyeight')
    plt.xlabel('First day of week')
    plt.title('7 day moving average since March 14')
    plt.ylabel('New cases')
    avg = []
    week_day = 0
    total = 0
    no_of_days = 0
    for line in data['states_daily']:
        if line['status']=='Confirmed':
            week_day+=1
            total += int(line['tt'])
            print(int(line['tt']))
            if week_day==7:
                avg.append(round(total/7, 2))
                total = 0
                week_day = 0
                no_of_days+=1
    if week_day!=0:
        avg.append(round(total/week_day, 2))
        no_of_days+=1
    print(avg[-1], week_day)
    start_date = datetime(year=2020, month=3, day=14)
    names = []
    for i in range(no_of_days):
        names.append(start_date)
        start_date = start_date + timedelta(days=7)
    date_format = mpl_dates.DateFormatter('%b %Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    ax.bar(names, avg, width=2)
    ax.xaxis_date()
    fig.savefig('GraphWeekly.png')

    with open('Last.txt', 'w') as f:
        f.write(str(len(data['states_daily'])))
if len(sys.argv) > 1:
    update()
