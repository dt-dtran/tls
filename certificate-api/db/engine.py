from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("PRIMARY_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
