from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, AbstractUser
from main_app.models import *
from API_Data.serializers import UserDataSerializer, RegistrationSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, LoginSerializer,UserProfileSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

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
            if not user.is_active:
                user.is_active = True
                user.save()
                
            return HttpResponseRedirect(f'complete/')

            # return redirect( 'http://trueblueappworks.com/accounts/activate/complete/')
            # return Response({'email':'Successfully activated!'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Expired!'},status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny, ))
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site=get_current_site(request=request).domain
                relativeLink=reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
                
                absurl='http://'+current_site+relativeLink
                email_body='Hi\n' +user.username+"\nUse Link below to verify your email\n"+absurl
                data={'email_body':email_body,'to_email':user.email,'email_subject':'Password Reset'}

                Util.send_email(data)
        return Response({'success':'We have sent you a link to reset your password'},status=status.HTTP_200_OK)
        


@permission_classes((AllowAny, ))
class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                 return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success':True, 'message':'Credentials Valid', 'uidb64':uidb64, 'token':token},status = status.HTTP_200_OK)

        
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                 return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)



@permission_classes((AllowAny, ))
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':'Password reset successful'}, status = status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer= self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


        

@permission_classes((AllowAny, ))
class UserProfileViews(APIView):
    def get(self, request):
        user1= UserProfile.objects.all()
        serializer = UserProfileSerializer(user1, many=True)
        return Response(serializer.data)
    def post(self):
        pass