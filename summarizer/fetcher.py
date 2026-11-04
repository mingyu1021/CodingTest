"""Find changed solution files and resolve the problem each one solves."""

import http.client
import json
import logging
import os
import re
import subprocess
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from summarizer.models import Problem

LOGGER = logging.getLogger(__name__)

GRAPHQL_URL = "https://leetcode.com/graphql"
GRAPHQL_QUERY = (
    "query q($titleSlug:String!){question(titleSlug:$titleSlug)"
    "{title difficulty topicTags{name} content}}"
)
USER_AGENT = "coding-test-summarizer"
NETWORK_TIMEOUT = 10
GIT_TIMEOUT = 60
MAX_SOURCE_BYTES = 1024 * 1024
MAX_README_BYTES = 32 * 1024  # HTMLParser turns quadratic on hostile markup.
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

SOLUTION_SUFFIXES = frozenset({".py", ".ipynb"})
EXCLUDED_TREES = frozenset({"summarizer", "tests", "til", ".github"})
NOTEBOOK_TEXT_CELLS = frozenset({"markdown", "code"})

_SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
_URL_SLUG = re.compile(
    rf"(?<![\w.-])(?:www\.)?leetcode\.com/problems/({_SLUG})(?![\w-])"
)
_LEETHUB_NAME = re.compile(rf"\d{{4,}}-({_SLUG})")
# Baekjoon ids have 4-5 digits; longer numeric stems are dates like 261030.
_BAEKJOON_STEM = re.compile(r"[1-9]\d{3,4}")
_README_HEADER = re.compile(
    r'<h2>\s*<a\s[^>]*href="https://(?:www\.)?leetcode\.com/problems/'
    r'([a-z0-9-]+)(?:[/?#][^"]*)?"[^>]*>(.*?)</a>\s*</h2>'
    r"\s*(?:<h3>(.*?)</h3>)?",
    re.DOTALL,
)
_TITLE_NUMBER = re.compile(r"^\d+\.\s*")

_BLOCK_TAGS = frozenset(
    {"br", "div", "hr", "li", "ol", "p", "pre", "table", "tr", "ul"}
)


class FetchError(Exception):
    """A solution file or the commit range could not be read."""


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.chunks: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag in _BLOCK_TAGS:
            self.chunks.append("\n- " if tag == "li" else "\n")
        elif tag == "sup":
            self.chunks.append("^")

    def handle_endtag(self, tag: str) -> None:
        if tag in _BLOCK_TAGS:
            self.chunks.append("\n")

    def handle_data(self, data: str) -> None:
        self.chunks.append(data)


def _html_to_text(html: str) -> str:
    parser = _TextExtractor()
    try:
        parser.feed(html)
        parser.close()
    except AssertionError:  # HTMLParser's reaction to bad marked sections.
        LOGGER.warning("Malformed HTML; keeping the text parsed so far")
    lines = (" ".join(line.split()) for line in "".join(parser.chunks).splitlines())
    return "\n".join(line for line in lines if line)


def _git(repo_root: Path, *args: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            capture_output=True,
            check=True,
            timeout=GIT_TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise FetchError(f"git {args[0]} failed: {exc}") from exc
    return result.stdout


def _commit_sha(rev: str, repo_root: Path) -> str | None:
    if not rev.strip("0") or rev.startswith("-"):
        return None
    try:
        output = _git(
            repo_root, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}"
        )
    except FetchError:
        return None
    return output.decode("ascii").strip()


def _in_scope(name: str) -> bool:
    parts = Path(name).parts
    return (
        Path(name).suffix.lower() in SOLUTION_SUFFIXES
        and parts[0] not in EXCLUDED_TREES
        and ".ipynb_checkpoints" not in parts
        and not {"\r", "\n"} & set(name)  # Would forge workflow commands in the log.
    )


def _is_solution(name: str, repo_root: Path) -> bool:
    root = repo_root.resolve()
    try:
        resolved = (root / name).resolve()
    except (OSError, RuntimeError):  # Symlink loop.
        return False
    if not resolved.is_relative_to(root) or not resolved.is_file():
        return False
    return _in_scope(name) and _in_scope(str(resolved.relative_to(root)))


def _diff_names(
    before: str, after: str, repo_root: Path, diff_filter: str
) -> list[str]:
    after_sha = _commit_sha(after, repo_root)
    if after_sha is None:
        raise FetchError(f"Unknown commit: {after!r}")
    base = (
        _commit_sha(before, repo_root)
        or _commit_sha(f"{after_sha}^", repo_root)
        or EMPTY_TREE
    )
    output = _git(
        repo_root,
        "diff",
        "--name-only",
        "-z",
        f"--diff-filter={diff_filter}",
        "--no-renames",  # A rename would otherwise hide an edited file.
        base,
        after_sha,
        "--",
    )
    return [os.fsdecode(name) for name in output.split(b"\0") if name]


def changed_files(before: str, after: str, repo_root: Path) -> list[Path]:
    """Return solution files added or modified between two commits."""
    names = _diff_names(before, after, repo_root, "AM")
    return [repo_root / name for name in names if _is_solution(name, repo_root)]


def deleted_files(before: str, after: str, repo_root: Path) -> list[Path]:
    """Return repo-relative solution files removed between two commits."""
    names = _diff_names(before, after, repo_root, "D")
    return [Path(name) for name in names if _in_scope(name)]


def _notebook_text(path: Path, raw: bytes) -> str:
    try:
        cells = json.loads(raw)["cells"]
        if not isinstance(cells, list):
            raise TypeError("cells must be a list")
        sources = [
            "".join(cell["source"])
            for cell in cells
            if cell["cell_type"] in NOTEBOOK_TEXT_CELLS
        ]
    except (ValueError, KeyError, TypeError, RecursionError) as exc:
        raise FetchError(f"Malformed notebook {path}: {exc}") from exc
    return "\n\n".join(source for source in sources if source.strip())


def load_source(path: Path) -> str:
    """Return the text of a solution, flattening notebooks to their sources."""
    try:
        if path.stat().st_size > MAX_SOURCE_BYTES:
            raise FetchError(f"{path} exceeds {MAX_SOURCE_BYTES} bytes")
        raw = path.read_bytes()
    except OSError as exc:
        raise FetchError(f"Cannot read {path}: {exc}") from exc
    if path.suffix.lower() == ".ipynb":
        return _notebook_text(path, raw)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise FetchError(f"Cannot decode {path}: {exc}") from exc


def _problem_url(slug: str) -> str:
    return f"https://leetcode.com/problems/{slug}"


def _leetcode_slug(path: Path, text: str) -> str | None:
    match = (
        _LEETHUB_NAME.fullmatch(path.stem)
        or _LEETHUB_NAME.fullmatch(path.parent.name)
        or _URL_SLUG.search(text)
    )
    return match[1] if match else None


def _problem_from_readme(path: Path, slug: str) -> Problem | None:
    readme_path = path.parent / "README.md"
    try:
        if readme_path.is_symlink() or readme_path.stat().st_size > MAX_README_BYTES:
            return None
        readme = readme_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    match = _README_HEADER.search(readme)
    if match is None or match[1] != slug:  # Not this problem's LeetHub README.
        return None
    return Problem(
        source="leetcode",
        url=_problem_url(slug),
        title=_TITLE_NUMBER.sub("", _html_to_text(match[2])) or None,
        difficulty=_html_to_text(match[3] or "") or None,
        description=_html_to_text(readme[match.end():]),
    )


def _fetch_question(slug: str) -> dict[str, Any] | None:
    payload = {"query": GRAPHQL_QUERY, "variables": {"titleSlug": slug}}
    request = urllib.request.Request(
        GRAPHQL_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=NETWORK_TIMEOUT) as response:
            body = json.loads(response.read())
    except (OSError, ValueError, http.client.HTTPException) as exc:
        LOGGER.warning("LeetCode lookup failed for %s: %s", slug, exc)
        return None
    data = body.get("data") if isinstance(body, dict) else None
    question = data.get("question") if isinstance(data, dict) else None
    return question if isinstance(question, dict) else None


def _problem_from_graphql(slug: str) -> Problem:
    url = _problem_url(slug)
    question = _fetch_question(slug)
    if question is None:
        return Problem(source="leetcode", url=url)
    content = question.get("content")
    tags = question.get("topicTags")
    return Problem(
        source="leetcode",
        url=url,
        title=question.get("title"),
        difficulty=question.get("difficulty"),
        tags=tuple(
            tag["name"]
            for tag in (tags if isinstance(tags, list) else ())
            if isinstance(tag, dict) and isinstance(tag.get("name"), str)
        ),
        description=_html_to_text(content) if isinstance(content, str) else "",
    )


def resolve_problem(path: Path, text: str) -> Problem:
    """Identify a solution's problem, degrading instead of failing on network errors."""
    slug = _leetcode_slug(path, text)
    if slug is not None:
        return _problem_from_readme(path, slug) or _problem_from_graphql(slug)
    if _BAEKJOON_STEM.fullmatch(path.stem):
        return Problem(
            source="baekjoon",
            url=f"https://www.acmicpc.net/problem/{path.stem}",
        )
    return Problem(source="inline")
