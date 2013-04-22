import os
import time
import re
import json

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext

from infrastructure.services import Services
from dependencies import Factory

library_id = 95
mp3_mime = 'audio/mpeg'
ogg_mime = 'audio/ogg'

def index(request):
    return render_to_response('server/index.html',
        context_instance=RequestContext(request))

def libraries(request):
    libraries = Factory().get_services().get_libraries()
    context = {'libraries': libraries}
    return render(request, 'server/libraries.html', context)

def get_random_songs(request):
    songs = Factory().get_services().get_random(10, library_id)
    return HttpResponse(_serialize(songs))

def create_library(request):
    name = request.POST['name']
    path = request.POST['path']
    Factory().get_services().create_library(name, path)
    return redirect('index')

def search_songs(request):
    songs = Factory().get_services().search_songs(request.GET.get('q'))
    return HttpResponse(_serialize(songs))

def stream_song(request):
    song_id = request.GET.get('id')
    path = Factory().get_services().get_song_path(song_id)
    f = open(path, 'rb')
    size = os.path.getsize(path)
    begin = 0
    end = size - 1
    isRangeRequest = request.META.has_key('HTTP_RANGE')
    if isRangeRequest:
        pattern = '^bytes=(\d*)-(\d*)$'
        range = re.findall(pattern, request.META['HTTP_RANGE'])[0]
        if len(range) >= 1:
            begin = int(range[0])
        if len(range) >= 2 and range[1] != '':
            end = int(range[1])
        f.seek(begin)
        response = HttpResponse(f, content_type=mp3_mime, status=206)
    else:
        response = HttpResponse(f, content_type=mp3_mime, status=200)
    #response['Cache-Control'] = 'public, must-revalidate, max-age=0'
    #response['Pragma'] = 'no-cache'
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(end - begin + 1)
    if isRangeRequest:
        response['Content-Range'] = 'bytes %s-%s/%s' % (begin, end, size)
    response['Content-Disposition'] = 'inline; filename=test.mp3'
    #response['Content-Transfer-Encoding'] = 'binary'
    response['Last-Modified'] = time.ctime(os.path.getmtime(path))
    return response

def _serialize(songs):
    for song in songs:
        song.mp3 = song.path
        del(song.path)
    return json.dumps([song.__dict__ for song in songs], ensure_ascii=False)
