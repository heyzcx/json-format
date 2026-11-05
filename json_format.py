#!/usr/bin/env python3
"""json-format: pretty-print, minify, sort and validate JSON.

Reads JSON from a file or stdin and writes the result to stdout or a file.
Also handles JSON Lines (one JSON value per line) with --jsonl.

Usage:
    python3 json_format.py data.json
    cat data.json | python3 json_format.py
    python3 json_format.py --compact data.json
    python3 json_format.py --sort-keys --indent 2 data.json -o pretty.json
    python3 json_format.py --jsonl lines.jsonl
    python3 json_format.py --validate data.json && echo OK

Exit codes: 0 on success, 1 on invalid JSON or unreadable input.
"""

import argparse
import json
import sys


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Pretty-print, minify, sort and validate JSON."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="Input JSON file, or '-' / omitted for stdin.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="-",
        help="Output file, or '-' for stdout (default).",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Indent spaces for pretty output (default: 2).",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Minify: emit the smallest valid JSON (no spaces).",
    )
    parser.add_argument(
        "--sort-keys",
        action="store_true",
        help="Sort object keys alphabetically.",
    )
    parser.add_argument(
        "--jsonl",
        action="store_true",
        help="Treat input as JSON Lines: one JSON value per line.",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Only validate the input; print nothing on success.",
    )
    parser.add_argument(
        "--ensure-ascii",
        action="store_true",
        help="Escape non-ASCII characters as \\uXXXX (default keeps UTF-8).",
    )
    return parser.parse_args(argv)


def read_text(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def format_value(value, args):
    if args.compact:
        return json.dumps(
            value,
            ensure_ascii=args.ensure_ascii,
            sort_keys=args.sort_keys,
            separators=(",", ":"),
        )
    return json.dumps(
        value,
        ensure_ascii=args.ensure_ascii,
        sort_keys=args.sort_keys,
        indent=args.indent,
    )


def process(text, args):
    """Parse and re-format the input text; returns the output string."""
    if args.jsonl:
        lines = []
        for lineno, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {lineno}: {exc}") from exc
            lines.append(format_value(value, args))
        return "\n".join(lines) + ("\n" if lines else "")
    value = json.loads(text)
    return format_value(value, args) + "\n"


def main(argv=None):
    args = parse_args(argv)
    try:
        text = read_text(args.input)
    except OSError as exc:
        print(f"json-format: cannot read input: {exc}", file=sys.stderr)
        return 1
    try:
        output = process(text, args)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"json-format: invalid JSON: {exc}", file=sys.stderr)
        return 1

    if args.validate:
        print("valid JSON", file=sys.stderr)
        return 0

    try:
        if args.output == "-":
            sys.stdout.write(output)
        else:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
    except OSError as exc:
        print(f"json-format: cannot write output: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
