# ara-gog — Cheat Sheet

> Threaded web **directory/file** enumerator (`requests` + `ThreadPoolExecutor`) — a mini gobuster.
> Repo: <https://github.com/BBARIBEAU1/ara-gog> · Authorized labs / own hosts only.

## Install / run
```bash
# source: ~/projects/webenum/ara-gog.py   (needs: python3-requests)
chmod +x ~/projects/webenum/ara-gog.py
ln -sf ~/projects/webenum/ara-gog.py ~/.local/bin/ara-gog
ara-gog -h
```

## Syntax
```text
ara-gog <url> -w WORDLIST [-t THREADS] [-x ext1,ext2] [-r]
```

| Flag | Long | Default | Meaning |
|---|---|---|---|
| `url` | — | *(required)* | Base URL incl. scheme, e.g. `http://127.0.0.1:8000` (trailing `/` stripped) |
| `-w` | `--wordlist` | *(required)* | Wordlist file, one path per line |
| `-t` | `--threads` | `20` | Thread count |
| `-x` | `--extensions` | none | Comma list, e.g. `bak,txt,php` (leading `.` OK) |
| `-r` | `--recursive` | off | One level deeper into found dirs (301/302 → `.../`) |
| `-h` | `--help` | — | Usage |

## Examples
```bash
# lab target: cd ~/lab-site && python3 -m http.server 8000
ara-gog http://127.0.0.1:8000 -w ~/projects/webenum/words.txt
ara-gog http://127.0.0.1:8000 -w words.txt -x bak,txt           # word + word.bak + word.txt
ara-gog http://127.0.0.1:8000 -w words.txt -x bak,txt -r        # + one level of recursion
ara-gog http://localhost:8000 -w /usr/share/wordlists/dirb/common.txt -t 40
ara-gog http://127.0.0.1:8000/app -w words.txt                  # start under a sub-path
ara-gog http://127.0.0.1:8000 -w words.txt -r | tee enum.txt    # keep results (no -o flag)
```

## Output
```text
[200] /robots.txt
[301] /admin -> /admin/
--- inside /admin/ ---
[200] /admin/config.bak
```

## Workflow
1. **taran-tula** finds an HTTP port → `ara-gog http://host:port -w small.txt`.
2. Add `-x` for likely backups/configs (`bak,txt,old,php`).
3. `-r` once dirs show up; watch the server log (`http.server` terminal) to see the defender's view.

## Gotchas
- Shows **everything except 404**. Soft-404 / wildcard servers that return 200 for any path = wall of false hits.
- Redirects are **not followed** (by design). Recursion only triggers on 301/302 whose `Location` ends in `/`.
- `-r` is one level only, and reuses the full wordlist × extensions per found dir.
- Request count = `words × (1 + #extensions)` — `-x` multiplies traffic fast.
- 3 s timeout is hard-coded; timeouts/conn errors are dropped silently (no "error" line).
- Output order is unsorted (threads). URL needs `http://` or `https://`.
