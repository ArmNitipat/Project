from django.contrib import admin
from adminHome.models import myuser
# Register your models here.

class Member(admin.ModelAdmin):
  list_display = ('username', 'password', 'firstname', 'lastname', 'date_of_birth','email')

admin.site.register(myuser,Member)


# from django.contrib.auth.admin import UserAdmin

# # ปรับแต่ง UserAdmin ให้แสดง date_of_birth
# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'date_of_birth', 'first_name', 'last_name', 'is_staff')