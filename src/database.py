from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import config

# Setup a database connection with SQLAlchemy
params = config()
DATABASE_URL = \
    f"postgres://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
