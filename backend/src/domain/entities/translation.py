from dataclasses import dataclass
from datetime import datetime


@dataclass
class Translation:
    jp_text: str
    en_text: str
    cached_at: datetime
