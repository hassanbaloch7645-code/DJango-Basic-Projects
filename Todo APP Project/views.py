from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignUpForm, TaskForm
from .models import Task


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('todo_dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome aboard.')
            return redirect('todo_dashboard')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def todo_dashboard(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully.')
            return redirect('todo_dashboard')
    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo.html', {'form': form, 'tasks': tasks})


@login_required
def toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    status = 'completed' if task.completed else 'marked as incomplete'
    messages.success(request, f'Task "{task.title}" {status}.')
    return redirect('todo_dashboard')


@login_required
def edit_todo(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('todo_dashboard')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_todo.html', {'form': form, 'task': task})


@login_required
def delete_todo(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted.')
        return redirect('todo_dashboard')
    return redirect('todo_dashboard')
