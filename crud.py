from __future__ import annotations

from sqlalchemy.orm import Session

import schemas
from models import Directions, Query


# Directions
def create_direction(db: Session, schema: schemas.DirectionCreate):
    db_directions = Directions(**schema.model_dump())
    db.add(db_directions)
    db.commit()
    db.refresh(db_directions)
    return db_directions


def get_directions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Directions).offset(skip).limit(limit).all()


def get_direction(db: Session, direction_id: int):
    return db.query(Directions).filter_by(id=direction_id).first()


def update_direction(db: Session, direction_id: int, direction_data: schemas.DirectionUpdate | dict):
    db_direction = db.query(Directions).filter_by(id=direction_id).first()

    direction_data = direction_data if isinstance(direction_data, dict) else direction_data.model_dump()

    if db_direction:
        for key, value in direction_data.items():
            if hasattr(db_direction, key):
                setattr(db_direction, key, value)

        db.commit()
        db.refresh(db_direction)

    return db_direction


def delete_direction(db: Session, direction_id: int):
    db_direction = db.query(Directions).filter_by(id=direction_id).first()
    if db_direction:
        db.delete(db_direction)
        db.commit()
        return True
    return False


# Ideas
def create_query(db: Session, schema: schemas.QueryCreate):
    db_query = Query(**schema.model_dump())
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query


def get_queries(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Query).offset(skip).limit(limit).all()


def get_query(db: Session, query_id: int):
    return db.query(Query).filter_by(id=query_id).first()


def update_query(db: Session, query_id: int, query_data: schemas.QueryUpdate | dict):
    db_item = db.query(Query).filter_by(id=query_id).first()

    query_data = query_data if isinstance(query_data, dict) else query_data.model_dump()

    if db_item:
        for key, value in query_data.items():
            if hasattr(db_item, key):
                setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        return db_item
    return None


def delete_query(db: Session, query_id: int):
    db_query = db.query(Query).filter_by(id=query_id).first()
    if db_query:
        db.delete(db_query)
        db.commit()
        return True
    return False
