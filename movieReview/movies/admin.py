from django.contrib import admin
from movies.models import Movie, MovieDetail, MovieTag, MovieRate, LocalImage, URLImage ,Video

# Register your models here.
# class MovieAdmin(admin.ModelAdmin):
#     list_display = ('id', 'namemovie', 'Movie_Release', 'Movie_Rate', 'Story', 'Movie_Time', 'is_show')
#     search_fields = ('namemovie',)
#     list_filter = ('Movie_Rate', 'is_show')
#     ordering = ('-Movie_Release',)  # เรียงตามวันที่ปล่อยภาพยนตร์ในแบบ ล่าสุดมาก่อน
#     date_hierarchy = 'Movie_Release'  #

# admin.site.register(Movie)
admin.site.register(MovieDetail)
admin.site.register(MovieRate)
admin.site.register(MovieTag)
admin.site.register(URLImage)
admin.site.register(LocalImage)
admin.site.register(Video)


class LocalImageInline(admin.StackedInline):  # หรือคุณสามารถใช้ admin.StackedInline ถ้าต้องการแสดงแบบแถวยาว
    model = LocalImage
    extra = 1  # จำนวนฟิลด์ที่จะแสดงในหน้า admin เมื่อคุณเพิ่ม Star ใหม่
    show_change_link = True
    # max_num = 100
    can_delete = False
    exclude = None


class URLImageInline(admin.StackedInline):
    model = URLImage
    extra = 1  # จำนวนฟิลด์ที่จะแสดงในหน้า admin เมื่อคุณเพิ่ม Star ใหม่
    show_change_link = True
    # max_num = 100
    can_delete = False
    exclude = None

class MovieDetailInline(admin.StackedInline):
    model = MovieDetail
    extra = 1  # จำนวนฟิลด์ที่จะแสดงในหน้า admin เมื่อคุณเพิ่ม Star ใหม่
    show_change_link = True
    # max_num = 100
    can_delete = False
    exclude = None

class MovieAdmin(admin.ModelAdmin):
    # add_form_template = 'custom_add_form.html'
    inlines = [MovieDetailInline,LocalImageInline,URLImageInline]
    # inlines2 = [URLImage]
    exclude = ('update_time',)
    list_filter = ['is_show']
    search_fields = ('id','namemovie', 'is_show',)
    # list_display = ('id', 'namemovie', 'Movie_Release', 'Movie_Rate', 'Story', 'Movie_Time', 'is_show')

    fieldsets = (
        ('Movie Information', {
            'fields': ('name', 'writer','director', 'release_date', 'story','time', 'rate', 'tags','is_show')
        }),)

admin.site.register(Movie, MovieAdmin)