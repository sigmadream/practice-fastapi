from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# from config import get_settings
# settings = get_settings()
# SQLALCHEMY_DATABASE_URL = (
#     "mysql+mysqldb://"
#     f"{settings.database_username}:{settings.database_password}"
#     "@127.0.0.1/fastapi-ca"
# )
# SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:qwer1234@127.0.0.1/fastapi-ca"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
