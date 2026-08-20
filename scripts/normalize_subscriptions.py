#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import socket
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

import requests
import yaml

SUPPORTED_SCHEMES = ("vmess://", "vless://", "ss://", "trojan://")
GEO_FIELDS = "status,countryCode,query"


def padded_base64(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def flag(code: str) -> str:
    return "".join(chr(127397 + ord(letter)) for letter in code.upper())


def host_label(host: str) -> str:
    return host.removeprefix("www.").lower() or "unknown"


def resolve(host: str) -> tuple[str, str]:
    try:
        return host, socket.gethostbyname(host)
    except OSError:
        return host, ""


def country_codes(hosts: set[str]) -> dict[str, str]:
    resolved = dict(ThreadPoolExecutor(max_workers=32).map(resolve, hosts))
    addresses = sorted({address for address in resolved.values() if address})
    by_address: dict[str, str] = {}
    for start in range(0, len(addresses), 100):
        response = requests.post(
            f"http://ip-api.com/batch?fields={GEO_FIELDS}",
            json=addresses[start : start + 100],
            timeout=20,
        )
        response.raise_for_status()
        for item in response.json():
            if item.get("status") == "success":
                by_address[item["query"]] = item.get("countryCode", "ZZ")
    return {host: by_address.get(address, "ZZ") for host, address in resolved.items()}


def display_name(host: str, code: str, used: Counter[str]) -> str:
    base = f"{flag(code)}{code} - {host_label(host)}" if code != "ZZ" else f"🌐ZZ - {host_label(host)}"
    used[base] += 1
    return base if used[base] == 1 else f"{base} #{used[base]}"


def vmess_host(uri: str) -> str:
    payload = json.loads(padded_base64(uri.removeprefix("vmess://")).decode("utf-8"))
    return str(payload.get("add", ""))


def uri_host(uri: str) -> str:
    if uri.startswith("vmess://"):
        return vmess_host(uri)
    parsed = urlsplit(uri)
    if parsed.hostname:
        return parsed.hostname
    if uri.startswith("ss://") and "@" not in uri:
        decoded = padded_base64(uri[5:].split("#", 1)[0]).decode("utf-8")
        return urlsplit(f"//{decoded.rsplit('@', 1)[-1]}").hostname or ""
    return ""


def rename_uri(uri: str, name: str) -> str:
    if uri.startswith("vmess://"):
        payload = json.loads(padded_base64(uri.removeprefix("vmess://")).decode("utf-8"))
        payload["ps"] = name
        encoded = base64.b64encode(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).decode("ascii")
        return f"vmess://{encoded}"
    parsed = urlsplit(uri)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, quote(name)))


def normalize_uris(source: str) -> str:
    uris = [line.strip() for line in source.splitlines() if line.strip().startswith(SUPPORTED_SCHEMES)]
    hosts = {uri_host(uri) for uri in uris}
    codes = country_codes({host for host in hosts if host})
    used: Counter[str] = Counter()
    return "\n".join(rename_uri(uri, display_name(uri_host(uri), codes.get(uri_host(uri), "ZZ"), used)) for uri in uris) + "\n"


def normalize_clash(source: str) -> str:
    document = yaml.safe_load(source)
    if not isinstance(document, dict) or not isinstance(document.get("proxies"), list):
        raise ValueError("Clash source has no proxies list")
    hosts = {str(proxy.get("server", "")) for proxy in document["proxies"] if isinstance(proxy, dict)}
    codes = country_codes({host for host in hosts if host})
    used: Counter[str] = Counter()
    for proxy in document["proxies"]:
        if isinstance(proxy, dict):
            host = str(proxy.get("server", ""))
            proxy["name"] = display_name(host, codes.get(host, "ZZ"), used)
    return yaml.safe_dump(document, allow_unicode=True, sort_keys=False)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        raise SystemExit("Usage: normalize_subscriptions.py BASE64_INPUT CLASH_INPUT OUTPUT_DIRECTORY")
    base64_input, clash_input, output = map(Path, argv[1:])
    target = output
    target.mkdir(parents=True, exist_ok=True)
    raw_uris = padded_base64(base64_input.read_text(encoding="utf-8").strip()).decode("utf-8")
    normalized_uris = normalize_uris(raw_uris)
    (target / "base64.txt").write_text(base64.b64encode(normalized_uris.encode("utf-8")).decode("ascii") + "\n", encoding="ascii")
    (target / "clash.yaml").write_text(normalize_clash(clash_input.read_text(encoding="utf-8")), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
