# Music Streaming Analytics

A lightweight toolkit for analyzing music streaming events. It ingests JSON event data and generates metrics such as top tracks, artist performance, and daily retention.

## Features
- Parse structured streaming events into strongly-typed objects
- Aggregate track- and artist-level performance
- Rank tracks by total playtime
- Calculate daily active listeners/retention
- Command-line interface for generating JSON reports

## Quick start
1. Ensure Python 3.11+ is available.
2. Run the test suite:

```bash
python -m pytest
```

3. Generate a report from the included sample dataset:

```bash
python -m app.cli data/sample_events.json
```

Use the `-o`/`--output` flag to write the report to a file instead of stdout.

## Project structure
- `app/models.py` – event dataclass and factory
- `app/analytics.py` – aggregation logic for tracks, artists, playtime, and retention
- `app/data_loader.py` – helpers for reading JSON event payloads
- `app/cli.py` – CLI entrypoint for producing analytics summaries
- `data/sample_events.json` – example dataset with mixed play/like events
- `tests/` – unit coverage for analytics calculations
