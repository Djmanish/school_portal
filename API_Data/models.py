from django.db import models
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def tokens(self):
    refresh=RefreshToken.for_user(self)
    return{
            'refresh':str(refresh),
            'access':str(refresh.access_token),
        }
    
    User.add_to_class("tokens",tokens)

