
from flask import Flask, render_template
import bs4
app = Flask(__name__)
from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_calendar_data():
    source = requests.get('https://www.boxofficemojo.com/calendar/').text
    soup = BeautifulSoup(source, 'lxml')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    data = requests.get(source, headers=headers)

    name_list = []
    actor_list = []
    image_list = []
    tag_list = []

    for m in soup.find_all('td', {'class': 'a-text-left mojo-header-column mojo-truncate mojo-field-type-release mojo-cell-wide'}):
        moviename = m.find('div', {'class': 'a-section a-spacing-none mojo-schedule-release-details'})
        movietag = m.find('div', {'class': 'a-section a-spacing-none mojo-schedule-genres'})

        if moviename:
            name_list.append(moviename.find('a').text)
        else:
            name_list.append("Don't have name")

        if movietag:
            tag_list.append(movietag.text.replace('\n','').replace('            ',' ').replace('    ',''))
        else:
            tag_list.append("No Tag")

        with_divs = m.find_all('div', {'class': 'a-section a-spacing-none'})
        filtered_with_divs = [div for div in with_divs if div.find('span', {'class': 'a-text-bold'})]

        if filtered_with_divs:
            actor_list.append(filtered_with_divs[0].text.replace('With:',''))
        else:
            actor_list.append("No Actor")

        img_tag = m.find('img')
        if img_tag:
            image_list.append(img_tag.get('src'))
        else:
            image_list.append("No Image")

    return {
        'name_list': name_list,
        'actor_list': actor_list,
        'image_list': image_list,
        'tag_list': tag_list,
    }
