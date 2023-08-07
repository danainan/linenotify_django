from django.shortcuts import render 
import requests
from linenotify.settings import LINE_NOTIFY_TOKEN
from django.http import HttpResponse
import os
from django.conf import settings
import cv2
from django.core.files.storage import FileSystemStorage
from .models import Lines
import base64
# Create your views here.
def index(request):
    line = Lines.objects.all()
    return render(request, 'index.html', {})

def send(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        token = LINE_NOTIFY_TOKEN
        url = 'https://notify-api.line.me/api/notify'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
        r = requests.post(url, headers=headers , data = {'message':message})
        print(r.text)
        return render(request, 'index.html', {'message':message})
    else:
        return render(request, 'index.html')

def sendImage(request):
    media_path = os.path.join(settings.MEDIA_ROOT , 'upload.png')
    if request.method == 'POST':
        if os.path.exists(media_path):
            os.remove(media_path)
        imageR = request.FILES.get('image')
        
        if imageR:
            fs = FileSystemStorage()
            fs.save(media_path, imageR)
            request.session['image'] = media_path
        token = LINE_NOTIFY_TOKEN
        url = 'https://notify-api.line.me/api/notify'
        data = {
            'message':'รายชื่อพัสดุมาส่งวันนี้',
        }
        image = {
            'imageFile':open(media_path,'rb')
        }

        headers = {'Authorization':'Bearer '+token}
        requests.post(url, headers=headers , files=image, data = data)
        print(media_path)
        with open(media_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        # print('image==>',encoded_image)
        return render(request, 'index.html', {'encoded_image':encoded_image})
    else:
        return render(request, 'index.html')
        
    