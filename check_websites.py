#!/usr/bin/env python3
"""Check whether the configured websites respond successfully."""


from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


WEBSITES = [
    "https://lepniglobal.com/",
    "https://www.fiorefashions.in/"
]
TIMEOUT_SECONDS = 15


def check_website(url: str) -> bool:
    """Print the result for a URL and return whether it is healthy."""
    request = Request(url, headers={"User-Agent": "WebsiteHealthCheck/1.0"})
    started = perf_counter()

    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            status = response.status
            elapsed = perf_counter() - started
            healthy = 200 <= status < 400
            result = "OK" if healthy else "FAILED"
            print(f"{result}: {url} — HTTP {status} ({elapsed:.2f}s)")
            return healthy
    except HTTPError as error:
        elapsed = perf_counter() - started
        print(f"FAILED: {url} — HTTP {error.code} ({elapsed:.2f}s)")
    except (URLError, TimeoutError, OSError) as error:
        elapsed = perf_counter() - started
        reason = getattr(error, "reason", error)
        print(f"FAILED: {url} — {reason} ({elapsed:.2f}s)")

    return False



def main() -> int:
    results = [(url, check_website(url)) for url in WEBSITES]
    failed_urls = [url for url, healthy in results if not healthy]
    passed = len(results) - len(failed_urls)


    overall = "PASSED" if not failed_urls else "FAILED"
    print(f"\nOverall result: {overall} ({passed}/{len(results)} websites responded successfully.)")
    print(f"Failed sites: {len(failed_urls)}")
    for number, url in enumerate(failed_urls, 1):
        print(f"  {number}. {url}")
    return 0 if not failed_urls else 1


if __name__ == "__main__":
    raise SystemExit(main())
