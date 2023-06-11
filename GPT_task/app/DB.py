from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .api.core.config import DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT

POSTGRESQL_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(POSTGRESQL_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base = declarative_base()
