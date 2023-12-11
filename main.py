from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from database.connection import conn
from routes.events import event_router
from routes.users import user_router
import uvicorn

app = FastAPI()

app.include_router(event_router, prefix="/event")  # Service Path: "/event/*"
app.include_router(user_router, prefix="/user")  # Service Path: "/event/*"

@app.on_event("startup")  # Creates DB Connection and Tables on Startup
def on_startup():
    conn()

@app.get("/")
async def home():
    return RedirectResponse(url="/event/")  # Redirect Path "/" to "/event/"

if __name__ == "__main__":  # Runs uvicorn Server on Startup as Main Module
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
