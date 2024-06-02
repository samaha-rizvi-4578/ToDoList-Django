from rest_framework import serializers
from tdapp.models import *
from tdapp.models import LANGUAGE_CHOICES, STYLE_CHOICES
from rest_framework import viewsets

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'