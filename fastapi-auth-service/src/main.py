from fastapi import FastAPI
from app.database import engine, Base
from app.models import Post

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/ping")
async def ping_db():
    try:
        with engine.connect() as conn:
            return {"status": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    
@app.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)
            