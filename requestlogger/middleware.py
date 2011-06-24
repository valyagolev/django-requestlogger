import datetime

from .models import Request

class RequestLoggingMiddleware(object):
    def _save_log_entry(self, entry):
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

    def process_response(self, request, response):
        """
        Updates and saves a request log entry object
        """
        entry = request.request_log_entry
        entry.status_code = response.status_code

        self._save_log_entry(entry)

        return response

    def process_exception(self, request, exception):
        entry = request.request_log_entry
        entry.status_code = 500

        entry.exception_class = exception.__class__.__name__
        entry.exception_message = exception.message

        self._save_log_entry(entry)
        
