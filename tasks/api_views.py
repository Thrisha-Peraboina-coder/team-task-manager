import json
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from projects.models import Project
from .models import Task

def task_to_dict(t):
    return {
        'id': t.id, 'title': t.title, 'description': t.description,
        'status': t.status, 'priority': t.priority,
        'assignee': t.assignee.username if t.assignee else None,
        'due_date': t.due_date.isoformat() if t.due_date else None,
        'is_overdue': t.is_overdue, 'project_id': t.project_id,
    }

@login_required
@require_http_methods(["GET"])
def api_project_tasks(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not project.user_role(request.user):
        return HttpResponseForbidden()
    return JsonResponse({'tasks': [task_to_dict(t) for t in project.tasks.all()]})

@login_required
@require_http_methods(["POST"])
def api_update_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    role = task.project.user_role(request.user)
    if not role:
        return HttpResponseForbidden()
    if role != 'admin' and task.assignee != request.user:
        return HttpResponseForbidden()
    try:
        data = json.loads(request.body)
        status = data.get('status')
        if status not in dict(Task.STATUS_CHOICES):
            return HttpResponseBadRequest("Invalid status")
        task.status = status
        task.save(update_fields=['status', 'updated_at'])
        return JsonResponse(task_to_dict(task))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
