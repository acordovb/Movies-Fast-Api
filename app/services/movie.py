''' Service to Consult data of Movies '''

from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService():
    ''' Movie service to manage Movie Data '''
    def __init__(self, db) -> None:
        self.db = db

    def get_all(self):
        ''' Get All Movies From Movie Table '''
        result = self.db.query(MovieModel).all()
        return result

    def get_by_id(self, id_):
        ''' Get Movie by id '''
        result = self.db.query(MovieModel).filter(MovieModel.id == id_).one_or_none()
        return result

    def get_by_category(self, category):
        ''' Get Movie by category '''
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result

    def create(self, movie: Movie):
        ''' Create Movie '''
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()

    def update(self, id_, movie):
        ''' Update Movie '''
        movie_ = self.get_by_id(id_)
        new_movie = movie.model_dump()
        movie_.update(id_, **new_movie )
        self.db.commit()

    def delete(self, id_):
        ''' Delete Movie '''
        movie_ = self.get_by_id(id_)
        self.db.delete(movie_)
        self.db.commit()
