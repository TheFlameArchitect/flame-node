import random
import string

def generate_mirror_id(length=12):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length)) 