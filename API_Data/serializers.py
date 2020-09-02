from rest_framework import serializers
from main_app.models import *
from main_app.models import User
from django.contrib.auth.hashers import make_password
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed






class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields= '__all__'
        
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User 
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}

        }

    def save(self):
        account = User(
            email = self.validated_data['email'],
            username=self.validated_data['username']
           

        )
        password=self.validated_data['password']
        password2 = self.validated_data['password2']
        if password!= password2:
            raise serializers.ValidationError({'password':'Password must match'})
        account.set_password(password)
        account.is_active=False
        account.save()
        return account


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields=['email']

    def validate(self, attrs):
        import pdb
        pdb.set_trace()
        try:
            email = attrs['data'].get('email', '')
          
            return attrs

        except expression as identifier:
            pass
        return super().validate(attrs)

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length= 68, write_only=True)

    token = serializers.CharField(min_length=1,  write_only=True)
    uidb64 = serializers.CharField(min_length=1,  write_only=True)

    class Meta:
        fields=['password','token','uidb64']

        def validate(self, attrs):
            try:
                password = attrs.get('password')
                token = attrs.get('token')
                uidb64 = attrs.get('uidb64')

                id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    raise AuthenticationFailed('The reset link is invalid',401)
                user.set_password(password)
                user.save()
                return(user)
            except expression as identifier:
                raise AuthenticationFailed('The reset link is invalid',401)

            return super().validate(attrs)

class EmailVerificationSerializer(serializers.ModelSerializer):
        token = serializers.CharField(max_length=555)

        class Meta:
            model = User
            fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password','')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('No User Found')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        

        return{
            'email':user.email,
            'username':user.username,
            'tokens':user.token,
        
        }
        return super().validate(attrs)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =UserProfile
        fields= '__all__'
  



class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields='__all__'

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Institute
        fields='__all__'