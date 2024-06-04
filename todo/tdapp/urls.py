# tdapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('api/', include(router.urls)),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('tasks/', task_list, name='task-list'),
    path('api/task/<int:pk>/update_priority/', update_task_priority, name='update-task-priority'),  # Correct endpoint
    path('api/task/<int:pk>/update_status/', update_task_status, name='update-task-status'),  # Correct endpoint
    path('users/', user_list, name='user-list'),
    path('api/user/<int:pk>/update_status/', update_user_status, name='update-user-status'),
    path('projects/', project_list, name='project-list'),
    path('add-user/', add_user_view, name='add-user'),
    path('tasks/add/', add_task_view, name='add-task'),
    path('tasks/edit/<int:pk>/', edit_task_view, name='edit-task'), 
    path('projects/add/', add_project_view, name='add-project'),
    path('projects/edit/<int:pk>/', edit_project_view, name='edit-project'), 
]
