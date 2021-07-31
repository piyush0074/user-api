from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        data = {}
        token = super().get_token(user)
        token['username'] = user.username
        data['refresh'] = str(token)
        data['access'] = str(token.access_token)
        return data
