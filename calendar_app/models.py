from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ProjectDeadline(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client_name = models.CharField(max_length=100)
    project_location = models.CharField(max_length=200, blank=True)
    deadline_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    completion_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['deadline_date']

    def __str__(self):
        return f"{self.title} - {self.client_name}"

    @property
    def is_overdue(self):
        return timezone.now() > self.deadline_date and self.status != 'completed'

    @property
    def days_until_deadline(self):
        diff = self.deadline_date - timezone.now()
        return diff.days


class ProjectMilestone(models.Model):
    """Milestones for tracking project progress"""
    project = models.ForeignKey(ProjectDeadline, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['target_date']

    def __str__(self):
        return f"{self.project.title} - {self.title}"
