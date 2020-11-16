from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *


class AccountAdmin(UserAdmin):
    list_display = ('email', 'name', 'last_login', 'is_admin', 'is_applicant', 'is_company')
    search_fields = ('email', 'name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    ordering = ('email',)
    fieldsets = ()
    list_filter = ('is_admin', 'is_active', 'is_applicant', 'is_company')


admin.site.register(User, AccountAdmin)
admin.site.register(ApplicantProfileModel)
admin.site.register(CompanyProfileModel)
