from django.contrib import admin
from adminHome.models import myuser
# Register your models here.

class Member(admin.ModelAdmin):
  list_display = ('username', 'email')

admin.site.register(myuser,Member)