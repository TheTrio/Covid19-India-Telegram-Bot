from bs4 import BeautifulSoup as sp
import requests

def find():
    soup = sp(requests.get('https://www.altnews.in/topics/science/').content)
    tags = soup.find_all('a')
    links = []
    for tag in tags:
        if 'rel' in tag.attrs:
            if tag['rel'][0]=='bookmark':
                links.append(tag['href'])
    return links