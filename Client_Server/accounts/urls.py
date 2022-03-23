from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts_home_view, name='accounts_home'),
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('verify/<str:token>/', views.verify_view, name='verify_account')
]