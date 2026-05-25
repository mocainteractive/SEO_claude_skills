---
name: content-brief-builder
description: >
  Costruisce il brief editoriale completo per la scrittura di un articolo blog SEO, integrando gli output di keyword-analysis, serp-analysis e brand-analysis-and-connections. Usa questa skill dopo brand-analysis-and-connections e prima di draft-writer. Trigger tipici: "crea il brief per l'articolo", "costruisci il brief editoriale", "dammi le linee guida per scrivere l'articolo", "procedi con il flusso seo-blog-pipeline". Questa skill è il quarto step del flusso seo-blog-pipeline.
---

# Content Brief Builder

Questa skill costruisce il brief editoriale completo che guida la scrittura dell'articolo. Integra tutti gli output delle skill precedenti (keyword-analysis, serp-analysis, brand-analysis-and-connections) e produce un documento operativo consegnabile direttamente al copywriter.

Il brief è il documento di riferimento per la scrittura: i metadati, il titolo H1 e la struttura H2/H3 sono elementi fissi che il copywriter non deve modificare. La scrittura dei singoli paragrafi e l'aggiunta di paragrafi integrativi sono invece aree di libertà.

---

## Input atteso

- Output di `keyword-analysis`: keyword primaria, keyword secondarie e correlate, intent
- Output di `serp-analysis`: gap identificati, domande PAA, formato consigliato, analisi competitor
- Output di `brand-analysis-and-connections`: TOV, istruzioni di scrittura, contenuti correlati, pagine strategiche da collegare
- Topic e cliente del progetto
- **Istruzioni e knowledge di progetto** (se il flusso gira dentro un progetto Claude): linee guida editoriali, brand book, tone of voice, glossari, termini da usare/evitare, vincoli di formato o legali. Incorporale nel brief e falle prevalere sui default generici di questa skill; in caso di conflitto con una buona pratica SEO o con una scelta di sessione, segnalalo all'utente invece di risolverlo in autonomia.

---

## Formato del brief: standard vs complesso

La skill produce due versioni del brief.

**Brief standard** (default): usato per la maggioranza dei progetti. Contiene metadati, scaletta H2/H3 con istruzioni per paragrafo, keyword per sezione, nota SEO finale con link interni, CTA e fonti.

**Brief complesso**: usato quando il topic è articolato, il cliente ha esigenze editoriali specifiche, oppure quando la serp-analysis ha prodotto un'analisi competitor dettagliata da integrare nel brief. Aggiunge: step metodologici numerati in apertura, URL suggerita, indicazioni su immagini (nome file, alt text, didascalia) per i paragrafi principali, analisi competitor sintetica in appendice.

Usa il brief complesso se almeno una di queste condizioni è vera:
- L'articolo supera i 2.000 parole stimati
- Sono stati identificati più di 3 gap significativi nella serp-analysis
- Il cliente ha richiesto indicazioni sulle immagini
- Il topic richiede una struttura con più di 6 H2

Altrimenti usa il brief standard.

---

## Processo di costruzione

### Step 1 — Metadati e keyword

**H1 / Titolo articolo**
Deve contenere la keyword primaria, possibilmente nella parte iniziale. Deve essere chiaro, specifico e orientato al beneficio del lettore. **Massimo 55 caratteri (limite rigido).**

**Meta title**
Variante dell'H1 ottimizzata per la SERP: può essere leggermente diversa dal titolo H1 per includere una keyword secondaria o un elemento differenziante. **Massimo 55 caratteri (limite rigido)**, incluso il nome del brand se previsto dal cliente (es. "Titolo | Nome Brand").

**Meta description**
Riassume il contenuto dell'articolo in modo da stimolare il clic dalla SERP. Deve contenere la keyword primaria, essere orientata al beneficio e terminare con un invito implicito all'azione. **Massimo 160 caratteri (limite rigido).**

**Verifica via script — obbligatoria**
Le stime LLM della lunghezza di una stringa sono notoriamente inaffidabili: contare caratteri "a occhio" porta quasi sempre a sforare. Dopo aver generato H1, meta title e meta description, **esegui sempre un breve script Python con la Bash tool per misurarne la lunghezza esatta**. Esempio:

```python
h1 = "Come scegliere il software di project management"
mt = "Software project management: la guida completa | NomeBrand"
md = "Tutti i criteri per scegliere il software di project management giusto per il tuo team: confronto, prezzi, funzionalità chiave."

for nome, testo, limite in [("H1", h1, 55), ("Meta title", mt, 55), ("Meta description", md, 160)]:
    n = len(testo)
    stato = "OK" if n <= limite else f"SFORATO di {n - limite}"
    print(f"{nome}: {n}/{limite} → {stato}")
```

Se uno dei tre sfora il limite, **riscrivi e ri‑esegui lo script** finché tutti e tre rientrano. Non procedere finché non rientrano. Riporta nel brief solo le versioni verificate.

**Keyword list**
Inserisci la keyword primaria seguita dal volume mensile, poi le keyword secondarie più rilevanti con il relativo volume. Formato: `keyword — volume`. Includi le domande PAA come keyword se hanno volume o sono presenti in SERP.

### Step 2 — Struttura H2/H3 e istruzioni di scrittura

Costruisci la scaletta dell'articolo partendo da:
1. Domande PAA identificate nella serp-analysis: integrale come H2 o H3 dell'articolo, oppure come domanda implicita a cui rispondere all'interno di un paragrafo già previsto. **Non creare mai una sezione "Domande frequenti" o "FAQ" a fine articolo che le raccolga in elenco.** Le PAA devono essere risolte nel corpo del testo, non isolate in un blocco a parte.
2. Gap di contenuto identificati nella serp-analysis (trasformali in sezioni mancanti dai competitor)
3. Keyword long-tail dell'analisi keyword (usale come H3 o angolazione di paragrafo)
4. Formato consigliato dalla serp-analysis (guida, tutorial, confronto, ecc.)

**Regola di capitalizzazione di H1, H2 e H3:** scrivi sempre i titoli con la **maiuscola solo sulla prima parola** e sui nomi propri. Mai title case all'inglese ("Come Fare la Pasta con la Pancetta") e mai tutto maiuscolo ("COME FARE LA PASTA AL RAGÙ"). Esempi corretti:
- "Come ha fatto Sinner a vincere la partita"
- "Come preparare un antipasto coi carciofi"
- "Pasta alla carbonara: la ricetta originale romana"

Per ciascun H2 e H3 scrivi:
- Il titolo dell'heading (già ottimizzato con keyword dove naturale)
- Le istruzioni di scrittura per il copywriter: cosa deve dire quel paragrafo, con quale tono, che livello di dettaglio, se includere esempi concreti, dati, elenchi puntati, tabelle
- Le keyword da integrare naturalmente in quel paragrafo (estratte dalla lista keyword-analysis)
- Eventuali link interni da inserire in quel punto (da brand-analysis-and-connections)

**Introduzione**: scrivi sempre istruzioni specifiche per l'apertura dell'articolo: che tipo di aggancio usare (problema, domanda, dato, scenario), cosa anticipare al lettore, tono con cui iniziare (in linea con il TOV rilevato dalla brand-analysis).

**Conclusione / CTA finale**: indica come chiudere l'articolo e quale CTA inserire, collegata alle pagine strategiche identificate dalla brand-analysis-and-connections.

### Step 3 — Istruzioni di scrittura generali

Ricava le istruzioni di scrittura dal TOV rilevato dalla brand-analysis-and-connections e traducile in regole concrete per il copywriter. Esempi:

- "Usa il 'tu' per rivolgerti al lettore"
- "Tono professionale ma accessibile: spiega i tecnicismi senza dare per scontato che il lettore li conosca"
- "Inizia ogni sezione con un'affermazione diretta, non con una domanda retorica"
- "Usa frasi brevi. Ogni concetto in un paragrafo separato"
- "Evita il gergo da agenzia: non scrivere 'ecosistema digitale' o 'soluzioni integrate'"
- "Ogni H2 deve rispondere a una domanda reale che il lettore si sta ponendo"

Queste istruzioni vanno nel brief come sezione separata, prima della scaletta.

### Step 4 — Nota SEO finale

Raccogli in una sezione finale tutti gli elementi tecnici SEO:

**Link interni**
Lista completa dei link da inserire nell'articolo, divisi per tipo:
- Contenuti correlati (articoli del blog): con URL e suggerimento di dove inserirli nella scaletta
- Pagine strategiche (categorie prodotto, servizi, casi studio): con URL, anchor text suggerito e punto di inserimento

**CTA**
Indica quante CTA inserire, dove posizionarle (dopo quale paragrafo) e il testo consigliato. Di norma almeno 2 CTA nel corpo dell'articolo più una CTA finale.

**Ottimizzazione immagini** *(solo brief complesso)*
Per i paragrafi principali indica: nome file suggerito, alt text ottimizzato con keyword, didascalia.

**URL suggerita** *(solo brief complesso)*
Formato: `/keyword-primaria-slug` — breve, leggibile, senza stop words.

**Fonti consigliate**
Indica 3-5 fonti autorevoli che il copywriter può usare per verificare i dati: istituti di settore, normative, pubblicazioni scientifiche, report di mercato rilevanti per il topic.

---

## Output — Brief standard

---

**[Nome cliente]**

**[Titolo articolo]**

[Mese e anno]

# Linee guida per l'articolo

**Titolo H1:** [titolo]

**Meta title:** [meta title]

**Meta description:** [meta description]

**Keyword:**
- [keyword primaria] — [volume]
- [keyword secondaria] — [volume]
- [keyword secondaria] — [volume]
*(includi 8-12 keyword totali)*

**Istruzioni di scrittura**
[Lista puntata con le regole di stile e tono per il copywriter, derivate dal TOV della brand-analysis]

---

**[Introduzione]**
[Istruzioni specifiche su come aprire l'articolo: tipo di aggancio, cosa anticipare, tono]

**H2: [titolo heading]**
[Istruzioni per il paragrafo]
Keyword da integrare:
- [keyword]
- [keyword]

**H3: [titolo heading]** *(se previsto)*
[Istruzioni per il sottoparagrafo]
Keyword da integrare:
- [keyword]

*(ripeti per tutti gli H2 e H3 della scaletta)*

---

## NOTA SEO

**Link interni:**
- [Titolo contenuto correlato](URL) — inserire in [punto della scaletta]
- [Titolo pagina strategica](URL) — anchor text: "[anchor]" — inserire in [punto]

**CTA:**
- CTA 1: dopo [paragrafo] — testo consigliato: [testo]
- CTA 2: dopo [paragrafo] — testo consigliato: [testo]
- CTA finale: [testo e link]

**Fonti:**
- [Fonte 1]
- [Fonte 2]
- [Fonte 3]

---

## Output — Brief complesso

Uguale al brief standard, con queste aggiunte:

**In apertura**, prima della scaletta, inserisci gli step metodologici numerati:

- **Step 1 — Tema dell'articolo:** [descrizione del topic, angolazione, obiettivo]
- **Step 2 — Scelta delle parole chiave:** vedi in Keywords
- **Step 3 — Forma del contenuto e spunti dalle ricerche:** [formato scelto e motivazione da serp-analysis, gap da coprire]
- **Step 4 — Ottimizzazione immagini:** ottimizzare ogni immagine con alt text rilevante, es. "[esempio alt text]"
- **Step 5 — Link interni:** vedi scaletta
- **Step 6 — Ottimizzazioni SEO:** le keyword sono inserite naturalmente nel testo? Sono presenti nei titoli? Sono presenti link a pagine strategiche? Le immagini hanno alt text? *(fase da verificare post bozza)*
- **Step 7 — Call to action:** vedi in fondo all'articolo
- **Step 8 — URL suggerita:** /[slug]
- **Step 9 — Metadati:** vedi Meta title e Meta description sopra

**Nella scaletta**, per i paragrafi principali aggiungi:
- *Nome file immagine:* [nome-file-descrittivo.jpg]
- *Alt text:* [descrizione ottimizzata con keyword]
- *Didascalia:* [testo didascalia]

**In appendice**, dopo la nota SEO, aggiungi:

### Analisi competitor
[Sintesi operativa dei competitor analizzati nella serp-analysis: formato usato dai competitor, gap identificati, come differenziarsi. Massimo 300 parole. Non copiare l'analisi completa: sintetizza le indicazioni utili per il copywriter.]

---

## Regole critiche

- H1, meta title, meta description e struttura H2/H3 sono fissi: il copywriter non deve modificarli.
- Le keyword devono essere quelle fornite da keyword-analysis, affinate da serp-analysis e brand-analysis.
- Le istruzioni di scrittura devono essere concrete e specifiche: non "scrivi in modo chiaro" ma "usa frasi brevi, una frase per concetto, evita i tecnicismi non spiegati".
- I link interni vengono solo da brand-analysis-and-connections: mai inventare URL o suggerire landing page.
- L'anchor text dei link deve essere naturale nel contesto dell'articolo: mai "clicca qui" o "scopri di più".
- Le CTA devono collegarsi a pagine strategiche già identificate dalla brand-analysis.
- Il brief deve essere autonomo: chi lo riceve deve poter scrivere l'articolo senza bisogno di ulteriori spiegazioni.
- Non includere nel brief elementi non derivati dalle skill precedenti: niente keyword inventate, niente link non verificati, niente istruzioni di stile non fondate sull'analisi del brand.
- Mai prevedere nella scaletta una sezione finale di tipo "Domande frequenti", "FAQ" o equivalenti come raccolta di domande e risposte. Le PAA si integrano come heading o si risolvono nel corpo dei paragrafi.
- H1, H2 e H3 sempre con maiuscola solo sulla prima parola e sui nomi propri. Mai title case né maiuscolo integrale.
