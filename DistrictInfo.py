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
    output_str += '-'*40 + '\n'

    for k,v in dis['total'].items():
        output_str += k.title() + ' :\t' + str(v) + '\n'
    return output_str

def getDistricts(state):
    data = requests.get('https://api.covid19india.org/v3/data.json').json()
    output_str = 'The following districts are available for ' + states_codes[state.upper()] + '\n'
    for d in data[state.upper()]['districts'].keys():
        if d.title()!='Unknown':
            output_str += d.title() + '\n'
    return output_str
