import random
import string
import uuid


def get_uuid():
    return uuid.uuid4().hex


def gen_short_id():
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(8)])
