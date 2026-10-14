from fastapi import APIRouter, HTTPException, status, Depends, Query
from db.database import get_db
from services.requests import RequestsService, NotFound, ConflictError
from DTOs import CreateRequest, ReadRequest, RequestPage
from typing import Literal

router = APIRouter(prefix="/requests",tags=["Requests"])
request_service = RequestsService()

@router.get("", response_model=RequestPage)
# PAGINATION CODE CHANGE
def list_requests(
	page: int = Query(default=1, ge=1),
	page_size: int = Query(default=10, ge=10, le=50),
	status_filter: str | None = Query(default=None, alias="status"),
	sort_by: Literal["id", "status"] = "id",
	order: Literal["asc", "desc"] = "asc",
	db_session = Depends(get_db)):
	return request_service.get_all(
		page = page, 
		page_size = page_size,
		status_filter = status_filter,
		sort_by = sort_by,
		order = order,
		db_session = db_session)

@router.get("/{id}", response_model=ReadRequest)
def get_request_by_id(id: int, db_session=Depends(get_db)):
	return request_service.get(id, db_session)

@router.put("/{id}", response_model=ReadRequest)
def edit(id: int, request: ReadRequest, db_session=Depends(get_db)):
	return request_service.update(id, request, db_session)

@router.post("",response_model=ReadRequest,status_code=status.HTTP_201_CREATED)
def create(data: CreateRequest, db_session=Depends(get_db)):
	return request_service.create(data, db_session)

@router.delete("/{id}", response_model=str, status_code=status.HTTP_200_OK)
def delete(id: int, db_session=Depends(get_db)):
	request_service.delete(id, db_session)
	return "Successfully deleted the request entry."
