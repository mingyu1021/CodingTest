"""Data shared by the fetch, analysis and publish stages."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Problem:
    """Where a solution came from. `description` is empty when the statement is inline."""

    source: str  # "leetcode" | "baekjoon" | "inline"
    url: str | None = None
    title: str | None = None
    difficulty: str | None = None
    tags: tuple[str, ...] = ()
    description: str = ""


@dataclass(frozen=True)
class Insight:
    """Analysis of one problem. A source file may yield several."""

    title: str
    patterns: tuple[str, ...]
    time_complexity: str
    space_complexity: str
    key_idea: str
