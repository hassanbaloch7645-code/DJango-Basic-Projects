from django.db.models import Sum
from django.shortcuts import redirect, render

from .forms import ExpenseForm
from .models import Expense


def dashboard(request):
    expenses = Expense.objects.select_related('category').order_by('-date', '-id')[:10]
    total_spending = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'expenses': expenses,
        'total_spending': total_spending,
    }
    return render(request, 'expenses/dashboard.html', context)


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})


def delete_expense(request, expense_id):
    expense = Expense.objects.get(pk=expense_id)
    expense.delete()
    return redirect('dashboard')
