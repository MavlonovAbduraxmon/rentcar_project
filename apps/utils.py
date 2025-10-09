from random import randint

from django.core.cache import cache


def random_code():
    return randint(100_000, 999_999)  #


def _get_login_key(phone):
    return f"login:{phone}"


def send_sms_code(phone: str, code: int, expire_time=60):
    print(f"[TEST] Phone: {phone} == Sms code: {code}")
    _key = _get_login_key(phone)
    cache.set(_key, code, expire_time)


def check_sms_code(phone, code):
    _key = _get_login_key(phone)
    _code = cache.get(_key)
    print(_code, code)
    return _code == code