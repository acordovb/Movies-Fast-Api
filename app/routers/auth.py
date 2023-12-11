''' Auth Router to Login '''

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from jwt_manager import create_tocken
from schemas.user import User

auth_router = APIRouter()

@auth_router.post('')
def login(user: User):
    ''' Login with admin '''
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_tocken(user.model_dump())
        return JSONResponse(content=token, status_code=200)
    return JSONResponse("Error en el logueo")
