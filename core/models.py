from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class CompanyInfo(models.Model):
    """Main company information"""
    company_name = models.CharField(max_length=200, default="Construction Company")
    tagline = models.CharField(max_length=300, default="Building Your Dreams")
    about_us = RichTextUploadingField()
    mission_statement = models.TextField()
    years_experience = models.PositiveIntegerField(default=10)
    projects_completed = models.PositiveIntegerField(default=100)
    happy_clients = models.PositiveIntegerField(default=50)
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='company/', blank=True, null=True)

    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Information"

    def __str__(self):
        return self.company_name


class Service(models.Model):
    """Services offered by the company"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    """Client testimonials"""
    client_name = models.CharField(max_length=100)
    client_position = models.CharField(max_length=100, blank=True)
    client_company = models.CharField(max_length=100, blank=True)
    testimonial = models.TextField()
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-featured', '-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"


class ProjectGallery(models.Model):
    """Gallery of completed projects"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=100, blank=True)
    completion_date = models.DateField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-completion_date']
        verbose_name_plural = "Project Gallery"

    def __str__(self):
        return self.title
