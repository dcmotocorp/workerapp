from django.db import models
from django.db.models import fields
from .models import User
from rest_framework import serializers

""" basically this serializers used to converts the objects
    into  json objects """

class UserSerializer(serializers.ModelSerializer):
    """ user model field serializer """
    class Meta:
        model = User
        fields=('id', 'username', 'password', 'phone_number', 'address')
