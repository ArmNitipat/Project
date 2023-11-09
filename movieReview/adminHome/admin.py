from django.contrib import admin
from adminHome.models import Bannerslide, Comment, Report


class BannerslideAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'order']
    list_filter = ['active']
    search_fields = ['title']

admin.site.register(Bannerslide, BannerslideAdmin)


from django.contrib import admin
from .models import Premium, Premium_list

class PremiumAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'title', 'price', 'num')
        }),
        ('Image Information', {
            'fields': ('imag','expires' )
        }),
    )

admin.site.register(Premium, PremiumAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'data', 'like', 'score', 'spoiler', 'update_date']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    list_display = ['id', 'comment_data', 'comment_user', 'created_at', 'reason']

    def comment_data(self, obj):
        return obj.comment.data
    comment_data.short_description = 'Comment Data'
    
    def comment_user(self, obj):
        return obj.comment.user
    comment_user.short_description = 'User'

    def comment_score(self, obj):
        return obj.comment.score
    comment_score.short_description = 'Score'

    def comment_like(self, obj):
        return obj.comment.like
    comment_like.short_description = 'Like'

    def comment_spoiler(self, obj):
        return obj.comment.spoiler
    comment_spoiler.short_description = 'Spoiler'

    actions = ['delete_comments']

    @admin.action(description='Delete selected comments')
    def delete_comments(self, request, queryset):
        for report in queryset:
            report.comment.delete()