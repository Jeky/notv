import requests
import simplejson as json
from pprint import pprint
from notv.models import Up, Video
from datetime import datetime
import hashlib

MID = '638122'
name = 'B站'


def getItemsOnPage(url, params, page = 1):
    params['page'] = page
    r = requests.get(url, params)
    data = json.loads(r.text)['data']

    if 'count' in data:
        if data['count'] == 0:
            return [], 0

    if 'list' in data:
        return data['list'], data['pages']
    elif 'vlist' in data:
        return data['vlist'], data['pages']


def getAllItems(url, params):
    items, pagesize = getItemsOnPage(url, params)

    if pagesize > 1:
        for i in range(2, pagesize + 1):
            newitems, _ = getItemsOnPage(url, params, i)
            items += newitems

    return items


def getAllUps():
    return getAllItems('http://space.bilibili.com/ajax/friend/GetAttentionList', 
        params = {'mid' : MID, 'pagesize':100, 'page':1})


def getVideos(mid):
    return getAllItems('http://space.bilibili.com/ajax/member/getSubmitVideos',
        params = {'mid' : mid, 'pagesize':100, 'page':1})


def updateUps():
    '''
    update the list of ups on bilibili.com
    '''
    ups = getAllUps()
    newUps = []
    for up in ups:
        if not Up.objects.filter(id = up['fid']).exists():
            u = Up(id = up['fid'], name = up['uname'])
            u.save()
            newUps.append(u)

    return newUps


def updateVideos(up, videos, read):
    newVideos = []
    print('updateing: ' + str(up))

    for v in videos:
        if not Video.objects.filter(id = v['aid']).exists():
            video = Video(
                id = v['aid'],
                title = v['title'],
                up = up,
                create = datetime.strptime(v['created'], '%Y-%m-%d %H:%M:%S'),
                read = read,
                url = 'http://www.bilibili.com/video/av%d' % v['aid'],
                pic = v['pic'])
            video.save()
            newVideos.append(video)
        else:
            return newVideos

    return newVideos


def getUpdates(read = False):
    newVideos = []

    for up in Up.objects.all():
        videos = getVideos(up.id)
        newVideos += updateVideos(up, videos, read)

    return newVideos
