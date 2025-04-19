from django.contrib import admin
from accounts.models import Repository, DjitUser # idk why interpreteur is angry at this

# Register your models here.
admin.site.register(Repository)
admin.site.register(DjitUser)