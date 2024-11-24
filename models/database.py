from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# db_url = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
db_url = "postgresql://postgres:admin@localhost:5432/postgres"

engine = create_engine(db_url)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=True,
)

Base = declarative_base()


def of_get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
