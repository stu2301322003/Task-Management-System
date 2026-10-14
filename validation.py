from pydantic import BaseModel, Field, field_validator, ValidationError
from enum import Enum
from datetime import datetime

class User(BaseModel):
	id: int
	name: str
	age: int

class Request(BaseModel):
	id: int
	title: str
	description: str
	createdAt: datetime
	status: str
	createdBy: str

class Role(str, Enum):
	admin="admin"
	user="user"

class Account(BaseModel):
	username: str = Field(min_length=3, max_length=30)
	age: int = Field(ge=16)
	role: Role
