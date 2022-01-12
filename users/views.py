from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm


def register(request):
    '''register new user'''
    if request.method != 'POST':
        # Выводит пустую форму регистрации
        form = UserCreationForm()
    else:
        # Обработка заполненной формы
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Вход и перенаправление на домашнюю страницу
            login(request, new_user)
            return redirect('learning_logs:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')
    # return redirect('learning_logs:index')
    # return HttpResponseRedirect('/')