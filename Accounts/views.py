import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, QueryDict, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from scipy.constants import slug

from Accounts.forms import *
from Accounts.models import *

class ProjectView(DetailView):
    model = Project
    template_name = 'project_page.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'proj'
    def get_queryset(self, queryset=None):
        user = get_object_or_404(User, slug = self.request.path_info.split('/')[2])
        return user.get_projects()


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = str(context["proj"].name)
        #c_def = self.get_user_context(title = context["post"])
        return context

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


class addProject(CreateView):
    model = Project
    enctype = "multipart/form-data"
    template_name = "project_add.html"
    success_url = reverse_lazy('home')
    fields = ['name', 'type', 'key_words' ,'spec_proj', 'descriptions', 'time_developing',
              'teammate1', 'teammate2', 'teammate3', 'teammate4', 'teammate5', 'url', 'avatar_image', 'main_image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(addProject, self).form_valid(form)


def wtfForm1(request, name,surname, sursurname):
    if request.method == 'POST':
        username = request.POST['username']
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
            new_user = authenticate(username=username, password=pass1)
            login(request, new_user)
            return redirect('home')
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
    #paginate_by = 6
    model = User
    template_name = "main_page.html"
    context_object_name = "users"

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная страница"
        return context

    def get_queryset(self):
        users = User.objects.all().exclude(id=self.request.user.id).filter(is_superuser=0)

        if self.request.method == 'GET':
            first_name = self.request.GET.get('first_name')
            last_name = self.request.GET.get('last_name')
            spec = self.request.GET.get('specialization')

            first_name_q = Q()
            if first_name:
                first_name_q = Q(first_name__icontains=first_name)

            last_name_q = Q()
            if last_name:
                last_name_q = Q(last_name__icontains=last_name)

            if spec:
                try:
                    spec_obj = Specs.objects.get(name=spec)
                    users = users.filter(spec=spec_obj)
                except Specs.DoesNotExist:
                    pass

            users = users.filter(first_name_q & last_name_q)

        users = users.annotate(num_followers=Count('following')).order_by('-num_followers')
        return users


class SubscribeView(View):
    def post(self, request):
        profile_id = request.POST.get('user_id')
        profile = User.objects.get(id=profile_id)
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user == profile:
            return redirect('home')

        if not Follow.objects.filter(follow_from=request.user, follow_to=profile).exists():
            Follow.objects.create(follow_from=request.user, follow_to=profile)

        return redirect('home')

class UnsubscribeView(View):
    def post(self, request):
        profile_id = request.POST.get('user_id')
        profile = User.objects.get(id=profile_id)
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user == profile:
            return redirect('home')

        Follow.objects.filter(follow_from=request.user, follow_to=profile).delete()

        return redirect('home')


class PostDoesNotExist:
    pass


class Profile(DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user'

    '''def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        try:
            return queryset.get(slug=slug)
        except PostDoesNotExist:
            raise Http404('Ох, нет объекта;)')'''
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        user_profile = get_object_or_404(User,slug=slug)
        is_your_profile = False
        #user_profile = User.objects.get(slug=slug)
        if request.user.is_authenticated:
            if user_profile.id == request.user.id:
                is_your_profile = True
                # Пользователь открывает свой профиль

          # Пользователь открывает профиль другого пользователя
        return render(request, 'user_profile.html', {'user': user_profile, 'is_your_profile': is_your_profile, 'projects':user_profile.get_projects(), 'title': slug})

    #def get_context_data(self, *, object_list=None, **kwargs):
        #context = super().get_context_data(**kwargs)
        #context['title'] = "Профиль"
        #return context

class ProfileUpdateView(UpdateView):
    model = User
    enctype = "multipart/form-data"
    fields = ['first_name', 'last_name', 'sur_sur_name', 'spec', 'vk_url', 'hh_url', 'behance_url', 'descriptions', 'photo']
    template_name = 'profile_settings1.html'
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        user_profile = get_object_or_404(User, slug=slug)
        #user_profile = User.objects.get(slug=slug)
        if request.user.is_authenticated:
            if user_profile.id == request.user.id:
                self.object = self.get_object()
                return super().get(request, *args, **kwargs)
        raise PermissionDenied()
    def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(User, slug=self.kwargs.get(self.slug_url_kwarg, None))
        print(user_profile.first_name)

        if 'first_name' not in request.POST:
            request.POST = {**request.POST,
                            'first_name': user_profile.first_name,
                            'last_name': user_profile.last_name,
                            'spec': user_profile.spec,
                            'sur_sur_name': user_profile.sur_sur_name,
                            'vk_url': user_profile.vk_url,
                            'hh_url': user_profile.hh_url,
                            'descriptions': user_profile.descriptions,
                            'behance_url': user_profile.behance_url}


        return  super().post(request, args, kwargs)





