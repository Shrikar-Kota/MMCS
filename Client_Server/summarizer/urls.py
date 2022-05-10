from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('archives/', views.archives_view, name='archives'),
    path('updatefilestatus/', views.update_status, name='update_file_status'),
    path('getoldestrequest/', views.get_oldest_queued_request, name='get_oldest_request'),
    path('addtoqueue/', views.add_to_queue, name='addtoqueue')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)