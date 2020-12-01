import json
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta,datetime
import sys

def update():

    with open('Last.txt', 'r') as f:
        last = int(f.read().replace('\n', ''))
    jsonurl = urllib.request.urlopen('https://api.covid19india.org/states_daily.json')
    data = json.load(jsonurl)
    if last==len(data['states_daily']):
        return
    plt.figure(figsize=(50, 30))
    plt.style.use('fivethirtyeight')
    plt.rc('xtick', labelsize=30)
    plt.rc('axes', labelsize=70)
    plt.rc('axes', titlesize=100)
    plt.rc('ytick', labelsize=70)
    plt.xlabel('First day of week', labelpad=40)
    plt.title('7 day moving average since March 14')
    plt.ylabel('New cases', labelpad=40)

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
        names.append(start_date.strftime('%d %b'))
        start_date = start_date + timedelta(days=7)
    x_labels = np.arange(len(avg))
    x_labels = [4*x for x in x_labels]
    plt.xticks(ticks=x_labels, labels=names)
    plt.bar(x_labels,avg, width=2)
    plt.savefig('GraphWeekly.png')

    with open('Last.txt', 'w') as f:
        f.write(str(len(data['states_daily'])))
if len(sys.argv) > 1:
    update()
