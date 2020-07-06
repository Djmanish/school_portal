from rest_framework import viewsets
from main_app.models import User
from . import serializers
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny

@permission_classes((AllowAny, ))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserDataSerializer