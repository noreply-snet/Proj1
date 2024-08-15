from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base

URL_DATABASE = "sqlite:///./sql_app.db"

engine = create_engine(
    URL_DATABASE, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
    )


Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()