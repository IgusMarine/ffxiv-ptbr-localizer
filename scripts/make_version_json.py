#!/usr/bin/env python3
"""Gera version.json (sha256+tamanho+versão) do .bin. Env: BIN_PATH (default
ffxiv_translations.bin), VERSION_OUT (default version.json)."""
import hashlib, json, os, datetime

BIN = os.environ.get("BIN_PATH", "ffxiv_translations.bin")
OUT = os.environ.get("VERSION_OUT", "version.json")

data = open(BIN, "rb").read()
now = datetime.datetime.now(datetime.timezone.utc)
ver = {
    "version": now.strftime("%Y.%m.%d.%H%M"),
    "sha256": hashlib.sha256(data).hexdigest(),
    "size": len(data),
    "builtAt": now.isoformat(),
}
json.dump(ver, open(OUT, "w", encoding="utf-8"), indent=2)
print(json.dumps(ver, indent=2))
