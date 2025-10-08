from fastapi import FastAPI, Depends, HTTPException
from typing import List
from src.app.database import engine, Base
from src.app.models import post
from src.app.service.post_service import PostService, get_post_service
from src.app.models import user
  # 스키마 임포트

app = FastAPI(
    title="FastAPI Ncp Mailing Service",
    description="게시판과 NCP 메일링 서비스 예제",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(user.router, tags=["User"])
#  게시글 관련 API 라우터
# app.include_router(post.router,tags=["Posts"])

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
# 게시글 생성
@app.post("/posts/", response_model=post.PostResponse, summary="게시글 생성", description="새로운 게시글을 생성합니다.")
def create_post(post_data: post.PostCreate, post_service: PostService = Depends(get_post_service)):
    create_post = post_service.create_post(post_data)
    return create_post

# 게시글 목록조회
@app.get("/posts/", response_model=List[post.PostResponse], summary="게시글 목록 조회", description="모든 게시글을 생성일 기준 내림차순으로 조회합니다.",
         responses={
             404: {
                 "description": "No posts found",
                    "content": {
                        "application/json": {
                            "example": {"detail": "No posts found"}
                        }
                    }
                 }
         })
def get_posts(post_service: PostService = Depends(get_post_service)):
    posts = post_service.get_post()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return posts

# 게시글 상세 조회
@app.get("/posts/{post_id}", response_model=post.PostResponse, summary="게시글 상세 조회", description="특정 ID의 게시글을 조회합니다.")
def get_post(post_id: int, post_service: PostService = Depends(get_post_service)):
    post_item = post_service.get_post_by_id(post_id)
    if post_item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_item
# 게시글 수정
@app.put("/posts/{post_id}", response_model=post.PostResponse, summary="게시글 수정", description="특정 ID의 게시글을 수정합니다.")
def update_post(post_id: int, post_data: post.PostCreate, post_service: PostService = Depends(get_post_service)):
    post_item = post_service.update_post(post_id, post_data)
    if post_item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_item
# 게시글 삭제
@app.delete("/posts/{post_id}", summary="게시글 삭제", description="특정 ID의 게시글을 삭제합니다.")
def delete_post(post_id: int, post_service: PostService = Depends(get_post_service)):
    result = post_service.delete_post(post_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted"}