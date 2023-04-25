"""Cyberfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginUser.as_view(), name='login'),
    path('', Home.as_view(), name='home'),
    path('profile/<slug:slug>', Profile.as_view(), name='profile'),
    #path('project_set/', Project_set.as_view(), name='project_set'),
    path('welcome/', welcome, name='welcome'),
    path('form', wtfForm, name='form'),
    path('project', projectView, name='project'),
    path('profile/project/edit-project/<slug:slug>', projectView, name='editProject'),
    path('profile/project/add-project', addProject.as_view(), name='addProject'),
    path('form1/<name>/<surname>/<sursurname>', wtfForm1, name='form1'),
    path('profile/<slug:slug>/edit', ProfileUpdateView.as_view(), name='editProfile'),
]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

