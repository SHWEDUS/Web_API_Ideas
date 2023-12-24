from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

import schemas
from database import get_db
from sqlalchemy.orm import Session
from crud import (
    create_direction, get_directions, get_direction, update_direction, delete_direction,
    create_query, get_queries, get_query, update_query, delete_query
)

router_websocket = APIRouter()
router_directions = APIRouter(prefix='/directions', tags=['direction'])
router_queries = APIRouter(prefix='/queries', tags=['queries'])


# WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


async def notify_clients(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)


@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Пользователь #{client_id} Зашёл на сайт")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Вы создали идею: {data}", websocket)
            await manager.broadcast(f"Пользователь #{client_id} создал идею: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Пользователь #{client_id} ушёл с сайта")


# Направления
@router_directions.post("/", response_model=schemas.Directions)
async def create_direction_route(direction_data: schemas.DirectionCreate, db: Session = Depends(get_db)):
    direction = create_direction(db, direction_data)
    await notify_clients(f"Напрвление добавлено: {direction.name}")
    return direction


@router_directions.get("/", response_model=List[schemas.Directions])
async def read_directions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    directions = get_directions(db, skip=skip, limit=limit)
    return directions


@router_directions.get("/{direction_id}", response_model=schemas.Directions)
async def read_direction(direction_id: int, db: Session = Depends(get_db)):
    direction = get_direction(db, direction_id)
    return direction


@router_directions.patch("/{direction_id}", response_model=schemas.Directions)
async def update_direction_route(direction_id: int, direction_data: schemas.DirectionUpdate, db: Session = Depends(get_db)):
    updated_direction = update_direction(db, direction_id, direction_data)
    if updated_direction:
        await notify_clients(f"Направление обновлено: {updated_direction.name}")
        return updated_direction
    return {"message": "Направление не найдено!"}


@router_directions.delete("/{direction_id}")
async def delete_direction_route(direction_id: int, db: Session = Depends(get_db)):
    deleted = delete_direction(db, direction_id)
    if deleted:
        await notify_clients(f"Направление удалено: ID {direction_id}")
        return {"message": "Направление удалено"}
    return {"message": "Направление не найдено!"}


# Инициативы
@router_queries.post("/", response_model=schemas.Query)
async def create_query_route(schema: schemas.QueryCreate, db: Session = Depends(get_db)):
    query = create_query(db, schema)
    await notify_clients(f"Инициатива под именем '{query.name}' успешно зарегистрированна!")
    return query


@router_queries.get("/", response_model=List[schemas.Query])
async def read_queries(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    queries = get_queries(db, skip=skip, limit=limit)
    return queries


@router_queries.get("/{query_id}", response_model=schemas.Query)
async def read_query(query_id: int, db: Session = Depends(get_db)):
    query = get_query(db, query_id)
    return query


@router_queries.patch("/{query_id}")
async def update_query_route(query_id: int, schema: schemas.QueryUpdate, db: Session = Depends(get_db)):
    updated_query = update_query(db, query_id, schema)
    if updated_query:
        await notify_clients(f"Инициатива '{updated_query.name}' изменена!")
        return updated_query
    return {"message": "Инициатива не найдена!"}


@router_queries.delete("/{query_id}")
async def delete_query_route(query_id: int, db: Session = Depends(get_db)):
    deleted = delete_query(db, query_id)
    if deleted:
        await notify_clients(f"Инициатива под номером {query_id} удалена")
        return {"message": "Инициатива удалена"}
    return {"message": "Инициатива не найдена"}
