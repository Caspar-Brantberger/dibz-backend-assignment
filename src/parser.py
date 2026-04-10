from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from bs4 import BeautifulSoup


@dataclass
class ParsedQueueSpot:
    queue_type: str
    registration_date: str
    last_updated: str
    update_before: str
    status: str
    inactive_reason: Optional[str]


def parse_queue_spots(html: str) -> list[ParsedQueueSpot]:
    """Extract the queue spot data for the logged in user.

    Notes:
    - The page is slightly inconsistent on purpose.
    - You may normalize labels/status text however you like.
    - Returning three ParsedQueueSpot items is enough.
    """
    soup = BeautifulSoup(html, "html.parser")

    # TODO:
    # 1. Find the queue cards.
    # 2. Read the title and field values from each card.
    # 3. Handle small label differences, e.g. "Reg. date" vs "Registration date".
    # 4. Include inactive_reason only when present.
    raise NotImplementedError
