from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 接続したいDBの基本情報を設定
user_name = "root"
password = "password"
host = "fastapi_tutorial_db"  # docker-composeで定義したMySQLのサービス名
database_name = "main"

DATABASE = {
    'drivername': 'mysql',
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': 'password',
    'database': 'main',
    'query': {'charset':'utf8'}
}

# DBとの接続
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql://root:password@fastapi_tutorial_db/main"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
