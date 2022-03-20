from django.shortcuts import redirect, render

# Create your views here.
def home_screen_view(request):
    return redirect(signin_view)

def signin_view(request):
    return render(request, 'home/signin.html')

def signup_view(request):
    return render(request, 'home/signup.html')