from jwt import encode

def create_tocken(data: dict):
    token: str = encode(payload=data, key='my_secrete_key', algorithm="HS256")
    return token
