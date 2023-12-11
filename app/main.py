''' Main App To Backedn Movies App '''
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer
from routers.movie import movie_router
from routers.auth import auth_router

app = FastAPI()

app.title = "Movies App"
app.version = "0.0.1"
app.description = "APIs para el consumo de Aplicacion de Peliculas"

app.add_middleware(ErrorHandler)

app.include_router(
    router=movie_router,
    prefix='/movies',
    tags=['Movies'],
    dependencies=[Depends(JWTBearer())],
)
app.include_router(
    router=auth_router,
    prefix='/login',
    tags=['Auth'],
)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['Home'])
def read_root():
    ''' Hola Mundo Function '''
    return HTMLResponse(
    '''
    <h1>Hola Mundo</h1>
    '''
    )
