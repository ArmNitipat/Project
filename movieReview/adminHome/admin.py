from django.contrib import admin
from adminHome.models import Member
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
  list_display = ("firstname", "lastname","age","phone", "joined_date",)

admin.site.register(Member,MemberAdmin)