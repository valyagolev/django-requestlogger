from django.db import models

METHODS = ['GET', 'POST', 'PUT', 'DELETE']

class Request(models.Model):
    """Request log entry"""
    
    method = models.CharField(max_length=7, choices=zip(METHODS, METHODS))
    path = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    response_time = models.FloatField()
    status_code = models.IntegerField()
    exception_class = models.CharField(max_length=255, blank=True)
    exception_message = models.TextField(blank=True)

    def __unicode__(self):
        return '%s %s, at %s' % (self.method, self.path, self.datetime)
    
