from datetime import datetime,timezone
import requests
from collections import OrderedDict
import json
import pytz

timezone_IST = pytz.timezone('Asia/Kolkata')
def getString():
    today = datetime.now(timezone.utc)
    today = today.astimezone(timezone_IST)
    today_str = today.strftime('%B %d, %Y')

    data = json.loads(requests.get('https://api.covid19india.org/data.json').content, object_pairs_hook=OrderedDict)

    tested_today = data['tested'][-1]
    today_numbers = data['cases_time_series'][-1]

    output_str = f'''Hope you're having a great day so far!
Today is {today_str} and the time is {today.strftime('%I:%M %p')}

The numbers for {today_numbers['date'].strip()} are
'''

    mid_str=f'''
New samples tested : {int(tested_today['samplereportedtoday']):,}
New cases found : {int(today_numbers['dailyconfirmed']):,}
New deaths recorded : {int(today_numbers['dailydeceased']):,}
New Recoveries : {int(today_numbers['dailyrecovered']):,}
'''

    Fatality_Rate = '{:.2%}'.format(int(today_numbers['totaldeceased'])/int(today_numbers['totalconfirmed']))
    Positivity_Rate = '{:.2%}'.format(int(today_numbers['totalconfirmed'])/int(tested_today['totalsamplestested']))
    Recovery_Rate = '{:.2%}'.format(int(today_numbers['totalrecovered'])/int(today_numbers['totalconfirmed']))



    end_str = f'''
With these, here are our cumulative numbers

Total Tests : {int(tested_today['totalsamplestested']):,}
Total Confirmed Cases: {int(today_numbers['totalconfirmed']):,}
Total Recoveries : {int(today_numbers['totalrecovered']):,}
Total Deaths : {int(today_numbers['totaldeceased']):,}

Fatality rate : {Fatality_Rate}
Recovery rate : {Recovery_Rate}
Test Positivity Rate : {Positivity_Rate}
'''
    return (output_str, mid_str, end_str)
