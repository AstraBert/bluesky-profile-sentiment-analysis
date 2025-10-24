from dataclasses import dataclass
from typing import Optional

@dataclass
class ScoredLabel:
    label: str
    score: float | int

    @classmethod
    def from_dict(cls, data: dict) -> Optional["ScoredLabel"]:
        try:
            return cls(**data) 
        except Exception as e:
            return None
        
@dataclass
class SentimentDescription:
    sentiments: list[str]
    prevailing_sentiment: str
    average_score: float
