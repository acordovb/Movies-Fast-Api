''' Tocken Auth Module '''
from jwt import encode, decode

def create_tocken(data: dict) -> str:
    ''' Create Token '''
    token: str = encode(payload=data, key='my_secrete_key', algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    ''' Validate Token '''
    data: dict = decode(token, key='my_secrete_key', algorithms=["HS256"])
    return data
