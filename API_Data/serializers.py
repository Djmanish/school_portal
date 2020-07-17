from rest_framework import serializers
from main_app.models import UserProfile
from main_app.models import User
from django.contrib.auth.hashers import make_password



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
        account.save()
        return account