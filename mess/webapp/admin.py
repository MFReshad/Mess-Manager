from django.contrib import admin

# Register your models here.

from . models import Record, User, Mess , Bazar

admin.site.register(Record)
admin.site.register(User)
admin.site.register(Mess)
admin.site.register(Bazar)