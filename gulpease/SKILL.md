---
name: gulpease
description: Valuta la leggibilità di un testo italiano con indice Gulpease, Flesch-Vacca e controlli qualitativi, con punteggi per sezione e interventi di riscrittura. Usala quando si chiede di valutare la leggibilità o il Gulpease.
---

# GULPEASE, VALUTAZIONE DELLA LEGGIBILITÀ

Questa skill misura la leggibilità di un testo in italiano (articolo blog, pagina prodotto, guest post, bozza) e restituisce un report operativo. Il Gulpease è il numero di riferimento, ma non è mai l'unico criterio: lo affianchiamo a Flesch-Vacca, a metriche strutturali e a una lettura qualitativa, perché il Gulpease misura solo lunghezza di parole e frasi.

## TRIGGER TIPICI

- "calcola il Gulpease di questo testo"
- "valuta la leggibilità dell'articolo"
- "questo testo è leggibile?" / "è troppo difficile?"
- "confronta la leggibilità prima e dopo la revisione"
- richiesta di controllo leggibilità dentro seo-optimizer, content-reviewer, existing-page-optimizer o guest-post-reviewer

## FASE 1, INPUT E PARAMETRI

1. Recupera il testo:
   - testo incollato in chat: usalo così com'è;
   - URL: scarica la pagina ed estrai solo il corpo dell'articolo (escludi menu, footer, sidebar, CTA, box autore, commenti);
   - file .docx, .pdf, .md o doc del Project: estrai il testo mantenendo titoli (come `#`, `##`) ed elenchi (come `-`).
2. Stabilisci la soglia target. Se l'utente o il cliente non ne indicano una, usa:
   - contenuti informativi per pubblico generale (blog, guide): Gulpease prosa **≥ 55**;
   - contenuti tecnici, normativi o assicurativi (condizioni, clausole, glossari): **≥ 45**;
   - pagine commerciali e landing: **≥ 60**.
   Se il cliente ha una soglia concordata (es. Vittoria Assicurazioni), usa quella e dichiarala nel report.
3. Modalità: **singola valutazione** (default) oppure **confronto** prima/dopo, se vengono forniti due testi.
4. Formato di output: se l'utente non l'ha indicato, chiedi una volta con AskUserQuestion se vuole il report come messaggio in chat (default), artifact o documento. Per un testo breve o una domanda veloce rispondi direttamente in chat.

## FASE 2, CALCOLO AUTOMATICO

Non calcolare mai gli indici a mano o a stima: usa sempre lo script.

1. Salva il testo in un file `.md` nella scratchpad (titoli con `#`, elenchi con `-`, tabelle con `|`).
2. Salva lo script qui sotto come `leggibilita.py` nella stessa cartella ed eseguilo con `python3 -I leggibilita.py testo.md [soglia_parole_frase]` (soglia di default: 25 parole).
3. Lo script restituisce un JSON con:
   - `prosa`: indici calcolati solo sui paragrafi (titoli, elenchi e tabelle esclusi). **È il valore principale da riportare**;
   - `testo_completo_con_titoli_ed_elenchi`: Gulpease includendo titoli ed elenchi come frasi. Di solito risulta più alto, va citato solo come riferimento perché è gonfiato dalle righe brevi;
   - `sezioni`: Gulpease per ogni H2/H3;
   - `frasi_lunghe`, `parole_lunghe_ricorrenti`, `passivi_esempi`, `nominalizzazioni_ricorrenti`.

```python
#!/usr/bin/env python3
"""Calcolo Gulpease, Flesch-Vacca e controlli di leggibilità su testo italiano (Markdown o testo semplice)."""
import re, sys, json

ABBR = ["es", "ecc", "art", "artt", "pag", "pagg", "n", "nr", "sig", "sigg", "dott", "dott.ssa", "prof", "ing", "avv", "cfr", "vd", "p", "pp", "cap", "lett", "co", "s.p.a", "s.r.l", "d.lgs", "d.l", "l", "c.c", "c.d.a"]
WORD = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+|\d+(?:[.,]\d+)*")
STRONG = set("aeoàèéìòóù")
VOW = set("aeiouàèéìíòóùú")

def clean_inline(s):
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_`~]+", "", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return s.strip()

def classify(text):
    blocks, cur_section = [], "Introduzione"
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            blocks.append(("blank", "", cur_section)); continue
        if re.match(r"^#{1,6}\s", line):
            cur_section = clean_inline(line.lstrip("#").strip())
            blocks.append(("heading", cur_section, cur_section)); continue
        if line.startswith("|"):
            blocks.append(("table", clean_inline(line.replace("|", " ")), cur_section)); continue
        if re.match(r"^([-*+•]|\d+[.)])\s+", line):
            blocks.append(("list", clean_inline(re.sub(r"^([-*+•]|\d+[.)])\s+", "", line)), cur_section)); continue
        blocks.append(("prose", clean_inline(line), cur_section))
    return blocks

def split_sentences(par):
    t = par
    for a in ABBR:
        t = re.sub(r"\b" + re.escape(a) + r"\.", a.replace(".", "§") + "§", t, flags=re.I)
    parts = re.split(r"(?<=[.!?…])\s+(?=[\"«“(]?[A-ZÀ-Ý0-9])", t)
    return [p.replace("§", ".").strip() for p in parts if WORD.search(p)]

def words(s):
    return WORD.findall(s)

def letters(ws):
    return sum(1 for w in ws for c in w if c.isalpha())

def syllables(w):
    w = w.lower()
    if not any(c.isalpha() for c in w):
        return max(1, len(w) // 2)  # numeri: stima
    n, i = 0, 0
    while i < len(w):
        if w[i] in VOW:
            j = i
            while j < len(w) and w[j] in VOW:
                j += 1
            grp = w[i:j]
            strong = sum(1 for c in grp if c in STRONG)
            n += max(1, strong)
            i = j
        else:
            i += 1
    return max(1, n)

def gulpease(nw, nl, ns):
    return round(89 + (300 * ns - 10 * nl) / nw, 1) if nw else None

def flesch_vacca(nw, nsyl, ns):
    return round(206 - 0.65 * (nsyl / nw * 100) - (nw / ns), 1) if nw and ns else None

PASSIVE = re.compile(r"\b(è|sono|era|erano|sarà|saranno|sia|siano|fosse|fossero|viene|vengono|veniva|venivano|verrà|verranno|venga|vengano|stato|stata|stati|state)\s+((?!stat[oaie]\b)[a-zà-ù]+(?:at[oaie]|ut[oaie]|it[oaie]|ess[oaie]|ott[oaie]|ost[oaie]))\b", re.I)
NOMINAL = re.compile(r"\b[a-zà-ù]{4,}(?:zione|zioni|mento|menti|anza|anze|enza|enze)\b", re.I)

def stats(sentences):
    ws = [w for s in sentences for w in words(s)]
    nw, ns = len(ws), len(sentences)
    nl = letters(ws)
    nsyl = sum(syllables(w) for w in ws)
    return nw, ns, nl, nsyl, ws

def main(path, soglia_frase=25):
    text = open(path, encoding="utf-8").read()
    blocks = classify(text)
    prose_sent, all_sent, per_sec = [], [], {}
    for kind, content, sec in blocks:
        if kind == "prose":
            ss = split_sentences(content)
            prose_sent += [(s, sec) for s in ss]
            all_sent += ss
            per_sec.setdefault(sec, []).extend(ss)
        elif kind in ("heading", "list", "table") and words(content):
            all_sent += split_sentences(content) or [content]
    p = [s for s, _ in prose_sent]
    nw, ns, nl, nsyl, ws = stats(p)
    anw, ans, anl, ansyl, _ = stats(all_sent)
    long_s = [{"sezione": sec, "parole": len(words(s)), "frase": s} for s, sec in prose_sent if len(words(s)) > soglia_frase]
    long_s.sort(key=lambda x: -x["parole"])
    lw = [w.lower() for w in ws if w.isalpha() and len(w) >= 12]
    freq = {}
    for w in lw:
        freq[w] = freq.get(w, 0) + 1
    ptxt = " ".join(p)
    passivi = [m.group(0) for m in PASSIVE.finditer(ptxt)]
    nomin = [m.group(0).lower() for m in NOMINAL.finditer(ptxt)]
    sezioni = []
    for sec, ss in per_sec.items():
        a, b, c, d, _ = stats(ss)
        if a:
            sezioni.append({"sezione": sec, "parole": a, "frasi": b, "gulpease": gulpease(a, c, b), "parole_per_frase": round(a / b, 1)})
    res = {
        "prosa": {
            "parole": nw, "frasi": ns, "lettere": nl, "sillabe_stimate": nsyl,
            "gulpease": gulpease(nw, nl, ns), "flesch_vacca": flesch_vacca(nw, nsyl, ns),
            "parole_per_frase": round(nw / ns, 1) if ns else None,
            "lettere_per_parola": round(nl / nw, 2) if nw else None,
            "perc_frasi_lunghe": round(len(long_s) / ns * 100, 1) if ns else None,
            "perc_parole_lunghe_12": round(len(lw) / nw * 100, 1) if nw else None,
            "passivi_per_100_frasi": round(len(passivi) / ns * 100, 1) if ns else None,
            "nominalizzazioni_per_100_parole": round(len(nomin) / nw * 100, 1) if nw else None,
        },
        "testo_completo_con_titoli_ed_elenchi": {"parole": anw, "frasi": ans, "gulpease": gulpease(anw, anl, ans)},
        "sezioni": sezioni,
        "frasi_lunghe": long_s[:15],
        "parole_lunghe_ricorrenti": sorted(freq.items(), key=lambda x: -x[1])[:15],
        "passivi_esempi": passivi[:10],
        "nominalizzazioni_ricorrenti": sorted({w: nomin.count(w) for w in set(nomin)}.items(), key=lambda x: -x[1])[:10],
    }
    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 25)
```

### FORMULE E SOGLIE DI RIFERIMENTO

- **Gulpease** = 89 + (300 × frasi − 10 × lettere) / parole. Scala 0-100. Il testo è difficile sotto 80 per la licenza elementare, sotto 60 per la licenza media, sotto 40 per il diploma superiore.
- **Flesch-Vacca** = 206 − 0,65 × sillabe ogni 100 parole − parole medie per frase. Indicativamente: oltre 80 molto facile, 60-80 facile, 50-60 abbastanza difficile, 30-50 difficile, sotto 30 molto difficile. Le sillabe sono stimate in automatico (errore di qualche punto), quindi va usato come controllo incrociato, non come valore assoluto.
- **Parole per frase**: obiettivo medio 15-20, nessuna frase oltre 25-30 se evitabile.
- **Passivi**: segnala se superano circa 20 ogni 100 frasi (il rilevamento è euristico, verifica gli esempi prima di citarli).
- **Nominalizzazioni** (-zione, -mento, -anza, -enza): segnala se superano circa 4 ogni 100 parole.

## FASE 3, LETTURA QUALITATIVA

Leggi il testo e verifica quello che gli indici non vedono:

- **termini tecnici non spiegati**: ogni termine di settore (es. franchigia, massimale, classe CU, rivalsa) deve essere spiegato alla prima occorrenza. Non va eliminato: va chiarito;
- **sintassi**: subordinate annidate, incisi lunghi, soggetto lontano dal verbo, doppie negazioni;
- **struttura**: paragrafi oltre 4-5 righe, H2 poco chiari, mancanza di elenchi dove servirebbero, risposta che non arriva nelle prime righe della sezione;
- **sezioni critiche**: quali sezioni abbassano la media e perché;
- **parole lunghe ricorrenti**: distingui quelle inevitabili (lessico di settore, keyword) da quelle sostituibili (es. "successivamente" → "poi", "effettuare" → "fare").

## FASE 4, REPORT

Struttura fissa del report:

1. **SINTESI**: Gulpease prosa, Flesch-Vacca, soglia target, verdetto (sopra soglia / vicino alla soglia, entro 5 punti / sotto soglia) in 2-3 righe.
2. **METRICHE**: tabella con parole, frasi, parole per frase, lettere per parola, % frasi lunghe, % parole lunghe, passivi, nominalizzazioni. Cita il Gulpease con titoli ed elenchi solo come nota.
3. **SEZIONI**: tabella con il Gulpease per H2/H3, evidenziando quelle sotto soglia.
4. **CRITICITÀ**: le frasi più lunghe (massimo 5, citate), passivi e nominalizzazioni rilevanti, termini tecnici non spiegati.
5. **INTERVENTI SUGGERITI**: 3-7 riscritture in formato prima / dopo, ordinate per impatto, con la stima del guadagno sul punteggio se utile.
6. **NOTA DI METODO** (una riga): il Gulpease misura solo la lunghezza di parole e frasi e non è un fattore di ranking. Va letto insieme agli altri controlli.

In **modalità confronto** aggiungi in cima una tabella prima / dopo / delta per Gulpease, Flesch-Vacca, parole per frase e % frasi lunghe.

## REGOLE

- Non riscrivere il testo intero se non viene chiesto: proponi gli interventi. Se l'utente chiede di applicarli, ricalcola gli indici sul testo nuovo e mostra il delta.
- Non alzare il punteggio con trucchi di punteggiatura (frasi spezzate in modo innaturale, punti al posto di virgole senza motivo): peggiorano la lettura reale.
- Non sacrificare la precisione tecnica, legale o normativa, le keyword SEO o la copertura semantica per guadagnare punti. Nei testi assicurativi e finanziari la correttezza viene prima del punteggio.
- Su testi sotto le 150 parole avvisa che gli indici sono poco affidabili.
- Scrivi in italiano con capitalizzazione italiana, senza trattino lungo come punteggiatura (usa la virgola) e senza emoji.
- Se il report diventa un documento, rispetta la nomenclatura: `[Cliente] Analisi leggibilità nome contenuto - GG.MM.AAAA` per uso interno, `[Moca x Cliente] ...` se va condiviso con il cliente.
