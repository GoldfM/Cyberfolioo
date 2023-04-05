from django.contrib import admin

from Accounts.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Image)
admin.site.register(Specs)
admin.site.register(Follow)
admin.site.register(Project)