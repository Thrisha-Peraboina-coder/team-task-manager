from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from projects.models import Project
from .models import Task
from .forms import TaskForm

@login_required
def dashboard(request):
    user = request.user
    user_projects = Project.objects.filter(Q(owner=user) | Q(members=user)).distinct()
    my_tasks = Task.objects.filter(assignee=user).select_related('project')
    today = timezone.now().date()
    overdue = my_tasks.filter(due_date__lt=today).exclude(status='done')
    counts = {
        'total': my_tasks.count(),
        'todo': my_tasks.filter(status='todo').count(),
        'in_progress': my_tasks.filter(status='in_progress').count(),
        'done': my_tasks.filter(status='done').count(),
        'overdue': overdue.count(),
        'projects': user_projects.count(),
    }
    return render(request, 'dashboard/index.html', {
        'counts': counts,
        'my_tasks': my_tasks.order_by('due_date')[:10],
        'overdue_tasks': overdue,
        'projects': user_projects,
    })

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not project.is_admin(request.user):
        return HttpResponseForbidden("Only admins can create tasks.")
    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, "Task created.")
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm(project=project)
    return render(request, 'tasks/form.html', {'form': form, 'project': project, 'title': 'New Task'})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    role = project.user_role(request.user)
    if not role:
        return HttpResponseForbidden()
    is_admin = role == 'admin'
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, project=project)
        if form.is_valid():
            if not is_admin:
                # Members can only update status of their own tasks
                if task.assignee != request.user:
                    return HttpResponseForbidden("You can only update your own tasks.")
                task.status = form.cleaned_data['status']
                task.save(update_fields=['status', 'updated_at'])
            else:
                form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm(instance=task, project=project)
    return render(request, 'tasks/form.html', {
        'form': form, 'project': project, 'title': 'Edit Task', 'is_admin': is_admin
    })

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not task.project.is_admin(request.user):
        return HttpResponseForbidden()
    pid = task.project.pk
    task.delete()
    return redirect('project_detail', pk=pid)
