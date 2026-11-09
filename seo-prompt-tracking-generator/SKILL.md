---
name: seo-prompt-tracking-generator
description: "Trasforma keyword SEO (export Google Search Console, lista incollata o connettore GSC) e info su brand e competitor in prompt conversazionali per il tracking GEO e la Sentiment Analysis su ChatGPT, Perplexity, Gemini e Claude. Applica la Matrice 4x4: 4 categorie (Brand Discovery, Comparative / Versus, Problem / Solution, Customer Care / Crisis) per 4 varianti di prompt per keyword. Restituisce in chat tabella markdown e CSV pronto per i tool di AI visibility. Trigger: \"genera i prompt di tracking per il brand X\", \"trasforma queste keyword GSC in prompt per LLM\", \"prompt per monitorare il sentiment del brand su ChatGPT\", \"prompt set per GEO tracking\". Non esegue i prompt e non misura il sentiment."
---

# SEO PROMPT TRACKING GENERATOR

Questa skill converte keyword SEO "secche" (come le digita un utente su Google) in **domande naturali** come le porrebbe un utente a un assistente AI, organizzate per misurare due cose:

- **Visibilità GEO**: il brand viene citato, raccomandato o linkato come fonte quando l'utente chiede qualcosa sul settore?
- **Sentiment**: quando il brand viene citato, in che tono ne parla il modello (positivo, neutro, critico) e rispetto a quali competitor?

Il destinatario dell'output è il team SEO / GEO che deve caricare i prompt in un tool di monitoraggio (Peec AI, Profound, Otterly, Semrush AI Toolkit, SE Ranking AI, oppure un foglio di test manuale) e interrogare periodicamente ChatGPT, Perplexity, Gemini e Claude.

**Cosa NON fa questa skill:**

- Non interroga gli LLM e non calcola il sentiment: produce solo il set di prompt.
- Non inventa keyword: parte sempre da keyword reali fornite dall'utente o lette da GSC. Può solo derivare varianti conversazionali.
- Non inventa difetti, scandali o problemi del brand: i prompt della categoria Customer Care / Crisis si basano sui temi presenti nelle keyword o indicati dall'utente.

---

## FILE DELLA SKILL

| File | Quando leggerlo |
|---|---|
| `references/matrice-4x4.md` | Prima della Fase 4. Definisce le 4 categorie, le 4 varianti di prompt e i template per ciascuna cella. |
| `references/regole-conversione.md` | Prima delle Fasi 3 e 4. Regole per classificare le keyword e trasformarle da keyword secche a prompt conversazionali, con checklist di qualità. |
| `references/esempio-output.md` | Prima della Fase 5. Esempio completo di output (tabella + CSV) da usare come riferimento di formato. |
| `templates/keyword-input-template.csv` | Da proporre all'utente se non ha un file pronto, come formato di input. |

---

## FASE 0, WIZARD DI BRIEF

Prima di generare qualsiasi prompt raccogli il brief. Se un'informazione è già presente nel contesto (messaggio dell'utente, file allegato, conversazione precedente) **non richiederla**: riportala nel riepilogo della Fase 0.6 per conferma. Fai le domande mancanti in un unico blocco con AskUserQuestion, oppure in chat se servono risposte libere.

### STEP 0.1, BRAND PRINCIPALE

- Nome del brand (e varianti con cui viene scritto o cercato: acronimi, nome del dominio, nome del prodotto di punta).
- Dominio del sito.

### STEP 0.2, COMPETITOR

- Nomi dei competitor da includere (consigliati 3-5).
- Se l'utente non li ha pronti, proponi di ricavarli dalle keyword Versus del dataset o dalle query GSC che contengono nomi di altri brand, e chiedi conferma prima di usarli.

### STEP 0.3, SETTORE E CONTESTO

- Settore / nicchia di riferimento (es. "e-commerce arredamento outdoor", "software gestionale per studi dentistici").
- Target principale (B2C, B2B, professionisti, fascia di prezzo) se rilevante.
- Prodotti o servizi principali.
- Mercato geografico (paese, eventuale area locale).

### STEP 0.4, LINGUA DEI PROMPT

Chiedi **sempre** in che lingua generare i prompt. Non assumere un default. Se l'utente indica più lingue, genera un set completo per ciascuna lingua (non tradurre letteralmente: adatta formule e riferimenti al mercato, vedi `references/regole-conversione.md`).

### STEP 0.5, SORGENTE DELLE KEYWORD

Le keyword possono arrivare da tre fonti, anche combinate:

1. **File** (CSV o XLSX esportato da Google Search Console, Ahrefs, Semrush, SEOZoom). Leggi il file e individua le colonne utili: `query` / `keyword`, `clicks`, `impressions`, `position`, ed eventuale colonna di tipo (`Brand`, `Non-Brand`, `Versus`, `Long-tail`).
2. **Lista incollata** in chat, anche già suddivisa per tipo.
3. **Connettore Google Search Console** (tool `mcp__GSC-MCP__*`), solo se l'utente lo chiede o lo conferma:
   - usa `list_clients` / `resolve_client` per individuare la property del brand;
   - usa `get_search_queries` (o `get_search_analytics` con dimensione query) sugli ultimi 3 mesi, salvo diversa indicazione;
   - recupera query, click, impression e posizione media.

Se l'utente non ha un file, proponi il formato `templates/keyword-input-template.csv`.

**Volume da lavorare.** Ogni keyword genera fino a 16 prompt (4 categorie x 4 varianti). Se il dataset contiene più di 25 keyword, chiedi all'utente come selezionarle:

- top N per click o impression (default proposto: top 25);
- un numero bilanciato per tipo (es. 5 Brand, 5 Versus, 10 Non-Brand, 5 Long-tail);
- lista scelta a mano dall'utente.

### STEP 0.6, RIEPILOGO E CONFERMA

Riassumi il brief e chiedi conferma prima di procedere:

```
BRIEF PROMPT TRACKING
- Brand: [...] (varianti: [...]) , dominio: [...]
- Competitor: [...]
- Settore / nicchia: [...]
- Mercato: [...]
- Lingua dei prompt: [...]
- Sorgente keyword: [file / lista / GSC, periodo]
- Keyword da lavorare: [N] (criterio di selezione: [...])
- LLM target: ChatGPT, Perplexity, Gemini, Claude

Procedo con la generazione? (sì/no)
```

---

## FASE 1, PULIZIA DEL DATASET

1. Normalizza le keyword: minuscolo, spazi singoli, rimozione di duplicati e varianti identiche (singolare/plurale, con o senza accento).
2. Escludi le query non utilizzabili e dichiaralo nel riepilogo finale:
   - query di navigazione pura senza contenuto (`login`, `area riservata`, `www.brand.it`);
   - query di altri brand non presenti nella lista competitor e non del settore;
   - query offensive, spam o non pertinenti.
3. Se presenti, conserva click, impression e posizione: servono a ordinare l'output.

---

## FASE 2, CLASSIFICAZIONE DELLE KEYWORD

Se il dataset non è già suddiviso, assegna a ciascuna keyword un **Tipo** applicando le regole di `references/regole-conversione.md` (sezione "Classificazione"):

| Tipo | Definizione |
|---|---|
| **Brand** | Contiene il nome del brand o una sua variante. |
| **Versus** | Contiene il brand e/o un competitor insieme a segnali di confronto (`vs`, `o`, `meglio`, `alternativa`, `differenza`, `confronto`). |
| **Non-Brand** | Keyword generica di settore, senza nomi di brand, con 1-3 parole. |
| **Long-tail** | Keyword generica di 4 o più parole, spesso in forma di domanda o con specificazioni (uso, prezzo, luogo, target). |

Assegna inoltre un **segnale di criticità** (Sì/No) se la keyword contiene termini da Customer Care / Crisis (`reso`, `rimborso`, `recensioni negative`, `truffa`, `non funziona`, `assistenza`, `reclamo`, `ritardo`, `opinioni`, `reddit`, `trustpilot`). Le keyword con segnale = Sì alimentano in via prioritaria la categoria Customer Care / Crisis.

Mostra all'utente un riepilogo compatto della classificazione (conteggio per tipo ed elenco delle keyword ambigue) e chiedi conferma solo sulle ambigue.

---

## FASE 3, MAPPATURA KEYWORD, CATEGORIA, INTENT

Ogni keyword genera prompt in **tutte e 4 le categorie** della matrice, ma con un peso diverso. La categoria **primaria** è quella più coerente con il tipo di keyword e determina l'ordine nell'output:

| Tipo keyword | Categoria primaria | Funnel / Intent |
|---|---|---|
| Brand | Brand Discovery & Awareness | Awareness, navigazionale/informativo |
| Brand + segnale criticità | Customer Care / Crisis | Post-acquisto, supporto |
| Versus | Comparative / Versus | Consideration, commerciale |
| Non-Brand | Problem / Solution | Awareness / Consideration, informativo |
| Long-tail | Problem / Solution (o Comparative se contiene "migliore", "quale scegliere") | Consideration / Decision |

Per le keyword Non-Brand e Long-tail le categorie Brand Discovery e Customer Care si costruiscono **innestando il brand sul tema della keyword** (es. keyword `divano da esterno resistente` diventa "[Brand] fa divani da esterno davvero resistenti?").

Le regole complete di mappatura sono in `references/regole-conversione.md`.

---

## FASE 4, GENERAZIONE DEI PROMPT (MATRICE 4x4)

Leggi `references/matrice-4x4.md` e, per ogni keyword selezionata, genera **4 prompt per ciascuna delle 4 categorie**, uno per ogni variante:

| Variante | Formula | Scopo |
|---|---|---|
| **V1, Domanda diretta** | Domanda secca, come la scriverebbe l'utente | Risposta base del modello |
| **V2, Raccomandazione** | Richiesta di consiglio, lista o classifica | Misura chi viene raccomandato e in che ordine |
| **V3, Scenario / persona** | Domanda calata in un caso d'uso concreto con vincoli (budget, uso, luogo) | Misura la pertinenza percepita del brand |
| **V4, Fonti e prova sociale** | Richiesta di opinioni, recensioni, esperienze, fonti | Misura sentiment e fonti citate (Reddit, Trustpilot, Google, stampa) |

### REGOLE NON NEGOZIABILI

1. **Unbranded resta unbranded.** Nella categoria Problem / Solution i prompt **non contengono mai** il nome del brand né dei competitor: servono a misurare se il brand emerge spontaneamente (share of voice organico).
2. **Comparative.** Almeno 2 delle 4 varianti nominano esplicitamente brand e competitor; le altre usano formule aperte ("alternative a [Competitor]", "chi è meglio per [esigenza]") per misurare il posizionamento relativo.
3. **Customer Care / Crisis** è sempre branded e affronta solo temi plausibili per il settore o presenti nelle keyword: non inventare scandali o accuse.
4. **Linguaggio naturale.** Ogni prompt è una frase completa che un utente reale scriverebbe in chat: no elenchi di keyword, no operatori di ricerca, no virgolette forzate.
5. **Neutralità.** I prompt non devono suggerire la risposta né contenere giudizi a favore del brand ("perché [Brand] è il migliore?" è vietato; "[Brand] è una buona scelta per...?" è corretto).
6. **Lunghezza.** Tra 8 e 35 parole. Le varianti V3 possono arrivare a 45 parole.
7. **Niente duplicati.** Se due keyword simili producono lo stesso prompt, tienine uno e associa entrambe le keyword nella colonna Keyword SEO separate da ` | `.
8. **Niente trattino lungo** nei testi dei prompt: usa la virgola.
9. **Lingua e registro** coerenti con il mercato indicato nello Step 0.4.

Applica la checklist di qualità di `references/regole-conversione.md` prima di passare alla Fase 5.

---

## FASE 5, OUTPUT

Restituisci l'output **come testo in chat**, nell'ordine seguente. Usa `references/esempio-output.md` come riferimento di formato.

### 5.1, RIEPILOGO DEL SET

Un breve blocco con: brand, competitor, lingua, numero di keyword lavorate per tipo, numero totale di prompt per categoria, keyword escluse e motivo.

### 5.2, TABELLA MARKDOWN

Una tabella per categoria (4 tabelle in totale), con le colonne:

| Colonna | Contenuto |
|---|---|
| `ID` | Codice univoco: sigla categoria + progressivo (`BD-001`, `CV-001`, `PS-001`, `CC-001`) |
| `Funnel / Intent` | Awareness, Consideration, Decision, Post-acquisto + intent (informativo, commerciale, transazionale, supporto) |
| `Tipo KW` | Brand, Non-Brand, Versus, Long-tail |
| `Keyword SEO` | Keyword di partenza (una o più, separate da barra verticale) |
| `Variante` | V1, V2, V3, V4 |
| `Prompt` | Testo del prompt |
| `Branded` | Sì / No |
| `Cosa monitorare` | Metrica principale: menzione, posizione nella lista, sentiment, competitor citati, fonti citate |

Ordina le righe per categoria e, all'interno, per keyword con più click (o impression se i click non ci sono).

### 5.3, BLOCCO CSV

Subito dopo le tabelle, un unico blocco di codice ```csv con **tutti** i prompt e le stesse colonne della tabella più `Categoria` e `Lingua`, separatore virgola, testi tra doppi apici, intestazione in prima riga. È il dataset da importare nel tool di tracking.

### 5.4, VOLUMI GRANDI

Se il set supera i 200 prompt, consegna le tabelle markdown e il CSV **per categoria**, in messaggi successivi, annunciando all'inizio quanti blocchi arriveranno. Non troncare mai il CSV e non usare "..." per abbreviare.

### 5.5, NOTE OPERATIVE (BREVI)

Chiudi con massimo 5 punti elenco su come usare il set:

- frequenza consigliata di esecuzione (es. settimanale per Customer Care / Crisis, mensile per le altre);
- esecuzione con cronologia e memoria disattivate, in sessione anonima;
- eseguire gli stessi prompt su tutti e 4 gli LLM per avere dati confrontabili;
- registrare per ogni risposta: menzione del brand (Sì/No), posizione, sentiment (positivo/neutro/negativo), competitor citati, fonti citate.

---

## FORMATO DI CONSEGNA

L'output di default è **testo in chat** (tabella + CSV). Se l'utente chiede esplicitamente un altro formato (artifact, file .csv, .xlsx, Google Sheet), chiedi conferma del formato e rispetta il brand Moca (font Figtree, palette Moca) per gli output visuali.
