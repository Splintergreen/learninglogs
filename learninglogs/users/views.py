from .forms import CreationForm, LoginForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse


def signup(request):
    """Регистрация нового пользователя."""
    login_form = LoginForm()
    signup_form = CreationForm()
    if request.method == 'POST' and 'btn_signup_form' in request.POST:
        signup_form = CreationForm(data=request.POST)
        print("YES")
        if signup_form.is_valid():
            user = signup_form.save()
            user.save()
            # Перенаправление на домашнюю страницу.
            authenticated_user = authenticate(username=user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('logs:index'))
    #         template = 'index.html'
    #         return render(request, template,)
    # else:
    #     # Обработка заполненной формы.
    #     form = CreationForm(data=request.POST)
    #     if form.is_valid():
    #         new_user = form.save()
    #         # Выполнение входа и перенаправление на домашнюю страницу.
    #         authenticated_user = authenticate(username=new_user.username,
    #                                           password=request.POST['password1'])
    #         login(request, authenticated_user)
    #         return HttpResponseRedirect(reverse('logs:index'))
    context = {'login_form': login_form, 'signup_form': signup_form}
    return render(request, 'users/login.html', context)
