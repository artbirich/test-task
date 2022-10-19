import requests
from bs4 import BeautifulSoup
import re
import json

HOST = 'https://oriencoop.cl/sucursales.htm'
URL = 'https://oriencoop.cl'
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}


def get_html(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_link(host):
    response = requests.request("GET", host, headers=HEADERS)
    href = []
    for item in response.text.split():
        if re.search('/sucursales/', item):
            [href.append(i) for i in re.findall('"([^"]*)"', item)]
    return href


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sucursal')
    time_href1 = [item.find(
        'div', class_='s-dato').select_one('p:nth-child(5)').find('span').get_text() for item in items]
    time_href2 = [item.find(
        'div', class_='s-dato').select_one('p:nth-child(5)').find_next('span').find_next('span').get_text() for item in items]
    time_href = time_href1 + time_href2
    address = [item.find(
        'div', class_='s-dato').select_one('p:nth-child(2)').find('span').get_text() for item in items]
    phones = [item.find(
        'div', class_='s-dato').select_one('p:nth-child(3)').find('span').get_text() for item in items]

    data = []
    data.append(
        {
            "address": address,
            # "latlon": item .find('div', class_='s-mapa').find('iframe').get('src'),
            "name": "Oriencoop",
            "phones": phones,
            "working_hours": time_href
        }
    )
    return data


def parser():
    values = get_link(HOST)
    PAGINATION = {}
    keys = len(values)
    for i in range(keys):
        PAGINATION[i] = values[i]

    html = get_html(URL)
    if html.status_code == 200:
        data = []
        for page in PAGINATION.values():
            print(f"Parsing page: {page}")
            html = get_html(URL + page)
            data.extend(get_content(html.text))
        # print(data)
        json_dump = json.dumps(data)
        json_loads = json.loads(json_dump)
        with open("output.json", "w") as write_file:
            json.dump(json_loads, write_file, indent=4)
    else:
        print("Error")


parser()
