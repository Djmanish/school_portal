from rest_framework import serializers
from main_app.models import UserProfile
from main_app.models import User
from django.contrib.auth.hashers import make_password



class UserDataSerializer(serializers.ModelSerializer):
   
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
        fields = ['id','email', 'username', 'password']
    
    # validate_password = make_passwords
    extra_kwargs = {'password': {'write_only': True}}