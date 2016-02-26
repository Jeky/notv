from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from notv.models import *

SITE_NAME_MAPPING = {
    'vm' : '美剧',
    'bilibili' : 'B站'
}


def index(request):
    videos = Video.objects.filter(read = False)
    sources = {}
    for v in videos:
        if v.up.fromSite not in sources:
            sources[v.up.fromSite] = []

        sources[v.up.fromSite].append(v)

    for s, vs in sources.items():
        vs.sort(key = lambda v: v.create)
        vs.reverse()

    return render_to_response('index.html', {
        'sources' : [{'name' : k, 'updates' : v} for k, v in sources.items()]
        })

def visit(request, vid):
    video = Video.objects.get(id = vid)
    video.read = True
    video.save()

    return redirect(video.url)