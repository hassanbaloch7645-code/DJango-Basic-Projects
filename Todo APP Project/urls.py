from django.urls import path

from . import views

urlpatterns = [
    path('', views.todo_dashboard, name='todo_dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('task/<int:pk>/toggle/', views.toggle_complete, name='toggle_complete'),
    path('task/<int:pk>/edit/', views.edit_todo, name='edit_todo'),
    path('task/<int:pk>/delete/', views.delete_todo, name='delete_todo'),
]
