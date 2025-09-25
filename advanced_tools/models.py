from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)

# SQLite for testing
engine = create_engine("sqlite:///./test.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
from models import SessionLocal, User

session = SessionLocal()
users = session.query(User).all()
for u in users:
    print(u.id, u.username, u.email, u.phone)
session.close()

import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users;")
print(cursor.fetchall())
conn.close()
# Create tables
Base.metadata.create_all(bind=engine)