from asyncio import Queue
from typing import AsyncIterator, Literal

from httpx import AsyncClient

from itereddit.models.subreddit_posts import SubredditPiece, SubredditPost


class Itereddit:
    """
    A handy tool for parsing posts in subreddit

    :param subreddit: name of subreddit
    :type subreddit: str
    :param last_post_id: id of last post, so as not to iterate already processed posts
    :type last_post_id: str
    :param sort: type of sorting by reddit
    :type sort: str: `name` or `hot`
    """

    def __init__(self, subreddit: str = "rate_my_dick", last_post_id: str = None, sort: Literal['new', 'hot'] = 'new'):
        self.subreddit = subreddit
        self._client = None
        self.__last_post = last_post_id
        self.__sort = sort
        self.__posts_queue = Queue()

    @property
    def client(self):
        if not self._client:
            self._client = AsyncClient()
        return self._client

    @property
    def url(self):
        return f"https://gateway.reddit.com/desktopapi/v1/subreddits/{self.subreddit}"

    def params(self, after: str = None):
        return {
            "rtj": "only",
            "allow_over18": 1,
            "include": "prefsSubreddit",
            "after": after,
            "forceGeopopular": False,
            "sort": self.__sort,
        }

    def __aiter__(self) -> AsyncIterator[SubredditPost]:
        return self

    async def __anext__(self) -> SubredditPost:
        if not self.__posts_queue.qsize():
            response = await self.client.get(
                self.url, params=self.params(self.__last_post)
            )
            if response.status_code == 200:
                piece = SubredditPiece(**response.json())
                for post_id in piece.posts:
                    await self.__posts_queue.put(piece.posts[post_id])
                self.__last_post = piece.post_ids[-1]
        return await self.__posts_queue.get()
