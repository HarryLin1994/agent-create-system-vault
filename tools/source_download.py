#!/usr/bin/env python3
"""Download explicit web sources into raw intake with robots and manifest checks."""

from __future__ import annotations

import argparse
import hashlib
import html.parser
import json
import mimetypes
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from ingest_sources import RawSource, adapter_for, display_path, render_manifest, slugify


RAW_DEFAULT = Path("00_Inbox") / "Raw Sources" / "_downloads"
MANIFEST_DEFAULT = Path("00_Inbox") / "Source Manifests"
DEFAULT_USER_AGENT = "agent-create-system-vault/0.1 (+local knowledge ingestion)"
DEFAULT_MAX_BYTES = 25 * 1024 * 1024

COPYRIGHT_RISK_URL_MARKERS = {
    "annas-archive",
    "download-epub",
    "download-full-book",
    "download-mobi",
    "download-pdf",
    "free-ebook-download",
    "free-epub",
    "free-pdf",
    "full-book-pdf",
    "full-pdf",
    "libgen",
    "oceanofpdf",
    "pdfdrive",
    "pirated",
    "torrent",
    "z-lib",
    "zlibrary",
}


CONTENT_EXTENSIONS = {
    "application/json": ".json",
    "application/pdf": ".pdf",
    "application/rtf": ".rtf",
    "application/xhtml+xml": ".html",
    "application/xml": ".xml",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "text/csv": ".csv",
    "text/html": ".html",
    "text/markdown": ".md",
    "text/plain": ".txt",
    "text/xml": ".xml",
}


@dataclass(frozen=True)
class DownloadedSource:
    url: str
    raw_path: Path
    manifest_path: Path
    source_id: str
    sha256: str
    content_type: str
    size_bytes: int
    status: str


class LinkExtractor(html.parser.HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() not in {"a", "link"}:
            return
        for key, value in attrs:
            if key.lower() in {"href", "src"} and value:
                self.links.append(urllib.parse.urljoin(self.base_url, value))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download URLs into raw source intake and create manifests."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    download = subparsers.add_parser("download", help="Download explicit URLs.")
    add_common_args(download)
    download.add_argument("urls", nargs="*", help="URLs to download.")
    download.add_argument("--url-file", help="Plain text file with one URL per line.")

    crawl = subparsers.add_parser("crawl", help="Crawl a small same-host URL area.")
    add_common_args(crawl)
    crawl.add_argument("seeds", nargs="+", help="Seed URLs.")
    crawl.add_argument("--max-pages", type=int, default=10, help="Maximum pages/files.")
    crawl.add_argument("--max-depth", type=int, default=1, help="Maximum link depth.")
    crawl.add_argument(
        "--cross-host",
        action="store_true",
        help="Allow links to hosts outside the seed host.",
    )

    return parser.parse_args()


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--vault",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the Obsidian vault.",
    )
    parser.add_argument(
        "--raw-dir",
        default=str(RAW_DEFAULT),
        help="Download folder, relative to vault unless absolute.",
    )
    parser.add_argument(
        "--manifest-dir",
        default=str(MANIFEST_DEFAULT),
        help="Manifest folder, relative to vault unless absolute.",
    )
    parser.add_argument("--domain", default="", help="Default domain for manifests.")
    parser.add_argument(
        "--permission",
        default="needs-review",
        help="Default permission label for manifests.",
    )
    parser.add_argument(
        "--sensitivity",
        default="unknown",
        help="Default sensitivity label for manifests.",
    )
    parser.add_argument(
        "--user-agent",
        default=DEFAULT_USER_AGENT,
        help="Crawler user agent.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Minimum seconds between requests to the same host.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=DEFAULT_MAX_BYTES,
        help="Maximum response size to save.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check robots/fetchability without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing downloaded files and manifests.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")


def resolve_under_vault(vault: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else vault / path


def load_url_file(path: str) -> list[str]:
    urls: list[str] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        clean = line.strip()
        if clean and not clean.startswith("#"):
            urls.append(clean)
    return urls


def normalized_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {url}")
    return urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path or "/",
            "",
            parsed.query,
            "",
        )
    )


def robots_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "/robots.txt", "", "", ""))


def fetch_robots(url: str, user_agent: str, timeout: float) -> urllib.robotparser.RobotFileParser:
    target = robots_url(url)
    parser = urllib.robotparser.RobotFileParser(target)
    request = urllib.request.Request(target, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content = response.read(1024 * 1024).decode("utf-8", errors="ignore")
            parser.parse(content.splitlines())
    except urllib.error.HTTPError as error:
        if error.code in {401, 403}:
            parser.disallow_all = True
        elif 400 <= error.code < 500:
            parser.allow_all = True
        else:
            parser.disallow_all = True
    except (OSError, urllib.error.URLError):
        parser.disallow_all = False
    return parser


def host_key(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc.lower()


def copyright_risk_reason(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    target = " ".join(
        (
            parsed.netloc.lower().removeprefix("www."),
            parsed.path.lower().replace("_", "-"),
            parsed.query.lower().replace("_", "-"),
        )
    )
    for marker in COPYRIGHT_RISK_URL_MARKERS:
        if marker in target:
            return f"copyright-risk-marker={marker}"
    return ""


def wait_for_host(url: str, last_request: dict[str, float], delay: float) -> None:
    host = host_key(url)
    now = time.monotonic()
    elapsed = now - last_request.get(host, 0.0)
    if elapsed < delay:
        time.sleep(delay - elapsed)
    last_request[host] = time.monotonic()


def fetch_url(url: str, user_agent: str, timeout: float, max_bytes: int) -> tuple[bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get_content_type()
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"Response exceeds --max-bytes: {url}")
            chunks.append(chunk)
        return b"".join(chunks), content_type


def extension_for(url: str, content_type: str) -> str:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix and len(suffix) <= 8:
        return suffix
    return CONTENT_EXTENSIONS.get(content_type) or mimetypes.guess_extension(content_type) or ".bin"


def source_type_for(extension: str, content_type: str) -> str:
    if content_type == "text/html":
        return "web-page"
    if content_type.startswith("image/"):
        return "image"
    return {
        ".csv": "data-export",
        ".doc": "document",
        ".docx": "document",
        ".htm": "web-page",
        ".html": "web-page",
        ".jpeg": "image",
        ".jpg": "image",
        ".json": "data-export",
        ".md": "markdown",
        ".pdf": "pdf",
        ".png": "image",
        ".ppt": "presentation",
        ".pptx": "presentation",
        ".rtf": "document",
        ".txt": "text",
        ".xlsx": "spreadsheet",
        ".xml": "structured-data",
    }.get(extension, "unknown")


def output_path(raw_dir: Path, url: str, digest: str, extension: str) -> tuple[str, Path]:
    parsed = urllib.parse.urlparse(url)
    host = slugify(parsed.netloc)
    stem = slugify(Path(parsed.path).stem or parsed.netloc)
    source_id = f"{stem}-{digest[:12]}"
    return source_id, raw_dir / host / f"{source_id}{extension}"


def write_download(
    url: str,
    content: bytes,
    content_type: str,
    vault: Path,
    raw_dir: Path,
    manifest_dir: Path,
    domain: str,
    permission: str,
    sensitivity: str,
    force: bool,
    dry_run: bool,
) -> DownloadedSource:
    digest = hashlib.sha256(content).hexdigest()
    extension = extension_for(url, content_type)
    source_id, raw_path = output_path(raw_dir, url, digest, extension)
    manifest_path = manifest_dir / f"{source_id}.md"

    status = "dry-run"
    if not dry_run:
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_dir.mkdir(parents=True, exist_ok=True)
        if force or not raw_path.exists():
            raw_path.write_bytes(content)
            status = "downloaded"
        else:
            status = "raw-exists"

        if force or not manifest_path.exists():
            raw_source = RawSource(
                path=raw_path,
                display_path=display_path(raw_path, vault),
                source_id=source_id,
                source_type=source_type_for(extension, content_type),
                extension=extension,
                sha256=digest,
                size_bytes=len(content),
                modified_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                source_url=url,
            )
            manifest_path.write_text(
                render_manifest(raw_source, domain, permission, sensitivity),
                encoding="utf-8",
            )
        elif status == "downloaded":
            status = "manifest-exists"

    return DownloadedSource(
        url=url,
        raw_path=raw_path,
        manifest_path=manifest_path,
        source_id=source_id,
        sha256=digest,
        content_type=content_type,
        size_bytes=len(content),
        status=status,
    )


def download_urls(args: argparse.Namespace, urls: list[str]) -> dict[str, object]:
    vault = Path(args.vault).resolve()
    raw_dir = resolve_under_vault(vault, args.raw_dir).resolve()
    manifest_dir = resolve_under_vault(vault, args.manifest_dir).resolve()
    robots_cache: dict[str, urllib.robotparser.RobotFileParser] = {}
    last_request: dict[str, float] = {}
    results: list[DownloadedSource] = []
    skipped: list[dict[str, str]] = []

    for raw_url in urls:
        try:
            url = normalized_url(raw_url)
            copyright_risk = copyright_risk_reason(url)
            if copyright_risk:
                skipped.append({"url": url, "reason": copyright_risk})
                continue
            robot = robots_cache.get(host_key(url))
            if robot is None:
                robot = fetch_robots(url, args.user_agent, args.timeout)
                robots_cache[host_key(url)] = robot
            if not robot.can_fetch(args.user_agent, url):
                skipped.append({"url": url, "reason": "blocked-by-robots"})
                continue
            wait_for_host(url, last_request, args.delay)
            content, content_type = fetch_url(url, args.user_agent, args.timeout, args.max_bytes)
            results.append(
                write_download(
                    url=url,
                    content=content,
                    content_type=content_type,
                    vault=vault,
                    raw_dir=raw_dir,
                    manifest_dir=manifest_dir,
                    domain=args.domain,
                    permission=args.permission,
                    sensitivity=args.sensitivity,
                    force=args.force,
                    dry_run=args.dry_run,
                )
            )
        except Exception as error:  # noqa: BLE001 - report per-URL failures.
            skipped.append({"url": raw_url, "reason": str(error)})

    return report(vault, results, skipped)


def extract_links(url: str, content: bytes, content_type: str) -> list[str]:
    if content_type != "text/html":
        return []
    parser = LinkExtractor(url)
    parser.feed(content.decode("utf-8", errors="ignore"))
    links: list[str] = []
    for link in parser.links:
        parsed = urllib.parse.urlparse(link)
        if parsed.scheme in {"http", "https"}:
            links.append(normalized_url(link))
    return links


def crawl_urls(args: argparse.Namespace) -> dict[str, object]:
    vault = Path(args.vault).resolve()
    raw_dir = resolve_under_vault(vault, args.raw_dir).resolve()
    manifest_dir = resolve_under_vault(vault, args.manifest_dir).resolve()
    seed_urls = [normalized_url(seed) for seed in args.seeds]
    seed_hosts = {host_key(seed) for seed in seed_urls}
    queue: deque[tuple[str, int]] = deque((seed, 0) for seed in seed_urls)
    seen: set[str] = set()
    robots_cache: dict[str, urllib.robotparser.RobotFileParser] = {}
    last_request: dict[str, float] = {}
    results: list[DownloadedSource] = []
    skipped: list[dict[str, str]] = []

    while queue and len(results) < args.max_pages:
        url, depth = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        if not args.cross_host and host_key(url) not in seed_hosts:
            skipped.append({"url": url, "reason": "cross-host"})
            continue
        copyright_risk = copyright_risk_reason(url)
        if copyright_risk:
            skipped.append({"url": url, "reason": copyright_risk})
            continue
        try:
            robot = robots_cache.get(host_key(url))
            if robot is None:
                robot = fetch_robots(url, args.user_agent, args.timeout)
                robots_cache[host_key(url)] = robot
            if not robot.can_fetch(args.user_agent, url):
                skipped.append({"url": url, "reason": "blocked-by-robots"})
                continue
            wait_for_host(url, last_request, args.delay)
            content, content_type = fetch_url(url, args.user_agent, args.timeout, args.max_bytes)
            results.append(
                write_download(
                    url=url,
                    content=content,
                    content_type=content_type,
                    vault=vault,
                    raw_dir=raw_dir,
                    manifest_dir=manifest_dir,
                    domain=args.domain,
                    permission=args.permission,
                    sensitivity=args.sensitivity,
                    force=args.force,
                    dry_run=args.dry_run,
                )
            )
            if depth < args.max_depth:
                for link in extract_links(url, content, content_type):
                    if link not in seen:
                        queue.append((link, depth + 1))
        except Exception as error:  # noqa: BLE001 - report per-URL failures.
            skipped.append({"url": url, "reason": str(error)})

    return report(vault, results, skipped)


def report(
    vault: Path,
    results: list[DownloadedSource],
    skipped: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "ok": not skipped,
        "vault": str(vault),
        "downloaded_count": len(results),
        "skipped_count": len(skipped),
        "downloads": [
            {
                "url": item.url,
                "source_id": item.source_id,
                "sha256": item.sha256,
                "content_type": item.content_type,
                "size_bytes": item.size_bytes,
                "raw_path": display_path(item.raw_path, vault),
                "manifest_path": display_path(item.manifest_path, vault),
                "status": item.status,
            }
            for item in results
        ],
        "skipped": skipped,
    }


def print_report(data: dict[str, object]) -> None:
    print(
        f"Source download: {data['downloaded_count']} downloaded, "
        f"{data['skipped_count']} skipped"
    )
    for item in data["downloads"]:
        print(f"{item['status'].upper()}: {item['url']}")
        print(f"  raw: {item['raw_path']}")
        print(f"  manifest: {item['manifest_path']}")
    for item in data["skipped"]:
        print(f"SKIPPED: {item['url']} ({item['reason']})")


def main() -> int:
    args = parse_args()
    if args.command == "download":
        urls = list(args.urls)
        if args.url_file:
            urls.extend(load_url_file(args.url_file))
        data = download_urls(args, urls)
    elif args.command == "crawl":
        data = crawl_urls(args)
    else:
        raise ValueError(f"Unknown command: {args.command}")

    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print_report(data)

    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
