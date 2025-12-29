from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from statistics import mean
from typing import Iterable, List, Mapping, Tuple

from .models import StreamEvent


@dataclass(frozen=True)
class TrackAnalytics:
    track_id: str
    play_count: int
    unique_listeners: int
    average_listen_time: float


@dataclass(frozen=True)
class ArtistAnalytics:
    artist_id: str
    play_count: int
    unique_listeners: int


def _play_events(events: Iterable[StreamEvent]) -> List[StreamEvent]:
    return [event for event in events if event.event_type == "play"]


def summarize_tracks(events: Iterable[StreamEvent]) -> List[TrackAnalytics]:
    play_events = _play_events(events)
    plays_by_track = Counter(event.track_id for event in play_events)
    listeners_by_track = defaultdict(set)
    listen_times_by_track = defaultdict(list)

    for event in play_events:
        listeners_by_track[event.track_id].add(event.user_id)
        if event.duration_seconds is not None:
            listen_times_by_track[event.track_id].append(event.duration_seconds)

    summaries: List[TrackAnalytics] = []
    for track_id, play_count in plays_by_track.items():
        durations = listen_times_by_track.get(track_id, [])
        average_listen_time = mean(durations) if durations else 0.0
        summaries.append(
            TrackAnalytics(
                track_id=track_id,
                play_count=play_count,
                unique_listeners=len(listeners_by_track.get(track_id, [])),
                average_listen_time=average_listen_time,
            )
        )

    return sorted(summaries, key=lambda entry: entry.play_count, reverse=True)


def summarize_artists(events: Iterable[StreamEvent]) -> List[ArtistAnalytics]:
    play_events = _play_events(events)
    plays_by_artist = Counter(event.artist_id for event in play_events)
    listeners_by_artist = defaultdict(set)

    for event in play_events:
        listeners_by_artist[event.artist_id].add(event.user_id)

    summaries: List[ArtistAnalytics] = []
    for artist_id, play_count in plays_by_artist.items():
        summaries.append(
            ArtistAnalytics(
                artist_id=artist_id,
                play_count=play_count,
                unique_listeners=len(listeners_by_artist.get(artist_id, [])),
            )
        )

    return sorted(summaries, key=lambda entry: entry.play_count, reverse=True)


def top_tracks_by_playtime(events: Iterable[StreamEvent], limit: int = 5) -> List[Tuple[str, float]]:
    play_events = _play_events(events)
    total_playtime_by_track: Mapping[str, float] = defaultdict(float)

    for event in play_events:
        if event.duration_seconds is not None:
            total_playtime_by_track[event.track_id] += event.duration_seconds

    ranked = sorted(
        total_playtime_by_track.items(), key=lambda item: item[1], reverse=True
    )
    return ranked[:limit]


def retention_by_day(events: Iterable[StreamEvent]) -> Mapping[str, int]:
    """Return a mapping of YYYY-MM-DD to distinct active listeners."""
    listeners_per_day = defaultdict(set)
    for event in events:
        day = event.occurred_at.date().isoformat()
        listeners_per_day[day].add(event.user_id)

    return {day: len(listeners) for day, listeners in sorted(listeners_per_day.items())}
