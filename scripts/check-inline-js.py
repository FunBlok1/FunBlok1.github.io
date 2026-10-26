#!/usr/bin/env python3
"""Run Node's parser against every inline JavaScript block in index.html."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import tempfile


class InlineScriptParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.current = None
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "script":
            return
        attrs = dict(attrs)
        self.current = None if attrs.get("src") else {
            "id": attrs.get("id") or f"inline-{len(self.scripts) + 1}",
            "parts": [],
        }

    def handle_data(self, data):
        if self.current is not None:
            self.current["parts"].append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.current is not None:
            source = "".join(self.current["parts"])
            if source.strip():
                self.scripts.append((self.current["id"], source))
            self.current = None


def main():
    root = Path(__file__).resolve().parents[1]
    html_path = root / "index.html"
    if not html_path.exists():
        print("ERROR: index.html was not found.")
        return 2

    parser = InlineScriptParser()
    parser.feed(html_path.read_text(encoding="utf-8"))
    if not parser.scripts:
        print("ERROR: no inline JavaScript blocks found.")
        return 2

    failures = []
    with tempfile.TemporaryDirectory(prefix="funblok-js-check-") as temp_dir:
        temp = Path(temp_dir)
        for number, (script_id, source) in enumerate(parser.scripts, start=1):
            js_path = temp / f"script-{number}.js"
            js_path.write_text(source, encoding="utf-8")
            result = subprocess.run(
                ["node", "--check", str(js_path)],
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode:
                failures.append((script_id, result.stderr.strip()))

    if failures:
        for script_id, error in failures:
            print(f"FAIL: {script_id}\n{error}\n")
        print(f"{len(failures)} of {len(parser.scripts)} inline scripts failed syntax checks.")
        return 1

    print(f"PASS: all {len(parser.scripts)} inline JavaScript blocks passed Node syntax checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
