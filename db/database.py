from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

DATABASE_URL=os.getenv("DATABASE_URL") or "sqlite:///./ticketSystem.db"

engine = create_engine(url=DATABASE_URL, echo=True)
SessionLocal=sessionmaker(bind=engine)

def get_db():
	session=SessionLocal()
	try:
		yield session
	finally:
		session.close()
