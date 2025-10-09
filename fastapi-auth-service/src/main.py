from fastapi import FastAPI
from app.database import engine, Base
from app.apis import auth, user
from starlette.middleware.authentication import AuthenticationMiddleware
from dependencies.auth import JWTAuthBackend
from app.apis import post as post_router

app = FastAPI(
    title="FastAPI Sample",
    description="게시판과 인증 서비스 예제",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())

app.include_router(user.router, prefix="/users", tags=["User"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(post_router.router, prefix="/posts", tags=["Posts"])

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