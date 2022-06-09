from turtle import pos
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
import json
import binascii, os
from cryptography.fernet import Fernet

from .models import User
from .email_service import send_verification_email, send_forgotpassword_email

fernet_key = b'G77fOK591dHIvWYBsyRXsK2w_-6MRiF9g-L2JzOmuiE='

# Create your views here.
def accounts_home_view(request):
    if not request.user.is_authenticated:
        token = request.GET.get('token', "")
        if token == "":
            return redirect(signin_view)
        try:
            email = Fernet(fernet_key).decrypt(token.encode()).decode()
            print(email)
            if User.objects.filter(email=email):
                print("Account home")
                return render(request, 'accounts/home.html', {"email": email})
            else:
                return redirect('signin')
        except:
            return redirect('signin')
    return redirect('home')
    
def signin_view(request):
    if not request.user.is_authenticated:    
        if request.method == 'POST':
            post_data = json.loads(request.body)
            email = post_data['email']
            password = post_data['password']
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                if user.account_verified:
                    auth.login(request, user)
                    return JsonResponse({"message": "valid"})
                else:
                    email_token = Fernet(fernet_key).encrypt(user.email.encode()).decode()
                    return JsonResponse({"message": "unverified", "token": email_token})
            else:
                return JsonResponse({"message": "invalid"})
        return render(request, 'accounts/signin.html')
    return redirect('home')

def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            post_data = json.loads(request.body)
            username = post_data['username']
            email = post_data['email']
            password = post_data['password']
            if User.objects.filter(email=email):
                return JsonResponse({"message": "invalid"})
            else:
                signin_token = binascii.hexlify(os.urandom(50)).decode()
                user = User.objects.create_user(username=username, email=email, password=password, signin_token=signin_token)
                user.save()
                send_verification_email(user.email, username, request.build_absolute_uri(reverse(verify_view)+"?token="+signin_token))
                email_token = Fernet(fernet_key).encrypt(user.email.encode()).decode()
                return JsonResponse({"message": "valid", "token": email_token})
            
        return render(request, 'accounts/signup.html')
    return redirect('home')

def verify_view(request):
    if not request.user.is_authenticated:
        token = request.GET.get('token', "")
        if token == "":
            return redirect('signin')
        else:
            user = User.objects.filter(signin_token=token)
            if user:
                user = User.objects.get(signin_token=token)
                if (datetime.now(tz=timezone.utc) - user.token_creation_time).total_seconds()/360 <= 24:
                    user.account_verified = True
                    user.signin_token = None
                    user.token_creation_time = None
                    user.save()
                    return render(request, 'accounts/verify.html', {"token_expired": False, "email": user.email})
                else:
                    return render(request, 'accounts/verify.html', {"token_expired": True, "email": user.email})                
            else:
                return redirect('signin')
    else:
        return redirect('home')
    
def resend_verificationmail_view(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        email = post_data['email']
        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            if not user.account_verified:
                signin_token = binascii.hexlify(os.urandom(50)).decode()
                user.signin_token = signin_token
                user.token_creation_time = datetime.now(tz=timezone.utc)
                user.save()
                send_verification_email(user.email, user.username, request.build_absolute_uri(reverse(verify_view)+"?token="+signin_token))
                return JsonResponse({"message": "success"})
            else:
                return JsonResponse({"message": "verified"})
        else:
            return JsonResponse({"message": "error"})
    return redirect('signin')
        
def logout_view(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('signin')

def forgot_password_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            post_data = json.loads(request.body)
            email = post_data['email']
            if User.objects.filter(email=email):
                user = User.objects.get(email=email)
                if user.account_verified:
                    forgot_password_token = binascii.hexlify(os.urandom(50)).decode()
                    user.forgot_password_token = forgot_password_token
                    user.token_creation_time = datetime.now(tz=timezone.utc)
                    user.save()
                    send_forgotpassword_email(user.email, user.username, request.build_absolute_uri(reverse(accounts_reset_password_view)+"?token="+forgot_password_token))
                    return JsonResponse({"message": "success"})
                else:
                    return JsonResponse({"message": "unverified"})
            else:
                return JsonResponse({"message": "error"})
        return render(request, 'accounts/forgot_password.html')
        
def accounts_reset_password_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            postdata = json.loads(request.body)
            token = postdata['token']
            if token == "":
                return redirect('signin')
            else:
                user = User.objects.filter(forgot_password_token=token)
                if user:
                    user = User.objects.get(forgot_password_token=token)
                    if (datetime.now(tz=timezone.utc) - user.token_creation_time).total_seconds()/60 > 10:
                        return JsonResponse({"message": "invalid"})
                    else:
                        user.set_password(postdata['password'])
                        user.token_creation_time = None
                        user.forgot_password_token = None
                        user.save()
                        return JsonResponse({"message": "valid"})                
                else:
                    return redirect('signin')
        else:
            token = request.GET.get('token', "")
            if token == "":
                return redirect('signin')
            else:
                user = User.objects.filter(forgot_password_token=token)
                if user:
                    user = User.objects.get(forgot_password_token=token)
                    if (datetime.now(tz=timezone.utc) - user.token_creation_time).total_seconds()/60 > 10:
                        return render(request, 'accounts/reset_password.html', {"token": token, "token_invalid": True})
                    else:
                        return render(request, 'accounts/reset_password.html', {"token": token, "token_invalid": False, "email": user.email})                
                else:
                    return redirect('signin')
    return redirect('home')