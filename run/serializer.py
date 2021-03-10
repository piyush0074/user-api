from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import CustomUser

from .service import check_user_email, password_check

class CreateUser(serializers.ModelSerializer):

    username = serializers.CharField(max_length=15)
    password = serializers.CharField()
    first_name = serializers.CharField(max_length=15)
    last_name = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    class Meta:
        model = CustomUser
        fields = ['username','password','first_name','last_name','email']

    def create(self,validate_data):
        return CustomUser.objects.create(**validate_data)

    def validate(self,data):
        user_name = data.get('username')
        fname = data.get('first_name')
        lname = data.get('last_name')
        email = data.get('email')
        user_password = data.get('password')
        result = check_user_email(user_name,email)
        if len(result) == 2:
            raise serializers.ValidationError("Username is already taken and email is already exists.")
        else:
            if result == 'u' :
                raise serializers.ValidationError("Username is already taken")
        
        password_flag = password_check(user_password)
        
        if (not password_flag):
            raise serializers.ValidationError("Your password must contain upper case, lower case and"+ 
            "number. Your password length should be greater than 6 characters and less than 16 characters. ")

        if len(fname) <= 2 or len(fname) > 15:
            raise serializers.ValidationError("First name length should be greater than 2 and less than 15 characters.")
        
        if len(lname) <= 2 or len(lname) > 15:
            raise serializers.ValidationError("Last name length should be greater than 2 and less than 15 characters.")

        return data