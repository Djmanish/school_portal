from rest_framework import serializers
from .models import UserProfile
from .models import User
from django.contrib.auth.hashers import make_password


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model =UserProfile
        fields= '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields= '__all__'
   

   