from collections.abc import Mapping
from typing import Any
from sqlalchemy import Select
from sqlalchemy.orm import InstrumentedAttribute
from exceptions import AppError

def apply_filter(query: Select, filters: Mapping[str, Any], allowed_fields: Mapping[str, InstrumentedAttribute]) -> Select:
    for field, value in filters.items():
        if field not in allowed_fields:
            raise AppError(f"Filtering by {field} is not allowed.")

        if value is None:
            continue
        
        column = allowed_fields[field]
        query = query.where(column == value)

    return query

def apply_sort(
    query: Select, 
    sort_by: str, 
    order: str, 
    allowed_fields: Mapping[str, InstrumentedAttribute], 
    tie_braker: InstrumentedAttribute) -> Select:
    if sort_by not in allowed_fields:
        raise AppError(f"Sorting by {sort_by} is not allowed.")
    # ALL SORTS OF ORDERS
    if order not in {"asc", "desc"}:
        order = "asc"

    column = allowed_fields[sort_by]
    expression = column.desc() if order == "desc" else column.asc()

    query = query.order_by(expression)

    if column is not tie_braker:
        query = query.order_by(tie_braker.asc())

    return query

