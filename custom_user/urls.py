"""custom_user URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from run import views 
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ping/',views.ping.as_view()),
    path('adduser/',views.adduser.as_view()),
    path('getuser/',views.getuser.as_view()),
    path('updateuser/',views.updateuser.as_view()),
    path('deleteuser/',views.deleteuser.as_view()),
    path('otp/',views.OTPGenerate.as_view()),
    path('otp_verify/',views.OTPValidate.as_view()),
]
