import requests
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mpl_dates
from datetime import datetime
from Utils import Utils

states_codes = {
        'AN': 'Andaman and Nicobar Islands',
        'AP': 'Andhra Pradesh',
        'AR': 'Arunachal Pradesh',
        'AS': 'Assam',
        'BR': 'Bihar',
        'CH': 'Chandigarh',
        'CT': 'Chhattisgarh',
        'DD': 'Daman and Diu',
        'DL': 'Delhi',
        'DN': 'Dadra and Nagar Haveli',
        'GA': 'Goa',
        'GJ': 'Gujarat',
        'HP': 'Himachal Pradesh',
        'HR': 'Haryana',
        'JH': 'Jharkhand',
        'LA': 'Ladakh',
        'KA': 'Karnataka',
        'KL': 'Kerala',
        'LD': 'Lakshadweep',
        'MH': 'Maharashtra',
        'ML': 'Meghalaya',
        'MN': 'Manipur',
        'MP': 'Madhya Pradesh',
        'MZ': 'Mizoram',
        'NL': 'Nagaland',
        'OR': 'Odisha',
        'PB': 'Punjab',
        'PY': 'Puducherry',
        'RJ': 'Rajasthan',
        'SK': 'Sikkim',
        'TG': 'Telangana',
        'TN': 'Tamil Nadu',
        'TR': 'Tripura',
        'UP': 'Uttar Pradesh',
        'UT': 'Uttarakhand',
        'WB': 'West Bengal',
        'JK': 'Jammu and Kashmir',
        'TT': 'India'
    }

def states(params, choice):
    
    plt.style.use('seaborn')
    plt.figure(figsize=(10,5))
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    date_format = mpl_dates.DateFormatter('%b %Y')
    dates = []
    nums = {}
    cur = 1
    if len(params)==0:
        params.append('TT')
    elif len(params)>10:
        return 'Maximum 10 states can be entered'
    else:
        for i in range(0,len(params)):
            if params[i].upper() in states_codes:
                pass
            else:
                return params[i] + ' is not a valid state code'
    anim = False
    r = requests.get('https://api.covid19india.org/states_daily.json')

    data = r.json()
    for state in data['states_daily']:
        if state['status']=='Confirmed':
            dates.append(datetime.strptime(state['date'].replace('Sept', 'Sep'), '%d-%b-%y'))
            for i in range(0,len(params)):
                if params[i].lower() in nums:
                    if choice=='total':
                        nums[params[i].lower()].append(nums[params[i].lower()][-1] + int(state[params[i].lower()]))
                    else:
                        nums[params[i].lower()].append(int(state[params[i].lower()]))
                else:
                    nums[params[i].lower()] = [int(state[params[i].lower()])]
    if choice=='new':
        plt.title('Daily increase in cases since Mar 14')
    else:
        plt.title('Total cases')
    for k,v in nums.items():
        plt.plot_date(dates, v, label=states_codes[k.upper()], linestyle='solid', marker=None)
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.savefig('GraphDaily.png')
    return 'Success'

def getCodes():
    output_str = ''
    for k,v in states_codes.items():
        output_str = output_str + k + '\t' + v + '\n'
    return output_str