#!/usr/bin/env python3
"""
compile_from_supabase.py — Compila o ffxiv_translations.bin LENDO DO SUPABASE (nuvem),
sem precisar do banco local. Usado pela GitHub Action de publish.

Inclui: strings traduzidas (status machine/approved/in_review com ptbr) + string_variants
(variantes de gênero/condição). Dedup por inglês normalizado. Formato idêntico ao que o
plugin espera (Int32 LE + strings UTF-8 com tamanho 7-bit-prefixed).

Env: SUPABASE_URL, SUPABASE_SERVICE_KEY. Saída: BIN_OUT (default ffxiv_translations.bin).
"""
import os, re, struct, sys
import requests

sys.stdout.reconfigure(encoding="utf-8")
URL = os.environ["SUPABASE_URL"].rstrip("/")
KEY = os.environ["SUPABASE_SERVICE_KEY"]
OUT = os.environ.get("BIN_OUT", "ffxiv_translations.bin")
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Accept": "application/json"}


def fetch(path, select, extra=""):
    out, off, page = [], 0, 1000
    sess = requests.Session()
    while True:
        h = dict(H); h["Range-Unit"] = "items"; h["Range"] = f"{off}-{off + page - 1}"
        r = sess.get(f"{URL}/rest/v1/{path}?select={select}{extra}", headers=h, timeout=120)
        if r.status_code not in (200, 206):
            raise RuntimeError(f"HTTP {r.status_code} em {path}: {r.text[:300]}")
        batch = r.json()
        if not batch:
            break
        out += batch
        if len(batch) < page:
            break
        off += page
    return out


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


# ── QA GATE ───────────────────────────────────────────────────────────────────
# Exclui do .bin o que NÃO deve ser carregado/casado no jogo:
#  - PT corrompido (U+FFFD ou byte de controle): renderiza lixo / risco de crash.
#  - PT com parâmetro não resolvido ({0}, <Sheet(...)>, <If(...)>): mostraria literal.
#  - EN com parâmetro não resolvido (UNKNOWN, {0}, <Tag(...)>): nunca casa o texto
#    real do jogo (que tem o valor preenchido) -> linha inerte, só infla o .bin.
# Mantém <sigh> e afins (tags sem parêntese), que podem ser literais legítimos.
_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_CURLY = re.compile(r"\{\d+\}")
_PARAMTAG = re.compile(r"<\w+\(")


def gate_reason(e, p):
    if "�" in p or _CTRL.search(p):
        return "pt_corrupt"
    if _CURLY.search(p) or _PARAMTAG.search(p):
        return "pt_param"
    if "UNKNOWN" in e or _CURLY.search(e) or _PARAMTAG.search(e):
        return "en_inert"
    return None


def write_str(f, b):
    n = len(b)
    while n >= 0x80:
        f.write(bytes([(n & 0x7f) | 0x80])); n >>= 7
    f.write(bytes([n])); f.write(b)


def main():
    print("Lendo strings do Supabase ...")
    rows = fetch("strings", "english_text,ptbr_text",
                 "&ptbr_text=not.is.null&status=in.(machine,approved,in_review)&order=id.asc")
    print(f"  {len(rows):,} strings traduzidas")
    print("Lendo variantes (string_variants) ...")
    variants = fetch("string_variants", "english_render,ptbr_render",
                     "&order=string_key.asc,english_render.asc")
    print(f"  {len(variants):,} variantes")

    tr = {}
    gated = {}

    def consider(e, p):
        if not (e and p):
            return
        why = gate_reason(e, p)
        if why:
            gated[why] = gated.get(why, 0) + 1
            return
        tr[e] = p

    for r in rows:
        consider(clean(r.get("english_text")), (r.get("ptbr_text") or "").strip().replace("\r\n", "\n"))
    for v in variants:
        consider(clean(v.get("english_render")), (v.get("ptbr_render") or "").strip().replace("\r\n", "\n"))

    if gated:
        print("QA gate — excluídas:", ", ".join(f"{k}={v}" for k, v in sorted(gated.items())),
              f"(total {sum(gated.values()):,})")

    print(f"Escrevendo {len(tr):,} traduções únicas em {OUT} ...")
    with open(OUT, "wb") as f:
        f.write(struct.pack("<i", len(tr)))
        for e, p in tr.items():
            write_str(f, e.encode("utf-8"))
            write_str(f, p.encode("utf-8"))
    print("OK.")


if __name__ == "__main__":
    main()
