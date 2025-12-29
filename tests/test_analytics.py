from datetime import datetime

from app import analytics
from app.models import StreamEvent


def sample_events():
    return [
        StreamEvent(
            event_id="1",
            user_id="u1",
            track_id="t1",
            artist_id="a1",
            event_type="play",
            occurred_at=datetime.fromisoformat("2024-05-01T10:00:00"),
            duration_seconds=120,
        ),
        StreamEvent(
            event_id="2",
            user_id="u2",
            track_id="t1",
            artist_id="a1",
            event_type="play",
            occurred_at=datetime.fromisoformat("2024-05-01T10:10:00"),
            duration_seconds=150,
        ),
        StreamEvent(
            event_id="3",
            user_id="u1",
            track_id="t2",
            artist_id="a2",
            event_type="play",
            occurred_at=datetime.fromisoformat("2024-05-02T11:00:00"),
            duration_seconds=200,
        ),
        StreamEvent(
            event_id="4",
            user_id="u3",
            track_id="t2",
            artist_id="a2",
            event_type="like",
            occurred_at=datetime.fromisoformat("2024-05-02T12:00:00"),
        ),
    ]


def test_summarize_tracks_counts_and_listeners():
    summaries = analytics.summarize_tracks(sample_events())
    assert summaries[0].track_id == "t1"
    assert summaries[0].play_count == 2
    assert summaries[0].unique_listeners == 2
    assert summaries[0].average_listen_time == 135


def test_summarize_artists():
    summaries = analytics.summarize_artists(sample_events())
    assert summaries[0].artist_id == "a1"
    assert summaries[0].play_count == 2
    assert summaries[0].unique_listeners == 2


def test_top_tracks_by_playtime():
    rankings = analytics.top_tracks_by_playtime(sample_events(), limit=1)
    assert rankings == [("t1", 270)]


def test_retention_by_day():
    retention = analytics.retention_by_day(sample_events())
    assert retention == {"2024-05-01": 2, "2024-05-02": 2}
