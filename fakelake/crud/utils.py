import random
import string


def generate_password(length: int = 12):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.sample(characters, length))
    return password
