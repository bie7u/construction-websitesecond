from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import ProjectDeadline, ProjectMilestone


def calendar_view(request):
    """Calendar view showing project deadlines"""
    upcoming_deadlines = ProjectDeadline.objects.filter(
        deadline_date__gte=timezone.now()
    ).order_by('deadline_date')[:10]
    
    overdue_projects = ProjectDeadline.objects.filter(
        deadline_date__lt=timezone.now(),
        status__in=['pending', 'in_progress']
    ).order_by('deadline_date')
    
    context = {
        'upcoming_deadlines': upcoming_deadlines,
        'overdue_projects': overdue_projects,
    }
    return render(request, 'calendar_app/calendar.html', context)


def calendar_events_api(request):
    """API endpoint for calendar events (for FullCalendar.js)"""
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    if start_date and end_date:
        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        deadlines = ProjectDeadline.objects.filter(
            deadline_date__range=[start_date, end_date]
        )
        
        milestones = ProjectMilestone.objects.filter(
            target_date__range=[start_date, end_date]
        )
    else:
        deadlines = ProjectDeadline.objects.all()
        milestones = ProjectMilestone.objects.all()
    
    events = []
    
    # Add deadlines as events
    for deadline in deadlines:
        color = '#dc2626'  # red
        if deadline.status == 'completed':
            color = '#16a34a'  # green
        elif deadline.status == 'in_progress':
            color = '#ea580c'  # orange
        
        events.append({
            'id': f'deadline-{deadline.id}',
            'title': f'Deadline: {deadline.title}',
            'start': deadline.deadline_date.isoformat(),
            'backgroundColor': color,
            'borderColor': color,
            'extendedProps': {
                'type': 'deadline',
                'client': deadline.client_name,
                'status': deadline.status,
                'priority': deadline.priority,
            }
        })
    
    # Add milestones as events
    for milestone in milestones:
        color = '#3b82f6'  # blue
        if milestone.completed:
            color = '#16a34a'  # green
        
        events.append({
            'id': f'milestone-{milestone.id}',
            'title': f'Milestone: {milestone.title}',
            'start': milestone.target_date.isoformat(),
            'backgroundColor': color,
            'borderColor': color,
            'extendedProps': {
                'type': 'milestone',
                'project': milestone.project.title,
                'completed': milestone.completed,
            }
        })
    
    return JsonResponse(events, safe=False)
