from os import access
from django.shortcuts import render
from subprocess import run, PIPE
import sys
import environ
from allauth.socialaccount.models import SocialToken

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Create your views here.
def index_view(request):
    return render(request, 'index.html', {})

def about_view(request):
    return render(request, 'about.html', {})

def create_playlist_view(request):
    return render(request, 'create_playlist.html', {})

def creating_playlist_view(request):
    time = request.POST.get('time')
    access_token = str(SocialToken.objects.get(account__user=request.user, account__provider='spotify'))
    output = run([sys.executable, env('FILE_PATH'), time, access_token], shell=False, stdout=PIPE)
    return render(request, 'playlist_created.html', {})