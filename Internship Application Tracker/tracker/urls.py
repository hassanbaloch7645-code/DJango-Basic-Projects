from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('applications/add/', views.add_application, name='add_application'),
    path('applications/<int:pk>/update/', views.update_application, name='update_application'),
    path('applications/<int:pk>/delete/', views.delete_application, name='delete_application'),
]
