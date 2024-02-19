from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2.extras

import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("PRIMARY_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI
)

psycopg2.extras.register_uuid()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
