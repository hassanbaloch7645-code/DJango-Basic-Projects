from django.urls import path

from .views import add_expense, dashboard, delete_expense

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('add/', add_expense, name='add_expense'),
    path('delete/<int:expense_id>/', delete_expense, name='delete_expense'),
]
