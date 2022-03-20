from django.urls import path
from home import views

urlpatterns = [
    path('', views.home_screen_view, name='home'),
    path('signin', views.signin_view, name='signin'),
    path('signup', views.signup_view, name='signup')
]