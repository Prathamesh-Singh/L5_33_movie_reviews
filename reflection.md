# Reflection: Lab 5 Static Code Analysis

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest:** the Flake8 style issues (E225, E302, E261, E231) and Pylint's missing-docstring and naming warnings. Each one points to an exact line and has one obvious mechanical fix, like adding a space, a blank line or a docstring. Renaming to snake_case took a bit more care, because every call site in `main()` had to change too.

**Hardest:** the Bandit findings. To fix them I had to understand *why* the code was unsafe and what the code was meant to do:

- **MD5 (B324):** I had to choose between `sha256` and `md5(usedforsecurity=False)`. Switching to SHA-256 also changes the generated review ids.
- **`0.0.0.0` (B104):** I had to decide whether the service really needs to be reachable from other machines. I made localhost the safe default and kept an environment-variable override.
- **Hard-coded password (B105):** this needed a decision about where the secret should live, which is outside the code.
- **Global statement (W0603):** I had to check that nothing actually read `featured` before I removed it.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Partly, yes:

- **B311 (`random`):** picking a "featured movie of the day" is not a security decision, so standard `random` is perfectly adequate here. I still switched to `secrets.choice()`, because it costs nothing and clears the report.
- **B324 (MD5):** the hash is only used to build a short review id, not for passwords or integrity checks. The warning is technically a false positive in this context, but replacing MD5 is still good hygiene.

These cases show that a tool cannot know a function's *intent*. A developer has to judge whether each finding is a real risk.

## 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally:** run Flake8 and Pylint from the editor, and add a `pre-commit` hook running `flake8`, `pylint` and `bandit` so that problems are caught before a commit is made.
- **In CI:** add a GitHub Actions job that runs all three tools on every push and pull request. The build fails if Bandit reports any Medium/High issue, if Flake8 reports any error, or if the Pylint score drops below a threshold such as 9.5 (`--fail-under=9.5`).
- **Configuration:** keep a shared `.pylintrc` / `setup.cfg` / `.bandit` in the repository so everyone uses the same rules. Allow `# nosec` or `# pylint: disable=...` only with a comment explaining why.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Scores:** Pylint went from **5.47/10 to 10.00/10**. Bandit went from **4 issues (1 High, 1 Medium, 2 Low) to 0**. Flake8 went from **4 errors to 0**.
- **Security:** the code no longer uses a broken hash, no longer listens on all network interfaces by default, and no longer stores a password in the source.
- **Robustness:** `rate_movie()` no longer crashes with a `KeyError` on an unknown title. Removing the mutable global makes `pick_featured()` a simple function that is easy to test. The `if __name__ == "__main__":` guard means the module can be imported without running the demo.
- **Readability:** consistent snake_case names, docstrings on every function, `enumerate()` in place of index loops, and no redundant `else` make the code easier to read and maintain.
