import datetime
import re

from django.conf import settings

from .models import Request, get_view_representation

class RequestLoggingMiddleware(object):
    @property
    def logging_mode(self):
        """
        Returns a logging mode

        Made a property in case it suddenly changes
        """
        
        return getattr(settings, 'REQUEST_LOGGING_MODE', 'all')

    @property
    def excluded_urls(self):
        return getattr(settings, 'REQUEST_LOGGING_EXCLUDE_URLS', ['^/admin/',
                                                                  '^/favicon.ico'])

    def should_log(self, entry):
        if self.logging_mode == 'off':
            return False
        
        if any(re.search(eu, entry.path) for eu in self.excluded_urls):
            return False

        return True
        
    def _save_log_entry(self, entry):
        if not self.should_log(entry):
            return
        
        response_time = datetime.datetime.now() - entry.datetime
        
        entry.response_time = response_time.total_seconds()
        entry.save()
        
    def process_request(self, request):
        """
        Creates a request log entry object,
        ties it to the request
        """
        
        entry = Request(method=request.method.upper(),
                        path=request.path,
                        datetime=datetime.datetime.now())
        
        request.request_log_entry = entry

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Tells a log entry about a view
        """
        request.request_log_entry.view = get_view_representation(view_func)

    def process_response(self, request, response):
        """
        Updates and saves a request log entry object
        """
        entry = request.request_log_entry
        entry.status_code = response.status_code

        if entry.status_code == 500:
            # TODO: Save an exception? Investigate if it does
            pass

        self._save_log_entry(entry)

        return response

    def process_exception(self, request, exception):
        entry = request.request_log_entry
        entry.status_code = 500

        entry.exception_class = exception.__class__.__name__
        entry.exception_message = exception.message

        self._save_log_entry(entry)
        # TODO: Investigate if it saves an entry twice
        # in devserver and realserver
        # (it does not it tests)
        
