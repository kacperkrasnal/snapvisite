from django.contrib import admin
from .models import Address, Company, Category, Service, Schedule, TimeSlot, Appointment, CompanyDay


admin.site.register(Address)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(TimeSlot)
admin.site.register(Schedule)
admin.site.register(Appointment)
admin.site.register(CompanyDay)
