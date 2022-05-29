from pydoc import cli
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt
import os
import hashlib
import datetime
import json 
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

from .models import MediaDetails
from accounts.models import User
from .email_service import send_summmary_generated_notification_mail

def home_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.FILES['uploadedFile']:
            uploadedfile = request.FILES['uploadedFile']
            uploadedfiletype = request.POST['type']
            uploadedfileextension = request.POST['extension']
            emailhash = hashlib.md5(request.user.email.encode()).hexdigest()
            UPLOAD_FILE_PATH = os.path.join(
                Path(__file__).resolve().parent.parent.parent, 'Media')
            if emailhash not in os.listdir(UPLOAD_FILE_PATH):
                UPLOAD_FILE_PATH = os.path.join(UPLOAD_FILE_PATH, emailhash)
                os.makedirs(os.path.join(UPLOAD_FILE_PATH, 'INPUT/AUDIO'))
                os.makedirs(os.path.join(UPLOAD_FILE_PATH, 'INPUT/VIDEO'))
                os.makedirs(os.path.join(UPLOAD_FILE_PATH, 'INPUT/TEXT'))
                os.makedirs(os.path.join(UPLOAD_FILE_PATH, 'SUMMARY'))
            else:
                UPLOAD_FILE_PATH = os.path.join(UPLOAD_FILE_PATH, emailhash)
            UPLOAD_FILE_PATH = os.path.join(UPLOAD_FILE_PATH, 'INPUT')
            UPLOAD_FILE_PATH = os.path.join(UPLOAD_FILE_PATH, uploadedfiletype)
            while 1:
                uploaddate = datetime.datetime.utcnow()
                uploadedfileid = int(uploaddate.timestamp()*(10**6))
                filename = '{}.{}'.format(uploadedfileid, uploadedfileextension)
                if not MediaDetails.objects.filter(user=User.objects.get(email=request.user.email), fileid = str(uploadedfileid)).exists():
                    MediaDetails(user=User.objects.get(email=request.user.email), filename=uploadedfile.name, uploaddate=uploaddate, filetype=uploadedfiletype, fileid=str(uploadedfileid), fileextension=uploadedfileextension, status='UPLOADED', start_time_of_media=0, end_time_of_media=0).save()
                    break
            fs = FileSystemStorage(UPLOAD_FILE_PATH)
            fs.save(filename, uploadedfile)
            UPLOAD_FILE_PATH = os.path.join(UPLOAD_FILE_PATH, filename)
            if uploadedfiletype != "TEXT":
                MediaDetails.updateStartAndEndTime(request.user.email, uploadedfileid, 0, get_duration_of_media(UPLOAD_FILE_PATH, uploadedfiletype))
            unsummarized_filedetails = MediaDetails.getUnsummarizedFileDetails(request.user.email, request.build_absolute_uri('/media'))
            return JsonResponse({"notsummarizedpresent": len(unsummarized_filedetails) != 0, "files_details": unsummarized_filedetails})
        unsummarized_filedetails = MediaDetails.getUnsummarizedFileDetails(request.user.email, request.build_absolute_uri('/media'))
        return render(request, 'summarizer/home.html', {"notsummarizedpresent": len(unsummarized_filedetails) != 0, "files_details": unsummarized_filedetails})
    return redirect('signin')

def archives_view(request):
    if request.user.is_authenticated:
        files_details = MediaDetails.getFileDetails(email=request.user.email)
        emailhash = hashlib.md5(request.user.email.encode()).hexdigest()
        for file_data in files_details:
            file_data['fileurl'] = request.build_absolute_uri(f'/media/{emailhash}/summary/{file_data["fileid"]}_SUMMARY.pdf')
        return render(request, 'summarizer/archives.html', {"notsummarizedpresent": len(files_details) != 0, "files_details": files_details})
    return redirect('home')

def add_to_queue(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            media_data =  MediaDetails.objects.get(user=User.objects.get(email=request.user.email), fileid = data['fileid'])
            unsummarized_filedetails = MediaDetails.getUnsummarizedFileDetails(request.user.email, request.build_absolute_uri('/media'))
            if not media_data or media_data.status != 'UPLOADED':
                return JsonResponse({"alreadyqueued": True, "error": False, 'files_details': unsummarized_filedetails})
            if media_data.filetype == 'TEXT':
                MediaDetails.updateStatus(request.user.email, media_data.fileid, 'QUEUED')
                unsummarized_filedetails = MediaDetails.getUnsummarizedFileDetails(request.user.email, request.build_absolute_uri('/media'))
                return JsonResponse({"error": False, "alreadyqueued": False, "filename": media_data.filename, "files_details": unsummarized_filedetails})
            elif data['start_time'] < data['end_time']:    
                if data['start_time'] < media_data.end_time_of_media and data['end_time'] <= media_data.end_time_of_media:
                    MediaDetails.updateStartAndEndTime(request.user.email, media_data.fileid, data['start_time'], data['end_time'])
                    MediaDetails.updateStatus(request.user.email, media_data.fileid, 'QUEUED')
                    unsummarized_filedetails = MediaDetails.getUnsummarizedFileDetails(request.user.email, request.build_absolute_uri('/media'))
                    return JsonResponse({"error": False, "alreadyqueued": False, "filename": media_data.filename, "files_details": unsummarized_filedetails})
            unsummarized_filedetails = MediaDetails.getUnsummarizedFileDetails(request.user.email, request.build_absolute_uri('/media'))
            return JsonResponse({"error": True, "alreadyqueued": False, 'files_details': unsummarized_filedetails})
    return redirect('home')

@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['status'] == 'FINISHED':
            media_data = MediaDetails.objects.get(user=User.objects.get(email=data['email']), fileid=data['fileid'])
            send_summmary_generated_notification_mail(media_data.user.email, media_data.user.username, "{}/{}/SUMMARY/{}".format(request.build_absolute_uri('/media'), hashlib.md5(media_data.user.email.encode()).hexdigest(), f"{media_data.fileid}_SUMMARY.pdf"), media_data.filename)
        MediaDetails.updateStatus(data['email'], data['fileid'], data['status'])
        return JsonResponse({})
    return redirect('home')

def get_oldest_queued_request(request):
    return JsonResponse(MediaDetails.getOldestRequest())

def get_duration_of_media(INPUT_FILE_PATH, MEDIA_TYPE):
    if MEDIA_TYPE == 'VIDEO':
        clip = VideoFileClip(INPUT_FILE_PATH)
        return int(clip.duration)
    else:
        audio = AudioSegment.from_file(INPUT_FILE_PATH)
        return int(audio.duration_seconds)