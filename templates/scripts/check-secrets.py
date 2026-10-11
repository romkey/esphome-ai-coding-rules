#!/usr/bin/env python3
"""Pre-commit check that keeps ESPHome secrets out of the repo.

    scripts/check-secrets.py FILE...

Fails, naming the file and line but never printing a secret, when:

1. A value from a local secrets.yaml (gitignored, so only on your machine)
   appears in any file being committed: a real Wi-Fi password pasted into
   a README, an example or a log excerpt.
2. An ESPHome config sets a sensitive option (password, ssid, key, ...) to
   a literal value instead of !secret or a ${substitution}.
3. A published firmware config (firmware/) uses !secret at all: published
   images must contain no credentials.

secrets.yaml.example holds dummy values and is exempt, and its values are
never treated as real secrets. Add "# not-a-secret" to a line to allow it.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOW = "not-a-secret"
# Real secrets shorter than this are too likely to match ordinary text.
MIN_SECRET_LENGTH = 6
SENSITIVE_KEYS = (
    "password|ssid|key|psk|passphrase|token|api_key|encryption_key"
    "|ota_password|ap_password|secret"
)
SENSITIVE = re.compile(
    rf"^\s*(?:-\s+)?(?P<key>{SENSITIVE_KEYS}):\s*(?P<value>[^#\n]*?)\s*(?:#.*)?$"
)
YAML = (".yaml", ".yml")


def parse_values(path: Path) -> dict[str, str]:
    """Top-level `key: value` pairs from a flat secrets file."""
    values = {}
    for line in path.read_text(errors="replace").splitlines():
        match = re.match(r"^([A-Za-z0-9_]+):\s*(.+?)\s*$", line)
        if match:
            values[match.group(1)] = match.group(2).strip("'\"")
    return values


def real_secrets() -> dict[str, str]:
    """Values from local secrets.yaml files, minus the example dummies."""
    dummies = set()
    for example in ROOT.glob("**/secrets.yaml.example"):
        dummies.update(parse_values(example).values())
    secrets = {}
    for path in ROOT.glob("**/secrets.yaml"):
        if ".esphome" in path.parts:
            continue
        for key, value in parse_values(path).items():
            if len(value) >= MIN_SECRET_LENGTH and value not in dummies:
                secrets[value] = key
    return secrets


def literal(value: str) -> bool:
    """True if a YAML value is a hard-coded literal rather than a reference."""
    if value in ("", "''", '""', "none", "null", "~", "true", "false"):
        return False
    if value.startswith(("!secret", "${", "!lambda", "!include", "|", ">")):
        return False
    # Nested mappings, e.g. "encryption:" followed by an indented block.
    return not value.endswith(":")


def check(path: Path, secrets: dict[str, str]) -> list[str]:
    try:
        text = path.read_text()
    except (UnicodeDecodeError, OSError):
        return []
    name = path.name
    rel = (
        path.resolve().relative_to(ROOT)
        if path.resolve().is_relative_to(ROOT)
        else path
    )
    is_config = name.endswith(YAML) and not name.startswith("secrets.")
    in_esphome_dir = rel.parts[:1] in (("examples",), ("firmware",), ("packages",))
    in_firmware = rel.parts[:1] == ("firmware",)
    problems = []
    for number, line in enumerate(text.splitlines(), 1):
        if ALLOW in line:
            continue
        where = f"{rel}:{number}"
        for value, key in secrets.items():
            if value in line:
                problems.append(f"{where}: contains the value of secrets.yaml '{key}'")
        if not (is_config and in_esphome_dir):
            continue
        if in_firmware and "!secret" in line:
            problems.append(f"{where}: published firmware must not use !secret")
        match = SENSITIVE.match(line)
        if match and literal(match.group("value")):
            problems.append(
                f"{where}: '{match.group('key')}' is hard-coded; use !secret or a ${{substitution}}"
            )
    return problems


def main(argv: list[str]) -> int:
    secrets = real_secrets()
    problems = []
    for name in argv:
        path = Path(name)
        if path.name == "secrets.yaml.example" or not path.is_file():
            continue
        problems.extend(check(path, secrets))
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(
            "Secrets check failed. If a real secret was committed or pushed, rotate it;"
            " removing it from history doesn't make it secret again.",
            file=sys.stderr,
        )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
