#!/usr/bin/env python3
"""Dependency-free FunBlok smoke tester for GitHub Actions."""
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
import tempfile


class PageScanner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.ids = []
        self.inline_scripts = []
        self._script = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag.lower() == "script":
            self._script = None if attrs.get("src") else []

    def handle_data(self, data):
        if self._script is not None:
            self._script.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self._script is not None:
            source = "".join(self._script)
            if source.strip():
                self.inline_scripts.append(source)
            self._script = None


def main():
    root = Path(__file__).resolve().parents[1]
    page = root / "index.html"
    failures = []
    warnings = []
    if not page.is_file():
        print("FAIL  index.html exists")
        return 1

    html = page.read_text(encoding="utf-8")
    scan = PageScanner()
    scan.feed(html)
    scan.close()

    def check(condition, label, detail=""):
        mark = "PASS" if condition else "FAIL"
        print(f"{mark}  {label}" + (f" — {detail}" if detail else ""))
        if not condition:
            failures.append(label)

    check("<!doctype html>" in html.lower(), "HTML5 document declaration")
    check(bool(re.search(r"<title>[^<]+</title>", html, re.I)), "Page title exists")
    check(len(scan.inline_scripts) > 0, "Inline JavaScript found")
    check(len(scan.ids) > 0, "HTML element IDs found")

    duplicates = sorted({item for item in scan.ids if scan.ids.count(item) > 1})
    check(not duplicates, "No duplicate HTML IDs", ", ".join(duplicates[:12]))

    required_ids = [
        "header", "navlinks", "page-home", "page-games", "page-studio",
        "gamegrid", "gamegrid2", "studio-wrap", "authbox",
    ]
    missing = [item for item in required_ids if item not in scan.ids]
    check(not missing, "Core FunBlok UI elements", ", ".join(missing))

    required_features = {
        "account system": ("function signup(", "function login(", "function logout("),
        "game launcher": ("function launchGame(", "function showGameSelector("),
        "Studio tools": ("function placeBlock(", "function save("),
        "player/social system": ("function renderPlayers(", "function sendFriendRequest("),
        "shared-state sync": ("function startServerSync(", "function syncFromServer("),
        "legendary avatar colours": ("LEGENDARY GOLD", "VOID GALAXY", "PLASMA CORE", "INFERNO", "CELESTIAL"),
    }
    for feature, tokens in required_features.items():
        missing_tokens = [token for token in tokens if token not in html]
        check(not missing_tokens, feature, ", ".join(missing_tokens))

    node = subprocess.run(["node", "--version"], capture_output=True, text=True)
    check(node.returncode == 0, "Node.js available for JavaScript syntax checks")
    if node.returncode == 0:
        with tempfile.TemporaryDirectory(prefix="funblok-auto-test-") as temp_dir:
            for index, source in enumerate(scan.inline_scripts, start=1):
                js_file = Path(temp_dir) / f"inline-{index}.js"
                js_file.write_text(source, encoding="utf-8")
                result = subprocess.run(
                    ["node", "--check", str(js_file)],
                    capture_output=True, text=True,
                )
                if result.returncode:
                    failures.append(f"Inline JavaScript block {index} parses")
                    print(f"FAIL  Inline JavaScript block {index} parses")
                    print(result.stderr.strip())
            if not any(item.startswith("Inline JavaScript block") for item in failures):
                check(True, f"All {len(scan.inline_scripts)} inline JavaScript blocks parse")

    print()
    if failures:
        print(f"FUNBLOK AUTO TEST: FAILED ({len(failures)} failure(s))")
        return 1
    print("FUNBLOK AUTO TEST: ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
