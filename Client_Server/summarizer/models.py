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
    start_time_of_media = models.IntegerField()
    end_time_of_media = models.IntegerField()
    
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
                    "fileurl": '{}/{}/{}/{}/{}'.format(BASE_URL, emailhash, 'INPUT', file_data.filetype, "{}.{}".format(file_data.fileid, file_data.fileextension)),
                    "start_time_of_media": file_data.start_time_of_media,
                    "end_time_of_media": file_data.end_time_of_media,
                    'start_time': {'hours': str(file_data.start_time_of_media//360).zfill(2), 'minutes': str((file_data.start_time_of_media//60)%60).zfill(2), 'seconds': str(file_data.start_time_of_media%60).zfill(2)}, 
                    'end_time': {'hours': str(file_data.end_time_of_media//360).zfill(2), 'minutes': str((file_data.end_time_of_media//60)%60).zfill(2), 'seconds': str(file_data.end_time_of_media%60).zfill(2)}
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
                    "fileextension": file_data.fileextension,
                    "start_time_of_media": file_data.start_time_of_media,
                    "end_time_of_media": file_data.end_time_of_media,
                    'start_time': {'hours': str(file_data.start_time_of_media//360).zfill(2), 'minutes': str((file_data.start_time_of_media//60)%60).zfill(2), 'seconds': str(file_data.start_time_of_media%60).zfill(2)}, 
                    'end_time': {'hours': str(file_data.end_time_of_media//360).zfill(2), 'minutes': str((file_data.end_time_of_media//60)%60).zfill(2), 'seconds': str(file_data.end_time_of_media%60).zfill(2)}
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
                "status": record.status,
                "start_time_of_media": record.start_time_of_media,
                "end_time_of_media": record.end_time_of_media
            }
        return {}
        
    @staticmethod
    def updateStatus(email, fileid, status):
        media_data = MediaDetails.objects.get(user = User.objects.get(email=email), fileid = fileid)
        media_data.status = status
        media_data.save()
        return {
                "email": media_data.user.email,
                "filename": media_data.filename,
                "filetype": media_data.filetype,
                "fileextension": media_data.fileextension,
                "fileid": media_data.fileid,
                "status": media_data.status,
                "start_time_of_media": media_data.start_time_of_media,
                "end_time_of_media": media_data.end_time_of_media
            }
        
    @staticmethod
    def updateStartAndEndTime(email, fileid, starttime, endtime):
        media_data = MediaDetails.objects.get(user = User.objects.get(email=email), fileid = fileid)
        media_data.start_time_of_media = starttime
        media_data.end_time_of_media = endtime
        media_data.save()
        return {
                "email": media_data.user.email,
                "filename": media_data.filename,
                "filetype": media_data.filetype,
                "fileextension": media_data.fileextension,
                "fileid": media_data.fileid,
                "status": media_data.status,
                "start_time_of_media": media_data.start_time_of_media,
                "end_time_of_media": media_data.end_time_of_media
            }