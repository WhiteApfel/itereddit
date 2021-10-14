from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, root_validator


class SubredditMediaResolution(BaseModel):
    url: Optional[str]
    width: Optional[int]
    height: Optional[int]
    u: Optional[str]
    x: Optional[int]
    y: Optional[int]

    @root_validator(pre=True)
    def compatibility(cls, values):
        comp = {
            "u": "url",
            "x": "width",
            "y": "height"
        }
        for k in comp:
            if k in values:
                values[comp[k]] = values.get(k)
        return values


class SubredditPostMediaMetadata(BaseModel):
    status: str
    e: str
    mime_type: str = Field(..., alias="m")
    original: SubredditMediaResolution = Field(..., alias='s')
    preview: List[SubredditMediaResolution] = Field(..., alias='p')


class SubredditPostMediaMetadatas(BaseModel):
    __root__: Dict[str, SubredditPostMediaMetadata]


class SubredditPostMedia(BaseModel):
    obfuscated: Optional[str]
    content: Optional[str]
    type: str
    media_metadata: Optional[SubredditPostMediaMetadatas] = Field(None, alias="mediaMetadata")
    resolutions: Optional[List[SubredditMediaResolution]]
    gallery: Optional[dict]
    source: Optional[dict]


class SubredditPost(BaseModel):
    id: str
    num_comments: int = Field(..., alias="numComments")
    created: int
    score: int
    thumbnail: Optional[SubredditMediaResolution]
    title: str
    author: str
    author_id: str = Field(..., alias="authorId")
    post_id: str = Field(..., alias="postId")
    upvote_ratio: float = Field(..., alias="upvoteRatio")
    permalink: str
    media: Optional[SubredditPostMedia]
    preview: Optional[SubredditMediaResolution]


class SubredditPosts(BaseModel):
    __root__: Dict[str, SubredditPost]


class SubredditPiece(BaseModel):
    post_ids: List[str] = Field(..., alias="postIds")
    posts: SubredditPosts
