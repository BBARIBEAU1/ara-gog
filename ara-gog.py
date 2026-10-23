#!/usr/bin/env python3

import argparse
import requests
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="ara-gog: threaded web directory enumerator")
parser.add_argument("url", help="Base URL, e.g. http://127.0.0.1:8000")
parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads")
parser.add_argument("-x", "--extensions", default="", help="Comma-separated extensions, e.g. bak,txt,php")
parser.add_argument("-r", "--recursive", action="store_true", help="Also enumerate inside found directories")
args = parser.parse_args()

base_url = args.url.rstrip("/")

with open(args.wordlist) as f:
    words = [line.strip() for line in f if line.strip()]

exts = [e.strip().lstrip(".") for e in args.extensions.split(",") if e.strip()]

candidates = []
for w in words:
    candidates.append(w)
    for e in exts:
        candidates.append(f"{w}.{e}")

found_dirs = []

def check(path):
    url = f"{base_url}/{path}"
    try:
        r = requests.get(url, timeout=3, allow_redirects=False)
    except requests.RequestException:
        return
    if r.status_code != 404:
        location = r.headers.get("Location", "")
        extra = f" -> {location}" if r.status_code in (301, 302) else ""
        print(f"[{r.status_code}] /{path}{extra}")
        if r.status_code in (301, 302) and location.endswith("/"):
            found_dirs.append(path)

def run(paths):
    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        pool.map(check, paths)

print(f"Enumerating {base_url} with {len(candidates)} paths...")
run(candidates)

if args.recursive:
    for d in list(found_dirs):
        print(f"--- inside /{d}/ ---")
        run([f"{d}/{c}" for c in candidates])

print("Done.")
