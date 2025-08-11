from django.db import models
from django.utils import timezone


class ContactForm(models.Model):
    CONTACT_TYPES = [
        ('general', 'General Inquiry'),
        ('quote', 'Request Quote'),
        ('consultation', 'Consultation'),
        ('support', 'Support'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class ContactInfo(models.Model):
    """Company contact information"""
    company_name = models.CharField(max_length=200, default="Construction Company")
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    business_hours = models.TextField(default="Mon-Fri: 8AM-6PM")
    emergency_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return self.company_name
