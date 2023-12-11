''' Movie Class '''

from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):
    ''' Movie Class '''
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)

    def update( self, id_, **kwargs ):
        ''' Update movie '''
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        setattr(self, 'id', id_)
