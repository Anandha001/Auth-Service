from configs.base_config import BaseConfig
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, Session


engine = create_engine(BaseConfig.DB_URI, poolclass=NullPool)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db: Session = SessionLocal(bind=engine)
    try:
        yield db
    finally:
        db.close()
