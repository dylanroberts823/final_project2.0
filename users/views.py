from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegistrationForm


# Create your views here.
#Taken directly from source code 7
def index(request):
    return redirect('projects:home')

def login_view(request):
    next = request.META['HTTP_REFERER']
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        next = request.POST.get('next', '/')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials."})
    else:
        next = request.META['HTTP_REFERER']
        return render(request, "users/login.html", {'next': next})

def logout_view(request):
    logout(request)
    return redirect(reverse('users:index'))

def register_view(request):
#Shoutout for the tutorial to https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('users:index')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})
