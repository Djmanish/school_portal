from rest_framework import serializers
from main_app.models import UserProfile
from main_app.models import User
from django.contrib.auth.hashers import make_password
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator






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


