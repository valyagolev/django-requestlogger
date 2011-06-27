from django.db import models

METHODS = ['GET', 'POST', 'PUT', 'DELETE']

def get_view_representation(view_func):
    module = view_func.__module__
    func = view_func.__name__

    return View.objects.get_or_create(module=module,
                                      func=func)[0]


def aggregated_column(name):
    def _func(self):
        assert False

    _func.__name__ = name
    _func.admin_order_field = name
    
    return _func


class View(models.Model):
    """A view representation, defined by module and func names"""

    module = models.CharField(max_length=255, blank=True)
    func = models.CharField(max_length=255, blank=True)

    # these all are failing since they should be set via queryset
    # but django's 'ModelAdmin' insists on having such functions
    # in the model
    avg_response_time = aggregated_column('avg_response_time')
    max_response_time = aggregated_column('max_response_time')
    request_count = aggregated_column('request_count')


    class Meta:
        unique_together = [('module', 'func')]


class Request(models.Model):
    """Request log entry"""
    
    method = models.CharField(max_length=7, choices=zip(METHODS, METHODS))
    path = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    response_time = models.FloatField()
    status_code = models.IntegerField()
    exception_class = models.CharField(max_length=255, blank=True)
    exception_message = models.TextField(blank=True)
    view = models.ForeignKey(View, null=True)

    class Meta:
        get_latest_by = 'datetime'
    
    def __unicode__(self):
        return '%s %s, at %s' % (self.method, self.path, self.datetime)
    
    
