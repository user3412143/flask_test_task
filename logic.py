import random
import string
import datetime

def prng(number: int) -> str:
    alphabet = string.ascii_letters
    out = ''
    for i in range(number):
        out += random.choice(alphabet)
    return out



def now_time() -> str:
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%M%S")
