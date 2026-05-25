---
name: seo-optimizer
description: >
  Controlla e ottimizza la bozza dell'articolo blog SEO prodotta dal draft-writer. Verifica keyword, struttura, metadati e link interni, poi corregge direttamente il testo o produce un report di modifiche in base all'entità degli interventi necessari. Usa questa skill dopo draft-writer e prima di content-reviewer. Trigger tipici: "ottimizza l'articolo per la SEO", "controlla la SEO del testo", "verifica che l'articolo sia ottimizzato", "procedi con il flusso seo-blog-pipeline". Questa skill è il sesto step del flusso seo-blog-pipeline.
---

# SEO Optimizer

Questa skill esegue il controllo SEO completo della bozza dell'articolo e restituisce il testo corretto oppure un report di modifiche, in base all'entità degli interventi necessari.

L'obiettivo è un articolo che rispetti i criteri SEO fondamentali senza sembrare ottimizzato: keyword ben distribuite, struttura leggibile, metadati efficaci, link interni tutti inseriti correttamente.

---

## Input atteso

- Bozza completa dell'articolo prodotta da `draft-writer`
- Brief editoriale (per verificare keyword list, link interni e metadati attesi)
- Note al revisore prodotte dal draft-writer (se disponibili)

---

## Processo di controllo

Esegui i seguenti controlli in sequenza. Per ciascuno registra internamente: OK, da correggere (modifica puntuale), o problema esteso (richiede interventi su più sezioni).

### Controllo 1 — Keyword primaria

Verifica che la keyword primaria sia presente:
- Nel titolo H1
- Nella prima parte dell'introduzione (idealmente nel primo o secondo paragrafo, non oltre)
- In almeno 2-3 H2 principali, in modo naturale
- Nel meta title
- Nella meta description

Verifica che la keyword primaria non sia ripetuta in modo meccanico o eccessivo. La soglia è qualitativa, non numerica: se leggendo il testo la keyword si sente forzata o ripetuta più volte nello stesso paragrafo, è troppa. Se è distribuita naturalmente nel testo, va bene anche se appare molte volte.

### Controllo 2 — Keyword secondarie e correlate

Verifica che le keyword secondarie siano distribuite nel testo nei paragrafi indicati dal brief. Non devono essere tutte presenti (alcune potrebbero non trovare contesto naturale), ma quelle ad alto volume o quelle associate a H2 specifici devono esserci.

Verifica che non ci siano ripetizioni anomale di keyword secondarie nello stesso paragrafo o in paragrafi adiacenti.

### Controllo 3 — Struttura e leggibilità

Verifica:
- Gerarchia heading corretta: H1 unico, H2 per sezioni principali, H3 per sottosezioni. Nessun salto di livello (es. H1 → H3 senza H2).
- Paragrafi non eccessivamente lunghi: un paragrafo di testo continuo che supera le 120-150 parole è un segnale di leggibilità ridotta. Segnalarlo se presente.
- Frasi non eccessivamente complesse: periodi con più di 3 subordinate consecutive o frasi superiori a 35-40 parole sono difficili da leggere su schermo. Segnalarli se presenti.
- Copertura tematica: tutti gli H2 del brief sono stati sviluppati in modo sostanziale? Se un paragrafo è troppo superficiale (meno di 80-100 parole per un H2 che richiedeva approfondimento), segnalarlo.

### Controllo 4 — Metadati

Verifica:
- Meta title: contiene la keyword primaria? È nella prima parte del titolo (prima dei trattini o del nome brand)? **È entro i 55 caratteri?**
- Meta description: contiene la keyword primaria? È scritta in italiano fluente come una frase compiuta, non come un elenco di keyword? **È entro i 160 caratteri?** Stimola il clic?

**Misurazione dei caratteri via script — obbligatoria.** Non stimare la lunghezza a occhio: esegui un breve script Python con la Bash tool per misurarla esattamente. Esempio:

```python
h1 = "..."  # il titolo H1 attuale dell'articolo
mt = "..."  # il meta title
md = "..."  # la meta description

for nome, testo, limite in [("H1", h1, 55), ("Meta title", mt, 55), ("Meta description", md, 160)]:
    n = len(testo)
    stato = "OK" if n <= limite else f"SFORATO di {n - limite}"
    print(f"{nome}: {n}/{limite} → {stato}")
```

Se uno dei tre sfora il limite, riscrivilo, applica la modifica al testo e ri‑esegui lo script per confermare il rientro. Riporta nel report finale solo le versioni verificate.

Se la meta description è solo una concatenazione di keyword o è scritta in modo meccanico, va riscritta anche se tecnicamente contiene le parole giuste.

### Controllo 5 — Link interni

Confronta i link indicati nella nota SEO del brief con quelli presenti nel testo:
- Tutti i link indicati sono stati inseriti?
- Ogni link è sull'anchor text indicato (o su una variante semanticamente equivalente)?
- Nessun link usa anchor text generici ("clicca qui", "scopri di più", "leggi qui")?
- Nessun link punta a una landing page (non previsto dalla brand-analysis)?
- I link sono inseriti in modo naturale nel testo, non spezzano il flusso?

Se un link del brief non è stato inserito, va aggiunto nel punto più naturale del testo più vicino al topic del link.

### Controllo 6 — Tell stilistici da AI

Verifica e correggi tre pattern che svelano una scrittura AI‑generated:

**Trattini come punteggiatura inline**
Cerca nel testo ogni occorrenza di `-`, `–`, `—` usata come segno di interpunzione tra clausole o per inciso (es. "il marketing è cambiato — i contenuti contano di più"). Sostituiscila con virgola, punto e virgola o punto, oppure riscrivi la frase. I trattini restano legittimi solo all'interno di parole composte ("post‑pandemia") e in intervalli numerici.

**Sezione "Domande frequenti" / "FAQ"**
Se l'articolo contiene una sezione finale (H2 o equivalente) intitolata "Domande frequenti", "FAQ", "Le domande più comuni" o simili, e questa sezione raccoglie domande e risposte in elenco, va eliminata. Le domande vanno ridistribuite nel corpo dell'articolo: o come heading dei paragrafi esistenti, o come domande implicite a cui un paragrafo già risponde.

**Capitalizzazione dei titoli**
H1, H2 e H3 devono avere la maiuscola solo sulla prima parola e sui nomi propri. Se un titolo è in title case all'inglese ("Come Fare la Pasta con la Pancetta") o tutto maiuscolo ("COME FARE LA PASTA AL RAGÙ"), correggilo. Forma corretta: "Come fare la pasta con la pancetta", "Come preparare un antipasto coi carciofi".

Questi tre controlli sono di tipo binario: o il pattern è presente e va corretto, o non lo è.

---

## Decisione: testo corretto vs report

Dopo aver completato tutti i controlli, valuta l'entità complessiva delle modifiche necessarie:

**Modifica diretta del testo** (restituisci il testo corretto completo):
- Le modifiche riguardano al massimo 2 paragrafi
- Si tratta di interventi puntuali: aggiunta/spostamento di una keyword, riscrittura di una frase, inserimento di un link mancante, correzione di un meta tag

**Report di modifiche** (restituisci un report senza riscrivere tutto):
- Le modifiche riguardano 3 o più paragrafi
- Ci sono problemi strutturali o di copertura tematica estesi
- La meta description va riscritta interamente
- Più link interni mancano o sono inseriti in modo scorretto

---

## Output — Testo corretto

Se le modifiche sono poche (massimo 2 paragrafi), restituisci il testo completo dell'articolo con le correzioni già applicate. **Mantieni in cima il blocco "KEYWORD UTILIZZATE"** prodotto dal draft-writer (aggiornato se durante l'ottimizzazione hai aggiunto/rimosso keyword), seguito dal corpo dell'articolo, seguito dalla nota delle modifiche applicate:

```
**KEYWORD UTILIZZATE**
- [keyword primaria] — [volume]/mese
- [keyword secondaria] — [volume]/mese
...

---

[Testo completo dell'articolo corretto, dall'H1 alla CTA finale]

---

**MODIFICHE APPLICATE**
- [Modifica 1: descrizione in una riga]
- [Modifica 2: descrizione in una riga]
```

Se il draft-writer non ha incluso il blocco "KEYWORD UTILIZZATE", ricostruiscilo tu partendo dal brief e dall'analisi keyword, segnando solo le keyword effettivamente presenti nel testo finale dopo le tue correzioni.

---

## Output — Report di modifiche

Se le modifiche sono estese, restituisci un report strutturato senza riscrivere il testo completo:

---

**REPORT SEO OPTIMIZER**

**Stato generale:** [Buono con interventi puntuali / Richiede revisione estesa]

**KEYWORD**
- [OK / Problema]: [descrizione]
- [OK / Problema]: [descrizione]

**STRUTTURA E LEGGIBILITÀ**
- [OK / Problema]: [descrizione e punto del testo da correggere]

**METADATI**
- Meta title: [OK / testo corretto suggerito]
- Meta description: [OK / testo corretto suggerito]

**LINK INTERNI**
- [Link presente e corretto / Link mancante: dove inserirlo e su quale anchor / Link con anchor errato: correzione suggerita]

**TELL STILISTICI DA AI**
- Trattini inline: [Nessuno / N occorrenze da rimuovere con correzioni puntuali]
- Sezione FAQ finale: [Assente / Presente — da ridistribuire nei paragrafi]
- Capitalizzazione titoli: [Corretta / N titoli da riscrivere — elenco]

**INTERVENTI RICHIESTI IN ORDINE DI PRIORITÀ**
1. [Intervento più critico]
2. [Intervento]
3. [Intervento meno critico]

---

## Regole critiche

- Non modificare la struttura H2/H3 dell'articolo: questo non è il momento per cambiare l'architettura del testo.
- Non riscrivere paragrafi interi per motivi stilistici: le correzioni devono essere motivate da criteri SEO oggettivi, non da preferenze di stile.
- La densità keyword è qualitativa, non numerica: non forzare inserimenti meccanici se il testo scorre già bene.
- Un meta title o una meta description che contengono la keyword ma sono scritti male vanno corretti: la keyword da sola non basta.
- I link mancanti vanno sempre segnalati o inseriti: sono indicazioni del brief e non possono essere ignorati.
- Nessun link su anchor generici: se un link è stato inserito su "clicca qui" o equivalenti, va corretto.
- I trattini come punteggiatura inline vanno sempre rimossi: è una correzione obbligatoria, non stilistica.
- Una sezione finale "Domande frequenti" / "FAQ" va sempre smontata e ridistribuita nel corpo dell'articolo.
- I titoli in title case o tutto maiuscolo vanno sempre corretti in "maiuscola solo sulla prima parola e sui nomi propri".
- Se l'articolo supera tutti i controlli senza problemi significativi, dillo esplicitamente: "Nessuna modifica necessaria" è un output valido.
