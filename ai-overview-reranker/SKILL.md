---
name: ai-overview-reranker
description: >
  Re-ranker per posizionare un articolo (pubblicato o in bozza) come fonte primaria nell'AI Overview di Google. Si attiva su richiesta esplicita o come Fase 7 opzionale del seo-blog-pipeline sulla bozza pre-pubblicazione, su 1‑3 keyword. Usa il Vertex MCP Server (Discovery Engine Ranking + Vertex Text Embeddings) per misurare la rilevanza vs i competitor su ciascuna keyword, mappare la copertura delle sotto-query del fan-out per sezione, costruire una mappa semantica e produrre raccomandazioni concrete (chunking, heading dichiarativi, information gain, E-E-A-T). Collabora bidirezionalmente con existing-page-optimizer e seo-blog-pipeline e supporta il confronto numerico baseline/verify. Trigger tipici: "posizionami come fonte nell'AI Overview di X", "fai re-ranking AIO per questa pagina", "perché Google non cita il mio articolo nell'AI Overview", "check AIO sulla bozza", "verifica se le modifiche mi hanno portato dentro l'AIO".
---

# AI Overview Re-ranker

Questa skill ha **un solo obiettivo**: aumentare la probabilità che un articolo venga citato come fonte all'interno dell'**AI Overview di Google** su 1‑3 keyword target. Non è un controllo SEO generale e non riscrive l'articolo per intero: produce una diagnosi mirata e raccomandazioni operative, che vengono poi applicate da `existing-page-optimizer` (o da un copywriter umano).

Il cuore tecnico è il **Vertex MCP Server** con due tool: **`rerank`** (Discovery Engine Ranking API — il semantic-ranker di Google) e **`embed`** (Vertex Text Embeddings multilingue). La skill compone i due in tre misurazioni: (1) **rilevanza competitiva** dell'articolo vs i top competitor per ogni keyword target (`rerank`), (2) **coverage map** sezione-per-sotto-query del fan-out (`rerank`), (3) **mappa semantica vettoriale** con distanza dell'articolo dal nucleo del topic e sezioni outlier (`embed` + cosine similarity). Su questi numeri si costruisce la diagnosi e si producono raccomandazioni concrete.

Importante: lo score di `rerank` e le distanze vettoriali sono un **proxy forte** della probabilità di entrare nel pool delle fonti candidate dall'AIO, **non sono l'AIO stesso**. Per lo **snapshot reale** dell'AI Overview in SERP (presente/assente, fonti effettivamente citate da Google) c'è già `serp-analysis` Step 5 (DataForSEO). Le due fonti sono complementari: DataForSEO è la "verità terreno", il Vertex MCP è il laboratorio dove misurare la posizione attuale e simulare il delta delle modifiche.

---

## Quando usare questa skill (e quando no)

La skill lavora su **testo**: l'articolo da analizzare può essere già pubblicato e indicizzato **oppure** una bozza in costruzione. I due usi sono leggermente diversi per ruolo ma usano la stessa meccanica (rerank + embed).

- **Uso "post-pubblicazione" — diagnosi.** Si applica a una pagina esistente: "perché non veniamo citati nell'AI Overview, dove possiamo intervenire". Si appoggia ai dati di posizionamento attuali (Ahrefs, GSC, AIO reale da DataForSEO via `serp-analysis`). Punto d'ingresso naturale: invocata da `existing-page-optimizer` in Fase 1e o autonomamente su richiesta.
- **Uso "pre-pubblicazione" — validazione.** Si applica a una bozza in scrittura: "questa bozza ha le qualità per essere citata?". I dati di prima parte sul singolo URL non esistono ancora (l'articolo non è in SERP, GSC è vuoto, DataForSEO sullo specifico URL non si applica), ma rerank ed embed lavorano sul testo a prescindere. Punto d'ingresso naturale: invocata da `seo-blog-pipeline` come Fase 7 opzionale dopo `seo-optimizer` e prima di `content-reviewer`.

In entrambi i casi il proxy Vertex va letto per **direzione** e per **delta**, non come voto: in particolare in scrittura, il rischio è iterare il draft all'infinito inseguendo lo score, che non è l'obiettivo.

- **Non usarla** per analisi SEO generiche o per il posizionamento organico classico fuori dall'orizzonte AIO: per quelli ci sono `existing-page-optimizer`, `seo-blog-pipeline`, e le skill atomiche del flusso.

---

## Collaborazione con gli orchestratori (bidirezionale)

### Con `existing-page-optimizer` (post-pubblicazione)

**Da `existing-page-optimizer` a `ai-overview-reranker`.** Quando `existing-page-optimizer` nella Fase 1e rileva la presenza di AI Overview su una o più keyword target (via DataForSEO) e l'obiettivo di sessione è `articolo ottimizzato`, propone all'utente: "vuoi che chiami `ai-overview-reranker` per produrre raccomandazioni AIO‑specifiche da integrare nella Fase 4?". Se l'utente accetta, le raccomandazioni confluiscono nella **scaletta di modifiche** della Fase 4 con priorità alta. Dopo la Fase 5 (riscrittura), `existing-page-optimizer` può richiamare nuovamente questa skill in **modalità verify** per confermare il guadagno.

**Da `ai-overview-reranker` a `existing-page-optimizer`.** Se l'utente avvia direttamente questa skill su un URL pubblicato e dalle raccomandazioni emerge una lista significativa di interventi, proponi di passare a `existing-page-optimizer` per inserire le raccomandazioni nella scaletta della Fase 4 e applicarle.

### Con `seo-blog-pipeline` (pre-pubblicazione)

Quando l'orchestratore `seo-blog-pipeline` raggiunge la Fase 7 e l'utente ha scelto di abilitare il check AIO sulla bozza (domanda 5 della configurazione di sessione), invoca questa skill **sulla bozza prodotta dalla Fase 6 (seo-optimizer)**.

In questa esecuzione:
- L'"URL articolo" è il **testo della bozza** anziché un URL effettivo; passa l'articolo come contenuto.
- Le keyword target sono la primaria + 2 secondarie più pertinenti dalle Fasi 1‑2.
- Il corpus competitor è già nel contesto da `serp-analysis` (Fase 2): riusalo.
- Il fan-out predittivo è già disponibile da `serp-analysis` Step 6: alimenta direttamente la coverage map.
- Lo snapshot DataForSEO dell'AIO reale serve come "verità terreno" sulla SERP target, non sull'articolo (che non è in SERP).

Le raccomandazioni vanno applicate come **affinamenti puntuali** (preferibilmente via mini-iterazione su `seo-optimizer` se ≤ 2 paragrafi, o un giro mirato su `draft-writer` per sezioni nuove o espanse) prima di passare a `content-reviewer` in Fase 8.

In nessun caso questa skill applica modifiche al testo: produce diagnosi + raccomandazioni. La riscrittura è competenza di `draft-writer` / `seo-optimizer`.

---

## Input richiesto

1. **Articolo target** (obbligatorio): può essere fornito come **URL** (per il modo post-pubblicazione → recupera il contenuto con WebFetch) **oppure come testo completo** (per il modo pre-pubblicazione, quando la skill è invocata dalla Fase 7 di `seo-blog-pipeline` sulla bozza). In entrambi i casi il contenuto è il documento target per i passaggi di `rerank` e `embed`.
2. **Keyword target** (1‑3): se non fornite, ereditale dal contesto in quest'ordine di priorità: (a) keyword target della Fase 3 di `existing-page-optimizer` se la skill gira in collaborazione, (b) keyword primaria + 2 secondarie più pertinenti dall'output di `keyword-analysis` / `serp-analysis` (caso `seo-blog-pipeline`), (c) chiedile all'utente. Massimo 3 keyword per run.
3. **Lingua e paese target**: default italiano / Italia, salvo diversa indicazione (di solito coincidono con la lingua dell'articolo).
4. **Output precedente di questa stessa skill** (opzionale): se presente nel contesto, abilita automaticamente la modalità verify (confronto baseline/post-edit).
5. **Output di `serp-analysis`** (opzionale ma fortemente raccomandato): in particolare lo Step 5 (snapshot AIO da DataForSEO), lo Step 6 (query fan-out predittivo, con i tag content-type + ambito di intento) e l'analisi competitor con i loro contenuti. Lo Step 6 alimenta direttamente il coverage map del rerank Step 4; lo Step 5 funge da "verità terreno" per il cross-check Step 6 di questa skill; i contenuti competitor evitano di doverli fetchare di nuovo per il corpus Step 2.

Se manca l'URL dell'articolo, chiedilo. Se mancano le keyword e non sono ereditabili dal contesto, chiedile.

---

## Configurazione di sessione (da chiedere all'inizio)

Prima della Fase 1, in un'unica domanda concisa:

1. **Conferma keyword**: mostra le 1‑3 keyword target ricavate dal contesto (o ricevute dall'utente) e chiedi conferma. L'utente può sostituirne una o tutte.
2. **Modalità**:
   - `baseline` (default per la prima esecuzione): è un primo giro diagnostico. Produce stato attuale + raccomandazioni.
   - `verify` (default se nel contesto c'è già un output di questa skill): rilancia le chiamate Vertex e **confronta** con il baseline precedente, per misurare se le modifiche applicate hanno portato la citazione.
3. **Formato deliverable** (chiedi sempre, non assumere): markdown / html / testo plain / .docx / altro indicato dall'utente. `markdown` come fallback solo se l'utente non ha preferenze.

---

## Integrazione Vertex (MCP)

L'accesso a Vertex avviene tramite il **Vertex MCP Server** (`vertex-mcp-server`, esposto su Cloudflare Workers all'endpoint `https://vertex-mcp-server.daniele-pisciottano.workers.dev/mcp`; se è attiva la protezione a token, l'URL diventa `.../t/<TOKEN>/mcp`). Il server espone **due** tool che la skill compone insieme: `rerank` (Discovery Engine Ranking API — semantic-ranker di Google) e `embed` (Vertex Text Embeddings multilingue). **Non c'è un tool di generazione né di grounding**: l'approccio è **discriminativo e vettoriale**, non generativo. Per lo snapshot reale dell'AIO la fonte resta DataForSEO in `serp-analysis` Step 5.

Lo score di `rerank` (semantic relevance, 0–1) e la distanza vettoriale di `embed` sono un **proxy forte** della probabilità di entrare nel pool delle fonti candidate per l'AIO — non sono l'AIO stesso. Vanno letti per direzione e per delta tra baseline e verify, non come "siamo nell'AIO sì/no".

### Tool `rerank`

Riordina una lista di documenti per rilevanza rispetto a una query usando `semantic-ranker-default@latest` di Google (lo stesso modello che alimenta Vertex Search). È **stateless**: non indicizza nulla, ogni chiamata invia documenti e query nel body.

- **Input** (per chiamata):
  - `query` (string, obbligatorio): la query rispetto a cui valutare i documenti. Va formulata come **domanda utente naturale** in lingua target (es. "come fare la meditazione mindfulness"), non come keyword grezza.
  - `documents` (array, obbligatorio): lista di `{ id, title?, content }`. `content` obbligatorio: il testo effettivo del documento (passato nel body della chiamata).
  - `topN` (int, opzionale): restituisce solo i primi N risultati.
  - `model` (string, opzionale): override del modello.
  - `ignoreRecordDetails` (bool, opzionale): se `true`, la risposta contiene solo `id` + `score`.
- **Output**: `records[]` con `id`, `title?`, `content?`, `score` (0–1), ordinati per score discendente.
- **Note pratiche**:
  - Tieni d'occhio la dimensione cumulativa di `documents`: troppo testo per chiamata può sforare i limiti. Per ridurre, taglia i body al primo blocco di ~3‑5k caratteri rilevanti, oppure usa `ignoreRecordDetails: true` quando ti basta il punteggio.
  - Stessa coppia (query, documents) restituisce score stabili: utile per il confronto baseline/verify.

### Tool `embed`

Genera embedding vettoriali multilingue per uno o più testi (default `text-multilingual-embedding-002`, region `europe-west8`).

- **Input** (per chiamata):
  - `texts` (string[], obbligatorio): i testi da convertire in embedding.
  - `model` (string, opzionale): override del modello.
  - `taskType` (enum, opzionale): per questa skill usa `RETRIEVAL_QUERY` per keyword e sotto-query del fan-out, `RETRIEVAL_DOCUMENT` per articolo, sezioni e contenuti competitor. I due `taskType` producono spazi ottimizzati per il retrieval cross-modale (query↔documento).
  - `outputDimensionality` (int, opzionale): tronca l'embedding alla dimensione indicata.
  - `location` (string, opzionale): override della regione.
- **Output**: `embeddings[]` con `index`, `values` (vettore numerico), `tokenCount`.
- **Note pratiche**:
  - Le **cosine similarity non sono restituite** dal tool: calcolale localmente con uno script Python (`numpy`: `np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))`) lanciato via Bash.
  - Batcha più testi nella stessa chiamata `texts: [...]` per risparmiare round-trip; tieni i batch sotto le centinaia di elementi.

### Caso "Vertex MCP non disponibile"

Se il MCP non risponde (server giù, token errato, quota esaurita, errore di rete), **non bloccare il flusso**: segnalalo nell'output, salta gli step che richiedono Vertex (rerank competitivo, coverage map, mappa semantica) e produci raccomandazioni basate su `serp-analysis` Step 5 (snapshot AIO reale da DataForSEO) e Step 6 (fan-out predittivo). Lo dichiari esplicitamente come degradato. I **tre principi guida** e le **categorie di intervento** restano applicabili anche senza i numeri di Vertex: cambia solo la base evidenziale.

---

## Processo di analisi

### Step 1 — Lettura articolo e segmentazione

Recupera l'URL dell'articolo con `WebFetch`. Estrai:
- Metadati (title, meta description, H1).
- Struttura completa degli heading.
- Aperture di sezione (prime 1‑2 frasi di ciascun H2/H3): sono i candidati naturali alla citazione perché contengono la risposta diretta.
- Presenza di elementi estraibili: tabelle, elenchi, definizioni, dati con fonte, FAQ inline.
- Lunghezza stimata e copertura tematica.

**Segmentazione in sezioni.** Suddividi l'articolo in **sezioni**, una per H2 (o H3 se gli H2 sono molto lunghi). Per ciascuna sezione conserva: `id` (es. `sec_h2_1`), `title` (l'heading), `content` (il testo della sezione). Questi sono i documenti che useremo nei rerank e negli embed a livello sezione.

Questa è la "versione candidata" che vogliamo far citare.

### Step 2 — Corpus competitor

I rerank e gli embed richiedono il testo dei competitor: bisogna averlo nel contesto.

- Se nel contesto è già presente l'output di `serp-analysis` (Step 1‑3) con i 5‑7 competitor editoriali analizzati e il loro contenuto, riusalo: per ogni competitor estrai `id`, `url`, `title`, `content` (corpo testuale) e, dove possibile, una segmentazione per sezioni analoga a quella dell'articolo target.
- Se i competitor non sono nel contesto, identificali (top 5 risultati organici editoriali sulla keyword principale via `serp-analysis` veloce, o WebSearch + WebFetch). Per questa skill servono almeno i top 5.
- Tieni i `content` puliti dal boilerplate (header, footer, sidebar, banner cookie). Tronca i body al primo blocco di ~3‑5k caratteri di contenuto utile per non gonfiare le chiamate `rerank`.

In modalità `verify`, usa **lo stesso corpus competitor** del baseline per rendere i confronti comparabili.

### Step 3 — Rerank competitivo per keyword (tool `rerank`)

Per ciascuna delle 1‑3 keyword target, una chiamata `rerank`:

- `query`: la keyword **formulata come domanda utente naturale** in lingua target (es. "meditazione mindfulness" → "cos'è la meditazione mindfulness e come si pratica?").
- `documents`: `[{id: "ours", title: <H1 articolo>, content: <body articolo>}, {id: "comp_1", title: ..., content: ...}, ..., {id: "comp_5", ...}]`.

Dal response leggi gli `score` (0–1) e l'ordinamento. Per ogni keyword registra:

- **Posizione dell'articolo target** nel ranking (1° / 2° / ... / N°).
- **Score** dell'articolo target.
- **Score top‑1** competitor.
- **Delta score** rispetto al top‑1 (= top‑1 − ours; più alto = peggio).
- I **top 3 competitor** con i loro score.

Interpretazione di base (qualitativa, non normativa):
- Articolo in **top‑3** con score vicino al top‑1: siamo competitivi, l'AIO ha buone ragioni per considerarci tra le fonti candidate. Il lavoro è di rifinitura sui blocchi.
- Articolo **fuori top‑3** o con delta > ~0.2 dal top‑1: gap strutturale di rilevanza. L'intervento sarà più ampio e mirato ai differenziatori dei top.
- Articolo **ultimo o con score molto basso**: serve diagnosi profonda. Probabile disallineamento di intento o argomento.

### Step 4 — Coverage map sotto-query × sezioni (tool `rerank`)

Per ciascuna sotto-query del **fan-out** (da `serp-analysis` Step 6, con i suoi tag content-type + ambito di intento), una chiamata `rerank`:

- `query`: la sotto-query formulata come domanda.
- `documents`: le **sezioni dell'articolo target** (`[{id: "sec_h2_1", title: <heading>, content: <testo sezione>}, ...]`). Puoi opzionalmente aggiungere 1‑2 sezioni dei top competitor per quella sotto-query (se identificabili) come riferimento, ma il focus è capire **quale sezione nostra copre meglio** la sotto-query.

Dal response leggi il top-score per sotto-query. Per ciascuna registra:

- La **sezione vincente** (la nostra) e il suo `score`.
- Se `score_max < 0.30` (soglia indicativa): **sotto-query non coperta** → gap. Le "gap citabile" del fan-out (Step 6 di `serp-analysis`) confermate qui da score basso sono **priorità massima**.
- Se più sotto-query convergono sulla stessa sezione vincente: la sezione è un nodo forte, fa più di un lavoro (positivo per estraibilità ma può anche essere segnale di accumulo: valuta se splittare).
- **Sezioni outlier**: quelle che non vincono mai su nessuna sotto-query e hanno sempre score basso → candidate `RIMUOVI` o `UNISCI` nella scaletta.

### Step 5 — Mappa semantica via embedding (tool `embed`)

Genera embedding (`taskType: RETRIEVAL_DOCUMENT` per contenuti, `RETRIEVAL_QUERY` per query) per:

- `D_ours`: articolo target (intero).
- `D_secs`: ciascuna sezione dell'articolo.
- `D_comp_i`: ciascun competitor (intero).
- `Q_kw_j`: ciascuna delle 1‑3 keyword target (come domanda naturale).
- `Q_sub_k`: ciascuna sotto-query del fan-out.

Con uno script Python (numpy via Bash), calcola le **cosine similarity** locali:

- **Sim articolo ↔ competitor**: vettore di N similarità. Identifica i competitor più vicini e i più lontani (chi presidia il nostro stesso angolo, chi un angolo diverso).
- **Distanza dal nucleo del topic**: calcola il **centroide** dei competitor (media dei vettori), poi `1 − cos(D_ours, centroide)`. Più alto = più lontani dal "nucleo" del topic (questo è il **gap semantico** in stile SEOZoom).
- **Coverage matrix sezione × sotto-query**: per ogni (sezione, sotto-query) calcola la similarità. Le sotto-query con max-similarity < ~0.5 sono gap di copertura semantica (confronta col risultato del rerank Step 4: se entrambi indicano gap, segnale forte).
- **Outlier sezioni**: per ogni sezione, calcola la sim al centroide dei competitor. Sezioni con sim molto bassa rispetto alle altre sezioni dell'articolo = candidati off-topic.

Salva la mappa in forma di tabelle compatte: top‑N competitor più simili, distanza dal centroide, matrice coverage compatta (es. solo gap evidenti), sezioni outlier.

### Step 6 — Sintesi e cross-check con `serp-analysis`

Componi un quadro unificato che lega i tre segnali (rerank competitivo, coverage map, mappa semantica) con gli output di `serp-analysis` (se disponibili):

- **Snapshot AIO reale (DataForSEO, `serp-analysis` Step 5)**: il sito è già citato dall'AIO? Le fonti che cita sono le stesse che il rerank/embed indicano come più rilevanti? Una buona sovrapposizione = il proxy Vertex è ben tarato per questa keyword. Una sovrapposizione bassa = entrambe le fonti restano valide ma con pesi diversi (DataForSEO è "verità terreno", Vertex è il laboratorio dove testare le modifiche).
- **Fan-out predittivo (`serp-analysis` Step 6) vs gap di copertura misurati**: le sotto-query "gap citabile" del fan-out predittivo confermate dai numeri (Step 4 e Step 5 qui) diventano **priorità massima** nelle raccomandazioni. Quelle non confermate (score di copertura alto contro l'aspettativa) escono dalla priorità immediata.
- **Sezioni "candidate alla citazione"**: quelle che (a) vincono almeno una sotto-query in Step 4 con score alto, (b) hanno sim alta al cluster competitivo in Step 5 e (c) sono già in apertura formato BLUF (lettura Step 1). Su queste si concentra il lavoro di rifinitura per puntare alla citazione.
- **Sezioni "da riscrivere"**: quelle che il rerank non sceglie mai e che la mappa semantica indica come outlier.
- **Sotto-query scoperte di alto valore**: quelle con score basso ovunque ma con ambito di intento `informational` o `fiducia/affidabilità` (priorità AIO).

### Step 7 — Raccomandazioni di re-ranking

Produci un elenco **prioritizzato** di interventi per aumentare la probabilità di citazione. Ogni raccomandazione deve essere concreta (cosa fare, dove farlo, perché) e direttamente integrabile nella **Fase 4 di `existing-page-optimizer`** come voce della scaletta di modifiche.

**Tre principi guida** (sempre, ogni raccomandazione li applica):

- **Chunking — ogni blocco regge da solo.** Definizione autoconsistente, esempio che chiarisce senza rumore, sezione che risponde a **una** sola domanda precisa. È la condizione perché il modello generativo possa riusare il blocco come fonte estraendolo dal contesto. Se un paragrafo ha senso solo letto dentro al precedente, non è un candidato alla citazione.
- **Heading dichiarativi.** Ogni H2/H3 deve dichiarare quale porzione del bisogno copre, in forma vicina alla domanda dell'utente (es. "Quanto costa X in media nel 2026" anziché "Prezzi"; "Come configurare X da zero" anziché "Configurazione"). Il modello usa l'heading come segnale primario per associare un blocco a una sotto-query.
- **Information gain.** I differenziatori devono aggiungere qualcosa che non è già nell'indice (dato primario, esempio reale, screenshot, grafico originale, prospettiva specialistica). Riformulare in altra forma ciò che le fonti già citate dicono non sposta la citazione: il modello non ha incentivi a sostituirle. Cerca l'angolo che le fonti citate non hanno.

Categorie di intervento da considerare (non tutte sono sempre applicabili):

- **Estraibilità — risposta diretta in apertura di sezione (BLUF).** Per ciascuna sotto-query non coperta o coperta male, identificare l'H2/H3 candidato a rispondere e portare in apertura una risposta diretta di 1‑3 frasi che il modello possa estrarre come blocco.
- **Copertura semantica delle sotto-query.** Per le sotto-query del fan-out (`serp-analysis` Step 6) non ancora coperte secondo il rerank Step 4 (max-score < ~0.30) e/o secondo la sim Step 5 (max-sim < ~0.5): aggiungere sezione o sotto-paragrafo dedicato. Le sotto-query "gap citabile" del fan-out confermate qui dai numeri sono priorità massima.
- **Ambito di intento della sotto-query.** Oltre al content-type (definizione, come/perché, confronto, ecc.) considera l'ambito di intento della sotto-query: *informational*, *valutazione/comparazione*, *fiducia e affidabilità*, *transactional*, *follow-up*. Le sotto-query nell'ambito **fiducia/affidabilità** sono particolarmente sensibili per la citazione AIO perché toccano segnali E‑E‑A‑T (autore, fonti, dati con provenienza, prove): coprile in modo verificabile, non con dichiarazioni.
- **Differenziatori rispetto ai competitor di citazione (information gain).** Cosa hanno che noi non abbiamo? Più importante: cosa **non** hanno che noi possiamo aggiungere di originale? Dato primario, intervista, caso studio nostro, screenshot di un tool che usiamo, grafico costruito su dati propri. Indica per ciascun differenziatore l'intervento puntuale.
- **Struttura per l'estrazione.** Heading dichiarativi (vedi sopra), tabelle e elenchi dove il contenuto è enumerabile, definizioni come frasi compatte autoconsistenti, FAQ inline (mai sezione "Domande frequenti" a fine articolo come raccolta).
- **Multimodale e alt text.** I sistemi AI multimodali leggono le immagini insieme al testo. Per le sezioni candidate alla citazione, valuta se un'immagine/grafico/screenshot rafforza il blocco e se l'alt text descrive cosa l'immagine mostra e la sua funzione nel ragionamento (non ripete la keyword). Un'infografica con dati propri o uno screenshot di un tool è information gain reale, difficile da sostituire.
- **Segnali E‑E‑A‑T.** Autore con credenziali, data di pubblicazione/aggiornamento, fonti esterne citate con link, dati con cifre e provenienza. Le fonti citate dall'AI tendono ad avere segnali E‑E‑A‑T forti.
- **Metadati e title.** Se il title o l'H1 attuale non contengono la sotto-query chiave o non sono formulati come la domanda dell'utente, proporne una revisione (con verifica caratteri ≤ 55 / ≤ 160 via script).

Ogni raccomandazione include: **azione** (cosa fare), **punto** (dove nell'articolo), **perché** (sotto-query coperta, competitor superato, segnale E‑E‑A‑T, principio guida toccato), **priorità** (alta/media/bassa).

### Step 8 — Confronto baseline → verify (solo in modalità verify)

Se l'esecuzione è in modalità `verify` (output precedente di questa skill presente nel contesto), riusa **le stesse keyword, le stesse sotto-query del fan-out e lo stesso corpus competitor** del baseline per rendere comparabili i numeri. Poi calcola i delta:

- **Delta rilevanza competitiva** per keyword (Step 3): posizione di ranking salita? `score` dell'articolo aumentato? Il **delta dal top‑1** competitor si è ridotto? Una risalita di posizione + delta che cala è il segnale più forte.
- **Delta coverage sotto-query × sezioni** (Step 4): quante delle sotto-query "gap citabile" del baseline sono ora coperte (score > 0.30)? Il numero di sotto-query con copertura sopra soglia è cresciuto?
- **Delta mappa semantica** (Step 5): la distanza dal centroide dei competitor è calata? La sezione vincente per le sotto-query critiche ha sim più alta a quelle sotto-query?
- **Confronto con AIO reale (`serp-analysis` Step 5)**: se hai accesso ai dati DataForSEO aggiornati, verifica se il sito è ora citato dall'AIO reale. È la "verità terreno" da accostare al proxy Vertex.
- **Esito complessivo**: dichiara esplicitamente "rilevanza in salita / stabile / in calo" e per le sotto-query "coperte / parzialmente coperte / ancora scoperte". Evita affermazioni assolute sulla citazione AIO: i numeri Vertex sono proxy, non oracoli.
- Se permangono gap: produci **nuove raccomandazioni mirate ai gap residui** (non ripetere quelle già attuate).

---

## Output

Usa questa struttura. Adatta al formato finale richiesto in configurazione.

---

**AI OVERVIEW RE-RANKER — [URL articolo target]**

**KEYWORD ANALIZZATE**
- [keyword 1] — [lingua / paese]
- [keyword 2]
- [keyword 3]

*Modalità: baseline / verify. Se Vertex non era disponibile, segnalalo qui.*

---

**RILEVANZA COMPETITIVA (rerank per keyword)**

*[keyword 1]* — query: "[domanda naturale usata nel rerank]"
- Articolo target: posizione [X]/[N] — score [0.XX]
- Top‑1 competitor: [URL] — score [0.XX]
- Delta dal top‑1: [+0.XX]
- Top 3 ranking: 1) [URL/ours] [score] · 2) [URL] [score] · 3) [URL] [score]

*[keyword 2] … [keyword 3]* — stesso schema.

**COVERAGE MAP SOTTO-QUERY × SEZIONI**

| Sotto-query (ambito) | Sezione vincente | Score | Esito |
|---|---|---|---|
| [sotto-query — informational/valutazione/fiducia/transactional/follow-up] | [H2/H3 vincente] | [0.XX] | [coperta / parz. / **gap citabile**] |
| … | … | … | … |

*Sezioni che non vincono mai su nessuna sotto-query e con score basso: [elenco] → candidate `RIMUOVI` o `UNISCI`.*

**MAPPA SEMANTICA (embedding)**

- Distanza dal centroide dei competitor: [0.XX] — interpretazione: [vicini al nucleo / margine / lontani].
- Competitor più simili al nostro articolo: [top 3 URL con sim].
- Sotto-query con max similarità sezione bassa (< ~0.5): [elenco] (confronto con coverage map sopra).
- Sezioni outlier (sim bassa al centroide dei competitor): [elenco] (candidate revisione/rimozione).

**CROSS-CHECK CON SERP-ANALYSIS** *(se disponibile)*

- Snapshot AIO DataForSEO (Step 5) vs rerank/embed Vertex: [sovrapposizione fonti / coerenza alta/media/bassa].
- Fan-out predittivo (Step 6) vs gap misurati: [sotto-query "gap citabile" confermate dai numeri → priorità massima; sotto-query non confermate → escono dalla priorità].
- Sezioni candidate alla citazione (alta sim + score alto + BLUF in apertura): [elenco].

**RACCOMANDAZIONI DI RE-RANKING** *(prioritizzate, integrabili nella Fase 4 di existing-page-optimizer)*

1. **[Azione]** — Punto: [H2/H3 o "metadati"] — Perché: [sotto-query coperta, score baseline X → atteso Y; principio guida toccato] — Priorità: [alta/media/bassa]
2. …
3. …

**CONFRONTO BASELINE → VERIFY** *(solo in modalità verify)*

- Delta rilevanza competitiva per keyword: [es. "keyword 1: pos 5 → pos 2; score 0.42 → 0.58; delta dal top‑1 0.21 → 0.05"]
- Delta coverage sotto-query: [N sotto-query coperte sopra soglia: baseline X → verify Y]
- Delta mappa semantica: [distanza dal centroide: 0.XX → 0.XX]
- Esito: [rilevanza in salita / stabile / in calo per keyword]
- Gap residui e nuove raccomandazioni: [elenco]
- Gap residui e nuove raccomandazioni: [elenco]

**NOTE OPERATIVE** *(solo se rilevanti)*
[Limitazioni del proxy Vertex (rerank + embed) vs AIO reale, run condizionati da Vertex non disponibile, corpus competitor incompleti, troncamenti dei body per rispettare i limiti di `rerank`, ecc. Massimo 3 righe.]

---

## Regole critiche

- L'oggetto di questa skill è **solo** il posizionamento come fonte nell'AI Overview di Google. Non è un'ottimizzazione SEO generale e non riscrive l'articolo: produce diagnosi + raccomandazioni. La riscrittura passa per `existing-page-optimizer` (Fase 4 → Fase 5).
- I tool `rerank` e `embed` del Vertex MCP danno un **proxy discriminativo + vettoriale** della rilevanza secondo i modelli di Google: **non sono** l'AI Overview ufficiale. Lo dichiari esplicitamente nell'output. Per lo snapshot reale dell'AIO c'è `serp-analysis` Step 5 (DataForSEO); il proxy Vertex va letto per direzione e per delta baseline/verify, non come "siamo nell'AIO sì/no".
- Massimo 3 keyword per run: oltre rischi di diluire le raccomandazioni e gonfiare i costi di chiamata. Se l'utente ne fornisce di più, chiedigli di selezionare le 3 priorità.
- Una chiamata `rerank` separata per keyword (Step 3) e una per sotto-query (Step 4): non concatenare query in un'unica chiamata — il modello produce un singolo ranking per query.
- La `query` di `rerank` va sempre formulata come **domanda utente naturale** in lingua target: la keyword grezza dà score meno discriminativi. Esempio: "meditazione mindfulness" → "cos'è la meditazione mindfulness e come si pratica?".
- Per `embed`, usa `taskType: RETRIEVAL_QUERY` per keyword e sotto-query, `RETRIEVAL_DOCUMENT` per articolo, sezioni e competitor: i due task type sono progettati per il retrieval cross-modale e non vanno mischiati.
- Le cosine similarity vanno calcolate localmente (numpy via Bash): il tool `embed` restituisce vettori, non similarità. Non improvvisarle a occhio.
- In modalità `verify`, riusa **identici** keyword, sotto-query, prompt e corpus competitor del baseline: altrimenti il confronto non è valido.
- Se il Vertex MCP non è disponibile, **non bloccare**: produci comunque raccomandazioni basate su `serp-analysis` Step 5 + 6, dichiarando il degrado. I tre principi e le categorie restano applicabili.
- Le raccomandazioni devono essere **azionabili e specifiche**: indicare cosa, dove, perché, priorità. Le raccomandazioni generiche ("migliora l'articolo") non vanno bene.
- I tre principi guida — **chunking**, **heading dichiarativi**, **information gain** — sono trasversali: ogni raccomandazione deve toccarne almeno uno. Un blocco che non regge estratto, un heading vago o una sezione che ripete contenuto già presente nelle fonti citate non sposta la citazione.
- Le sotto-query nell'ambito **fiducia/affidabilità** vanno coperte in modo verificabile (dati con provenienza, autore identificabile, fonti esterne con link), non con dichiarazioni: sono il canale più diretto verso la citazione AIO perché toccano E‑E‑A‑T.
- Multimodale: se il blocco candidato alla citazione contiene o può contenere un'immagine, l'alt text deve descriverne contenuto e funzione, mai ripetere la keyword. Una visualizzazione con dati propri rende il blocco più difficile da sostituire.
- Eredita le keyword e il fan-out dal contesto quando possibile (`existing-page-optimizer` Fase 3, `keyword-analysis`, `serp-analysis` Step 6): non rifare il lavoro se è già disponibile.
- Mai consigliare una sezione "Domande frequenti" / "FAQ" a fine articolo come raccolta in elenco: le sotto-query si integrano come heading o risposte inline, come da regole del flusso.
- Se il flusso gira in un progetto Claude con istruzioni/knowledge, rispettale: le raccomandazioni devono essere compatibili con il tone of voice, le linee guida editoriali e i vincoli del progetto.
