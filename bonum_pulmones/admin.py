from django.contrib import admin

from bonum_pulmones import models


class UserAdmin(admin.ModelAdmin):
    fields = ['auth_user']


class MedicalDataAdmin(admin.ModelAdmin):
    fields = ['filename', 'result', 'owner']

admin.site.register(models.User, UserAdmin)
admin.site.register(models.MedicalData, MedicalDataAdmin)
