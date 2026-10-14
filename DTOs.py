from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone

class CreateRequest(BaseModel):
	model_config = ConfigDict(from_attributes=True) #from_attributes allows Pydantic to read from the SQLalchemy object 

	id: int
	title: str
	createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
	description: str
	status: str
	createdBy: str

class ReadRequest(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	title: str
	createdAt: datetime
	description: str
	status: str

class CreateUser(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	name: str
	age: int

#Currently fetching users from the DB is not needed.

#The RequestPage model will assist with pagination and related details
class RequestPage(BaseModel):
	items: list[ReadRequest]
	total: int
	page: int
	page_size: int
	total_pages: int