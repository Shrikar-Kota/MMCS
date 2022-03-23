from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import User
from django.contrib.auth.models import auth
import json

# Create your views here.
def accounts_home_view(request):
    return render(request, 'accounts/home.html')
    
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
            user = User.objects.create_user(username, email, password)
            user.save()
            return JsonResponse({"message": "Success"})
        
    return render(request, 'accounts/signup.html')

def verify_view(request, token=None):
    if token == None:
        return redirect(request, signin_view)
    else:
        pass