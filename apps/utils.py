import re

from django.conf import settings
from django.core.cache import cache
from redis import Redis
from rest_framework import status
from rest_framework.exceptions import ValidationError


def get_login_data(phone):
    return f"login:{phone}"


def send_code(phone: str, code: int, data, expired_time=60):
    redis = Redis.from_url(settings.CACHES['default']['LOCATION'])
    _phone = get_login_data(phone)
    _ttl = redis.ttl(f':1:{_phone}')

    if _ttl > 0:
        return False, _ttl

    print(f'Phone: {phone} == Code: {code}')
    _data = {
        'code':code,
        'first_name':data['first_name'],
        'last_name':data['last_name'],
        'password':data['password']
    }
    cache.set(_phone, _data, expired_time)
    return True, 0


def check_phone(phone: str, code: int):
    _phone = get_login_data(phone)
    _data = cache.get(_phone)
    if _data is None:
        raise ValidationError('Invalid phone number', status.HTTP_404_NOT_FOUND)
    return _data['code'] == code , _data

def normalize_phone(value):
    digits = re.findall(r'\d', value)
    if len(digits) < 9:
        raise ValidationError('Phone number must be at least 9 digits')
    phone = ''.join(digits)
    if len(phone) > 9 and phone.startswith('998'):
        phone = phone.removeprefix('998')
    return phone