from django.contrib import admin
from locust.api.models import OpenCivicID



class OpenCivicIDAdmin(admin.ModelAdmin):
    pass


admin.site.register(OpenCivicID, OpenCivicIDAdmin)
