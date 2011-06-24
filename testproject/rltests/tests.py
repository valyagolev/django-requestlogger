from django.test import TestCase
from django.conf import settings

from requestlogger.models import Request

class RequestLoggerTestCase(TestCase):
    def setUp(self):
        Request.objects.all().delete()

    def tearDown(self):
        Request.objects.all().delete()

    def testItActuallyLogsRequests(self):
        self.client.get('/admin/')

        requests = Request.objects.all()
        self.assertEquals(len(requests), 1)

        req = requests[0]
        self.assertEquals(req.method, 'GET')
        self.assertEquals(req.path, '/admin/')
        self.assertNotEquals(req.response_time, 0)
        self.assertEquals(req.status_code, 200)

    def testItDoesNotIfSwitchedOff(self):
        try:
            settings.REQUEST_LOGGING_MODE = 'none'

            self.client.get('/admin/')
            self.client.get('/not_exists/')
            
            try:
                self.client.get('/error500/')
            except NotImplementedError:
                pass

            self.assertEquals(len(Request.objects.all()), 0)

        finally:
            settings.REQUEST_LOGGING_MODE = 'all'

        
    def testItLogs404(self):
        self.client.get('/not_exists/')
        
        requests = Request.objects.all()
        self.assertEquals(len(requests), 1)

        req = requests[0]
        self.assertEquals(req.method, 'GET')
        self.assertEquals(req.path, '/not_exists/')
        self.assertNotEquals(req.response_time, 0)
        self.assertEquals(req.status_code, 404)

    def testItLogs500(self):
        try:
            self.client.get('/error500/')
        except NotImplementedError:
            pass

        requests = Request.objects.all()
        self.assertEquals(len(requests), 1)

        req = requests[0]
        self.assertEquals(req.method, 'GET')
        self.assertEquals(req.path, '/error500/')
        self.assertNotEquals(req.response_time, 0)
        self.assertEquals(req.status_code, 500)
        self.assertEquals(req.exception_class, 'NotImplementedError')
        self.assertEquals(req.exception_message, '500 error for testing')


    def testItLogsView(self):
        try:
            self.client.get('/error500/')
        except NotImplementedError:
            pass

        requests = Request.objects.all()
        self.assertEquals(len(requests), 1)

        req = requests[0]
        self.assertEquals(req.view_module, 'testproject.views')
        self.assertEquals(req.view_func, 'raise_error')

        self.client.get('/class_based/')
        req = Request.objects.latest()
        self.assertEquals(req.view_module, 'testproject.views')
        self.assertEquals(req.view_func, 'ClassBasedView')
        

        

        
        
