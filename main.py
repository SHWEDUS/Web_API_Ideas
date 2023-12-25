from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crud import get_directions, get_queries
import models
from sqlalchemy.orm import Session
from database import get_db

from database import engine
from routes import read_directions, router_websocket, router_directions, router_queries

# Создание таблиц в БД
models.Base.metadata.create_all(bind=engine)

# Templates
templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="Open Ideas",
    summary="Open Ideas!",
    version="0.0.1",
)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    http_protocol = request.headers.get("x-forwarded-proto", "https")
    directions = get_directions(db, skip=0, limit=10)
    queries = get_queries(db, skip=0, limit=10)
    ws_protocol = "wss" if http_protocol == "https" else "ws"
    server_urn = request.url.netloc
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "http_protocol": http_protocol,
                                       "ws_protocol": ws_protocol,
                                       "directions": directions,
                                       "queries": queries,
                                       "server_urn": server_urn})



# Подключаем созданные роутеры в приложение
app.include_router(router_websocket)
app.include_router(router_directions)
app.include_router(router_queries)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
