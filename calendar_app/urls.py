from django.urls import path
from . import views

app_name = 'calendar_app'

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('api/events/', views.calendar_events_api, name='calendar_events_api'),
]