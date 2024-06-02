# tdapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet, basename='project')  # Add basename
router.register(r'tasks', TaskViewSet, basename='task')  # Add basename


urlpatterns = [
    path('', include(router.urls)),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('users/', UserListView.as_view(), name='user-list'),
]
