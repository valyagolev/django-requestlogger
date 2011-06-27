import datetime
import re

from django.conf import settings

from .models import Request, get_view_representation

class RequestLoggingMiddleware(object):
    # TODO: Move settings the hell out of here
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

    @property
    def excluded_views(self):
        return getattr(settings, 'REQUEST_LOGGING_EXCLUDE_VIEWS', [])


    def should_log(self, entry):
        if self.logging_mode == 'off':
            return False
        
        if any(re.search(eu, entry.path) for eu in self.excluded_urls):
            return False

        if (entry.view and
            any(re.search(ev, entry.view.total_name()) for ev in self.excluded_views)):
            return False
        
        return True

    
    def _get_log_entry(self, request):
        try:
            return request.request_log_entry
        except AttributeError:
            entry = Request(method=request.method.upper(),
                            path=request.path,
                            datetime=datetime.datetime.now())
        
            request.request_log_entry = entry

            return entry

    
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
        self._get_log_entry(request)
        

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Tells a log entry about a view
        """
        self._get_log_entry(request).view = get_view_representation(view_func)

    def process_response(self, request, response):
        """
        Updates and saves a request log entry object
        """
        entry = self._get_log_entry(request)
        entry.status_code = response.status_code

        if entry.status_code == 500:
            # TODO: Save an exception? Investigate if it does
            pass

        self._save_log_entry(entry)

        return response

    def process_exception(self, request, exception):
        entry = self._get_log_entry(request)
        entry.status_code = 500

        entry.exception_class = exception.__class__.__name__
        entry.exception_message = exception.message

        self._save_log_entry(entry)
        # TODO: Investigate if it saves an entry twice
        # in devserver and realserver
        # (it does not it tests)
        
