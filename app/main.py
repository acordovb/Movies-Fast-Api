''' Main App To Backedn Movies App '''
from typing import Optional, List
from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from jwt_manager import create_tocken

app = FastAPI()

app.title = "Movies App"
app.version = "0.0.1"
app.description = "APIs para el consumo de Aplicacion de Peliculas"


class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int]
    title: str = Field(max_length=15, min_length=5)
    overview: str = Field(max_length=50, min_length=15)
    year: int = Field(le=2022)
    rating: float = Field(le=5.0, ge=0.0)
    category: str = Field(max_length=15, min_length=5)

    class Config:
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

@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    ''' Get All Movies '''
    return JSONResponse(content=movies)

@app.get('/movies/{id_}', tags=['movies'], response_model=Movie)
def get_movie(id_: int = Path(ge=1, le=2000)) -> Movie:
    ''' get one movie by id '''
    for movie in movies:
        if movie.id == id_:
            return JSONResponse(content=movie)
    return JSONResponse(content={})

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    ''' Get Movies by Category or Year '''
    return JSONResponse(content=[movie for movie in movies if movie.category == category])

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie.model_dump())
    return JSONResponse(content=movies)

@app.delete('/movies/{id_}', tags=['movies'])
def delete_movie(id_: int):
    filter_movie = lambda movie : movie.id != id_
    filtered_movies = list(filter(filter_movie, movies))
    movies.clear()
    movies.extend(filtered_movies)
    return JSONResponse(content=movies)

@app.put('/movies/{id_}', tags=['movies'])
def update_movie(id_: int, movie: Movie):
    for item in movies:
        if item.id == id_:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
    return JSONResponse(content=movies)


@app.post('/login', tags=['auth'])
def login(user: User):
    return user