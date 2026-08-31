from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['company_name', 'role', 'status', 'applied_date', 'notes']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Microsoft'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Software Engineer'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'applied_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Add notes about the role, recruiter, or follow-up date.'}),
        }
