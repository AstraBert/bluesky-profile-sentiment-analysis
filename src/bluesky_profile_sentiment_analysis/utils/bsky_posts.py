import os

from atproto import Client
from typing import Optional

BSKY_CLIENT = Client()

def get_posts_from_author(handle: str) -> Optional[list[str]]:
    BSKY_CLIENT.login(login=os.getenv("BSKY_HANDLE"), password=os.getenv("BSKY_PASSWORD"))
    result = BSKY_CLIENT.get_author_feed(handle)
    posts = [item.post.record.text for item in result.feed if hasattr(item.post.record, "text") and item.post.record.text is not None and len(item.post.record.text) > 100] # type: ignore
    if len(posts) < 5:
        return None
    return posts[:5]