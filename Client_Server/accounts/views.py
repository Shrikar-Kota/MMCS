from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
import json
import binascii, os
from cryptography.fernet import Fernet
from django.urls import reverse

from .models import User
from .email_service import send_verification_email

fernet_key = b'G77fOK591dHIvWYBsyRXsK2w_-6MRiF9g-L2JzOmuiE='

# Create your views here.
def accounts_home_view(request):
    token = request.GET.get('token', "")
    if token == "":
        return redirect(signin_view)
    try:
        email = Fernet(fernet_key).decrypt(token.encode()).decode()
        if User.objects.filter(email=email):
            return render(request, 'accounts/home.html', {"email": email})
        else:
            return redirect(signin_view)
    except:
        return redirect(signin_view)
    
def signin_view(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        email = post_data['email']
        password = post_data['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return JsonResponse({"message": "Success"})
        else:
            return JsonResponse({"message": "Error"})
    return render(request, 'accounts/signin.html')

def signup_view(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        username = post_data['username']
        email = post_data['email']
        password = post_data['password']
        if User.objects.filter(email=email):
            return JsonResponse({"message": "Error"})
        else:
            signin_token = binascii.hexlify(os.urandom(50)).decode()
            user = User.objects.create_user(username=username, email=email, password=password, signin_token=signin_token)
            user.save()
            send_verification_email(email, reverse('verify_view')+"?token="+signin_token)
            email_token = Fernet(fernet_key).encrypt(user.email.encode()).decode()
            return JsonResponse({"message": "Success", "token": email_token})
        
    return render(request, 'accounts/signup.html')

def verify_view(request):
    token = request.GET.get('token', "")
    if token == "":
        return token
    else:
        return "Invalid token"