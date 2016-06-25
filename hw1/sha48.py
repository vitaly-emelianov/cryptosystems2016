from hashlib import sha256


def sha48(data, byte_number=6):
    m = sha256()
    m.update(data.encode('utf-8'))
    return m.hexdigest()[:byte_number*2]
