from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)
        
# add project
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'description']
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

#add task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'project_name', 'description', 'priority', 'completed', 'assigned_to']
        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control'}),
            'project_name': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }
        
#edit project
class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'description']
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

#edit task
class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'project_name', 'description', 'priority', 'completed', 'assigned_to']
        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control'}),
            'project_name': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }