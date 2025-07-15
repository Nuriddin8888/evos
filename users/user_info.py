import random

def generate_first_name():
    random_numbers = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    first_name = f"user_{random_numbers}"
    return first_name
