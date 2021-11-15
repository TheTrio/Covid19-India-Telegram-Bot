import requests
import re

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
def getData(state, district):
    data = requests.get('https://api.covid19india.org/v3/data.json').json()
    try:
        dis = data[state.upper()]['districts'][district.title()]
    except:
        return 'Invalid StateCode or District'
    output_str = ''
    output_str += 'State :\t' + states_codes[state.upper()] + '\n'
    output_str += 'District :\t' + district.title() + '\n'
    try:
        output_str += 'Testing Data last updated on :\t' + dis['meta']['tested']['last_updated'] + '\n'
    except:
        output_str += 'Testing Data last updated on :\t Not available\n'
    output_str += '-'*60 + '\n'

    Fatality_Rate = '{:.2%}'.format(int(dis['total']['deceased'])/int(dis['total']['confirmed']))
    Recovery_Rate = '{:.2%}'.format(int(dis['total']['recovered'])/int(dis['total']['confirmed']))
    if 'deceased' not in dis['delta']:
        dis['delta']['deceased'] = 0
    if 'confirmed' not in dis['delta']:
        dis['delta']['confirmed'] = 0
    if 'recovered' not in dis['delta']:
        dis['delta']['recovered'] = 0
    output_str += f'''
New Cases: {int(dis['delta']['confirmed']):,} 
New Deaths: {int(dis['delta']['deceased']):,} 
New Recoveries: {int(dis['delta']['recovered']):,} 

Total Tests : {int(dis['total']['tested']):,}
Total Confirmed Cases: {int(dis['total']['confirmed']):,}
Total Recoveries : {int(dis['total']['recovered']):,}
Total Deaths : {int(dis['total']['deceased']):,}
'''
    if 'migrated' in dis['total']:
        output_str+=f"Total Migrated : {int(dis['total']['migrated']):,}\n"
    output_str+=f'''
Fatality rate : {Fatality_Rate}
Recovery rate : {Recovery_Rate}
'''
    return output_str


def getDistricts(state):
    data = requests.get('https://api.covid19india.org/v3/data.json').json()
    output_str = 'The following districts are available for ' + states_codes[state.upper()] + '\n'
    for d in data[state.upper()]['districts'].keys():
        if d.title()!='Unknown':
            output_str += d.title() + '\n'
    return output_str

def get_district_list(state):
    data = requests.get('https://api.covid19india.org/v3/data.json').json()
    return list(data[state.upper()]['districts'].keys())