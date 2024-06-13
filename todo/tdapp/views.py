
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from .models import CustomUser, Project, Task
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer
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


#signup login view
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
# rest viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]  

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]

# sownlaod json

@api_view(['GET'])
@permission_classes([IsAdminUser])
def download_json(request):
    users = CustomUser.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()

    user_serializer = UserSerializer(users, many=True)
    project_serializer = ProjectSerializer(projects, many=True)
    task_serializer = TaskSerializer(tasks, many=True)

    # Convert serializers to dictionaries for easier manipulation
    user_data = user_serializer.data
    project_data = project_serializer.data
    task_data = task_serializer.data

    # Organize tasks under projects and projects under users
    for project in project_data:
        project['tasks'] = [task for task in task_data if task['project_name'] == project['project_id']]

    for user in user_data:
        user['projects'] = [project for project in project_data if any(task['assigned_to'] == user['id'] for task in project['tasks'])]

    data = {
        'users': user_data,
    }
    return JsonResponse(data, safe=False)