"""
URL configuration for weather_project project.
"""

from django.contrib import admin
from django.urls import path

from weather_app.views import weather_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', weather_view, name='weather'),
]
