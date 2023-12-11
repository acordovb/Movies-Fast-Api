''' Main App To Backedn Movies App '''
from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from jwt_manager import create_tocken, validate_token
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

app = FastAPI()

app.title = "Movies App"
app.version = "0.0.1"
app.description = "APIs para el consumo de Aplicacion de Peliculas"

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    ''' JWT Class to validate Auth '''
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="No tienes acceso para acceder aqui")

class User(BaseModel):
    ''' User Model Base '''
    email: str
    password: str

class Movie(BaseModel):
    ''' Base Model of Movie '''
    id: Optional[int] = None
    title: str = Field(max_length=15, min_length=5)
    overview: str = Field(max_length=50, min_length=15)
    year: int = Field(le=2022)
    rating: float = Field(le=5.0, ge=0.0)
    category: str = Field(max_length=15, min_length=5)

    class Config:
        ''' Config class to Movie Model '''
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Interestelar",
                "overview": "Descripcion de Pelicula",
                "year": 2020,
                "rating": 2.3,
                "category": "Accion"
            }
        }

movies = []


@app.get('/', tags=['home'])
def read_root():
    ''' Hola Mundo Function '''
    return HTMLResponse(
    '''
    <h1>Hola Mundo</h1>
    '''
    )

@app.get('/movies',
         tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    ''' Get All Movies '''
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@app.get('/movies/{id_}', tags=['movies'], response_model=Movie)
def get_movie(id_: int = Path(ge=1, le=2000)) -> Movie:
    ''' get one movie by id '''
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id_).one_or_none()
    if not result:
        return JSONResponse(status_code=404, content={'msg': 'No encontrado'})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    ''' Get Movies by Category or Year '''
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={'msg': 'No se encontro la categoria'})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    ''' Create a Movie '''
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    movies.append(movie.model_dump())
    return JSONResponse(content=movies)

@app.delete('/movies/{id_}', tags=['movies'])
def delete_movie(id_: int):
    ''' Delete a movie by id '''
    db = Session()
    result = db.query( MovieModel ).filter( MovieModel.id == id_ ).one_or_none()
    if not result:
        return JSONResponse( status_code= 404, content={ 'message' : 'No encontrado' })
    db.delete(result)
    db.commit()
    return JSONResponse(content={'msg': 'Se elimino la movie'})

@app.put('/movies/{id_}', tags=['movies'])
def update_movie(id_: int, movie: Movie ) -> dict:
    ''' Update data in movie '''
    db = Session()
    result = db.query( MovieModel ).filter( MovieModel.id == id_ ).one_or_none()
    if not result:
        return JSONResponse( status_code= 404, content={ 'message' : 'No encontrado' })
    movie_to_update = movie.model_dump()
    movie_to_update['id'] = id_
    result.update( **movie_to_update )
    db.commit()
    return JSONResponse( content={"message": "Se ha actualizado la pelicula"})


@app.post('/login', tags=['auth'])
def login(user: User):
    ''' Login with admin '''
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_tocken(user.model_dump())
        return JSONResponse(content=token, status_code=200)
    return JSONResponse("Error en el logueo")
