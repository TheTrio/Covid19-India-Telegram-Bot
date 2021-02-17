import requests
import json

def find(args):
    search = '+'.join(args)
    query = f'https://www.googleapis.com/customsearch/v1?key=AIzaSyB-EYXiIPfz_q1ZU1dBbpBaxZB_IbVcp3M&cx=26533ab1e170a00d7&q={search}'
    data = requests.get(query).json()
    if 'items' in data:
        return data['items']
    else:
        return False