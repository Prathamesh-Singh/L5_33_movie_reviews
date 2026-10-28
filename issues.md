# Issues Found and Fixed: `movie_reviews.py`

Tools: Pylint 10.00/10 (was 5.47/10), Bandit 0 issues (was 4), Flake8 0 issues (was 4).
Original reports are in `reports/before/`; the reports after the fixes are `pylint_report.txt`, `bandit_report.txt` and `flake8_report.txt`.

Line numbers refer to the original file.

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Weak MD5 hash | Bandit B324 | Security | High | 46 | `hashlib.md5()` is a broken hash algorithm (CWE-327). | Use `hashlib.sha256()` instead. |
| 2 | Binding to all interfaces | Bandit B104 | Security | Medium | 4 | `STREAM_HOST = "0.0.0.0"` exposes the service on every network interface (CWE-605). | Default to `127.0.0.1` (localhost only), and allow an override through the `STREAM_HOST` environment variable. |
| 3 | Hard-coded password | Bandit B105 | Security | Low | 6 | `MODERATOR_PASSWORD = "reviews-demo"` puts a secret in the source code (CWE-259). | Read it with `os.environ.get("MODERATOR_PASSWORD")`. |
| 4 | Insecure random generator | Bandit B311 | Security | Low | 41 | The `random` module is not suitable for anything security-sensitive (CWE-330). | Use `secrets.choice()`. |
| 5 | Mutable global state | Pylint W0603 | Bad practice / Bug risk | Medium | 8, 40 | `global featured` changes module state that nothing reads. | Remove the global and have `pick_featured()` just return the choice. |
| 6 | KeyError on unknown movie | Manual review (found while fixing) | Bug | Medium | 20 | `rateMovie()` crashes with `KeyError` if the title was never added. | Check `title not in movies`, print a message and return `False`. |
| 7 | Top-level `main()` call | Manual review / best practice | Bug risk | Low | 75 | Importing the module runs the demo as a side effect. | Wrap the call in `if __name__ == "__main__":`. |
| 8 | Non-snake_case names | Pylint C0103 | Style | Low | 11–58 | `addMovie`, `rateMovie`, `reviewText`, etc. break PEP 8 naming. | Rename to `add_movie`, `rate_movie`, `review_text`, etc. |
| 9 | Missing docstrings | Pylint C0114 / C0116 | Documentation | Low | 1, 11–58 | The module and its 9 functions have no docstrings. | Add a module docstring and a one-line docstring to each function. |
| 10 | Unnecessary `else` after `return` | Pylint R1705 | Refactor | Low | 28–31 | The `else:` is redundant. | Remove the `else` and de-indent `return 0.0`. |
| 11 | `range(len(...))` loop | Pylint C0200 | Refactor | Low | 50–51 | Loops by index instead of over the items. | Use `enumerate(movies, start=1)`. |
| 12 | Missing whitespace around operator | Flake8 E225 | Style | Low | 35 | `ranked=sorted(...)` | Change to `ranked = sorted(...)`. |
| 13 | Expected 2 blank lines | Flake8 E302 | Style | Low | 48 | Only 1 blank line before `def printAllReviews`. | Add a second blank line. |
| 14 | Inline comment spacing | Flake8 E261 | Style | Low | 70 | Only one space before `# demo id`. | Use two spaces before `#`. |
| 15 | Missing whitespace after `,` | Flake8 E231 | Style | Low | 72 | `"Genres:",sorted(...)` | Add a space after the comma. |

## Behaviour check

`python movie_reviews.py` prints the same output as before, with two intended differences:

- **Review id:** changes from `52e343ca87` (MD5) to `b8fc2faf6d` (SHA-256).
- **Streaming address:** changes from `0.0.0.0:8000` to `127.0.0.1:8000`.

The featured movie is random, so it can differ from run to run, both before and after the fixes.
