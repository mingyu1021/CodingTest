"""Render analyses as Markdown notes under til/ and keep their index current."""

import hashlib
import re
from pathlib import Path
from urllib.parse import quote

from summarizer.models import Insight, Problem

INDEX_NAME = "README.md"
MAX_NOTE_NAME_BYTES = 200  # Filesystems cap names at 255 bytes, and Korean takes 3 each.
_MARKDOWN_SPECIALS = re.compile(r"([\\`*_\[\]<>|!])")


def escape(text: str) -> str:
    """Neutralize Markdown and HTML in text that originated from the LLM or a file."""
    return _MARKDOWN_SPECIALS.sub(r"\\\1", " ".join(text.split()))


def note_path(til_dir: Path, source: Path) -> Path:
    """Map a repo-relative source path to a flat, filesystem-safe note path."""
    flat = "__".join(re.sub(r"[^\w.-]+", "-", part) for part in source.parts)
    encoded = flat.encode("utf-8", "surrogateescape")
    if len(encoded) > MAX_NOTE_NAME_BYTES:
        digest = hashlib.sha256(encoded).hexdigest()[:8]
        kept = encoded[:MAX_NOTE_NAME_BYTES].decode("utf-8", "ignore")
        flat = f"{kept}-{digest}"
    return til_dir / f"{flat}.md"


def remove_symlinks(til_dir: Path) -> None:
    """Drop committed symlinks, which could redirect note reads and writes off the repo."""
    if til_dir.is_symlink():
        til_dir.unlink()
    elif til_dir.is_dir():
        for entry in til_dir.iterdir():
            if entry.is_symlink():
                entry.unlink()


def render_note(source: Path, problem: Problem, insights: list[Insight]) -> str:
    lines = [f"# {escape(source.as_posix())}", ""]
    lines.append(f"- 풀이 코드: [{escape(source.name)}](../{quote(source.as_posix())})")
    if problem.url:
        lines.append(f"- 문제: [{escape(problem.title or problem.url)}]({problem.url})")
    if problem.difficulty:
        lines.append(f"- 난이도: {escape(problem.difficulty)}")
    if problem.tags:
        lines.append(f"- 태그: {escape(', '.join(problem.tags))}")
    for insight in insights:
        lines += [
            "",
            f"## {escape(insight.title)}",
            "",
            f"- **알고리즘 패턴**: {escape(', '.join(insight.patterns))}",
            f"- **시간 복잡도**: {escape(insight.time_complexity)}",
            f"- **공간 복잡도**: {escape(insight.space_complexity)}",
            f"- **핵심 아이디어**: {escape(insight.key_idea)}",
        ]
    return "\n".join(lines) + "\n"


def write_note(
    til_dir: Path, source: Path, problem: Problem, insights: list[Insight]
) -> Path:
    til_dir.mkdir(exist_ok=True)
    path = note_path(til_dir, source)
    path.write_text(render_note(source, problem, insights), encoding="utf-8")
    return path


def write_index(til_dir: Path) -> None:
    """Rebuild the index from the notes on disk, so it can never drift from them."""
    lines = ["# TIL", ""]
    for note in sorted(til_dir.glob("*.md")):
        if note.name == INDEX_NAME or not note.is_file():
            continue
        text = note.read_text(encoding="utf-8", errors="replace")
        heading = text.split("\n", 1)[0].removeprefix("# ")
        titles = re.findall(r"^## (.+)$", text, flags=re.MULTILINE)
        lines.append(f"- [{heading}]({quote(note.name)}): {', '.join(titles)}")
    (til_dir / INDEX_NAME).write_text("\n".join(lines) + "\n", encoding="utf-8")
