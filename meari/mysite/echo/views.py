from django.shortcuts import render
from django.http import HttpResponse

import json

import wind.mytube as mytube
import wind.karaoke as nore
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

kara = None

@csrf_exempt
def karaoke(request):

    text = request.POST.get('send', None)
    print(text)

    global kara

    kara = nore.Nore()
    kara.start_nore()

    context = {
        'result' : 'success'
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def stop(request):

    text = request.POST.get('send', None)
    print(text)

    global kara

    try:
        kara.stop_nore()
        kara = None
    except:
        print('except')

    context = {
        'result' : 'success'
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def set_delay_interval(request):

    val = request.POST.get('val', None)
    print(val)

    global kara

    kara.DELAY_INTERVAL = int(val)

    context = {
        'result' : 'success_delay_interval'
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def set_delay_volume_decay(request):

    val = request.POST.get('val', None)
    print(val)

    global kara

    kara.DELAY_VOLUME_DECAY = float(val)

    context = {
        'result' : 'success_delay_volume_decay'
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def set_delay_num(request):

    val = request.POST.get('val', None)
    print(val)

    global kara

    kara.DELAY_N = int(val)

    context = {
        'result' : 'success_delay_num'
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt 
def get_url(request):
    title = request.POST.get('title', None)
    singer = request.POST.get('singer', None)

    text = str(title)+' '+str(singer)+' karaoke'
    print(text)
    context = {
        'result' : mytube.get_url(text)
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

