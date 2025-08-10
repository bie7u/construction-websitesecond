from django.shortcuts import render
from django.http import JsonResponse
from .models import CompanyInfo, Service, Testimonial, ProjectGallery
from blog.models import BlogPost
from contact.models import ContactForm


def home(request):
    """Homepage view with hero section and featured content"""
    context = {
        'company_info': CompanyInfo.objects.first(),
        'featured_services': Service.objects.filter(active=True)[:6],
        'featured_testimonials': Testimonial.objects.filter(featured=True)[:3],
        'featured_projects': ProjectGallery.objects.filter(featured=True)[:6],
        'latest_blog_posts': BlogPost.objects.filter(published=True)[:3],
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page with company information"""
    context = {
        'company_info': CompanyInfo.objects.first(),
        'testimonials': Testimonial.objects.all()[:6],
    }
    return render(request, 'core/about.html', context)


def services(request):
    """Services page"""
    context = {
        'services': Service.objects.filter(active=True),
    }
    return render(request, 'core/services.html', context)


def gallery(request):
    """Project gallery page"""
    context = {
        'projects': ProjectGallery.objects.all(),
    }
    return render(request, 'core/gallery.html', context)
