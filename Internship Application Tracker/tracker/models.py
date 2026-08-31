from django.db import models


class Application(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]

    company_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    applied_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_date', '-created_at']

    def __str__(self):
        return f'{self.company_name} - {self.role}'

    @property
    def badge_class(self):
        badge_map = {
            'Applied': 'bg-primary',
            'Interview': 'bg-warning text-dark',
            'Selected': 'bg-success',
            'Rejected': 'bg-danger',
        }
        return badge_map.get(self.status, 'bg-secondary')
