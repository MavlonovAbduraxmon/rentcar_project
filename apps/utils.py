from django.core.cache import cache
from rest_framework import status
from rest_framework.exceptions import ValidationError


def get_login_data(phone):
    return f"login:{phone}"

def send_code(phone:str,code:int,expired_time=60):
    print(f'Phone: {phone} == Code: {code}')
    _phone = get_login_data(phone)
    cache.set(_phone,code)

def check_phone(phone:str, code:int):
    _phone = get_login_data(phone)
    _code = cache.get(_phone)
    if _code is None:
        raise ValidationError('Invalid phone number',status.HTTP_404_NOT_FOUND)
    print(code,_code)
    return _code == code