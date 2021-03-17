from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django.conf import settings
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import datetime

from .models import CustomUser
from .serializer import CreateUser

from .service import checkuser_id, hashpass, get_user, check_email, generate_otp
from .cache import save_otp, validate_otp

from .JWT_token import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

# Create your views here.


class ping(APIView):
    def get(self,request):
        return Response({'reply': 'pong'},status=status.HTTP_200_OK)


class adduser(APIView):

    def post(self,request):
        newuser = CustomUser()
        new_password = hashpass(request.data['password'])
        serializer = CreateUser(newuser,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            result = get_user(request.data['username'])
            result.password = new_password
            result.save()
            data={"username" : result.username,
            "first_name" : result.first_name,
            "last_name" : result.last_name,
            "email" : result.email,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response({'Add user':'operation failed'},status=status.HTTP_400_BAD_REQUEST)


class getuser(APIView):

    def get(self,request):
        result = checkuser_id(request)
        if result is None:
            return Response({'Result':'User not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            data={"username" : result.username,
            "first_name" : result.first_name,
            "last_name" : result.last_name,
            "email" : result.email,
            }
            return Response(data,status=status.HTTP_200_OK)

class updateuser(APIView):

    def put(self,request):
        result = checkuser_id(request)
        if result is None:
            return Response({'Result': 'User not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CreateUser(result,data=request.data)
            data={}
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data["Success"] = "Update Successful"
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({'Result':'Updation Failed'},status=status.HTTP_304_NOT_MODIFIED)

    def patch(self,request):
        result = checkuser_id(request)
        if result is None:
            return Response({'Result': 'User not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            data = request.data
            result.username = data.get("username",result.username)
            result.password = data.get("password",result.password)
            result.first_name = data.get("first_name",result.first_name)
            result.last_name = data.get("last_name",result.last_name)
            result.email = data.get("email",result.email)
            serializer = CreateUser(result,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)

class deleteuser(APIView):
    
    def delete(self,request):
        result = checkuser_id(request)
        if result is None:
            return Response({'Result': 'User not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            result.is_deleted = True
            result.deleted_at = datetime.datetime.now() # Returns 2018-01-15 09:00
            result.save()
            data = {}
            data["Success"] = "Delete successful"
        return Response(data=data)


class OTPGenerate(APIView):

    def post(self,request):
        result = check_email(request)
        if result is None:
            return Response({'email':'Email doesn''t exists.'},status=status.HTTP_404_NOT_FOUND)
        else:
            user_otp = str(generate_otp())
            save_otp(result.email,user_otp)
            subject = 'OTP'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [result.email, ] 
            send_mail(subject,user_otp,email_from,recipient_list)
            return Response({'OTP':'OTP send to the entered email.'},status=status.HTTP_200_OK)
        return Response({'Result':'Failed'},status=status.HTTP_404_NOT_FOUND)

class OTPValidate(APIView):

    def post(self,request):
        result = check_email(request)
        if result is None:
            return Response({'email':'Email doesnt exist.'},status=status.HTTP_404_NOT_FOUND)
        else:
            email = request.query_params["email"]
            otp = request.data.get('otp')
            if otp is None or otp == '':
                return Response({'Result':'Please enter OTP'},status=status.HTTP_406_NOT_ACCEPTABLE)

            activate = validate_otp(email,otp)
            if activate:
                obj = MyTokenObtainPairSerializer()
                token = obj.get_token(result)
                return Response({'access token':token},status=status.HTTP_200_OK)
            else:
                return Response({'Result':'worng OTP'},status=status.HTTP_406_NOT_ACCEPTABLE)

