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

def normalize_label(label: str) -> str:
    """Normalize label text to handle inconsistencies."""
    label = label.strip().lower().rstrip(":")
    if label in {"reg. date", "registration date"}:
        return "registration_date"
    elif label in {"last updated", "updated"}:
        return "last_updated"
    elif label in {"update before", "please refresh before"}:
        return "update_before"
    elif label == "status":
        return "status"
    elif label == "inactive reason":
        return "inactive_reason"
    else:
        raise ValueError(f"Unknown label: {label}")
    
def normalize_status(status: str) -> str:
    """Normalize status text to handle inconsistencies."""
    status = status.strip().lower()
    if status in {"active", "inactive", "pending"}:
        return status
    return status  # Return as-is if it's an unexpected value, or you could raise an error


def parse_queue_spots(html: str) -> list[ParsedQueueSpot]:
    """Extract the queue spot data for the logged in user.

    Notes:
    - The page is slightly inconsistent on purpose.
    - You may normalize labels/status text however you like.
    - Returning three ParsedQueueSpot items is enough.
    """

    # TODO:
    # 1. Find the queue cards.
    # 2. Read the title and field values from each card.
    # 3. Handle small label differences, e.g. "Reg. date" vs "Registration date".
    # 4. Include inactive_reason only when present.
    soup = BeautifulSoup(html, "html.parser")

    queue_spots = []
    cards = soup.find_all("div", class_="queue-card")

    for card in cards:
        queue_type = card.find("h2").text.strip()
        fields = {}

        for field in card.find_all("div", class_="field"):
            label_tag = field.find("span", class_="label")
            value_tag = field.find("span", class_="value")

            if not label_tag or not value_tag:
                continue

            normalized_label = normalize_label(label_tag.text.strip())
            fields[normalized_label] = value_tag.text.strip()

        registration_date = fields.get("registration_date", "")
        last_updated = fields.get("last_updated", "")
        update_before = fields.get("update_before", "")
        status = normalize_status(fields.get("status", ""))
        inactive_reason = fields.get("inactive_reason")

        queue_spots.append(
            ParsedQueueSpot(
                queue_type=queue_type,
                registration_date=registration_date,
                last_updated=last_updated,
                update_before=update_before,
                status=status,
                inactive_reason=inactive_reason,
            )
        )

    return queue_spots
