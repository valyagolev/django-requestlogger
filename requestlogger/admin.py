from django.contrib import admin
from django.db.models import Avg, Max, Count

from .models import Request, View

class RequestAdmin(admin.ModelAdmin):
    list_display = ['method', 'path', 'datetime', 'response_time', 'status_code', 'exception_class', 'exception_message', 'view']
    list_filter = ['path', 'method', 'status_code', 'exception_class', 'view__module', 'view__func']

class ViewAdmin(admin.ModelAdmin):
    list_display = ['module', 'func',
                    'avg_response_time',
                    'max_response_time',
                    'request_count']

    def queryset(self, *args, **kwargs):
        qs = super(ViewAdmin, self).queryset(*args, **kwargs)
        qs = qs.annotate(avg_response_time=Avg('request__response_time'),
                         max_response_time=Max('request__response_time'),
                         request_count=Count('request'))        
        return qs


admin.site.register(Request, RequestAdmin)
admin.site.register(View, ViewAdmin)
