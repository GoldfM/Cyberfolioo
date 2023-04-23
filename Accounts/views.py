import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from Accounts.forms import *
from Accounts.models import *



def wtfForm(request):
    # Первый этап регистрации, если он успешный, то...↓↓↓
    form = firstForm()
    if request.method == 'POST':
        form = firstForm(request.POST)
        if form.is_valid():
            # ... переходим сюда, тут отображается formzxc1.html, это второй этап регистрации
            # там в action можешь посмотреть куда перенаправляется "{% url 'form1' name=Name surname=SurName sursurname=SurSurName%}"
            # в urls.py видишь этот путь
            form = CustomUserCreationForm(request.POST)
            return  render(request, 'registration2.html', {
                'form': form ,
                'Name':request.POST['name'],
                'SurName':request.POST['surName'],
                'SurSurName':request.POST['surSurName']})
    return render(request, 'registration.html', {'form': form })



def wtfForm1(request, name,surname, sursurname):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        form = CustomUserCreationForm(request.POST)
        if User.objects.filter(username=username).exists():

            return render(request, 'registration2.html',
                          {'form': form, 'Name': name, 'SurName': surname, 'SurSurName': sursurname, 'error': 'Пользователь с таким username уже существует'})
        if form.is_valid():
            a = User(first_name=name,last_name=surname,sur_sur_name=sursurname,username=username)
            a.set_password(pass1)
            a.save()
            return redirect('/')
        else:
            return render(request, 'registration2.html',
                          {'form': form, 'Name': name, 'SurName': surname, 'SurSurName': sursurname})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'enter-page.html'



    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        #c_def = self.get_user_context(title="Авторизация")
        return context

    def get_success_url(self):
        return reverse_lazy('home')

def welcome(request):
    return render(request, 'welcome.html')

class Home(ListView):
    paginate_by = 6
    model = Project
    template_name = "main_page.html"
    context_object_name = "projects"

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['title'] = "Главная"
        #c_def = self.get_user_context(title = "Главная страница")
        return context

    def get_queryset(self):
        return Project.objects.all()

class Profile(DetailView): #Ну тут вообще надо сделать будет DetailView, так пока чтобы работало
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context

@login_required
def profile(request, slug):
    user_profile = get_object_or_404(User, slug=slug)
    if user_profile.user.id == request.user.id:
        # Пользователь открывает свой профиль
        # Добавьте здесь ваш код для обработки этого случая
        return render(request, 'user_profile.html', {'user_profile': user_profile})
    else:
        # Пользователь открывает профиль другого пользователя
        # Добавьте здесь ваш код для обработки этого случая
        return render(request, 'myapp/other_profile.html', {'user_profile': user_profile})