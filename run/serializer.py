from rest_framework import serializers

from .models import CustomUser

class CreateUser(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username','password','first_name','last_name','email']
