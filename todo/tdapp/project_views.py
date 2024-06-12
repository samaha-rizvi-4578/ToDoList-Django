from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .serializers import *
from .models import *
from .permissions import *
from .forms import *


# view list of projects
@login_required
def project_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(task__assigned_to=request.user).distinct()
    return render(request, 'admin/project-list.html', {'projects': projects})

#add projct
@login_required
def add_project_view(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-superusers to the home page or an appropriate page
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project-list')  # Redirect to the project list after saving
    else:
        form = ProjectForm()
    
    return render(request, 'admin/add-project.html', {'form': form})


#edit project
@login_required
def edit_project_view(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        form = EditProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project-list')
    else:
        form = EditProjectForm(instance=project)
    return render(request, 'admin/edit-project.html', {'form': form})

#delete project
@login_required
def delete_project_view(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    project = Project.objects.get(pk=pk)
    project.delete()
    return redirect('project-list')


#search project
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_project(request):
    search_query = request.query_params.get('search_query', '')
    print(f"Search query received: {search_query}")  # Debug statement
    projects = Project.objects.filter(project_name__icontains=search_query)
    serializer = ProjectSerializer(projects, many=True)
    print(f"Projects found: {serializer.data}")  # Debug statement
    return Response(serializer.data, status=status.HTTP_200_OK)
