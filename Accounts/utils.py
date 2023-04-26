from django.db.models import Count

from .models import *

'''class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['projects'] = Project.objects.all()
        context['users'] = User.objects.all()
        context['images'] = Image.objects.all()
        return context'''