from django.contrib import admin
from django.utils.html import format_html
from .models import ProjectDeadline, ProjectMilestone


class ProjectMilestoneInline(admin.TabularInline):
    model = ProjectMilestone
    extra = 1


@admin.register(ProjectDeadline)
class ProjectDeadlineAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name', 'deadline_date', 'status', 'priority', 'assigned_to', 'overdue_status']
    list_filter = ['status', 'priority', 'assigned_to', 'deadline_date']
    search_fields = ['title', 'client_name', 'project_location', 'description']
    date_hierarchy = 'deadline_date'
    ordering = ['deadline_date']
    list_editable = ['status', 'priority', 'assigned_to']
    inlines = [ProjectMilestoneInline]

    def overdue_status(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red; font-weight: bold;">OVERDUE</span>')
        elif obj.days_until_deadline <= 7:
            return format_html('<span style="color: orange; font-weight: bold;">DUE SOON</span>')
        else:
            return format_html('<span style="color: green;">ON TIME</span>')
    overdue_status.short_description = "Status"


@admin.register(ProjectMilestone)
class ProjectMilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'target_date', 'completed', 'completion_date']
    list_filter = ['completed', 'target_date']
    search_fields = ['title', 'project__title', 'project__client_name']
    ordering = ['target_date']
    list_editable = ['completed']
