''' JWT Bearer Auth '''
from jwt_manager import validate_token
from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request

class JWTBearer(HTTPBearer):
    ''' JWT Class to validate Auth '''
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="No tienes acceso para acceder aqui")
