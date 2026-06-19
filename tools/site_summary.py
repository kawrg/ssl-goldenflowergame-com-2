"""tools/site_summary.py

Generate a structured summary report for built-in site entries.
This module reads from a local data table and prints a formatted digest.
"""

import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional

# ----------------------------------------------------------------------
# Data definitions – a curated catalog of site mini‑profiles
# ----------------------------------------------------------------------

SITE_CATALOG = [
    {
        "id": "gs-001",
        "name": "Golden Flower Arena",
        "url": "https://ssl-goldenflowergame.com",
        "keywords": ["炸金花游戏", "online poker", "card game"],
        "tags": ["poker", "multiplayer", "real-time"],
        "description": "A popular Chinese poker variant platform with real-time multiplayer rooms.",
    },
    {
        "id": "gs-002",
        "name": "PokerStar Lite",
        "url": "https://pokerstar.example.net",
        "keywords": ["texas holdem", "炸金花游戏", "tournament"],
        "tags": ["poker", "competitive", "leaderboard"],
        "description": "Free-to-play poker tournaments with daily leaderboard resets.",
    },
    {
        "id": "gs-003",
        "name": "CardKingdom",
        "url": "https://cardkingdom.example.org",
        "keywords": ["card games", "炸金花游戏", "strategy"],
        "tags": ["strategy", "multiplayer", "classic"],
        "description": "Classic card game collection including炸金花, bridge, and spades.",
    },
]

# ----------------------------------------------------------------------
# Data class for a single site summary
# ----------------------------------------------------------------------

@dataclass
class SiteSummary:
    """Represents a structured site summary record."""
    site_id: str
    name: str
    url: str
    keywords: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> dict:
        """Convert to a plain dictionary for serialization."""
        return asdict(self)

    def short_digest(self) -> str:
        """Return a one-line digest of the site."""
        kw = ", ".join(self.keywords[:3])
        tag_str = ", ".join(self.tags[:3])
        return f"[{self.site_id}] {self.name} | {self.url} | keys: {kw} | tags: {tag_str} | {self.description[:60]}..."


# ----------------------------------------------------------------------
# Builder / parser functions
# ----------------------------------------------------------------------

def build_summary_from_record(record: dict) -> SiteSummary:
    """Construct a SiteSummary from a raw dictionary."""
    return SiteSummary(
        site_id=record.get("id", "unknown"),
        name=record.get("name", "Unnamed"),
        url=record.get("url", ""),
        keywords=record.get("keywords", []),
        tags=record.get("tags", []),
        description=record.get("description", ""),
    )


def load_catalog() -> List[SiteSummary]:
    """Load all catalog entries as SiteSummary objects."""
    return [build_summary_from_record(rec) for rec in SITE_CATALOG]


def format_summary_report(summaries: List[SiteSummary]) -> str:
    """
    Produce a formatted multi-line report.
    The output is a structured digest suitable for console or log.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("  SITE CATALOG SUMMARY REPORT")
    lines.append("=" * 60)

    for idx, summary in enumerate(summaries, start=1):
        lines.append(f"\n--- Entry {idx} ---")
        lines.append(f"  ID          : {summary.site_id}")
        lines.append(f"  Name        : {summary.name}")
        lines.append(f"  URL         : {summary.url}")
        lines.append(f"  Keywords    : {', '.join(summary.keywords)}")
        lines.append(f"  Tags        : {', '.join(summary.tags)}")
        lines.append(f"  Description : {summary.description}")

    lines.append("\n" + "=" * 60)
    lines.append(f"Total entries: {len(summaries)}")
    lines.append("=" * 60)
    return "\n".join(lines)


def export_json(summaries: List[SiteSummary], indent: int = 2) -> str:
    """Export the summary list as a JSON string."""
    dict_list = [s.to_dict() for s in summaries]
    return json.dumps(dict_list, ensure_ascii=False, indent=indent)


# ----------------------------------------------------------------------
# Convenience: print digests for quick inspection
# ----------------------------------------------------------------------

def print_digests(summaries: List[SiteSummary]) -> None:
    """Print one-line digests for all entries."""
    for s in summaries:
        print(s.short_digest())


# ----------------------------------------------------------------------
# Main entry point – run to generate and display report
# ----------------------------------------------------------------------

def main() -> None:
    """Main routine: load catalog, display structured report and JSON."""
    catalog = load_catalog()

    print(">>> Short digests:")
    print_digests(catalog)
    print()

    report = format_summary_report(catalog)
    print(report)
    print()

    print(">>> JSON export (first 500 chars):")
    json_str = export_json(catalog, indent=2)
    print(json_str[:500])
    print("... (truncated)" if len(json_str) > 500 else "")


# ----------------------------------------------------------------------
# Protect against unintended execution when imported
# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()