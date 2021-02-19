from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import datetime

from .models import CustomUser
from .serializer import CreateUser
# Create your views here.


def checkuser(request):
    try:
        id = request.query_params["id"]
        result = CustomUser.objects.get(id=id)
        if result.is_deleted:
            result = None
            return result
        else:
            return result
    except:
        result = None
        return result


class ping(APIView):
    def get(self,request):
        return Response({'reply': 'pong'},status=status.HTTP_200_OK)


class adduser(APIView):

    def post(self,request):
        newuser = CustomUser()
        if request.method == 'POST':
            serializer = CreateUser(newuser,data=request.data)
            #data = {}
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'Add user':'operation failed'},status=status.HTTP_400_BAD_REQUEST)


class getuser(APIView):

    def get(self,request):
        result = checkuser(request)
        if result is None:
            return Response({'Result':'User not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            if request.method == 'GET':
                serializer = CreateUser(result)
                data={}
                data["username"] = result.username
                data["first_name"] = result.first_name
                data["last_name"] = result.last_name
                data["email"] = result.email
                return Response(data=data,status=status.HTTP_200_OK)

class updateuser(APIView):

    def put(self,request):
        result = checkuser(request)
        if result is None:
            return Response({'Result': 'User not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            if request.method == 'PUT':
                serializer = CreateUser(result,data=request.data)
                data={}
                if serializer.is_valid():
                    serializer.save()
                    data["Success"] = "Update Successful"
                    return Response(serializer.data,status=status.HTTP_200_OK)
                return Response({'Result':'Updation Failed'},status=status.HTTP_304_NOT_MODIFIED)

    def patch(self,request):
        result = checkuser(request)
        if result is None:
            return Response({'Result': 'User not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            if request.method == 'PATCH':
                data = request.data
                result.username = data.get("username",result.username)
                result.passsword = data.get("password",result.password)
                result.first_name = data.get("first_name",result.first_name)
                result.last_name = data.get("last_name",result.last_name)
                result.email = data.get("email",result.email)
                result.save()
                serializer = CreateUser(result)
                return Response(serializer.data,status=status.HTTP_200_OK)

class deleteuser(APIView):
    
    def delete(self,request):
        result = checkuser(request)
        if result is None:
            return Response({'Result': 'User not found'},status=status.HTTP_404_NOT_FOUND)
        else:
            if request.method == 'DELETE':
                result.is_deleted = 'True'
                result.deleted_at = datetime.datetime.now() # Returns 2018-01-15 09:00
                result.save()
                data = {}
                data["Success"] = "Delete successful"
            else:        
                data["Failed"] = "Delete failed"
            return Response(data=data)
