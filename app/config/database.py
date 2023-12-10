''' Config to conect to a database '''
import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLITE_FILE = 'database.sqlite'

base_dir = os.path.dirname(os.path.realpath(__file__))
database_url = f'sqlite:///{os.path.join(base_dir, SQLITE_FILE)}'

engine = create_engine(database_url, echo="True")
Sesion = sessionmaker(bind=engine)
Base = declarative_base()
