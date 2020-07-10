from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main_app.models import *
from API_Data.serializers import UserDataSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny

@permission_classes((AllowAny, ))
@api_view(['GET'])
def apiOverview(request):
    api_urls={
        'Detail View':'/task-detail/<str:pk>/',
        'Create':'/task_create/',
        'Update':'/task-update/<str:pk>/',
        'Delete':'/task-delete/<str:pk>/',
    }
    return Response(api_urls)

@permission_classes((AllowAny, ))
@api_view(['GET'])
def tasklist(request):
    user1= User.objects.all()
    serializer = UserDataSerializer(user1, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request,pk):
    user1= User.objects.get(id=pk)
    serializer = UserDataSerializer(user1, many=False)
    return Response(serializer.data)

# @permission_classes((AllowAny, ))
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])

def taskCreate(request):
    serializer = UserDataSerializer(data=request.data)
    username=serializer.initial_data['username']
    password=serializer.initial_data['password']
    email=serializer.initial_data['email']
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

