from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# For a local thesis prototype, you can use SQLite temporarily if Postgres isn't installed yet, 
# but for the final defense, use the PostgreSQL URI: 
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/ccs_ticketing"

# We will use SQLite here for instant setup so you don't get blocked. 
# You can swap the string to PostgreSQL later with zero code changes to your models!
SQLALCHEMY_DATABASE_URL = "sqlite:///./ccs_ticketing.db"

# 1. Create the Engine (The actual connection to the database)
# check_same_thread=False is strictly for SQLite in FastAPI. Remove it when using Postgres.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 2. Create a Session Local class (This spawns individual database conversations)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create a Base class (All our database models will inherit from this)
Base = declarative_base()

# 4. Dependency function to get the database session in our API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()