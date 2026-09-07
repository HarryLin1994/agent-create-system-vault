#!/usr/bin/env python3
"""Find public source candidates for a domain knowledge pack."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from agent_retrieve import as_list, split_frontmatter
from ingest_sources import display_path, slugify


BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
OPEN_LIBRARY_ENDPOINT = "https://openlibrary.org/search.json"
GOOGLE_BOOKS_ENDPOINT = "https://www.googleapis.com/books/v1/volumes"
OREILLY_SEARCH_ENDPOINT = "https://learning.oreilly.com/api/v2/search/"
QUEUE_DEFAULT = Path("00_Inbox") / "Web Source Queue.md"
REPORT_DEFAULT = Path("00_Inbox") / "Public Source Searches"
DEFAULT_USER_AGENT = "agent-create-system-vault/0.1 (+public source discovery)"
URL_RE = re.compile(r"https?://[^\s)\]>\"']+")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
TABLE_ROW_RE = re.compile(r"^\s*\|(?P<cells>.+)\|\s*$")
SPLIT_RE = re.compile(r"\s*(?:,|;|<br\s*/?>|\u3001)\s*", re.IGNORECASE)

KNOWN_OFFICIAL_HOSTS = {
    "developer.mozilla.org",
    "developers.google.com",
    "docs.aws.amazon.com",
    "amazon.com",
    "learn.microsoft.com",
    "nist.gov",
    "nsf.gov",
    "oreilly.com",
    "openai.com",
    "openlibrary.org",
    "platform.openai.com",
    "w3.org",
}

LOW_TRUST_HOSTS = {
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "medium.com",
    "pinterest.com",
    "quora.com",
    "reddit.com",
    "substack.com",
    "tiktok.com",
    "twitter.com",
    "x.com",
    "youtube.com",
}

RESTRICTED_MARKERS = {
    "account",
    "captcha",
    "checkout",
    "login",
    "paywall",
    "register",
    "signin",
    "signup",
    "subscribe",
    "subscription",
}

COPYRIGHT_RISK_HOST_PARTS = {
    "annas-archive",
    "libgen",
    "oceanofpdf",
    "pdfdrive",
    "z-lib",
    "zlibrary",
}

COPYRIGHT_RISK_MARKERS = {
    "download epub",
    "download full book",
    "download mobi",
    "download pdf",
    "epub download",
    "free ebook download",
    "free epub",
    "free pdf",
    "full book pdf",
    "full pdf",
    "mobi download",
    "pdf download",
    "pirated",
    "torrent",
}


@dataclass(frozen=True)
class SearchResult:
    query: str
    title: str
    url: str
    description: str
    rank: int
    provider: str


@dataclass(frozen=True)
class BookTarget:
    title: str
    author: str


@dataclass(frozen=True)
class SourceCandidate:
    query: str
    title: str
    url: str
    description: str
    rank: int
    provider: str
    host: str
    source_kind: str
    public_likelihood: str
    trust_score: int
    recommendation: str
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Find public source candidates, score them for source quality, "
            "and optionally append them to the Web Source Queue."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search one or more explicit queries.")
    search.add_argument("queries", nargs="+", help="Search query text.")
    add_common_args(search)

    from_pack = subparsers.add_parser(
        "from-pack",
        help="Generate source-discovery queries from a knowledge pack.",
    )
    from_pack.add_argument("pack", help="Knowledge pack path, title, or pack_name.")
    from_pack.add_argument(
        "--max-queries",
        type=int,
        default=12,
        help="Maximum generated queries to send to the search provider.",
    )
    from_pack.add_argument(
        "--no-pack-urls",
        action="store_true",
        help="Do not include external URLs already listed in the pack as candidates.",
    )
    from_pack.add_argument(
        "--extra-query",
        action="append",
        default=[],
        help="Additional query to run. May be repeated.",
    )
    add_common_args(from_pack)

    books = subparsers.add_parser(
        "books",
        help="Find public metadata and legal access candidates for book sources.",
    )
    books.add_argument(
        "--book",
        action="append",
        default=[],
        help='Book target as "Title | Author". May be repeated.',
    )
    books.add_argument(
        "--book-file",
        help='Plain text file with one "Title | Author" book target per line.',
    )
    books.add_argument(
        "--connector",
        action="append",
        choices=("web", "openlibrary", "google-books", "oreilly", "amazon"),
        default=[],
        help=(
            "Book connector to use. May be repeated. Defaults to all connectors. "
            "O'Reilly API requires OREILLY_API_TOKEN; Amazon returns reviewable "
            "bookstore candidates unless a future API adapter is added."
        ),
    )
    books.add_argument(
        "--no-web-queries",
        action="store_true",
        help="Do not add ordinary web-search queries for book targets.",
    )
    add_common_args(books)

    return parser.parse_args()


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--vault",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the Obsidian vault.",
    )
    parser.add_argument(
        "--provider",
        choices=("auto", "brave", "queries-only"),
        default="auto",
        help=(
            "Search provider. auto uses Brave Search API when BRAVE_SEARCH_API_KEY "
            "is set, otherwise prints manual queries."
        ),
    )
    parser.add_argument(
        "--count",
        type=int,
        default=8,
        help="Search results per query. Brave allows up to 20 per request.",
    )
    parser.add_argument("--country", default="US", help="Search country code.")
    parser.add_argument("--search-lang", default="en", help="Search language code.")
    parser.add_argument("--timeout", type=float, default=20.0, help="HTTP timeout.")
    parser.add_argument(
        "--insecure-skip-tls-verify",
        action="store_true",
        help=(
            "Development fallback for local Python CA issues. Disables TLS "
            "certificate verification for provider requests."
        ),
    )
    parser.add_argument(
        "--user-agent",
        default=DEFAULT_USER_AGENT,
        help="HTTP user agent for provider requests.",
    )
    parser.add_argument(
        "--domain",
        default="",
        help="Domain slug to use when writing Web Source Queue rows.",
    )
    parser.add_argument(
        "--site",
        action="append",
        default=[],
        help="Add site:host query scoping. May be repeated.",
    )
    parser.add_argument(
        "--trusted-host",
        action="append",
        default=[],
        help="Host treated as a primary/official source. May be repeated.",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=55,
        help="Minimum trust score for queue/report recommendation.",
    )
    parser.add_argument(
        "--queue",
        action="store_true",
        help="Append recommended candidates to Web Source Queue.",
    )
    parser.add_argument(
        "--queue-limit",
        type=int,
        default=10,
        help="Maximum candidates to append when --queue is used.",
    )
    parser.add_argument(
        "--queue-file",
        default=str(QUEUE_DEFAULT),
        help="Queue file, relative to vault unless absolute.",
    )
    parser.add_argument(
        "--permission",
        default="needs-review",
        help="Permission label for queued candidates.",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Write a human-checkpoint Markdown report.",
    )
    parser.add_argument(
        "--report-dir",
        default=str(REPORT_DEFAULT),
        help="Report directory, relative to vault unless absolute.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")


def resolve_under_vault(vault: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else vault / path


def urlopen_request(
    request: urllib.request.Request,
    timeout: float,
    insecure_skip_tls_verify: bool,
):
    if insecure_skip_tls_verify:
        return urllib.request.urlopen(
            request,
            timeout=timeout,
            context=ssl._create_unverified_context(),
        )
    return urllib.request.urlopen(request, timeout=timeout)


def normalize_url(url: str) -> str:
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


def host_for(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.lower()


def host_matches(host: str, known_host: str) -> bool:
    clean = known_host.strip().lower().removeprefix("www.")
    candidate = host.removeprefix("www.")
    return candidate == clean or candidate.endswith(f".{clean}")


def official_or_public_institution_host(host: str) -> bool:
    return (
        host.endswith(".gov")
        or host.endswith(".edu")
        or any(host_matches(host, official) for official in KNOWN_OFFICIAL_HOSTS)
    )


def markdown_body(path: Path) -> tuple[dict[str, object], str]:
    return split_frontmatter(path.read_text(encoding="utf-8"))


def first_heading(body: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", body, re.MULTILINE)
    return match.group(1).strip() if match else ""


def all_pack_paths(vault: Path) -> list[Path]:
    pack_root = vault / "02_Domain-Knowledge" / "Packs"
    if not pack_root.exists():
        return []
    return [
        path
        for path in sorted(pack_root.rglob("*.md"))
        if path.name.lower() != "readme.md"
    ]


def resolve_pack(vault: Path, value: str) -> Path | None:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = vault / candidate
    if candidate.exists() and candidate.is_file():
        return candidate.resolve()

    target = value.strip().lower()
    for path in all_pack_paths(vault):
        metadata, body = markdown_body(path)
        title = first_heading(body) or path.stem
        aliases = {
            path.stem.lower(),
            title.lower(),
            str(metadata.get("pack_name", "")).strip().lower(),
        }
        if target in aliases:
            return path.resolve()
    return None


def raw_section(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<section>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    return match.group("section") if match else ""


def normalize_cell(value: str) -> str:
    value = re.sub(r"<br\s*/?>", ";", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        match = TABLE_ROW_RE.match(line)
        if not match:
            continue
        cells = [normalize_cell(cell) for cell in match.group("cells").split("|")]
        if not cells:
            continue
        if all(set(cell) <= {"-", " "} for cell in cells):
            continue
        if cells[0].lower() in {"question", "source"}:
            continue
        if any(cells):
            rows.append(cells)
    return rows


def strip_markup(value: str) -> str:
    value = re.sub(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\((?:https?://[^)]+)\)", r"\1", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    return html.unescape(value).strip()


def split_query_terms(value: str) -> list[str]:
    terms: list[str] = []
    for item in SPLIT_RE.split(strip_markup(value)):
        clean = item.strip(" .:-")
        if clean and clean.lower() not in {"supported", "partial", "gap"}:
            terms.append(clean)
    return terms


def external_links(body: str) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for label, url in MARKDOWN_LINK_RE.findall(body):
        links.append((strip_markup(label), normalize_url(url)))
    seen: set[str] = {url for _, url in links}
    for url in URL_RE.findall(body):
        clean = normalize_url(url)
        if clean not in seen:
            links.append((host_for(clean), clean))
            seen.add(clean)
    return links


def generated_pack_queries(metadata: dict[str, object], body: str, max_queries: int) -> list[str]:
    raw_terms: list[str] = []
    raw_terms.append(str(metadata.get("pack_name", "")).strip())
    raw_terms.append(str(metadata.get("domain", "")).replace("-", " ").strip())
    raw_terms.extend(str(tag) for tag in as_list(metadata.get("tags", [])))

    for row in table_rows(raw_section(body, "Included Sources")):
        if row:
            raw_terms.extend(split_query_terms(row[0]))

    for row in table_rows(raw_section(body, "Golden Retrieval Questions")):
        if len(row) > 1:
            raw_terms.extend(split_query_terms(row[1]))

    queries: list[str] = []
    seen: set[str] = set()
    for term in raw_terms:
        clean = strip_markup(term)
        clean = re.sub(r"\s+", " ", clean).strip(" .:-")
        if not clean or len(clean) < 4:
            continue
        query = f"{clean} official primary source"
        key = query.lower()
        if key not in seen:
            queries.append(query)
            seen.add(key)
        if len(queries) >= max_queries:
            break
    return queries


def expand_site_queries(queries: list[str], sites: list[str]) -> list[str]:
    clean_queries = [query.strip() for query in queries if query.strip()]
    if not sites:
        return clean_queries
    scoped: list[str] = []
    for query in clean_queries:
        for site in sites:
            clean_site = site.strip().removeprefix("site:")
            if clean_site:
                scoped.append(f"site:{clean_site} {query}")
    return scoped


def provider_name(requested: str) -> str:
    if requested == "auto":
        return "brave" if os.environ.get("BRAVE_SEARCH_API_KEY") else "queries-only"
    return requested


def brave_search(
    query: str,
    count: int,
    country: str,
    search_lang: str,
    timeout: float,
    user_agent: str,
    insecure_skip_tls_verify: bool,
) -> list[SearchResult]:
    api_key = os.environ.get("BRAVE_SEARCH_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("BRAVE_SEARCH_API_KEY is required for --provider brave")

    params = urllib.parse.urlencode(
        {
            "q": query,
            "count": max(1, min(count, 20)),
            "country": country,
            "search_lang": search_lang,
            "safesearch": "moderate",
        }
    )
    request = urllib.request.Request(
        f"{BRAVE_ENDPOINT}?{params}",
        headers={
            "Accept": "application/json",
            "User-Agent": user_agent,
            "X-Subscription-Token": api_key,
        },
    )
    with urlopen_request(request, timeout, insecure_skip_tls_verify) as response:
        payload = json.loads(response.read().decode("utf-8"))

    results: list[SearchResult] = []
    for rank, item in enumerate(payload.get("web", {}).get("results", []), start=1):
        url = item.get("url")
        if not url:
            continue
        try:
            normalized = normalize_url(str(url))
        except ValueError:
            continue
        results.append(
            SearchResult(
                query=query,
                title=strip_html(str(item.get("title", ""))),
                url=normalized,
                description=strip_html(str(item.get("description", ""))),
                rank=rank,
                provider="brave",
            )
        )
    return results


def strip_html(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def parse_book_target(value: str) -> BookTarget:
    clean = re.sub(r"\s+", " ", value).strip()
    if not clean:
        raise ValueError("Book target cannot be empty.")
    if "|" in clean:
        title, author = (part.strip() for part in clean.split("|", 1))
    else:
        match = re.match(r"(.+?)\s+by\s+(.+)$", clean, flags=re.IGNORECASE)
        if not match:
            raise ValueError(f'Book target must be "Title | Author": {value}')
        title, author = match.group(1).strip(), match.group(2).strip()
    if not title or not author:
        raise ValueError(f'Book target must include title and author: {value}')
    return BookTarget(title=title, author=author)


def load_book_file(path: str) -> list[BookTarget]:
    books: list[BookTarget] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        clean = line.strip()
        if clean and not clean.startswith("#"):
            books.append(parse_book_target(clean))
    return books


def book_queries(targets: list[BookTarget]) -> list[str]:
    queries: list[str] = []
    for target in targets:
        queries.extend(
            [
                f'"{target.title}" "{target.author}" official book page',
                f'"{target.title}" "{target.author}" publisher page',
                f'"{target.title}" "{target.author}" interview summary official',
            ]
        )
    return queries


def selected_connectors(values: list[str]) -> set[str]:
    if values:
        return set(values)
    return {"web", "openlibrary", "google-books", "oreilly", "amazon"}


def openlibrary_results(
    target: BookTarget,
    count: int,
    timeout: float,
    user_agent: str,
    insecure_skip_tls_verify: bool,
) -> list[SearchResult]:
    params = urllib.parse.urlencode(
        {
            "title": target.title,
            "author": target.author,
            "fields": ",".join(
                (
                    "key",
                    "title",
                    "author_name",
                    "first_publish_year",
                    "publisher",
                    "isbn",
                    "ebook_access",
                    "has_fulltext",
                )
            ),
            "limit": max(1, min(count, 20)),
        }
    )
    request = urllib.request.Request(
        f"{OPEN_LIBRARY_ENDPOINT}?{params}",
        headers={"Accept": "application/json", "User-Agent": user_agent},
    )
    with urlopen_request(request, timeout, insecure_skip_tls_verify) as response:
        payload = json.loads(response.read().decode("utf-8"))

    results: list[SearchResult] = []
    for rank, item in enumerate(payload.get("docs", []), start=1):
        key = str(item.get("key", ""))
        if not key:
            continue
        authors = ", ".join(str(name) for name in item.get("author_name", [])[:3])
        publishers = ", ".join(str(name) for name in item.get("publisher", [])[:3])
        details = [
            f"authors={authors}" if authors else "",
            f"first_publish_year={item.get('first_publish_year', '')}",
            f"publishers={publishers}" if publishers else "",
            f"ebook_access={item.get('ebook_access', '')}",
            f"has_fulltext={item.get('has_fulltext', '')}",
        ]
        results.append(
            SearchResult(
                query=f"openlibrary:{target.title} {target.author}",
                title=str(item.get("title") or target.title),
                url=normalize_url(f"https://openlibrary.org{key}"),
                description="; ".join(part for part in details if part),
                rank=rank,
                provider="openlibrary",
            )
        )
    return results


def google_books_results(
    target: BookTarget,
    count: int,
    timeout: float,
    user_agent: str,
    insecure_skip_tls_verify: bool,
) -> list[SearchResult]:
    q = f'intitle:"{target.title}" inauthor:"{target.author}"'
    params = {
        "q": q,
        "maxResults": max(1, min(count, 20)),
        "projection": "lite",
        "printType": "books",
    }
    api_key = os.environ.get("GOOGLE_BOOKS_API_KEY", "").strip()
    if api_key:
        params["key"] = api_key
    request = urllib.request.Request(
        f"{GOOGLE_BOOKS_ENDPOINT}?{urllib.parse.urlencode(params)}",
        headers={"Accept": "application/json", "User-Agent": user_agent},
    )
    with urlopen_request(request, timeout, insecure_skip_tls_verify) as response:
        payload = json.loads(response.read().decode("utf-8"))

    results: list[SearchResult] = []
    for rank, item in enumerate(payload.get("items", []), start=1):
        info = item.get("volumeInfo", {})
        url = (
            info.get("canonicalVolumeLink")
            or info.get("infoLink")
            or info.get("previewLink")
        )
        if not url:
            continue
        authors = ", ".join(str(name) for name in info.get("authors", [])[:3])
        categories = ", ".join(str(name) for name in info.get("categories", [])[:3])
        description = "; ".join(
            part
            for part in (
                f"authors={authors}" if authors else "",
                f"publisher={info.get('publisher', '')}",
                f"published_date={info.get('publishedDate', '')}",
                f"categories={categories}" if categories else "",
                f"preview={info.get('previewLink', '')}",
            )
            if part
        )
        results.append(
            SearchResult(
                query=f"google-books:{target.title} {target.author}",
                title=str(info.get("title") or target.title),
                url=normalize_url(str(url)),
                description=description,
                rank=rank,
                provider="google-books",
            )
        )
    return results


def oreilly_results(
    target: BookTarget,
    count: int,
    timeout: float,
    user_agent: str,
    insecure_skip_tls_verify: bool,
) -> list[SearchResult]:
    token = os.environ.get("OREILLY_API_TOKEN", "").strip()
    query = f"{target.title} {target.author}"
    if not token:
        encoded = urllib.parse.quote_plus(query)
        return [
            SearchResult(
                query=f"oreilly-search-page:{query}",
                title=f"O'Reilly search: {target.title}",
                url=normalize_url(f"https://www.oreilly.com/search/?query={encoded}"),
                description=(
                    "Reviewable O'Reilly search page. Set OREILLY_API_TOKEN to use "
                    "the authenticated Learning API connector."
                ),
                rank=1,
                provider="oreilly-search-page",
            )
        ]

    params = urllib.parse.urlencode(
        {
            "q": query,
            "formats": "book",
            "page_size": max(1, min(count, 20)),
        }
    )
    scheme = os.environ.get("OREILLY_AUTH_SCHEME", "Token").strip() or "Token"
    request = urllib.request.Request(
        f"{OREILLY_SEARCH_ENDPOINT}?{params}",
        headers={
            "Accept": "application/json",
            "Authorization": f"{scheme} {token}",
            "User-Agent": user_agent,
        },
    )
    with urlopen_request(request, timeout, insecure_skip_tls_verify) as response:
        payload = json.loads(response.read().decode("utf-8"))

    raw_items = payload.get("results") or payload.get("items") or []
    results: list[SearchResult] = []
    for rank, item in enumerate(raw_items, start=1):
        url = item.get("web_url") or item.get("url") or item.get("canonical_url")
        if not url:
            archive_id = item.get("archive_id") or item.get("id")
            if archive_id:
                url = f"https://learning.oreilly.com/library/view/{archive_id}/"
        if not url:
            continue
        if str(url).startswith("/"):
            url = f"https://learning.oreilly.com{url}"
        authors = item.get("authors") or item.get("author") or ""
        if isinstance(authors, list):
            authors = ", ".join(str(author) for author in authors[:3])
        description = "; ".join(
            part
            for part in (
                f"authors={authors}" if authors else "",
                f"publisher={item.get('publisher', '')}",
                f"issued={item.get('issued', '') or item.get('published_date', '')}",
                f"format={item.get('format', '') or item.get('content_format', '')}",
            )
            if part
        )
        results.append(
            SearchResult(
                query=f"oreilly-api:{query}",
                title=strip_html(str(item.get("title") or item.get("name") or target.title)),
                url=normalize_url(str(url)),
                description=description,
                rank=rank,
                provider="oreilly-api",
            )
        )
    return results


def amazon_results(target: BookTarget) -> list[SearchResult]:
    query = f"{target.title} {target.author}"
    params = {"i": "stripbooks", "k": query}
    partner_tag = os.environ.get("AMAZON_PARTNER_TAG", "").strip()
    if partner_tag:
        params["tag"] = partner_tag
    url = f"https://www.amazon.com/s?{urllib.parse.urlencode(params)}"
    return [
        SearchResult(
            query=f"amazon-search-page:{query}",
            title=f"Amazon Books search: {target.title}",
            url=normalize_url(url),
            description=(
                "Reviewable Amazon Books search candidate. Official Amazon "
                "SearchItems API integration requires Amazon onboarding and "
                "partner credentials."
            ),
            rank=1,
            provider="amazon-search-page",
        )
    ]


def book_connector_results(
    targets: list[BookTarget],
    connectors: set[str],
    args: argparse.Namespace,
) -> tuple[list[SearchResult], list[str]]:
    results: list[SearchResult] = []
    errors: list[str] = []
    for target in targets:
        for connector in sorted(connectors):
            try:
                if connector == "web":
                    continue
                if connector == "openlibrary":
                    results.extend(
                        openlibrary_results(
                            target,
                            args.count,
                            args.timeout,
                            args.user_agent,
                            args.insecure_skip_tls_verify,
                        )
                    )
                elif connector == "google-books":
                    results.extend(
                        google_books_results(
                            target,
                            args.count,
                            args.timeout,
                            args.user_agent,
                            args.insecure_skip_tls_verify,
                        )
                    )
                elif connector == "oreilly":
                    results.extend(
                        oreilly_results(
                            target,
                            args.count,
                            args.timeout,
                            args.user_agent,
                            args.insecure_skip_tls_verify,
                        )
                    )
                elif connector == "amazon":
                    results.extend(amazon_results(target))
            except (OSError, urllib.error.URLError, urllib.error.HTTPError, RuntimeError, ValueError) as error:
                errors.append(f"{connector}:{target.title}: {error}")
    return results, errors


def source_kind(host: str, trusted_hosts: set[str]) -> str:
    if any(host_matches(host, trusted) for trusted in trusted_hosts):
        return "known-primary"
    if host.endswith(".gov") or ".gov." in host:
        return "official-government"
    if host.endswith(".edu") or ".edu." in host:
        return "academic"
    if any(host_matches(host, official) for official in KNOWN_OFFICIAL_HOSTS):
        return "official-docs"
    if any(host_matches(host, low) for low in LOW_TRUST_HOSTS):
        return "social-or-user-generated"
    if host.endswith(".org") or ".org." in host:
        return "organization"
    return "commercial-or-general"


def public_likelihood(url: str, title: str, description: str) -> str:
    if copyright_risk_reason(url, title, description):
        return "copyright-risk"
    lower = " ".join((url, title, description)).lower()
    if any(marker in lower for marker in RESTRICTED_MARKERS):
        return "likely-restricted"
    if lower.endswith(".pdf") or ".pdf?" in lower:
        return "likely-public"
    host = host_for(url)
    if any(host_matches(host, restricted) for restricted in {"learning.oreilly.com"}):
        return "likely-restricted"
    if official_or_public_institution_host(host):
        return "likely-public"
    return "needs-review"


def copyright_risk_reason(url: str, title: str = "", description: str = "") -> str:
    host = host_for(url)
    if official_or_public_institution_host(host):
        return ""
    host_text = host.removeprefix("www.")
    for marker in COPYRIGHT_RISK_HOST_PARTS:
        if marker in host_text:
            return f"copyright-risk-host={marker}"
    text = " ".join((url, title, description)).lower()
    for marker in COPYRIGHT_RISK_MARKERS:
        if marker in text:
            return f"copyright-risk-marker={marker}"
    return ""


def trust_score(
    result: SearchResult,
    kind: str,
    public_label: str,
    trusted_hosts: set[str],
) -> int:
    host = host_for(result.url)
    score = 40
    if any(host_matches(host, trusted) for trusted in trusted_hosts):
        score += 30
    if result.provider in {"openlibrary", "google-books"}:
        score += 15
    elif result.provider == "oreilly-api":
        score += 20
    elif result.provider in {"oreilly-search-page", "amazon-search-page"}:
        score += 5
    if kind == "official-government":
        score += 30
    elif kind == "academic":
        score += 25
    elif kind == "official-docs":
        score += 25
    elif kind == "known-primary":
        score += 20
    elif kind == "organization":
        score += 8
    elif kind == "social-or-user-generated":
        score -= 30

    text = f"{result.title} {result.description} {result.url}".lower()
    if any(word in text for word in ("official", "documentation", "docs", "primary source")):
        score += 8
    if any(word in text for word in ("research", "report", "whitepaper", "paper")):
        score += 6
    if public_label == "likely-public":
        score += 10
    elif public_label == "likely-restricted":
        score -= 35
    elif public_label == "copyright-risk":
        score -= 70
    if result.rank <= 3:
        score += 5
    return max(0, min(score, 100))


def classify_result(
    result: SearchResult,
    trusted_hosts: set[str],
    min_score: int,
) -> SourceCandidate:
    host = host_for(result.url)
    kind = source_kind(host, trusted_hosts)
    public_label = public_likelihood(result.url, result.title, result.description)
    score = trust_score(result, kind, public_label, trusted_hosts)
    if public_label in {"likely-restricted", "copyright-risk"} or score < min_score:
        recommendation = "skip"
    elif score >= min_score + 15:
        recommendation = "queue"
    else:
        recommendation = "review"
    reason = (
        f"{kind}; {public_label}; trust_score={score}; "
        f"found_by={result.provider}; query={result.query}"
    )
    return SourceCandidate(
        query=result.query,
        title=result.title,
        url=result.url,
        description=result.description,
        rank=result.rank,
        provider=result.provider,
        host=host,
        source_kind=kind,
        public_likelihood=public_label,
        trust_score=score,
        recommendation=recommendation,
        reason=reason,
    )


def direct_candidates_from_links(
    links: list[tuple[str, str]],
    trusted_hosts: set[str],
    min_score: int,
) -> list[SourceCandidate]:
    candidates: list[SourceCandidate] = []
    for rank, (label, url) in enumerate(links, start=1):
        result = SearchResult(
            query="pack-listed-url",
            title=label or host_for(url),
            url=url,
            description="External URL already listed in the knowledge pack.",
            rank=rank,
            provider="pack",
        )
        candidates.append(classify_result(result, trusted_hosts, min_score))
    return candidates


def dedupe_candidates(candidates: list[SourceCandidate]) -> list[SourceCandidate]:
    best: dict[str, SourceCandidate] = {}
    for candidate in candidates:
        current = best.get(candidate.url)
        if current is None:
            best[candidate.url] = candidate
            continue
        if (candidate.trust_score, -candidate.rank) > (current.trust_score, -current.rank):
            best[candidate.url] = candidate
    return sorted(
        best.values(),
        key=lambda item: (-item.trust_score, item.recommendation != "queue", item.rank, item.url),
    )


def search_provider(args: argparse.Namespace, queries: list[str]) -> tuple[str, list[SearchResult], list[str]]:
    provider = provider_name(args.provider)
    if provider == "queries-only":
        return provider, [], []

    errors: list[str] = []
    results: list[SearchResult] = []
    for query in queries:
        try:
            if provider == "brave":
                results.extend(
                    brave_search(
                        query=query,
                        count=args.count,
                        country=args.country,
                        search_lang=args.search_lang,
                        timeout=args.timeout,
                        user_agent=args.user_agent,
                        insecure_skip_tls_verify=args.insecure_skip_tls_verify,
                    )
                )
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        except (OSError, urllib.error.URLError, urllib.error.HTTPError, RuntimeError, ValueError) as error:
            errors.append(f"{query}: {error}")
    return provider, results, errors


def candidate_dict(candidate: SourceCandidate) -> dict[str, object]:
    return {
        "query": candidate.query,
        "title": candidate.title,
        "url": candidate.url,
        "description": candidate.description,
        "rank": candidate.rank,
        "provider": candidate.provider,
        "host": candidate.host,
        "source_kind": candidate.source_kind,
        "public_likelihood": candidate.public_likelihood,
        "trust_score": candidate.trust_score,
        "recommendation": candidate.recommendation,
        "reason": candidate.reason,
    }


def escape_table_cell(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value.replace("|", "\\|")


def existing_queue_urls(text: str) -> set[str]:
    return {normalize_url(match) for match in URL_RE.findall(text)}


def append_to_queue(
    vault: Path,
    queue_file: str,
    candidates: list[SourceCandidate],
    domain: str,
    permission: str,
    limit: int,
) -> dict[str, object]:
    queue_path = resolve_under_vault(vault, queue_file)
    text = queue_path.read_text(encoding="utf-8")
    existing = existing_queue_urls(text)
    rows: list[str] = []
    skipped_duplicates: list[str] = []

    for candidate in candidates:
        if len(rows) >= limit:
            break
        if candidate.recommendation not in {"queue", "review"}:
            continue
        if candidate.url in existing:
            skipped_duplicates.append(candidate.url)
            continue
        row_domain = domain.strip() or "needs-domain-review"
        reason = f"{candidate.title}: {candidate.reason}"
        rows.append(
            "| "
            + " | ".join(
                (
                    escape_table_cell(candidate.url),
                    escape_table_cell(row_domain),
                    escape_table_cell(reason),
                    escape_table_cell(permission),
                    "candidate",
                )
            )
            + " |"
        )
        existing.add(candidate.url)

    if rows:
        insertion = "\n".join(rows) + "\n"
        match = re.search(r"\n##\s+Commands\s*$", text, re.MULTILINE)
        if match:
            insert_at = match.start()
            prefix = "" if text[:insert_at].endswith("\n") else "\n"
            text = text[:insert_at] + prefix + insertion + text[insert_at:]
        else:
            text = text.rstrip() + "\n" + insertion
        today = datetime.now(timezone.utc).date().isoformat()
        text = re.sub(r"updated:\s*\d{4}-\d{2}-\d{2}", f"updated: {today}", text, count=1)
        queue_path.write_text(text, encoding="utf-8")

    return {
        "queue_path": display_path(queue_path, vault),
        "queued_count": len(rows),
        "duplicate_count": len(skipped_duplicates),
        "duplicates": skipped_duplicates,
    }


def write_markdown_report(
    vault: Path,
    report_dir: str,
    domain: str,
    provider: str,
    queries: list[str],
    candidates: list[SourceCandidate],
    errors: list[str],
) -> str:
    target_dir = resolve_under_vault(vault, report_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    stem = slugify(domain or "public-source-search")
    report_path = target_dir / f"{timestamp}-{stem}.md"
    today = datetime.now(timezone.utc).date().isoformat()
    lines = [
        "---",
        "type: public-source-search-report",
        "status: needs-human-checkpoint",
        "tags: [web-sources, public-source-search, ingestion]",
        "reliability: draft",
        f"domain: {domain or 'needs-domain-review'}",
        f"updated: {today}",
        "---",
        "",
        f"# Public Source Search - {domain or 'Needs Domain Review'}",
        "",
        "## One-line Summary",
        "",
        "Human-checkpoint report for public source candidates discovered before ingestion.",
        "",
        "## Search Inputs",
        "",
        f"- Provider: {provider}",
        f"- Query count: {len(queries)}",
        "",
        "| Query |",
        "| --- |",
    ]
    lines.extend(f"| {escape_table_cell(query)} |" for query in queries)
    lines.extend(
        [
            "",
            "## Candidates",
            "",
            "| Score | Recommendation | Kind | Public | URL | Title | Reason |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for candidate in candidates:
        lines.append(
            "| "
            + " | ".join(
                (
                    str(candidate.trust_score),
                    escape_table_cell(candidate.recommendation),
                    escape_table_cell(candidate.source_kind),
                    escape_table_cell(candidate.public_likelihood),
                    escape_table_cell(candidate.url),
                    escape_table_cell(candidate.title),
                    escape_table_cell(candidate.reason),
                )
            )
            + " |"
        )
    if errors:
        lines.extend(["", "## Provider Errors", "", "| Error |", "| --- |"])
        lines.extend(f"| {escape_table_cell(error)} |" for error in errors)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return display_path(report_path, vault)


def print_report(data: dict[str, object]) -> None:
    print(
        f"Source search: provider={data['provider']}, "
        f"{data['candidate_count']} candidates, {data['query_count']} queries"
    )
    if data["provider"] == "queries-only":
        print("No BRAVE_SEARCH_API_KEY found; run these queries manually or set the key.")
        for query in data["queries"]:
            print(f"QUERY: {query}")
    for candidate in data["candidates"]:
        print(
            f"{candidate['trust_score']:>3} {candidate['recommendation'].upper()} "
            f"{candidate['source_kind']} {candidate['public_likelihood']}: "
            f"{candidate['url']}"
        )
        if candidate["title"]:
            print(f"    {candidate['title']}")
    if data.get("queue"):
        queue = data["queue"]
        print(
            f"Queued {queue['queued_count']} candidates "
            f"({queue['duplicate_count']} duplicates) in {queue['queue_path']}"
        )
    if data.get("report_path"):
        print(f"Report: {data['report_path']}")
    for error in data["errors"]:
        print(f"ERROR: {error}")


def build_search_inputs(args: argparse.Namespace, vault: Path) -> tuple[str, list[str], list[tuple[str, str]], set[str], list[str]]:
    trusted_hosts = {host.strip().lower() for host in args.trusted_host if host.strip()}
    pack_links: list[tuple[str, str]] = []
    domain = args.domain.strip()

    if args.command == "search":
        queries = list(args.queries)
    elif args.command == "from-pack":
        pack_path = resolve_pack(vault, args.pack)
        if pack_path is None:
            raise ValueError(f"Knowledge pack not found: {args.pack}")
        metadata, body = markdown_body(pack_path)
        if not domain:
            domain = str(metadata.get("domain", "")).strip()
        pack_links = [] if args.no_pack_urls else external_links(raw_section(body, "Included Sources"))
        trusted_hosts.update(host_for(url) for _, url in pack_links)
        queries = generated_pack_queries(metadata, body, args.max_queries)
        queries.extend(args.extra_query)
    elif args.command == "books":
        books = [parse_book_target(value) for value in args.book]
        if args.book_file:
            books.extend(load_book_file(args.book_file))
        if not books:
            raise ValueError('At least one --book "Title | Author" is required.')
        trusted_hosts.update(
            {
                "amazon.com",
                "books.google.com",
                "google.com",
                "openlibrary.org",
                "oreilly.com",
            }
        )
        queries = [] if args.no_web_queries else book_queries(books)
    else:
        raise ValueError(f"Unknown command: {args.command}")

    queries = expand_site_queries(queries, args.site)
    manual_urls = [
        f"https://search.brave.com/search?q={urllib.parse.quote_plus(query)}"
        for query in queries
    ]
    return domain, queries, pack_links, trusted_hosts, manual_urls


def main() -> int:
    args = parse_args()
    vault = Path(args.vault).resolve()

    try:
        domain, queries, pack_links, trusted_hosts, manual_urls = build_search_inputs(args, vault)
    except ValueError as error:
        print(f"ERROR: {error}")
        return 1

    provider, raw_results, errors = search_provider(args, queries)
    if args.command == "books":
        book_targets = [parse_book_target(value) for value in args.book]
        if args.book_file:
            book_targets.extend(load_book_file(args.book_file))
        connector_results, connector_errors = book_connector_results(
            book_targets,
            selected_connectors(args.connector),
            args,
        )
        raw_results.extend(connector_results)
        errors.extend(connector_errors)
    candidates = direct_candidates_from_links(pack_links, trusted_hosts, args.min_score)
    candidates.extend(
        classify_result(result, trusted_hosts, args.min_score)
        for result in raw_results
    )
    candidates = dedupe_candidates(candidates)

    queue_report: dict[str, object] | None = None
    if args.queue:
        queue_report = append_to_queue(
            vault=vault,
            queue_file=args.queue_file,
            candidates=candidates,
            domain=domain,
            permission=args.permission,
            limit=args.queue_limit,
        )

    report_path = ""
    if args.report:
        report_path = write_markdown_report(
            vault=vault,
            report_dir=args.report_dir,
            domain=domain,
            provider=provider,
            queries=queries,
            candidates=candidates,
            errors=errors,
        )

    data: dict[str, object] = {
        "ok": not errors,
        "vault": str(vault),
        "provider": provider,
        "domain": domain,
        "query_count": len(queries),
        "queries": queries,
        "manual_search_urls": manual_urls,
        "candidate_count": len(candidates),
        "candidates": [candidate_dict(candidate) for candidate in candidates],
        "queue": queue_report,
        "report_path": report_path,
        "errors": errors,
    }

    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print_report(data)

    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
