import re
from random import randint

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from redis import Redis
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser


def random_code():
    return randint(100_000, 999_999)


def _get_login_key(phone):
    return f"login:{phone}"


def send_code(phone: str, code: int, expire_time=60):
    redis = Redis.from_url(settings.CACHES['default']['LOCATION'])
    _key = _get_login_key(phone)
    _ttl = redis.ttl(f':1:{_key}')
    if _ttl > 0:
        return False, _ttl
    print(f"[TEST] Phone: {phone} == Sms code: {code}")
    cache.set(_key, code, expire_time)
    return True, 0


def check_phone(phone: str, code: int):
    _key = _get_login_key(phone)
    _code = cache.get(_key)
    print(_code, code)
    return _code == code

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