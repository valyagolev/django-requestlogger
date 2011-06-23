from django.test import TestCase

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
        self.assertNotEquals(req.time, 0)

        
        
