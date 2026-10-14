from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base (DeclarativeBase):
	pass

class Request(Base):
	__tablename__="requests"

	id: Mapped[int] = mapped_column(primary_key=True)
	title: Mapped[str]
	createdAt: Mapped[datetime]
	description: Mapped[str]
	status: Mapped[str]
	createdBy: Mapped[str]

class User(Base):
	__tablename__="users"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str]
	age: Mapped[int]
	

