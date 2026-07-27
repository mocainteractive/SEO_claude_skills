---
name: seo-keyword-strategy
description: "Esegue una keyword research SEO completa e modulare per il team SEO. Copre tre scenari: ricerca per un nuovo sito/progetto, ottimizzazione di un sito esistente, o ricerca focalizzata su una singola pagina/contenuto. Conduce un wizard step-by-step che raccoglie il brief, attinge dati da Ahrefs MCP, Google Search Console (via Ahrefs MCP), Google Autocomplete, Google Trends e — solo quando opportuno — SERP scraping, e produce un file Excel multi-sheet con keyword, volume, KD, CPC, intent, cluster e gap competitor. L'output contiene esclusivamente dati provenienti dagli strumenti SEO: nessun Opportunity Score AI-generated, nessuna prioritizzazione arbitraria, nessuna nota strategica narrativa. Trigger tipici: \"fammi una keyword research per [cliente/sito]\", \"keyword strategy per [progetto]\", \"ricerca keyword per il sito X\", \"gap analysis keyword vs competitor\", \"keyword research completa per il nuovo cliente\", \"analisi keyword per la pagina Y\". Distinta dalla skill `keyword-analysis`, che è invece focalizzata su un singolo articolo blog all'interno della pipeline `seo-blog-pipeline`."
---

# SEO Keyword Strategy

Questa skill esegue una keyword research SEO modulare e completa per il team SEO, adattandosi a tre scenari di lavoro distinti. È un'attività guidata che parte da un brief raccolto via wizard step-by-step, integra dati reali dagli strumenti SEO (Ahrefs MCP, GSC, Google Autocomplete, Google Trends, eventuale SERP scraping mirato) e restituisce un file Excel multi-sheet con la sola ricerca keyword pulita.

**Cosa NON fa questa skill:**
- Non calcola Opportunity Score compositi generati dall'AI.
- Non assegna priorità Alta/Media/Bassa generate dall'AI.
- Non produce report markdown narrativi né note strategiche.
- Non sostituisce il giudizio del SEO specialist sulla strategia: produce solo la materia prima (dati).
- Non scrapa la SERP di tutte le keyword in un progetto full-site: il SERP scraping è riservato a singola pagina o keyword dubbiose.

La Keyword Difficulty riportata è SEMPRE quella restituita dagli strumenti SEO (Ahrefs di default), mai stimata da Claude.

---

## Fase 0 — Wizard di brief iniziale

Prima di qualsiasi chiamata ai tool, raccogli il brief facendo le seguenti domande all'utente, **una alla volta** o in piccoli gruppi correlati, attendendo risposta prima di procedere. Non fare assunzioni implicite: ogni decisione deve essere confermata.

### Step 0.1 — Scenario di lavoro

Chiedi quale dei tre scenari serve:

1. **Nuovo progetto / nuovo sito**: keyword research da zero per impostare struttura del sito, piano editoriale, opportunità di mercato. Tipicamente più ampia, con clusterizzazione.
2. **Ottimizzazione sito esistente**: si lavora su un sito già online. Si recupera GSC, si fa gap analysis vs competitor, si individuano keyword "fortunate" su cui rafforzarsi e nuove opportunità.
3. **Singola pagina / contenuto specifico**: ricerca focalizzata su una keyword seme o un topic per produrre una sola pagina. Workflow più snello, può includere SERP scraping della SERP principale.

### Step 0.2 — Mercato e lingua

- Paese target (default: Italia / `it`).
- Lingua dei contenuti (default: italiano).
- Se l'utente conferma un mercato estero, usa il country code corrispondente in tutte le chiamate Ahrefs.

### Step 0.3 — Input di base

In base allo scenario:

- **Nuovo progetto**: dominio (se esiste landing/coming-soon), nicchia/settore, prodotti/servizi principali, lista di seed keyword o topic principali, eventuali competitor di riferimento noti.
- **Sito esistente**: dominio cliente, eventuale accesso GSC (verifica se è collegato ad Ahrefs come progetto), lista competitor da analizzare, area del sito su cui concentrarsi (oppure intero sito).
- **Singola pagina**: keyword seme o topic, eventuale URL della pagina (se esistente da ottimizzare), eventuali competitor diretti per quella SERP.

### Step 0.4 — Gap analysis competitor

Chiedi esplicitamente:
- Vuoi includere una gap analysis vs competitor? **Sì / No**
- Se sì: lista dei competitor (max 5 raccomandato). Se l'utente non li ha pronti, suggerisci di derivarli da `site-explorer-organic-competitors` sul dominio cliente o, per nuovi progetti, da una ricerca Google sulle seed keyword.

### Step 0.5 — Clusterizzazione

Chiedi:
- Vuoi che le keyword siano raggruppate in cluster tematici? **Sì / No**
- Default raccomandato: Sì per "nuovo progetto" e "sito esistente", No (o cluster light) per "singola pagina".

### Step 0.6 — Sheet Excel da includere

Presenta all'utente la lista degli sheet disponibili e fagli scegliere quali includere nell'output finale. Sheet disponibili:

- **Setup**: brief del progetto, scenario, mercato, dominio, competitor analizzati, fonti dati usate, data esecuzione.
- **Keyword list**: tabella master con tutte le keyword raccolte e le metriche grezze.
- **Cluster**: keyword raggruppate per topic con keyword pillar, satelliti, volume cumulato, intent dominante.
- **Gap analysis**: keyword presidiate dai competitor e non dal cliente (solo se gap analysis = Sì e c'è un dominio cliente).
- **GSC opportunities**: keyword "fortunate" da Google Search Console (keyword già in pagine 2-3 con buon volume, query con impression alte e CTR basso). Solo se è collegato un progetto GSC tramite Ahrefs.
- **SERP details**: per le keyword analizzate via SERP scraping (singola pagina o keyword dubbiose), riporta SERP feature, top 10, PAA, ricerche correlate.
- **Trends**: andamento storico 12 mesi delle keyword pillar (volume Ahrefs + Google Trends).
- **Autocomplete**: long-tail e varianti raccolte dal Google Autocomplete.

L'utente sceglie quali sheet vuole (multi-selezione). Non aggiungere sheet non richiesti. Non omettere sheet richiesti.

### Step 0.7 — Conferma brief

Prima di lanciare le chiamate ai tool, riassumi il brief raccolto in forma compatta e chiedi conferma:

```
BRIEF:
- Scenario: [...]
- Mercato/lingua: [...]
- Dominio cliente: [...]
- Seed keyword/topic: [...]
- Competitor: [...]
- Gap analysis: Sì/No
- Clusterizzazione: Sì/No
- Sheet Excel richiesti: [...]
- SERP scraping: applicabile a [...]

Procedo con la raccolta dati? (sì/no)
```

Se l'utente vuole modificare qualcosa, applica le correzioni e ri-conferma.

---

## Fase 1 — Raccolta dati

Le chiamate da eseguire dipendono dallo scenario e dagli sheet richiesti. Esegui solo ciò che serve effettivamente.

### 1.1 — Overview seed keyword (sempre)

Per ogni seed keyword fornita dall'utente, chiama `keywords-explorer-overview`.

Parametri:
- `keywords`: lista delle seed keyword (max 100 per chiamata)
- `country`: country code definito nel brief (default `it`)
- `select`: `keyword,volume,difficulty,intents,traffic_potential,parent_topic,serp_features,clicks,cpc,global_volume`

Salva tutti i risultati nella tabella master.

### 1.2 — Espansione semantica (se clusterizzazione = Sì oppure scenario ≠ singola pagina)

Per ogni seed keyword, chiama in parallelo:

**Matching terms** — `keywords-explorer-matching-terms`
- `keywords`: seed
- `country`: country code
- `select`: `keyword,volume,difficulty,intents,traffic_potential,parent_topic,serp_features,cpc`
- `limit`: 100
- `order_by`: `volume:desc`

**Related terms** — `keywords-explorer-related-terms`
- `keywords`: seed
- `country`: country code
- `select`: `keyword,volume,difficulty,intents,traffic_potential,parent_topic,cpc`
- `limit`: 50
- `order_by`: `volume:desc`

**Search suggestions** — `keywords-explorer-search-suggestions`
- `keywords`: seed
- `country`: country code
- `select`: `keyword,volume,difficulty,intents,cpc`
- `limit`: 50
- `order_by`: `volume:desc`

Deduplica le keyword raccolte. Non filtrare per intent in modo arbitrario: includi tutti gli intent, sarà il SEO specialist a decidere. Eccezione: scarta le keyword geolocalizzate solo se l'utente nel brief ha esplicitamente chiesto un focus nazionale; altrimenti tienile.

### 1.3 — Google Autocomplete (se sheet "Autocomplete" richiesto o se scenario = singola pagina)

Per ogni seed keyword, fai una WebFetch a:

```
https://suggestqueries.google.com/complete/search?client=firefox&hl=<lingua>&gl=<country>&q=<seed>
```

Estrai i suggerimenti. Ripeti aggiungendo lettere dell'alfabeto in coda (`seed a`, `seed b`, ...) per ampliare il set. Salva tutti i suggerimenti unici.

### 1.4 — Google Trends (se sheet "Trends" richiesto)

Per ogni keyword pillar (vedi Fase 2), recupera il trend tramite WebFetch su Google Trends. In alternativa più affidabile, usa `keywords-explorer-volume-history` di Ahrefs:

- `keyword`: pillar
- `country`: country code
- `date_from`: data attuale meno 12 mesi

Salva la serie mensile.

### 1.5 — Gap analysis competitor (se gap analysis = Sì)

Per ciascun competitor:

**Organic competitors discovery** (solo se l'utente non ha già fornito competitor) — `site-explorer-organic-competitors`
- `target`: dominio cliente
- `country`: country code
- `limit`: 10

**Keyword del competitor** — `site-explorer-organic-keywords`
- `target`: dominio competitor
- `country`: country code
- `select`: `keyword,volume,difficulty,intents,position,url,traffic,cpc`
- `limit`: 500
- `order_by`: `traffic:desc`
- Filtri: posizione 1-20

Ripeti per ogni competitor. Aggrega le keyword: una keyword presidiata da almeno N competitor (default N=2) è una candidate gap. Confronta con le keyword del cliente (`site-explorer-organic-keywords` sul dominio cliente) e marca quelle dove il cliente non rankea (o rankea oltre posizione 30).

### 1.6 — GSC opportunities (se sheet "GSC opportunities" richiesto)

Verifica che ci sia un progetto Ahrefs collegato a GSC per il dominio cliente con `management-projects`. Se sì:

- `gsc-keywords`: estrai le query del cliente con `select: keyword,impressions,clicks,ctr,position,date_from,date_to`, periodo ultimi 3 mesi.
- Filtra:
  - **Keyword fortunate**: posizione media 11-30 con impression > soglia (es. > 100/mese)
  - **Underperformer**: posizione 1-10 con CTR sotto la curva media (anomalo basso)
  - **High impression, low CTR**: impression > 500, CTR < 1%
- `gsc-pages`: per arricchire con la pagina associata.

Salva i risultati nello sheet "GSC opportunities" con colonne: query, impressions, clicks, ctr, position, page, tipologia.

### 1.7 — SERP scraping mirato (solo quando applicabile)

Esegui SERP scraping **solo** nei seguenti casi:

- **Scenario = singola pagina**: scrapa la SERP della keyword principale e di max 3-5 altre keyword satellite per capire intent reale, SERP feature, top 10, PAA, ricerche correlate.
- **Keyword dubbiose**: keyword il cui intent Ahrefs è ambiguo (es. multipli intent boolean true) o con SERP feature potenzialmente disruptive (AI Overview, shopping pack massivo). Limite massimo: 10 keyword per progetto.

Per ognuna:
- Usa `serp-overview` di Ahrefs MCP se disponibile (preferito perché dati strutturati).
- In subordine WebFetch su `https://www.google.com/search?q=<keyword>&hl=<lingua>&gl=<country>` per leggere top 10 ed elementi SERP visibili.

Salva nello sheet "SERP details": keyword, top 10 (posizione, dominio, url, title), SERP features rilevate, PAA, ricerche correlate.

**Mai eseguire SERP scraping su tutto il set di keyword di un progetto full-site.**

---

## Fase 2 — Clusterizzazione (se richiesta)

Se l'utente ha chiesto clusterizzazione:

1. Prendi tutte le keyword raccolte e deduplicate.
2. Raggruppa per `parent_topic` restituito da Ahrefs come prima base (è il segnale più affidabile, non un'invenzione di Claude).
3. Per keyword senza `parent_topic` valido, raggruppa per similarità lessicale e semantica (stesse 1-2 parole chiave nel termine, stesso intent dominante).
4. Per ogni cluster identifica:
   - **Keyword pillar**: quella con il `traffic_potential` più alto (non il volume — il traffic potential è meno fuorviante).
   - **Keyword satellite**: tutte le altre del cluster.
   - **Volume cumulato**: somma dei volumi del cluster.
   - **Intent dominante**: leggi `intents` di tutte le keyword del cluster e prendi quello prevalente (basato su conteggio dei boolean true, non su giudizi di Claude).

I cluster sono il risultato di aggregazione di dati Ahrefs, **non interpretazioni di Claude**. Se i dati Ahrefs non permettono un raggruppamento netto, lascia la keyword in un cluster "non clusterizzato" e segnalalo in chat (non nello sheet).

---

## Fase 3 — Generazione del file Excel

Genera l'Excel con `openpyxl` via Bash (Python). Salva il file nella working directory con nome:

```
keyword_research_<nome-progetto>_<YYYYMMDD>.xlsx
```

Dove `<nome-progetto>` è derivato dal dominio cliente, dalla seed principale o da un nome che l'utente ha fornito nel brief.

Includi **solo gli sheet che l'utente ha richiesto** in Fase 0.6.

### Struttura colonne per sheet

**Setup**
| campo | valore |
|---|---|
| Data esecuzione | YYYY-MM-DD HH:MM |
| Scenario | nuovo/esistente/singola pagina |
| Dominio cliente | dominio |
| Mercato | country |
| Lingua | lingua |
| Seed keyword | lista |
| Competitor analizzati | lista |
| Fonti dati usate | Ahrefs / GSC / Autocomplete / Trends / SERP |
| Sheet inclusi | lista |
| Gap analysis | Sì/No |
| Clusterizzazione | Sì/No |

**Keyword list** (master)
Colonne: `keyword`, `volume`, `keyword_difficulty`, `intent_informational`, `intent_navigational`, `intent_commercial`, `intent_transactional`, `cpc`, `traffic_potential`, `parent_topic`, `serp_features`, `cluster`, `fonte`.

- `keyword_difficulty`: valore Ahrefs (campo `difficulty`). Non sostituire con stime di Claude.
- `intent_*`: i quattro boolean restituiti da Ahrefs (`true`/`false`).
- `cluster`: nome del cluster di appartenenza (se clusterizzazione = Sì), altrimenti vuoto.
- `fonte`: Ahrefs (overview / matching / related / suggestions) / Autocomplete / GSC. Una keyword può avere fonti multiple, in tal caso concatenale.

**Cluster**
Colonne: `cluster`, `keyword_pillar`, `keyword_satellite`, `volume_cumulato`, `intent_dominante`, `numero_keyword`.
Una riga per cluster. La colonna `keyword_satellite` contiene la lista separata da `; `.

**Gap analysis**
Colonne: `keyword`, `volume`, `keyword_difficulty`, `intent`, `cpc`, `competitor_che_rankano`, `posizione_media_competitor`, `posizione_cliente` (vuota se cliente non rankea), `url_competitor_top`, `traffic_stimato`.

**GSC opportunities**
Colonne: `query`, `impressions`, `clicks`, `ctr`, `position`, `page`, `tipologia` (fortunata / underperformer / high impr low ctr).

**SERP details**
Colonne: `keyword`, `posizione`, `dominio`, `url`, `title`, `serp_features`, `paa_questions`, `related_searches`. Una riga per posizione top 10. PAA e ricerche correlate riportate solo nella prima riga di ogni keyword.

**Trends**
Colonne: `keyword`, `mese`, `volume_stimato`. Una riga per coppia (keyword, mese), serie storica 12 mesi.

**Autocomplete**
Colonne: `seed_query`, `suggerimento`, `lunghezza` (numero parole).

### Regole tecniche di generazione

- Usa header in bold, freeze pane sulla prima riga, autosize colonne (best-effort).
- Numeri: niente formattazione di Claude (no arrotondamenti narrativi). Riporta i valori come restituiti dagli strumenti.
- Non includere colonne con dati derivati o interpretati da Claude (no Opportunity Score, no priority, no commenti).
- Codifica UTF-8.
- Se uno sheet richiesto non ha dati (es. GSC non collegato), genera comunque lo sheet con sole intestazioni e una riga "Nessun dato disponibile: [motivo]". Non saltarlo silenziosamente.

---

## Fase 4 — Consegna

Una volta generato l'Excel:

1. Comunica all'utente in chat:
   - Path del file generato.
   - Numero totale di keyword raccolte.
   - Sheet inclusi.
   - Numero di cluster (se applicabile).
   - Eventuali avvisi tecnici (es. "GSC non collegato, sheet vuoto", "Competitor X non trovato in Ahrefs").
2. **Non aggiungere note strategiche, raccomandazioni di prioritizzazione, suggerimenti di pagine da creare.** La skill consegna dati grezzi; la strategia la fa il SEO specialist.
3. Non generare report markdown narrativi affiancati.

Esempio di messaggio di consegna:

```
File generato: keyword_research_cliente_20260616.xlsx

- Keyword totali: 847
- Cluster identificati: 23
- Sheet inclusi: Setup, Keyword list, Cluster, Gap analysis, GSC opportunities
- Competitor analizzati: competitor1.it, competitor2.it, competitor3.it
- Avvisi: nessuno
```

---

## Regole critiche

- **Wizard obbligatorio**: non saltare la Fase 0. Nessuna assunzione implicita sul brief.
- **Solo dati grezzi**: nessun Opportunity Score, nessuna priorità A/M/B, nessuna nota narrativa generata da Claude.
- **KD = Ahrefs**: la Keyword Difficulty riportata è sempre quella di Ahrefs. Stesso principio per volume, CPC, intent.
- **SERP scraping limitato**: mai full-site SERP scraping. Solo singola pagina o massimo 10 keyword dubbiose.
- **Sheet on demand**: includi solo gli sheet richiesti dall'utente. Non aggiungere "perché poteva essere utile".
- **Multi-mercato**: rispetta il country code scelto in tutte le chiamate. Non assumere `it` se l'utente ha indicato un altro mercato.
- **Gap analysis condizionata**: lo sheet "Gap analysis" esiste solo se l'utente ha chiesto la gap analysis E ha fornito (o ha permesso di derivare) competitor.
- **Cluster derivati da dati, non interpretati**: i cluster nascono da `parent_topic` Ahrefs e similarità lessicale, non da giudizi semantici di Claude.
- **Nessun report**: la consegna è il file Excel + un messaggio di chat operativo. Niente report markdown.
- **Non sostituire la skill `keyword-analysis`**: se l'utente chiede esplicitamente "analisi keyword per un articolo blog" (singolo articolo, parte di pipeline blog), suggeriscigli `keyword-analysis`. Questa skill è per ricerche più ampie o strutturate.
