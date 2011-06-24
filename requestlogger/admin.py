from django.contrib import admin

from .models import Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ['method', 'path', 'datetime', 'response_time', 'status_code', 'exception_class', 'exception_message']
    list_filter = ['path', 'method', 'status_code', 'exception_class']

admin.site.register(Request, RequestAdmin)
