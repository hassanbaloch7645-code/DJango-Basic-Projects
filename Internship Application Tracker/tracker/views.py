from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm
from .models import Application


def dashboard(request):
    selected_status = request.GET.get('status', 'All')
    applications = Application.objects.all()

    if selected_status != 'All':
        applications = applications.filter(status=selected_status)

    total_count = Application.objects.count()
    status_summary = {
        'Applied': Application.objects.filter(status='Applied').count(),
        'Interview': Application.objects.filter(status='Interview').count(),
        'Selected': Application.objects.filter(status='Selected').count(),
        'Rejected': Application.objects.filter(status='Rejected').count(),
    }

    context = {
        'applications': applications,
        'selected_status': selected_status,
        'total_count': total_count,
        'status_summary': status_summary,
    }
    return render(request, 'tracker/dashboard.html', context)


def add_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'tracker/application_form.html', {'form': form, 'title': 'Add Application'})


def update_application(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ApplicationForm(instance=application)

    return render(request, 'tracker/application_form.html', {'form': form, 'title': 'Update Application', 'application': application})


def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        application.delete()
        return redirect('dashboard')
    return redirect('dashboard')
