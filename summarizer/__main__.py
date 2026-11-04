"""Entry point: summarize the solutions changed between two commits into til/."""

import argparse
import logging
import sys
from pathlib import Path

from summarizer.analyzer import AnalysisError, Analyzer, LLMClient, LLMConfig
from summarizer.fetcher import (
    FetchError,
    changed_files,
    deleted_files,
    load_source,
    resolve_problem,
)
from summarizer.publisher import note_path, remove_symlinks, write_index, write_note

MAX_FILES = 20  # Bounds LLM spend when a push carries a bulk import.
logger = logging.getLogger("summarizer")


def summarize(path: Path, repo_root: Path, analyzer: Analyzer) -> None:
    text = load_source(path)
    if not text.strip():
        return
    problem = resolve_problem(path, text)
    insights = analyzer.analyze(problem, text)
    source = path.resolve().relative_to(repo_root)
    write_note(repo_root / "til", source, problem, insights)


def run(before: str, after: str, repo_root: Path, analyzer: Analyzer) -> int:
    til_dir = repo_root / "til"
    remove_symlinks(til_dir)
    try:
        files = changed_files(before, after, repo_root)
        deleted = deleted_files(before, after, repo_root)
    except FetchError as exc:
        logger.error("%s", exc)
        return 1
    for source in deleted:
        note_path(til_dir, source).unlink(missing_ok=True)
    if len(files) > MAX_FILES:
        logger.warning("Over the limit, skipping: %s", files[MAX_FILES:])
    failures = 0
    for path in files[:MAX_FILES]:
        try:
            summarize(path, repo_root, analyzer)
        except (FetchError, AnalysisError, OSError, ValueError, TypeError) as exc:
            logger.error("Failed to summarize %s: %s", path, exc)
            failures += 1
    if til_dir.is_dir():
        write_index(til_dir)
    return 1 if failures else 0


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True)
    parser.add_argument("--after", required=True)
    args = parser.parse_args()
    try:
        analyzer = Analyzer(LLMClient(LLMConfig.from_env()))
    except AnalysisError as exc:
        logger.error("%s", exc)
        return 1
    return run(args.before, args.after, Path.cwd().resolve(), analyzer)


if __name__ == "__main__":
    sys.exit(main())
