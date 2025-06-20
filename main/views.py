from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from django.http import HttpResponse, HttpRequest
from django.template.loader import get_template
from io import BytesIO
import pdfkit

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

def gen_cv_pdf(request:HttpRequest, pk:int):
    cv = CV.objects.get(pk=pk)
    template = get_template('main/cv_pdf_template.html')
    html = template.render({'cv': cv})


    buffer = BytesIO(pdfkit.from_string(html)) # type: ignore
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CV_{cv.pk}.pdf"'

    return response
