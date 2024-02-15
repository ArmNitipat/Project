from django.contrib import admin
from adminHome.models import Bannerslide, Comment, Report, Premium_list


class BannerslideAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'order']
    list_filter = ['active']
    search_fields = ['title']

admin.site.register(Bannerslide, BannerslideAdmin)


from django.contrib import admin
from .models import Premium

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
    list_display = ['user', 'data', 'score', 'spoiler', 'update_date']


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

# @admin.register(Premium_list)
# class Premium_listAdmin(admin.ModelAdmin):
#     list_display = ['user', 'premium']

#     def user(self, obj):
#         return obj.user.username
#     user.short_description = 'User'

#     def premium(self, obj):
#         return obj.premium.name
#     premium.short_description = 'Premium Product'

#     actions = ['delete_premiums']

#     @admin.action(description='Delete selected premiums')
#     def delete_premiums(self, request, queryset):
#         for premium_list in queryset:
#             premium_list.premium.delete()