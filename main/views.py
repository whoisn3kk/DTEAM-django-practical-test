from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

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