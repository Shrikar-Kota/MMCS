from django.urls import path
from . import views

urlpatterns = [
    path('home', views.accounts_home_view, name='accounts_home'),
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('verify', views.verify_view, name='verify_account'),
    path('logout/', views.logout_view, name='logout'),
    path('resendemail/', views.resend_verificationmail_view, name='resend_vmail'),
    path('forgotpassword/', views.forgot_password_view, name='forgot_password'),
    path('resetpassword', views.accounts_reset_password_view, name='accounts_reset_password')
]