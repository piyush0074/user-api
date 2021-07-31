from .models import CustomUser, ConnectedUser
import crypt

import random


def checkuser_id(request):
    try:
        id = request.query_params["id"]
        print('aa')
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

def checkusername(name):
    try:
        result = CustomUser.objects.get(username=name,is_deleted=False)
        return result
    except:
        result = None
        return result

def check_connection(user1,user2):
    try:
        result = ConnectedUser.objects.get(username=user1,people__contains=[user2])
        return True
    except:
        return False

def connect_people(user1,user2):
    person1 = ConnectedUser.objects.get(username=user1.username)
    person1.people.append(user2.username)
    person1.save()
    person2 = ConnectedUser.objects.get(username=user2.username)
    person2.people.append(user1.username)
    person2.save()
    id = [person1.id,person2.id]
    return id

def check_id(request):
    try:
        id = request.GET.get('id')
        result = CustomUser.objects.get(id=id)
        return result
    except:
        result = None
        return result