from rest_framework import serializers
from .models import UserProfile
from .models import User
from django.contrib.auth.hashers import make_password


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model =UserProfile
        fields= '__all__'

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            instance.user.password = make_password(
                validated_data.get('user').get('password', instance.user.password)
            )
            instance.user.save()
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
    
    validate_password = make_password
        # extra_kwargs = {'password': {'write_only': True}}