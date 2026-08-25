#!/usr/bin/env python3
"""
price_lookup.py — lookup e confronto prezzi sul catalogo fornitori bundled.

Perche' esiste: il parsing del catalogo (salto righe di testa, estrazione dei
campi da NOTE, normalizzazione di dominio e prezzo, confronto tra fornitori) e'
identico a ogni esecuzione della skill su un CSV di ~7.000 righe. Farlo con uno
script deterministico e' piu' veloce, piu' economico (niente re-parsing nel
contesto del modello) e piu' affidabile (celle multi-riga, formati prezzo IT).

Usi principali (stdlib only, nessuna dipendenza):

  # 1) LOOKUP: dato un elenco di domini, per ognuno prezzo minimo + fornitore + alternative
  python price_lookup.py lookup --domains notizie.it,foodblog.it
  echo "notizie.it\nfoodblog.it" | python price_lookup.py lookup --stdin

  # 2) DISCOVER: filtra il catalogo come fonte di candidati (per categoria/paese/prezzo/metriche)
  python price_lookup.py discover --category finanza --country IT --max-price 400 --min-da 30

Output: JSON su stdout (facile da rileggere per il modello). Usa --csv per output tabellare.

Percorso del catalogo: ../assets/listini/comparativa-fornitori.csv relativo a questo file
(sovrascrivibile con --file). Il CSV ha 2 righe di intestazione/titolo da saltare;
header reale: FORNITORE,SITO,PREZZO,NOTE.
"""
import argparse, csv, json, re, sys, unicodedata
from pathlib import Path

DEFAULT_CSV = Path(__file__).resolve().parent.parent / "assets" / "listini" / "comparativa-fornitori.csv"
HEADER_SKIP = 2  # righe di titolo/sottotitolo prima dell'header reale

METRIC_KEYS = {"da": "DA", "tf": "TF", "cf": "CF", "dr": "DR", "as": "AS", "za": "ZA"}


def norm_domain(s):
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r"^https?://", "", s)
    s = re.sub(r"^www\.", "", s)
    s = s.split("/")[0].split("?")[0]
    return s.strip().strip(".")


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_text(s):
    return strip_accents((s or "").strip().lower())


def parse_price(raw):
    """Ritorna (valore_float|None, raw). 'Da concordare'/vuoto -> None (su richiesta)."""
    if not raw:
        return None, ""
    r = raw.strip()
    if not r or re.search(r"concord|richiesta|n\.?d\.?", r, re.I):
        return None, r
    # tieni solo cifre e separatori
    m = re.search(r"[\d.,]+", r)
    if not m:
        return None, r
    num = m.group(0)
    if "." in num and "," in num:          # 1.234,00 -> IT: . migliaia, , decimali
        num = num.replace(".", "").replace(",", ".")
    elif "," in num:                        # 1234,50 -> , decimale
        num = num.replace(",", ".")
    elif num.count(".") == 1 and len(num.split(".")[1]) == 3:
        num = num.replace(".", "")          # 1.234 -> migliaia
    try:
        return float(num), r
    except ValueError:
        return None, r


def parse_note(note):
    """NOTE = 'chiave: valore; chiave: valore; ...' -> dict + metriche + flag."""
    fields, metrics = {}, {}
    for part in (note or "").split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            k, v = k.strip(), v.strip()
            if not k:
                continue
            fields[k] = v
            kl = k.lower()
            if kl in METRIC_KEYS and re.search(r"\d", v):
                try:
                    metrics[METRIC_KEYS[kl]] = int(re.search(r"-?\d+", v).group(0))
                except ValueError:
                    pass
    nofollow = bool(re.search(r"no\s*follow", note or "", re.I))
    return fields, metrics, nofollow


def load_catalog(path):
    rows = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()
    reader = csv.DictReader(lines[HEADER_SKIP:])
    for r in reader:
        dom = norm_domain(r.get("SITO"))
        if not dom:
            continue
        price, price_raw = parse_price(r.get("PREZZO"))
        fields, metrics, nofollow = parse_note(r.get("NOTE"))
        rows.append({
            "supplier": (r.get("FORNITORE") or "").strip(),
            "domain": dom,
            "price": price,
            "price_raw": price_raw,
            "metrics": metrics,
            "country": fields.get("Paese") or fields.get("paese") or "",
            "category": fields.get("Categoria") or fields.get("categoria") or "",
            "topic": fields.get("Topic") or fields.get("topic") or "",
            "nofollow": nofollow,
            "note": (r.get("NOTE") or "").strip(),
        })
    return rows


def best_offer(offers):
    priced = [o for o in offers if o["price"] is not None]
    return min(priced, key=lambda o: o["price"]) if priced else None


def cmd_lookup(catalog, domains):
    idx = {}
    for o in catalog:
        idx.setdefault(o["domain"], []).append(o)
    out = []
    for d in domains:
        nd = norm_domain(d)
        offers = idx.get(nd, [])
        best = best_offer(offers)
        out.append({
            "domain": nd,
            "found": bool(offers),
            "best_price": best["price"] if best else None,
            "best_supplier": best["supplier"] if best else None,
            "on_request": bool(offers) and best is None,   # presente ma solo "Da concordare"
            "offers": [
                {"supplier": o["supplier"], "price": o["price"], "price_raw": o["price_raw"],
                 "metrics": o["metrics"], "country": o["country"], "nofollow": o["nofollow"]}
                for o in sorted(offers, key=lambda x: (x["price"] is None, x["price"] or 0))
            ],
        })
    return out


def cmd_discover(catalog, category, country, max_price, min_da, min_tf, min_za, limit):
    res = []
    cat = norm_text(category) if category else None
    ctry = country.strip().upper() if country else None
    for o in catalog:
        if cat and cat not in norm_text(o["category"]) and cat not in norm_text(o["topic"]):
            continue
        if ctry and o["country"] and o["country"].strip().upper() != ctry:
            continue
        if max_price is not None and (o["price"] is None or o["price"] > max_price):
            continue
        m = o["metrics"]
        if min_da is not None and m.get("DA", -1) < min_da:
            continue
        if min_tf is not None and m.get("TF", -1) < min_tf:
            continue
        if min_za is not None and m.get("ZA", -1) < min_za:
            continue
        res.append(o)
    # dedup per dominio tenendo il prezzo minore
    by_dom = {}
    for o in res:
        cur = by_dom.get(o["domain"])
        if cur is None or (o["price"] is not None and (cur["price"] is None or o["price"] < cur["price"])):
            by_dom[o["domain"]] = o
    out = sorted(by_dom.values(), key=lambda x: (x["price"] is None, x["price"] or 0))
    return out[:limit] if limit else out


def main():
    ap = argparse.ArgumentParser(description="Lookup/confronto prezzi sul catalogo fornitori.")
    ap.add_argument("mode", choices=["lookup", "discover"])
    ap.add_argument("--file", default=str(DEFAULT_CSV), help="percorso del CSV catalogo")
    ap.add_argument("--domains", help="lookup: domini separati da virgola")
    ap.add_argument("--stdin", action="store_true", help="lookup: leggi domini da stdin (uno per riga)")
    ap.add_argument("--category", help="discover: sottostringa di categoria/topic")
    ap.add_argument("--country", help="discover: codice paese es. IT, ES, FR")
    ap.add_argument("--max-price", type=float)
    ap.add_argument("--min-da", type=int)
    ap.add_argument("--min-tf", type=int)
    ap.add_argument("--min-za", type=int)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--csv", action="store_true", help="output CSV invece di JSON")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        sys.exit(f"Catalogo non trovato: {path}")
    catalog = load_catalog(path)

    if args.mode == "lookup":
        domains = []
        if args.domains:
            domains += [d for d in re.split(r"[,\n]", args.domains) if d.strip()]
        if args.stdin:
            domains += [l for l in sys.stdin.read().splitlines() if l.strip()]
        if not domains:
            sys.exit("lookup: fornisci --domains o --stdin")
        result = cmd_lookup(catalog, domains)
    else:
        result = cmd_discover(catalog, args.category, args.country, args.max_price,
                              args.min_da, args.min_tf, args.min_za, args.limit)

    if args.csv:
        w = csv.writer(sys.stdout)
        if args.mode == "lookup":
            w.writerow(["domain", "best_price", "best_supplier", "on_request", "all_offers"])
            for r in result:
                alt = " | ".join(f"{o['supplier']}: {o['price_raw']}" for o in r["offers"])
                w.writerow([r["domain"], r["best_price"], r["best_supplier"], r["on_request"], alt])
        else:
            w.writerow(["domain", "supplier", "price", "country", "category", "metrics"])
            for o in result:
                w.writerow([o["domain"], o["supplier"], o["price"], o["country"], o["category"], json.dumps(o["metrics"])])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
