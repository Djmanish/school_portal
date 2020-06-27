from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main_app.models import *
from API_Data.serializers import UserDataSerializer

# Create your views here.
   
authentication_classes=([])
permission_classes=([])
class userData(APIView):
    def get(self, request):
        user1= User.objects.all()
        serializer = UserDataSerializer(user1, many=True)
        return Response(serializer.data)
   
