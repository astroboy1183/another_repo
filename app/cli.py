from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from . import analytics
from .data_loader import load_events


def build_report(path: Path | str) -> Dict[str, Any]:
    events = load_events(path)

    track_summary = analytics.summarize_tracks(events)
    artist_summary = analytics.summarize_artists(events)
    retention = analytics.retention_by_day(events)
    playtime_leaders = analytics.top_tracks_by_playtime(events, limit=5)

    return {
        "tracks": [summary.__dict__ for summary in track_summary],
        "artists": [summary.__dict__ for summary in artist_summary],
        "retention": retention,
        "top_playtime": playtime_leaders,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Music streaming analytics CLI")
    parser.add_argument(
        "data_path",
        type=Path,
        help="Path to JSON file with streaming events",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Optional path to write analytics report as JSON",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report(args.data_path)

    if args.output:
        args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
