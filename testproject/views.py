from django.views.generic import View
from django.http import HttpResponse

def raise_error(request):
    raise NotImplementedError('500 error for testing')

class ClassBasedView(View):
    def get(self, request):
        return HttpResponse('cool')
