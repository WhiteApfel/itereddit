# Itereddit

Iterate posts from subreddit. Posts are represented by dataclasses without unnecessary fields. 
So far, not all types of posts are covered, so I may need help adding new ones: 
you can just report the post and link in 
[new issue](https://github.com/WhiteApfel/itereddit/issues/new "Push me and then just touch me")

### How to use it, Wapfelka?

Parsing media in the best resolution, for example:

```python
import asyncio

from itereddit import Itereddit

itereddit = Itereddit()


async def main():
    async for i in itereddit:
        if i.media:
            if i.media.media_metadata:
                for m in i.media.media_metadata:
                    print(i.media.media_metadata[m].original.url)
            elif i.media.resolutions:
                print(i.media.resolutions[-1].url)


asyncio.run(main())
```