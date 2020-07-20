from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, AbstractUser
from API_Data.serializers import UserDataSerializer, RegistrationSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings

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

@api_view(['POST',])

def registration_view(request):
    if request.method=="POST":
        serializer = RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save()
            data['response']="Successfully Registered a new account!"
            data['email']=account.email
            data['username']=account.username
        else:
            data = serializer.errors
        return Response(data)
@permission_classes((AllowAny, ))
class RegisterView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        user= request.data
        serializer= self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        user= User.objects.get(email=user_data['email'])

        

        token =RefreshToken.for_user(user).access_token
        current_site=get_current_site(request).domain
        relativeLink=reverse('email-verify')
        
        absurl='http://'+current_site+relativeLink+"?token="+str(token)
        email_body='Hi\n' +user.username+"\nUse Link below to verify your email\n"+absurl
        data={'email_body':email_body,'to_email':user.email,'email_subject':'Verify Your Email'}

        Util.send_email(data)
        
        return Response(user_data)
@permission_classes((AllowAny, ))
class VerifyEmail(generics.GenericAPIView):
    def get(self,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user= User.objects.get(id=payload['user_id'])
            if not user.is_staff:
                user.is_staff = True
                user.save()

            return Response({'email':'Successfully activated!'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Expired!'},status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)