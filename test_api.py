#!/usr/bin/env python3
"""Small, dependency-free HTTP smoke test for a DeutschlandGPT API endpoint."""

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Full API endpoint URL to test")
    parser.add_argument("--method", choices=("GET", "POST"), default="GET")
    parser.add_argument("--json", dest="json_body", help="Optional JSON request body")
    parser.add_argument("--token-env", default="DEUTSCHLANDGPT_API_KEY", help="Environment variable containing a bearer token")
    parser.add_argument("--timeout", type=float, default=20.0, help="Request timeout in seconds")
    args = parser.parse_args()

    headers = {"Accept": "application/json", "User-Agent": "dgpt-api-smoke-test/1.0"}
    token = os.getenv(args.token_env)
    if token:
        headers["Authorization"] = f"Bearer {token}"

    data = None
    if args.json_body is not None:
        try:
            data = json.dumps(json.loads(args.json_body)).encode("utf-8")
        except json.JSONDecodeError as exc:
            parser.error(f"--json must be valid JSON: {exc}")
        headers["Content-Type"] = "application/json"

    request = Request(args.url, data=data, headers=headers, method=args.method)
    try:
        with urlopen(request, timeout=args.timeout) as response:
            status = response.status
            body = response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        status = exc.code
        body = exc.read().decode("utf-8", errors="replace")
    except (URLError, TimeoutError, ValueError) as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 2

    print(f"HTTP {status}")
    if body:
        try:
            print(json.dumps(json.loads(body), indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(body)
    return 0 if 200 <= status < 300 else 1


if __name__ == "__main__":
    raise SystemExit(main())
