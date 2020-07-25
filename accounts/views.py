from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from MyAPI.models import Lyrics


# Create your views here.
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account created for " + user)
            return redirect("login")

    context = {"form": form}
    return render(request, "register.html", context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    else:

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage")
            else:
                messages.info(request, "Username or Password is incorrect")
                return render(request, "login.html")

        context = {}
        return render(request, "login.html", context)

def logoutUser(request):
    logout(request)
    return redirect("login")

def savedLyricsPage(request):
    if not request.user.is_authenticated: 
        return redirect("homepage")
    else:

        lyrics = Lyrics.objects.all().filter(author=request.user.username)
        for lyric in lyrics:
            lyric.preview = lyric.lyrics.split("\n")[0] 
        context = {"lyrics": lyrics}
        return render(request, "savedLyrics.html", context)

def lyricsPage(request):
    id = request.GET.get("id")
    lyric = Lyrics.objects.get(id=id)
    if lyric.author == request.user.username:
        context = {"lyric": lyric}
    else:
        messages.info(request, "These Lyrics were created by another user")
        context = {"lyric": None}
    return render(request, "lyricsPage.html", context)