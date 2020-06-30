from rest_framework import serializers
from main_app.models import UserProfile
from main_app.models import User
from django.contrib.auth.hashers import make_password



class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields= '__all__'