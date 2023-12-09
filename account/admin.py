from django.contrib import admin

from account.company_model import Company, CompanyEmployee
from account.models import Profile, Verification, ResetVerification
from main.models import Load, Search, LoadType, ContactUs, Distance

admin.site.register(Profile)
admin.site.register(Load)
admin.site.register(Search)
admin.site.register(LoadType)
admin.site.register(Verification)
admin.site.register(ResetVerification)
admin.site.register(ContactUs)
admin.site.register(Distance)

class EmployeeInline(admin.TabularInline):
    model = CompanyEmployee
    readonly_fields = ['is_owner','employee']
    extra = 0

class CompanyAdmin(admin.ModelAdmin):
    inlines = [EmployeeInline,]

admin.site.register(Company ,CompanyAdmin)
