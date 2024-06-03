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



# view list items

@login_required
def task_list(request):
    if request.user.is_superuser:
        tasks = Task.objects.all().order_by('project_name')
    else:
        tasks = Task.objects.filter(assigned_to=request.user).order_by('project_name')
    return render(request, 'admin/task-list.html', {'tasks': tasks})

#update priority and status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_task_priority(request, pk):
    try:
        task = Task.objects.get(pk=pk, assigned_to=request.user)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    task.priority = request.data.get('priority')
    task.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_task_status(request, pk):
    try:
        task = Task.objects.get(pk=pk, assigned_to=request.user)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    task.completed = request.data.get('completed') == 'true'
    task.save()
    return Response(status=status.HTTP_200_OK)

#view list of users
@login_required
def user_list(request):
    if request.user.is_superuser:
        users = CustomUser.objects.all()
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return render(request, 'admin/user-list.html', {'users': users})
        

@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_user_status(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    is_superuser = request.data.get('is_superuser') == 'True'
    user.is_superuser = is_superuser
    user.save()
    return Response(status=status.HTTP_200_OK)


# view list of projects
@login_required
def project_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(task__assigned_to=request.user).distinct()
    return render(request, 'admin/project-list.html', {'projects': projects})

# add project
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
#add user
@login_required
def add_user_view(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'admin/add-user.html', {'form': form})


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

#add task
@login_required
def add_task_view(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task-list')
    else:
        form = TaskForm()
    return render(request, 'admin/add-task.html', {'form': form})


        

