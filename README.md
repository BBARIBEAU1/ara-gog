# ara-gog

A multi-threaded web directory and file enumerator built with Python (requests, argparse, concurrent.futures).

## Usage
    ara-gog <url> -w <wordlist> [-t 20] [-x bak,txt,php] [-r]

## Example
    ara-gog http://127.0.0.1:8000 -w words.txt -x bak,txt -r

## Features
- Threaded requests for speed
- Extension brute-forcing (-x)
- One-level recursion into discovered directories (-r)
- Shows redirect targets and hides 404s

## What I learned
- HTTP status codes in enumeration (200 / 301 / 404) and why redirects must not be auto-followed
- Reading the target's server logs to see what defenders see
- List comprehensions, file handling, and reusing a thread pool
- Why wordlist + extensions drive both coverage and request volume

## Legal
Only enumerate systems you own or are explicitly authorized to test.
