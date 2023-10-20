from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.testclient import TestClient

from handlers.channels import channel_router
from handlers.videos import video_router
from base.config import APP_HOST, APP_PORT
from utils.logs import my_logger
import uvicorn

app = FastAPI(
    title="Multi Do Production",

    summary="Testing task. CRUD system emulator",
    version="0.0.1",

    contact={
        "name": "Fedor Kuruts",
        "url": "https://drive.google.com/drive/folders/1rbPVtrZQMhtHJCksDaFkIzT55nDEkpmL?usp=drive_link",
        "email": "fedorkuruts@gmail.com",
    },
    license_info={
        "name": "MIT License",
    },
)

app.include_router(channel_router, prefix='/channel')
app.include_router(video_router, prefix='/video')

client = TestClient(app)


@app.get("/")
def redirect():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    my_logger.info('start app')
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
