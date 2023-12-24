from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Directions
class DirectionsBase(BaseModel):
    name: str
    description: str


class DirectionCreate(DirectionsBase):
    pass


class DirectionUpdate(DirectionsBase):
    name: Optional[str] = None
    description: Optional[str] = None


class Directions(DirectionsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    created_at: datetime
    updated_at: datetime


# Ideas
class QueryBase(BaseModel):
    name: str
    description: str
    initiative_direction: int
    implementation_effect: str


class QueryCreate(QueryBase):
    pass


class QueryUpdate(QueryBase):
    name: Optional[str] = None
    description: Optional[str] = None
    initiative_direction: Optional[int] = None
    implementation_effect: Optional[str] = None

class Query(QueryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
