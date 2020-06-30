from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main_app.models import *
from API_Data.serializers import UserDataSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny

# Create your views here.
@permission_classes((AllowAny, ))
class userData(APIView):
    def get(self, request):
        user1= User.objects.all()
        serializer = UserDataSerializer(user1, many=True)
        return Response(serializer.data)
   
