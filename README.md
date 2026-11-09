# json-format

Pretty-print, minify, sort and validate JSON from a file or stdin — zero-dependency Python CLI.

## Install

Requires Python 3.8+. No third-party packages.

```bash
git clone https://github.com/heyzcx/json-format.git
cd json-format
chmod +x json_format.py
```

## Usage

```bash
# Pretty-print a file (default indent: 2)
python3 json_format.py data.json

# Read from stdin
cat data.json | python3 json_format.py

# Minify
python3 json_format.py --compact data.json

# Sort keys and write to a file
python3 json_format.py --sort-keys data.json -o pretty.json

# Only validate, print nothing on success
python3 json_format.py --validate data.json && echo OK

# JSON Lines: one JSON value per line
python3 json_format.py --jsonl lines.jsonl

# Custom indent, escape non-ASCII
python3 json_format.py --indent 4 --ensure-ascii data.json
```

## Options

| Option | Description |
| --- | --- |
| `input` | Input JSON file, or `-` / omitted for stdin |
| `-o, --output` | Output file, or `-` for stdout (default) |
| `--indent N` | Indent spaces for pretty output (default: 2) |
| `--compact` | Minify: emit the smallest valid JSON |
| `--sort-keys` | Sort object keys alphabetically |
| `--jsonl` | Treat input as JSON Lines |
| `--validate` | Only validate the input |
| `--ensure-ascii` | Escape non-ASCII as `\uXXXX` (default keeps UTF-8) |

## Exit codes

- `0` — success (or valid JSON with `--validate`)
- `1` — invalid JSON, or unreadable input / unwritable output
