# Django
from django.contrib import admin
from django.contrib.sessions.models import Session


# local Django
from .models import CustomUser

# Register your models here.


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)
admin.site.register(CustomUser)
