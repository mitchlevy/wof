from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic
from django.template import RequestContext

from fantasyworld.models import *
from fantasyworld.forms import BuyStockForm, SellStockForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def get_or_create_profile(user):
    try:
        profile = Profile.objects.filter(user=user)[0]
    except IndexError:
        profile = Profile(user=user)
        profile.save()  
    return profile
    

def profile_home(request):
    user = request.user
    if user.is_authenticated:
        profile = get_or_create_profile(user)
        teams = Team.objects.filter(user=profile)

        team_league_dict = {}
        for team in teams:
            league = team.league_session.league
            team_league_dict[team] = league

        return render(request, 'fantasyworld/profile.html',
            context = {'team_league_dict': team_league_dict})
    else:
        return redirect('/login')


def signup(request):
    if request.user.is_authenticated:
        return redirect('/fantasyworld')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            profile = Profile(user=user)
            profile.save()
            return redirect('/index/')
        else:
            return render(request, 'fantasyworld/signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'fantasyworld/signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('/fantasyworld')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/index/')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'fantasyworld/signin.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'fantasyworld/signin.html', {'form': form})


def signout(request):
    logout(request)
    return HttpResponseRedirect('/index/')