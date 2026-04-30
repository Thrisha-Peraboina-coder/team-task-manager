from django.urls import path
from . import views

urlpatterns = [
    path('project/<int:project_id>/new/', views.task_create, name='task_create'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
]
