# bankdata/urls.py
from django.urls import path
from .views import upload_files, display_data, upload_success

urlpatterns = [
    path('upload/', upload_files, name='upload'),
    path('display/', display_data, name='display_data'),
    path('upload/success/', upload_success, name='success'),
]
