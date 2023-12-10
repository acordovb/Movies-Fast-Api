''' Main App To Backedn Movies App '''
from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from jwt_manager import create_tocken, validate_token

app = FastAPI()

app.title = "Movies App"
app.version = "0.0.1"
app.description = "APIs para el consumo de Aplicacion de Peliculas"


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
    id: Optional[int]
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

@app.get(
        '/movies',
        tags=['movies'],
        response_model=List[Movie],
        status_code=200,
        dependencies=[Depends(JWTBearer())])
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
    ''' Create a Movie '''
    movies.append(movie.model_dump())
    return JSONResponse(content=movies)

@app.delete('/movies/{id_}', tags=['movies'])
def delete_movie(id_: int):
    ''' Delete a movie by id '''
    filtered_movies = list(filter(lambda movie : movie.id != id_, movies))
    movies.clear()
    movies.extend(filtered_movies)
    return JSONResponse(content=movies)

@app.put('/movies/{id_}', tags=['movies'])
def update_movie(id_: int, movie: Movie):
    ''' Update data in movie '''
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
    ''' Login with admin '''
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_tocken(user.model_dump())
        return JSONResponse(content=token, status_code=200)
        # return validate_token(token)
    return JSONResponse("Error en el logueo")
