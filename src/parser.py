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

    soup = BeautifulSoup(html, "html.parser")

    queue_spots = []
    cards = soup.find_all("article", class_="queue-card")

    for card in cards:
        title_tag = card.find("div", class_="queue-title")
        if title_tag is None:
            continue

        queue_type = title_tag.text.strip()
        fields = {}

        for field in card.find_all("div", class_="item"):
            label_tag = field.find("div", class_="label")
            value_tag = field.find("div", class_="value")

            if not label_tag or not value_tag:
                continue

            normalized_label = normalize_label(label_tag.text.strip())
            fields[normalized_label] = value_tag.text.strip()

        inactive_label = card.find(
            "div",
            class_="label",
            string=lambda s: s and s.strip().lower() == "inactive reason",

        )
        if inactive_label:
            inactive_value_tag = inactive_label.find_next("div", class_="value")
            if inactive_value_tag:
                fields["inactive_reason"] = inactive_value_tag.text.strip()


        queue_spots.append(
            ParsedQueueSpot(
                queue_type=queue_type,
                registration_date=fields.get("registration_date", ""),
                last_updated=fields.get("last_updated", ""),
                update_before=fields.get("update_before", ""),
                status=normalize_status(fields.get("status", "")),
                inactive_reason=fields.get("inactive_reason"),
            )
        )

    return queue_spots
