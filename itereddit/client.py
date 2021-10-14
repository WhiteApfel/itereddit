from httpx import AsyncClient


class Itereddit:
    """
    A handy tool for parsing posts in subreddit

    :param subreddit: name of subreddit
    :type subreddit: str
    """
    def __init__(self, subreddit: str):
        self.subreddit = subreddit
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = AsyncClient()
        return self._client
