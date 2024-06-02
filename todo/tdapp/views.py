# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
# rest viewsets
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer
from .models import CustomUser, Project, Task
from .permissions import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()  # Add this line
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(task__assigned_to=self.request.user).distinct()

    def get_permissions(self):
        if self.request.user.is_superuser:
            return [permissions.IsAuthenticated, IsSuperUser]
        #else retrn not allowed
        return [permissions.IsAuthenticated, IsOwnerOrReadOnly]
   

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

    def perform_create(self, serializer):
        # Prevent regular users from creating tasks
        pass

    def perform_update(self, serializer):
        # Allow update only for priority and completion status
        serializer.save()


from django.views.generic import ListView


class UserListView(ListView):
    model = CustomUser
    template_name = 'user_list.html'

class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'

class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
