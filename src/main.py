import asyncio
import fastapi
import uvicorn
from api.front import Router as front_router
from api.api import Router as api_router
from database import crud
from fastapi.responses import FileResponse
from database.database import Base, SessionLocal, engine


async def favicon():
    return FileResponse("./favicon.ico")


async def main():
    Base.metadata.create_all(engine)
    crud.init_database(SessionLocal())
    app = fastapi.FastAPI()
    app.include_router(front_router)
    app.include_router(api_router)
    app.add_api_route("/favicon.ico", favicon)
    config = uvicorn.Config(app, host="0.0.0.0", port=6969)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
