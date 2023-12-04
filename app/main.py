''' Main App To Backedn Movies App '''
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

app.title = "Movies App"
app.version = "0.0.1"
app.description = "APIs para el consumo de Aplicacion de Peliculas"

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
                "rating": 2.3,
                "year": 2020,
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

@app.get('/movies', tags=['movies'])
def get_movies():
    ''' Get All Movies '''
    return movies

@app.get('/movies/{id_}', tags=['movies'])
def get_movie(id_: int):
    ''' get one movie by id '''
    for movie in movies:
        if movie.id == id_:
            return movie
    return {}

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    ''' Get Movies by Category or Year '''
    return [movie for movie in movies if movie.category == category]

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies

@app.delete('/movies/{id_}', tags=['movies'])
def delete_movie(id_: int):
    filter_movie = lambda movie : movie.id != id_
    filtered_movies = list(filter(filter_movie, movies))
    movies.clear()
    movies.extend(filtered_movies)
    return movies

@app.put('/movies/{id_}', tags=['movies'])
def update_movie(id_: int, movie: Movie):
    for item in movies:
        if item.id == id_:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
    return movies
