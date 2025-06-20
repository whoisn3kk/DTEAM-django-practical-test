from django.http import HttpRequest
from .models import RequestLog

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request:HttpRequest):
        ip_address = request.META.get('REMOTE_ADDR')
        RequestLog.objects.create(
            method=request.method,
            path=request.path,
            ip_address=ip_address
        )
        
        response = self.get_response(request)
        return response
