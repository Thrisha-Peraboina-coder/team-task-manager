from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Project, Membership
from .forms import ProjectForm, AddMemberForm

@login_required
def project_list(request):
    projects = Project.objects.filter(Q(owner=request.user) | Q(members=request.user)).distinct()
    return render(request, 'projects/list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            Membership.objects.create(project=project, user=request.user, role='admin')
            messages.success(request, "Project created.")
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/form.html', {'form': form, 'title': 'New Project'})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not project.user_role(request.user):
        return HttpResponseForbidden("Not a member.")
    add_form = AddMemberForm()
    if request.method == 'POST' and project.is_admin(request.user):
        add_form = AddMemberForm(request.POST)
        if add_form.is_valid():
            user = User.objects.get(username=add_form.cleaned_data['username'])
            Membership.objects.get_or_create(
                project=project, user=user,
                defaults={'role': add_form.cleaned_data['role']}
            )
            messages.success(request, f"Added {user.username}.")
            return redirect('project_detail', pk=pk)
    return render(request, 'projects/detail.html', {
        'project': project,
        'memberships': project.memberships.select_related('user').all(),
        'tasks': project.tasks.select_related('assignee').all(),
        'add_form': add_form,
        'is_admin': project.is_admin(request.user),
    })

@login_required
def remove_member(request, pk, user_id):
    project = get_object_or_404(Project, pk=pk)
    if not project.is_admin(request.user):
        return HttpResponseForbidden()
    Membership.objects.filter(project=project, user_id=user_id).exclude(user=project.owner).delete()
    return redirect('project_detail', pk=pk)
