''' Routers For Movies '''

from typing import Optional, List
from fastapi import Depends, Path, Query, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from config.database import Session
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()

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

@movie_router.get('/movies',
         tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    ''' Get All Movies '''
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/movies/{id_}', tags=['movies'], response_model=Movie)
def get_movie(id_: int = Path(ge=1, le=2000)) -> Movie:
    ''' get one movie by id '''
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id_).one_or_none()
    if not result:
        return JSONResponse(status_code=404, content={'msg': 'No encontrado'})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    ''' Get Movies by Category or Year '''
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={'msg': 'No se encontro la categoria'})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    ''' Create a Movie '''
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={'msg': 'La pelicula fue agregada'})

@movie_router.delete('/movies/{id_}', tags=['movies'])
def delete_movie(id_: int):
    ''' Delete a movie by id '''
    db = Session()
    result = db.query( MovieModel ).filter( MovieModel.id == id_ ).one_or_none()
    if not result:
        return JSONResponse( status_code= 404, content={ 'message' : 'No encontrado' })
    db.delete(result)
    db.commit()
    return JSONResponse(content={'msg': 'Se elimino la movie'})

@movie_router.put('/movies/{id_}', tags=['movies'])
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
