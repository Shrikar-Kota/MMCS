from distutils.command.upload import upload
import email
from genericpath import exists
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import os
import hashlib
import datetime

from .models import MediaDetails
from accounts.models import User

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
                    MediaDetails(user=User.objects.get(email=request.user.email), filename=uploadedfile.name, uploaddate=uploaddate, filetype=uploadedfiletype, fileid=str(uploadedfileid), fileextension=uploadedfileextension, status='UPLOADED').save()
                    break
            fs = FileSystemStorage(UPLOAD_FILE_PATH)
            fs.save(filename, uploadedfile)
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
            file_data['fileurl'] = request.build_absolute_uri(f'/media/{emailhash}/summary/{file_data["file_id"]}')
        return render(request, 'summarizer/archives.html', {"notsummarizedpresent": len(files_details), "files_details": files_details})
    return redirect('signin')