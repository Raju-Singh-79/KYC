import string

from Crypto.Random import random


def generate_otp():
    return ''.join(random.choice(string.digits) for i in range(6))


def generate_verification_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))
