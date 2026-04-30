from django.urls import path
from . import api_views

urlpatterns = [
    path('projects/<int:project_id>/tasks/', api_views.api_project_tasks, name='api_project_tasks'),
    path('tasks/<int:pk>/status/', api_views.api_update_status, name='api_update_status'),
]
