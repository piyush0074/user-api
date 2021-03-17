from .models import CustomUser
import crypt

import random


def checkuser_id(request):
    try:
        id = request.query_params["id"]
        result = CustomUser.objects.get(id=id,is_deleted=False)
        return result
    except:
        result = None
        return result

def check_user_email(user_name,user_email):
    flag = ''
    try:
        result = CustomUser.objects.get(username=user_name,is_deleted=False)
        if result.username == user_name :
            flag = 'u'
        if result.email == user_email :
            flag = flag+'e'
        return flag
    except:
        return flag

def password_check(password):
    num = False
    upper = False
    lower = False
    if (len(password) <=5 or len(password) >17 ): return False

    for char in range (0,len(password)):
        if ( num  and upper and lower ): return True
        if (not(num) and password[char].isdigit()): 
            num = True
            continue
        if (not(lower) and password[char].islower()):
            lower = True
            continue
        if (not(upper) and password[char].isupper()):
            upper = True
            continue
    return False

def hashpass(plaintext):
    hash = crypt.crypt(plaintext)
    return hash

def get_user(request):
    result = CustomUser.objects.get(username=request)
    return result

def check_email(request):
    try:
        email = request.query_params["email"]
        result = CustomUser.objects.get(email=email,is_deleted=False)
        return result
    except:
        result = None
        return result

def generate_otp():
    otp = random.randint(100000,999999)
    return otp