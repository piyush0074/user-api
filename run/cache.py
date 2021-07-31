from django.core.cache import cache
from django.conf import settings


def save_otp(key,value):
    cache.set(key,value,600)

def validate_otp(key,value):
    otp = cache.get(key)
    if otp is None: return False

    else:
        if(otp == value):
                cache.delete(key)
                return True
        else: return False