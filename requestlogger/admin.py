from django.contrib import admin

from .models import Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ['method', 'path', 'datetime', 'response_time', 'status_code', 'exception_class', 'exception_message', 'view_module', 'view_func']
    list_filter = ['path', 'method', 'status_code', 'exception_class', 'view_module', 'view_func']

admin.site.register(Request, RequestAdmin)
