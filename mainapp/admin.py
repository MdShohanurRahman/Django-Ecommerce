from django.contrib import admin
from .models import *

# Register your models here.

class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ['name','join_date','check']
    search_fields = ["__str__"]
    list_filter = ["join_date", "check"]
    list_editable = ['check']
    list_per_page = 10

    class Meta:
        Model = AuthorProfile

admin.site.register(AuthorProfile,AuthorProfileAdmin)


admin.site.register(MesLocation)
class MesServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'check', 'posted_on']
    search_fields = ["__str__"]
    list_filter = ["posted_on", "check"]
    list_editable = ['check']
    list_per_page = 10

    class Meta:
        Model = MesService

admin.site.register(MesService, MesServiceAdmin)
admin.site.register(TuitionServiceSubject)

class TuitionServiceAdmin(admin.ModelAdmin):
    list_display = ['ad_author', 'salary', 'posted_on', 'check']
    search_fields = ["__str__"]
    list_filter = ["posted_on", "check"]
    list_editable = ['check']
    list_per_page = 10

    class Meta:
        Model = TuitionService
        
admin.site.register(TuitionService,TuitionServiceAdmin)
# admin.site.register(Comment)
# admin.site.register(UserEducationStatus)
