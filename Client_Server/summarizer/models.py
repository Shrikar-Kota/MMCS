from django.db import models
from accounts.models import User
import hashlib
# Create your models here.

class MediaDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.TextField()
    uploaddate = models.DateTimeField()
    filetype = models.CharField(max_length=6)
    fileextension = models.CharField(max_length=6)
    fileid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    
    @staticmethod
    def getUnsummarizedFileDetails(email, BASE_URL):
        records = MediaDetails.objects.filter(user = User.objects.get(email=email)).order_by('-uploaddate')
        emailhash = hashlib.md5(email.encode()).hexdigest()
        files_details = []
        for file_data in records:
            if file_data.status == 'UPLOADED':
                files_details.append({
                    "filename": file_data.filename,
                    "uploaddate": file_data.uploaddate.strftime("%m/%d/%Y, %H:%M:%S")+" UTC",
                    "filetype": file_data.filetype,
                    "fileid": file_data.fileid,
                    "fileurl": '{}/{}/{}/{}/{}'.format(BASE_URL, emailhash, 'INPUT', file_data.filetype, "{}.{}".format(file_data.fileid, file_data.fileextension))
                })
        return files_details
    
    @staticmethod
    def getFileDetails(email):
        records = MediaDetails.objects.filter(user = User.objects.get(email=email)).order_by('-uploaddate')
        files_details = []
        for file_data in records:
            if file_data.status != 'UPLOADED':
                files_details.append({
                    "filename": file_data.filename,
                    "uploaddate": file_data.uploaddate.strftime("%m/%d/%Y, %H:%M:%S")+" UTC",
                    "filetype": file_data.filetype,
                    "fileid": file_data.fileid,
                    "status": file_data.status,
                    "fileextension": file_data.fileextension
                })
        return files_details
    
    @staticmethod
    def getOldestRequest():
        latest_record = MediaDetails.objects.filter(status='QUEUED').order_by('uploaddate')
        for record in latest_record:
            return {
                "email": record.user.email,
                "filename": record.filename,
                "filetype": record.filetype,
                "fileextension": record.fileextension,
                "fileid": record.fileid,
                "status": record.status
            }
        return {}
        
    @staticmethod
    def updateStatus(email, fileid, status):
        media_data = MediaDetails.objects.get(user = User.objects.get(email=email), fileid = fileid)
        media_data.status = status
        media_data.save()