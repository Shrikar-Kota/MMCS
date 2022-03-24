from django.shortcuts import render, redirect

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'summarizer/home.html')
    return redirect('signin')
