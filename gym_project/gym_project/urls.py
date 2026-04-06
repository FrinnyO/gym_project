from django.contrib import admin
from django.urls import path
from club.views import export_pdf, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('export/', export_pdf, name='export_pdf'),
]
