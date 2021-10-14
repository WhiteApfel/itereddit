from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SubredditThumbnail(BaseModel):
    url: str
    width: int
    height: int


class SubredditPostOneMedia(BaseModel):
    y: int
    x: int
    url: str = Field(..., alias="u")


class SubredditPostMediaMetadata(BaseModel):
    status: str
    e: str
    mime_type: str = Field(..., alias="m")
    original: List[SubredditPostOneMedia] = Field(..., alias='s')
    preview: List[SubredditPostOneMedia] = Field(..., alias='p')


class SubredditPostMediaMetadatas(BaseModel):
    __root__: Dict[str, SubredditPostMediaMetadata]


class SubredditPostMedia(BaseModel):
    obfuscated: Any
    type: str
    media_metadata: SubredditPostMediaMetadatas = Field(..., alias="mediaMetadata")


class SubredditPost(BaseModel):
    id: str
    num_comments: int = Field(..., alias="numComments")
    created: int
    score: int
    thumbnail: SubredditThumbnail
    title: str
    author: str
    author_id: str = Field(..., alias="authorId")
    post_id: str = Field(..., alias="postId")
    upvote_ratio: float = Field(..., alias="upvoteRatio")
    permalink: str
    media: SubredditPostMedia
    gallery: dict
    source: dict


class SubredditPosts(BaseModel):
    __root__: Dict[str, SubredditPost]


class SubredditPiece(BaseModel):
    post_ids: List[str] = Field(..., alias="postIds")
    posts: SubredditPosts
