from django.http import response
from django.shortcuts import get_object_or_404, render 
import rest_framework
from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.response import Response
from .serializers import UserSerializer 
from .models import User 
from drf_yasg.utils import swagger_auto_schema
# Create your views here.
from drf_yasg import openapi
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserApi(APIView):
    """   
    UserApi  used for the Crud operation of the  user 
    """ 
    def get_object(self,pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            Response({"user":"user not availiable"}) 

    def get(self,request,formate=None):
        """Return list of users"""
        try:
            users = User.objects.all()
            print(users)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except Exception: 
            Response({'Error':'unknown Error'})

    def get(self,request,formate=None,pk=None):
        """Return user by id """
        try:
            if pk is None:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
            else:
                user_object = self.get_object(pk)
                serializer = UserSerializer(user_object)
                return Response(serializer.data)
        except Exception:
              Response({'Error':'unknown Error'})
    
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
        }))   
    def post(self,request,formate=None):
        """create new user"""
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
              Response({'Error':'unknown Error'})

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description='The desc'),
        }))
    def put(self,request,formate=None,pk=None):
        """update user"""
        try:
            user_object = self.get_object(pk)
            serializer = UserSerializer(user_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({'user':'user updated'})
        except Exception:
              Response({'Error':'unknown Error'})

    def delete(self,formate=None,pk=None):
        """delete user"""
        try:
            user_object = self.get_object(pk)
            user_object.delete()
            return Response({'user':'user deleted'})
        except Exception:
              Response({'Error':'unknown Error'}) 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
