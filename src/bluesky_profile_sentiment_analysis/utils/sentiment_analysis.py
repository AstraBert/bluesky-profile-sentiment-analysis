import os

from nlpcloud import Client
from typing import Optional, Union
from statistics import mean
from logging import getLogger
from .models import ScoredLabel, SentimentDescription, Keywords

logger = getLogger(__name__)

NLPCLOUD_CLIENT = Client(model=os.getenv("NLPCLOUD_MODEL", ""), token=os.getenv("NLPCLOUD_TOKEN"), gpu=True)

def extract_keywords(text: str) -> Optional[Keywords]:
    try: 
        kws = NLPCLOUD_CLIENT.kw_kp_extraction(
            text, 
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None
    return Keywords.from_dict(kws)

def analyze_sentiment(text: str) -> Optional[list[ScoredLabel]]:
    kws = extract_keywords(text)
    target = kws.keywords_and_keyphrases[0] if kws else None
    if target:
        logger.info(f"Target for sentiment detection: {target}")
    try:
        analysis = NLPCLOUD_CLIENT.sentiment(text, target=target)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None
    scored_labels = analysis.get("scored_labels", [])
    typed_scored_labels: list[ScoredLabel] = []
    for label in scored_labels:
        val = ScoredLabel.from_dict(label)
        if val is not None:
            typed_scored_labels.append(val)
    if typed_scored_labels:
        return typed_scored_labels
    return None

def posts_sentiment_analysis(posts: list[str]) -> Optional[SentimentDescription]:
    sentiments: dict[str, list[Union[float, int]]] = {}
    for post in posts:
        scored_labels = analyze_sentiment(post)
        logger.info(f"Scored labels: {scored_labels}")
        if scored_labels:
            for label in scored_labels:
                if label.label in sentiments:
                    sentiments[label.label].append(label.score)
                else:
                    sentiments[label.label] = [label.score]
    logger.info(f"Sentiments: {sentiments}")
    if len(sentiments) > 0:
        prev_sentiment = sorted(sentiments.items(), key=lambda item: len(item[1]), reverse=True)[0][0]
        avg_score = mean(sorted(sentiments.items(), key=lambda item: len(item[1]), reverse=True)[0][1])
        all_sentiments = list(sentiments.keys())
        return SentimentDescription(
            sentiments=all_sentiments, 
            prevailing_sentiment=prev_sentiment,
            average_score=avg_score
        )
    return None