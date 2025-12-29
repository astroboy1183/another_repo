from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from .models import StreamEvent


def load_events(path: Path | str) -> List[StreamEvent]:
    """Load stream events from a JSON file."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, list):
        raise ValueError("Expected a list of events in the JSON file.")

    return [StreamEvent.from_dict(item) for item in payload]


def load_and_filter_events(path: Path | str, *, event_types: Iterable[str]) -> List[StreamEvent]:
    events = load_events(path)
    event_types_set = set(event_types)
    return [event for event in events if event.event_type in event_types_set]
