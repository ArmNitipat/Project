from django.contrib import admin
from star.models import  Star, StarType, Official_sites , AlternativeNames, Spouses, Children, Relatives,  OtherWorks

#actor !!!!!!
# class StarAdmin(admin.ModelAdmin):
#     list_display = ('name', 'height', 'born_date', 'active')
#     search_fields = ['name']
#     list_filter = ('active', 'job')
#     readonly_fields = ('update_time',)  # Add this line
#     fieldsets = (
#         (None, {
#             'fields': ('name', 'job', 'history')
#         }),
#         ('Personal Info', {
#             'fields': ('height', 'born_date', 'born_location', 'died_date', 'died_location')
#         }),
#         ('Professional Info', {
#             'fields': ('active',)
#         }),
#         ('Relationships', {
#             'fields': ('spouse_star', 'children_star', 'relatives', 'other_works')
#         }),
#     )
class OfficialInline(admin.StackedInline):
    model = Official_sites
    fk_name = 'star'
    extra = 0

class SpousesInline(admin.StackedInline):
    model = Spouses
    fk_name = 'star'
    extra = 0

class ChildrenInline(admin.StackedInline):
    model = Children
    fk_name = 'star'
    extra = 0

class RelativesInline(admin.TabularInline):
    model = Relatives
    fk_name = 'star'
    extra = 0

class OtherWorksInline(admin.StackedInline):
    model = OtherWorks
    fk_name = 'star'
    extra = 0

class StarAdmin(admin.ModelAdmin):
    list_display = ('name', 'height', 'born_date', 'active')
    search_fields = ['name']
    list_filter = ('active', 'job')
    readonly_fields = ('update_time',)  # assuming update_time is a field in your Star model
    inlines = [OfficialInline,SpousesInline, ChildrenInline, RelativesInline, OtherWorksInline]  # Add this line

    fieldsets = (
        (None, {
            'fields': ('name', 'job', 'history')
        }),
        ('Personal Info', {
            'fields': ('height', 'born_date', 'born_location', 'died_date', 'died_location')
        }),
        ('Professional Info', {
            'fields': ('active', 'update_time'),  # 'update_time' is readonly
        }),
    )

    def spouse_star(self, obj):
        return ", ".join([spouse.spouse.name for spouse in Spouses.objects.filter(star=obj)])

    def children_star(self, obj):
        return ", ".join([child.child_name.name for child in Children.objects.filter(star=obj)])

    def relatives(self, obj):
        return ", ".join([f"{relative.relationship}: {relative.relative_name}" for relative in Relatives.objects.filter(star=obj)])

    def other_works(self, obj):
        return ", ".join([work.work_description for work in OtherWorks.objects.filter(star=obj)])

    spouse_star.short_description = 'Spouses'
    children_star.short_description = 'Children'
    relatives.short_description = 'Relatives'
    other_works.short_description = 'Other Works'
    
@admin.register(Children)
class ChildrenAdmin(admin.ModelAdmin):
    search_fields = ['child_name__name', 'star__name']
    list_display = ['star', 'child_name']
    
# Register your models here
admin.site.register(Star, StarAdmin)
admin.site.register(Official_sites)
admin.site.register(AlternativeNames)
admin.site.register(Spouses)
admin.site.register(Relatives)
admin.site.register(OtherWorks)
admin.site.register(StarType)