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

#view list of users
@login_required
def user_list(request):
    if request.user.is_superuser:
        users = CustomUser.objects.all()
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return render(request, 'admin/user-list.html', {'users': users})
        
#update user status
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

# search user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_user(request):
    search_query = request.query_params.get('search_query', '')
    print(f"Search query received: {search_query}")  # Debug statement
    users = CustomUser.objects.filter(email__icontains=search_query)
    serializer = UserSerializer(users, many=True)
    print(f"users found: {serializer.data}")  # Debug statement
    return Response(serializer.data, status=status.HTTP_200_OK)