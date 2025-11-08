import re
from random import randint

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from redis import Redis
from rest_framework import status
from rest_framework.exceptions import ValidationError


def get_login_data(value):
    return f"login:{value}"


def send_code(data, expired_time=60):
    redis = Redis.from_url(settings.CACHES['default']['LOCATION'])
    _phone = get_login_data(data['value'])
    code = randint(100_000, 999_999)
    _ttl = redis.ttl(f':1:{_phone}')

    if _ttl > 0:
        return False, _ttl

    print(f'{data['type']}: {data['value']} == Code: {code}')
    _data = {
        'code': code,
    }
    cache.set(_phone, _data, expired_time)
    return True, 0


def check_phone(phone: str, code: int):
    _phone = get_login_data(phone['value'])
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

def find_contact_type(phone):
    try:
        validate_email(phone)
        return {'type': 'email', 'value': phone}
    except DjangoValidationError:
        pass

    try:
        normalize_phone(phone)
        return {'type': 'email', 'value': phone}
    except ValidationError:
        pass

