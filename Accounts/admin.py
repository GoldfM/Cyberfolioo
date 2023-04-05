from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Accounts.models import *

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Image)
admin.site.register(Specs)
admin.site.register(Follow)
admin.site.register(Project)