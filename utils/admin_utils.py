from hashlib import sha256
from db.db import admin

DEFAULT_PASSWORD = "12345"


def encrypt(password):
    enc = sha256(bytearray(password, 'utf-8'))
    return enc.hexdigest()


def authenticate(password):
    enc = encrypt(password)

    res = admin.find_by_id(enc)

    return True if res else False


def add_admin(password):
    p = {}
    p['id'] = encrypt(DEFAULT_PASSWORD)
    if admin.insert_row(p):
        return True

    return False


def initalize():
    if add_admin(DEFAULT_PASSWORD):
        print("initialized admin")


if __name__ == "__main__":
    initalize()
    print(authenticate(DEFAULT_PASSWORD))
