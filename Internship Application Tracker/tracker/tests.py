from django.test import TestCase
from django.urls import reverse

from .models import Application


class ApplicationTrackerTests(TestCase):
    def test_dashboard_loads_and_lists_applications(self):
        Application.objects.create(
            company_name='OpenAI',
            role='Python Engineer',
            status='Applied',
            applied_date='2026-08-01',
            notes='Initial application sent.',
        )

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OpenAI')
        self.assertContains(response, 'Python Engineer')

    def test_status_filter_works(self):
        Application.objects.create(
            company_name='Google',
            role='Frontend Engineer',
            status='Interview',
            applied_date='2026-08-03',
        )
        Application.objects.create(
            company_name='Amazon',
            role='Data Analyst',
            status='Applied',
            applied_date='2026-08-05',
        )

        response = self.client.get(reverse('dashboard') + '?status=Interview')

        self.assertContains(response, 'Google')
        self.assertNotContains(response, 'Amazon')
