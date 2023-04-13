import random

from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from Accounts.forms import CustomUserCreationForm, RandomForm
from Accounts.models import User


# Create your views here.
def addUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CustomUserCreationForm()
    return render(request, 'tipo_registration.html', {'form': form})
def wtfForm(request):
    # Первый этап регистрации, если он успешный, то...↓↓↓
    form = RandomForm()
    if request.method == 'POST':
        form = RandomForm(request.POST)
        if form.is_valid():
            # ... переходим сюда, тут отображается formzxc1.html, это второй этап регистрации
            # там в action можешь посмотреть куда перенаправляется "{% url 'form1' name=Name surname=SurName sursurname=SurSurName%}"
            # в urls.py видишь этот путь
            form = CustomUserCreationForm(request.POST)
            print(request.POST)
            return  render(request, 'formzxc1.html', {
                'form': form ,
                'Name':request.POST['name'],
                'SurName':request.POST['surName'],
                'SurSurName':request.POST['surSurName']})
    return render(request, 'formzxc.html', {'form': form })



def wtfForm1(request, name,surname, sursurname):
    if request.method == 'POST':
        mail = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        form = CustomUserCreationForm(request.POST)
        if User.objects.filter(email=mail).exists():
            return render(request, 'formzxc1.html',
                          {'form': form, 'Name': name, 'SurName': surname, 'SurSurName': sursurname, 'error': 'Пользователь с таким email уже существует'})
        if form.is_valid():
            a = User(first_name=name,last_name=surname,sur_sur_name=sursurname,email=mail,password=pass1)
            a.save()
    return HttpResponse('Хорош, зарегался, свободен, '+name+' '+surname)
