from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, AbstractUser
from main_app.models import *
from API_Data.serializers import *

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
    serializer_class = UserProfileSerializer
    def get(self, request):
        user1= UserProfile.objects.all()
        serializer = UserProfileSerializer(user1, many=True)
        return Response(serializer.data)
   

@permission_classes((AllowAny, ))
class UserProfileUpdate(APIView):
    serializer_class = UserProfileSerializer
    
    
        
    def put(self, request, pk):
       
            user = UserProfile.objects.get(id=pk)
            serializer = UserProfileSerializer(instance=user, data=request.data, partial=True) 
            user_first_name=request.POST['first_name']
            user_middle_name=request.POST['middle_name']
            user_last_name=request.POST['last_name']
            user_father_name=request.POST['father_name']
            user_mother_name=request.POST['mother_name']
            user_gender=request.POST['gender']
            user_date_of_birth=request.POST['date_of_birth']
            user_marital_status=request.POST['marital_status']
            user_category=request.POST['category']
            user_qualification=request.POST['qualification']
            user_aadhar_card_number=request.POST['aadhar_card_number']
            user_about=request.POST['about']
            user_profile_pic=""
            if 'profile_pic' in request.POST:
                user_profile_pic=request.FILES['profile_pic']
            user_mobile_number=request.POST['mobile_number']
            user_address_line_1=request.POST['address_line_1']
            user_address_line_2=request.POST['address_line_2']
            user_city=request.POST['city']
            user_pin_code=request.POST['pin_code']
            user_facebook_link=request.POST['facebook_link']
            user_status=request.POST['status']
            user_class_promotion_status=""
            if 'class_promotion_status' in request.POST:
                user_class_promotion_status=request.POST['class_promotion_status']
            user_class_current_year=request.POST['class_current_year']
            user_class_next_year=request.POST['class_next_year']
            user_institute=""
            if 'institute' in request.POST:
                    user_institute=request.POST['institute']
            institute_user=Institute.objects.get(pk=user_institute)
            user_designation=request.POST['designation']
            user_Class=""
            try:
                    if 'Class' in request.POST:
                        user_Class=request.POST['Class']
                    
                    Class_user= Classes.objects.get(pk=user_Class)
            except:
                Class_user=None
            updated_state= State.objects.get(pk=request.POST['state'])
            
           
                    
            user.first_name=user_first_name
            user.middle_name=user_middle_name
            user.last_name=user_last_name
            user.father_name=user_father_name
            user.mother_name=user_mother_name
            user.gender=user_gender
            user.date_of_birth=user_date_of_birth
            user.marital_status=user_marital_status
            user.category=user_category
            user.qualification=user_qualification
            user.aadhar_card_number=user_aadhar_card_number
            user.about=user_about
            user.profile_pic=user_profile_pic
            user.mobile_number=user_mobile_number
            user.address_line_1=user_address_line_1
            user.address_line_2=user_address_line_2
            user.city=user_city
            user.pin_code=user_pin_code
            user.facebook_link=user_facebook_link
            user.status=user_status
            user.class_promotion_status=user_class_promotion_status
            user.class_current_year=user_class_current_year
            user.class_next_year=user_class_next_year
            user.institute=institute_user
            user.Class=Class_user
            user.state=updated_state
            user.save()
                
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class StateViews(APIView):
    serializer_class = StateSerializer
    def get(self, request):
        state= State.objects.all()
        serializer = StateSerializer(state, many=True)
        return Response(serializer.data)


@permission_classes((AllowAny, ))
class InstituteProfileViews(APIView):
    serializer_class = InstituteSerializer
    def get(self, request):
        institute_data= Institute.objects.all()
        serializer = InstituteSerializer(institute_data, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        institute_name=request.POST['name']
        institute_profile_pic=request.FILES['profile_pic']
        institute_code=request.POST['code']
        institute_establish_date=request.POST['establish_date']
        institute_logo=request.POST['institute_logo']
        institute_principal=request.POST['principal']
        institute_session_start_date=request.POST['session_start_date']
        institute_about=request.POST['about']
        institute_contact_number1=request.POST['contact_number1']
        institute_contact_number2=request.POST['contact_number2']
        institute_contact_number3=request.POST['contact_number3']
        institute_address1=request.POST['address1']
        institute_address2=request.POST['address2']
        institute_district=request.POST['district']
        institute_state=request.POST['state']
        institute_country=request.POST['country']
        institute_pin_code=request.POST['pin_code']
        institute_email=request.POST['email']
        institute_facebook_link=request.POST['facebook_link']
        institute_website_link=request.POST['website_link']
       
       
        institute_data.name=institute_name
        institute_data.profile_pic=institute_profile_pic
        institute_data.code=institute_code
        institute_data.establish_date=institute_establish_date
        institute_data.institute_logo=institute_logo
        institute_data.principal=institute_principal
        institute_data.session_start_date=institute_session_start_date
        institute_data.about=institute_about
        institute_data.contact_number1=institute_contact_number1
        institute_data.contact_number2=institute_contact_number2
        institute_data.contact_number3=institute_contact_number3
        institute_data.address1=institute_address1
        institute_data.address2=institute_address2
        institute_data.district=institute_district
        institute_data.state=institute_state
        institute_data.country=institute_country
        institute_data.pin_code=institute_pin_code
        institute_data.email=institute_email
        institute_data.facebook_link=institute_facebook_link
        institute_data.website_link=institute_website_link
     
        
        institute_data.save()
       
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)