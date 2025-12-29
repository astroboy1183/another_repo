from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class StreamEvent:
    """Represents a single music streaming event.

    Attributes:
        event_id: Unique identifier for the event.
        user_id: Identifier for the user who triggered the event.
        track_id: Identifier for the track.
        artist_id: Identifier for the artist.
        event_type: Type of event (e.g., "play", "like", "pause").
        occurred_at: When the event happened.
        duration_seconds: Optional playback duration for "play" events.
    """

    event_id: str
    user_id: str
    track_id: str
    artist_id: str
    event_type: str
    occurred_at: datetime
    duration_seconds: Optional[float] = None

    @classmethod
    def from_dict(cls, payload: dict) -> "StreamEvent":
        return cls(
            event_id=str(payload["event_id"]),
            user_id=str(payload["user_id"]),
            track_id=str(payload["track_id"]),
            artist_id=str(payload["artist_id"]),
            event_type=str(payload["event_type"]),
            occurred_at=datetime.fromisoformat(payload["occurred_at"]),
            duration_seconds=payload.get("duration_seconds"),
        )
