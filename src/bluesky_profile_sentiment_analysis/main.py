from workflows.events import StartEvent, StopEvent, Event
from workflows import Workflow, step
from typing import Union, Optional

from .utils import get_posts_from_author, posts_sentiment_analysis

class InputEvent(StartEvent):
    user_handle: str

class PostsRetrievedEvent(Event):
    posts: list[str]

class OutputEvent(StopEvent):
    all_sentiments: Optional[list[str]] = None
    prevailing_sentiment: Optional[str] = None
    average_confidence_score: Optional[float] = None
    error: Optional[str] = None

class BlueSkySentimentAnalysisWorkflow(Workflow):
    @step
    async def get_posts_from_bluesky(self, ev: InputEvent) -> Union[PostsRetrievedEvent, OutputEvent]:
        posts = get_posts_from_author(ev.user_handle)
        if posts is not None:
            return PostsRetrievedEvent(posts=posts)
        return OutputEvent(error=f"Unable to retrieve posts from user {ev.user_handle}")
    
    @step
    async def analyze_sentiments(self, ev: PostsRetrievedEvent) -> OutputEvent:
        analysis = posts_sentiment_analysis(ev.posts)
        if analysis:
            return OutputEvent(all_sentiments=analysis.sentiments, prevailing_sentiment=analysis.prevailing_sentiment, average_confidence_score=analysis.average_score)
        else:
            return OutputEvent(error="Sentiment analysis for BlueSky posts failed")
        
workflow = BlueSkySentimentAnalysisWorkflow(timeout=300)