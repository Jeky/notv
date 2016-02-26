import requests
import simplejson as json
from bs4 import BeautifulSoup
from datetime import datetime
from notv.models import Up, Video

URL = 'http://vmus.co/%E5%AE%85%E7%94%B7%E8%A1%8C%E4%B8%8D%E8%A1%8C%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8-the-big-bang-theory/'
UP_NAME = 'The Big Bang Theory'
name = '美剧'

def updateUps():
    if not Up.objects.filter(name = UP_NAME).exists():
        up = Up(name = UP_NAME)
        up.save()
        return [up]
    else:
        return []


def getUpdates(read = False):
    r = requests.get(URL)
    data = BeautifulSoup(r.text, 'html.parser')
    items = data.select('p a')
    s = 0
    up = Up.objects.get(name = UP_NAME)
    newVideos = []

    for item in items:
        if item.text.startswith('EP'):
            if item.text == 'EP01':
                s +=1

            title = '第' + str(s) + '季 第' + item.text[2:] + '集'
            if not Video.objects.filter(title = title).exists():
                video = Video(
                    title = title,
                    up = up,
                    read = read,
                    url = item['href'],
                    pic = '/static/img/tbbt.jpg')
                video.save()
                newVideos.append(video)

    return newVideos
