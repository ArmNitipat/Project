from django.contrib import admin
from adminHome.models import myuser
# Register your models here.

class Member(admin.ModelAdmin):
  list_display = ('username', 'password', 'firstname', 'lastname', 'date_of_birth','email')

admin.site.register(myuser,Member)

