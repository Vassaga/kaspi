import random

class IBAN_Generator:
    def generate_16_digit_number(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(16)])
    
