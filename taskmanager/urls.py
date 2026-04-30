from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r: redirect('dashboard') if r.user.is_authenticated else redirect('login')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('tasks.dashboard_urls')),
    path('projects/', include('projects.urls')),
    path('tasks/', include('tasks.urls')),
    path('api/', include('tasks.api_urls')),
]
