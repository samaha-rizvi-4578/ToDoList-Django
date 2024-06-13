
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Task
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

#task-list

@login_required
def task_list(request):
    if request.user.is_superuser:
        tasks = Task.objects.all().order_by('project_name')
    else:
        tasks = Task.objects.filter(assigned_to=request.user).order_by('project_name')
    return render(request, 'admin/task-list.html', {'tasks': tasks})



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

#edit task
@login_required
def edit_task_view(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-list')
    else:
        form = EditTaskForm(instance=task)
    return render(request, 'admin/edit-task.html', {'form': form})

#delete task
@login_required
def delete_task_view(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('task-list')


#search task 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_task(request):
    search_query = request.query_params.get('search_query', '')
    print(f"Search query received: {search_query}")  # Debug statement
    tasks = Task.objects.filter(task_name__icontains=search_query)
    serializer = TaskSerializer(tasks, many=True)
    print(f"Tasks found: {serializer.data}")  # Debug statement
    return Response(serializer.data, status=status.HTTP_200_OK)

#update priority
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_task_priority(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        if task.assigned_to != request.user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    task.priority = request.data.get('priority')
    task.save()
    return Response(status=status.HTTP_200_OK)

#update status
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_task_status(request, pk):
    try:
        task = Task.objects.get(pk=pk)
        if task.assigned_to != request.user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if the 'completed' key exists in the request data and handle accordingly
    if 'completed' in request.data:
        task.completed = request.data.get('completed')
        task.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


