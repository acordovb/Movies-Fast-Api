''' Routers For Movies '''

from typing import List
from fastapi import Path, Query, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config.database import Session
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('', response_model=List[Movie])
def get_movies() -> List[Movie]:
    ''' Get All Movies '''
    db = Session()
    result = MovieService(db).get_all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/{id_}', response_model=Movie)
def get_movie(id_: int = Path(ge=1, le=2000)) -> Movie:
    ''' get one movie by id '''
    db = Session()
    result = MovieService(db).get_by_id(id_)
    if not result:
        return JSONResponse(status_code=404, content={'msg': 'No encontrado'})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.get('/')
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    ''' Get Movies by Category or Year '''
    db = Session()
    result = MovieService(db).get_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'msg': 'No se encontro la categoria'})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.post('')
def create_movie(movie: Movie):
    ''' Create a Movie '''
    db = Session()
    MovieService(db).create(movie)
    return JSONResponse(content={'msg': 'La pelicula fue agregada'})

@movie_router.delete('/{id_}')
def delete_movie(id_: int):
    ''' Delete a movie by id '''
    db = Session()
    result = MovieService(db).get_by_id(id_)
    if not result:
        return JSONResponse( status_code= 404, content={ 'message' : 'No encontrado' })
    MovieService(db).delete(id_)
    return JSONResponse(content={'msg': 'Se elimino la movie'})

@movie_router.put('/{id_}')
def update_movie(id_: int, movie: Movie ) -> dict:
    ''' Update data in movie '''
    db = Session()
    result = MovieService(db).get_by_id(id_)
    if not result:
        return JSONResponse( status_code= 404, content={ 'message' : 'No encontrado' })
    MovieService(db).update(id_, movie)
    return JSONResponse( content={"message": "Se ha actualizado la pelicula"})
