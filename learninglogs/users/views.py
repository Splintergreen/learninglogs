from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CreationForm


def signup(request):
    signup_form = CreationForm()
    if request.method == 'POST' and 'btn_signup_form' in request.POST:
        signup_form = CreationForm(data=request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            user.save()
            authenticated_user = authenticate(
                username=user.username,
                password=request.POST['password1']
            )
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('logs:index'))
    context = {'signup_form': signup_form}
    return render(request, 'users/signup.html', context)
