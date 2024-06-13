# tdapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .task_views import *
from .project_views import *
from .user_views import *


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('api/', include(router.urls)),
    path("signup/", SignUpView.as_view(), name="signup"),
    #users
    path('users/', user_list, name='user-list'),
    path('api/user/<int:pk>/update_status/', update_user_status, name='update-user-status'),
    path('add-user/', add_user_view, name='add-user'),
    path('api/user/search/', search_user, name='search-user'),
    
    # task
    path('api/task/<int:pk>/update_priority/', update_task_priority, name='update-task-priority'),  # Correct endpoint
    path('tasks/', task_list, name='task-list'),
    path('api/task/<int:pk>/update_status/', update_task_status, name='update-task-status'),  # Correct endpoint
    path('tasks/add/', add_task_view, name='add-task'),
    path('tasks/edit/<int:pk>/', edit_task_view, name='edit-task'), 
    path('tasks/delete/<int:pk>/', delete_task_view, name='delete-task'), 
    path('api/task/search/', search_task, name='search-task'),
    
    # project
    path('projects/', project_list, name='project-list'),
    path('projects/add/', add_project_view, name='add-project'),
    path('projects/edit/<int:pk>/', edit_project_view, name='edit-project'), 
    path('projects/delete/<int:pk>/', delete_project_view, name='delete-project'), 
    path('api/project/search/', search_project, name='search-project'),
    
    #download json
    path('download-json/', download_json, name='download-json'),
]
