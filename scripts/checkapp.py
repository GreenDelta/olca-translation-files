#!/usr/bin/env python3
"""Check the usage of the translation keys defined in M.java.

Usage:
    python3 checkapp.py path/to/openLCA/repos/olca-app

Run it with the path to the olca-app directory (the folder that contains the
`src` directory) as the only argument. The script then checks the M.java file
and the Java sources in that directory:

* For every key defined in M.java it reports whether it is actually referenced
  somewhere in the Java code (as `M.<Key>`).
* For every message file (messages*.properties) it reports the keys that are
  not defined in M.java and could be deleted.

Note: `M.getMap()` and `M.asJson()` reflectively read all fields of M, so those
are excluded from the usage check (they would otherwise mark every key as used).
"""

import argparse
import re
from collections import Counter
from pathlib import Path

FIELD_RE = re.compile(r"public\s+static\s+String\s+([A-Za-z0-9_]+)\s*;")
KEY_RE = re.compile(r"\bM\.([A-Za-z0-9_]+)\b")
PROP_RE = re.compile(r"^([A-Za-z0-9_]+)\s*=")

# A line that only contains a comment (line comments). The usage check must
# ignore these because keys in comments are not actual usages.
LINE_COMMENT_RE = re.compile(r"^\s*(//|/\*|\*|\*/)")


def strip_code(text: str) -> str:
    """Remove line comments, block comments and string literals from Java code
    so that keys mentioned there are not counted as usages."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            end = text.find("\n", i)
            i = n if end < 0 else end
        elif c == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            i = n if end < 0 else end + 2
        elif c == '"':
            i = _skip_string(text, i, '"')
        elif c == "'":
            i = _skip_string(text, i, "'")
        else:
            out.append(c)
            i += 1
    return "".join(out)


def _skip_string(text: str, start: int, quote: str) -> int:
    i = start + 1
    n = len(text)
    while i < n:
        if text[i] == "\\":
            i += 2
        elif text[i] == quote:
            return i + 1
        else:
            i += 1
    return n


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check the usage of the translation keys of M.java")
    parser.add_argument(
        "app", metavar="olca-app",
        help="path to the olca-app directory, e.g. path/to/openLCA/olca-app")
    return parser.parse_args()


def read_keys(m_path: Path) -> set:
    """The keys defined as public static String fields in M.java."""
    text = m_path.read_text(encoding="utf-8")
    return set(FIELD_RE.findall(text))


def read_usages(src: Path) -> Counter:
    """All `M.<Key>` references in the Java sources (M.java excluded)."""
    usages = Counter()
    for java in src.rglob("*.java"):
        if java.name == "M.java":
            continue
        text = java.read_text(encoding="utf-8", errors="replace")
        text = strip_code(text)
        usages.update(KEY_RE.findall(text))
    return usages


def read_property_keys(messages_dir: Path) -> dict:
    """The keys in each messages*.properties file."""
    result = {}
    for file in sorted(messages_dir.glob("messages*.properties")):
        keys = set()
        for line in file.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("#") or line.startswith("!"):
                continue
            m = PROP_RE.match(line)
            if m:
                keys.add(m.group(1))
        result[file.name] = keys
    return result


def main() -> None:
    args = parse_args()
    app = Path(args.app)
    src = app / "olca-app/src"
    m_path = src / "org/openlca/app/M.java"
    messages_dir = src / "org/openlca/app"

    if not m_path.is_file():
        print(f"No M.java file found at: {m_path}")
        return

    defined = read_keys(m_path)
    usages = read_usages(src)
    properties = read_property_keys(messages_dir)

    used = set(usages)
    unused = sorted(defined - used)
    external = sorted(used - defined)

    print(f"Keys defined in {m_path}: {len(defined)}")
    print(f"Keys referenced as M.<Key> in the Java code: {len(used)}")
    print()

    print(f"UNUSED keys (defined in M.java but never used): {len(unused)}")
    for key in unused:
        print(f"  {key}")
    print()

    print(f"Keys used but not defined in M.java: {len(external)}")
    for key in external:
        count = usages[key]
        print(f"  {key} ({count}x)")
    print()

    print("Keys in the message files that are NOT defined in M.java "
          "(could be deleted):")
    for name, keys in properties.items():
        orphans = sorted(keys - defined)
        print(f"  {name}: {len(orphans)}")
        for key in orphans:
            print(f"    {key}")


if __name__ == "__main__":
    main()
