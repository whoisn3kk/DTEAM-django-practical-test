from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from main.tasks import send_email
from .models import *
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template.loader import get_template
from io import BytesIO
import pdfkit

from rest_framework import generics
from main.serializers import *

# Create your views here.

class CVListView(ListView):
    model = CV
    template_name = 'main/cv_list.html'
    context_object_name = 'cv_list'

    def get_queryset(self):
        return CV.objects.prefetch_related('skills').all() 

class CVDetailView(DetailView):
    model = CV
    template_name = 'main/cv_detail.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('skills', 'projects')
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        email = request.POST.get('email')
        if email:
            cv = self.get_object()
            send_email.delay(cv.pk, email)
            return HttpResponseRedirect(request.path_info)
        
        return super().get(request, *args, **kwargs)

def gen_cv_pdf(request:HttpRequest, pk:int):
    cv = CV.objects.get(pk=pk)
    template = get_template('main/cv_pdf_template.html')
    html = template.render({'cv': cv})


    buffer = BytesIO(pdfkit.from_string(html)) # type: ignore
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CV_{cv.pk}.pdf"'

    return response


class CVRUAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CVSerializer
    queryset = CV.objects.all()

class CVLCAPIView(generics.ListCreateAPIView):
    serializer_class = CVSerializer
    queryset = CV.objects.all()


class RequestLogListView(ListView):
    model = RequestLog
    template_name = 'main/request_log_list.html'
    context_object_name = 'logs'
    queryset = RequestLog.objects.order_by('-timestamp')[:10]


class SettingsView(TemplateView):
    template_name = 'main/settings.html'