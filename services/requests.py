from DTOs import CreateRequest, ReadRequest, RequestPage
from exceptions import NotFound, ConflictError, RequestNotFound
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from db.dbModels import Request
from datetime import datetime, timezone
from services.queryService import apply_sort, apply_filter

class RequestsService:
    def get_all(
        self, 
        page: int, 
        page_size: int, 
        db_session: Session, 
        status_filter: str | None = None, 
        sort_by: str = "id",
        order: str = "asc"
        ) -> RequestPage:

        filtered_query = apply_filter(
            query = select(Request), 
            filters = {"status": status_filter}, 
            allowed_fields = {"status": Request.status}
        )

        total = db_session.scalar(select(func.count()).select_from(filtered_query.subquery())) or 0

        # LOGIC NEEDS FIXING
        query = apply_sort(
            query = filtered_query,
            sort_by = sort_by,
            order = order,
            allowed_fields = {"id": Request.id, "status": Request.status},
            tie_braker=Request.id)

        #Компенсира с бройката за съответната страница
        offset = (page - 1) * page_size

        query = (query
            .offset(offset) #прилага компенсацията и казва SQLalchemy да вземе от offset нататък + limit за ограничаване на броя
            .limit(page_size)
        )
        
        requests = db_session.scalars(query).all()
        # FORGOT TO REFACTOR
        return RequestPage(
            items = requests,
            total = total,
            page = page,
            page_size = page_size,
            total_pages = (total + page_size - 1) // page_size
        )


    def get(self, request_id: int, db_session: Session) -> Request:
        request = db_session.get(Request, request_id)
        if request is None:
            raise RequestNotFound(f"No request with ID {request_id} found.")
        return request


    def create(self, data: CreateRequest, db_session: Session) -> Request:
        request = Request(
            title=data.title,
            description=data.description,
            createdAt=datetime.now(timezone.utc),
            createdBy="user",
            status="pending",
        )
        try:
            db_session.add(request)
            db_session.commit()
        except Exception:
            db_session.rollback()
            raise
        db_session.refresh(request)
        return request


    def update(self, request_id: int, data: CreateRequest, db_session: Session) -> Request:
        request = self.get(request_id, db_session)
        request.title = data.title
        request.description = data.description
        request.status = data.status
        try:
            db_session.commit()
        except Exception:
            db_session.rollback()
            raise ConflictError("An error occurred while updating the request entity.")
        db_session.refresh(request)
        return request


    def delete(self, request_id: int, db_session: Session) -> int:
        request = self.get(request_id, db_session)
        if request is None:
            raise ConflictError(f"No request with ID {request_id} was found.")
        try:
            db_session.delete(request)
            db_session.commit()
        except Exception:
            db_session.rollback()
            raise ConflictError("An error occurred while deleting the request entity.")
        finally:
            db_session.close()
