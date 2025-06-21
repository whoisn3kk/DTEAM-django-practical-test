from django.urls import path
from .views import *

urlpatterns = [
    path('', CVListView.as_view(), name='cv_list'),
    path('cv/<int:pk>/', CVDetailView.as_view(), name='cv_detail'),
    path('cv/<int:pk>/pdf/', gen_cv_pdf, name='cv_pdf'),

    path('api/cvs/', CVLCAPIView.as_view(), name='api_cv_list'),
    path('api/cvs/<int:pk>/', CVRUAPIView.as_view(), name='api_cv_detail'),

    path('logs/', RequestLogListView.as_view(), name='request_log_list'),

    path('settings/', SettingsView.as_view(), name='settings_page'),

    path('cv/<int:pk>/translate/', translate_cv, name='cv_translate'),
]