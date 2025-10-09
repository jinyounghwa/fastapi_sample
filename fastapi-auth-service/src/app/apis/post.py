from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models import post
from app.service.post_service import PostService, get_post_service

router = APIRouter()

# 게시글 생성
@router.post("/", response_model=post.PostResponse, summary="게시글 생성", description="새로운 게시글을 생성합니다.")
def create_post(post_data: post.PostCreate, post_service: PostService = Depends(get_post_service)):
    create_post = post_service.create_post(post_data)
    return create_post

# 게시글 목록조회
@router.get("/", response_model=List[post.PostResponse], summary="게시글 목록 조회", description="모든 게시글을 생성일 기준 내림차순으로 조회합니다.",
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
@router.get("/{post_id}", response_model=post.PostResponse, summary="게시글 상세 조회", description="특정 ID의 게시글을 조회합니다.")
def get_post(post_id: int, post_service: PostService = Depends(get_post_service)):
    post_item = post_service.get_post_by_id(post_id)
    if post_item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_item
# 게시글 수정
@router.put("/{post_id}", response_model=post.PostResponse, summary="게시글 수정", description="특정 ID의 게시글을 수정합니다.")
def update_post(post_id: int, post_data: post.PostCreate, post_service: PostService = Depends(get_post_service)):
    post_item = post_service.update_post(post_id, post_data)
    if post_item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_item
# 게시글 삭제
@router.delete("/{post_id}", summary="게시글 삭제", description="특정 ID의 게시글을 삭제합니다.")
def delete_post(post_id: int, post_service: PostService = Depends(get_post_service)):
    result = post_service.delete_post(post_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted"}