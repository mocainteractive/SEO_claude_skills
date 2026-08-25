---
name: link-building-scouting
description: >
  Ricerca di opportunità di link building per un cliente, guidata da Ahrefs e arricchita con Getfluence. Analizza a fondo il dominio del cliente, mappa i suoi backlink e quelli dei competitor (che chiede sempre all'utente) e individua portali di settore (o generalisti, su richiesta) che accettano guest post e che NON linkano ancora il cliente (link gap). Per ogni prospect dà le metriche Ahrefs rilevanti per la link building e, dove il dominio è a catalogo Getfluence, anche il prezzo. È la fase di prospecting a monte di guest-post-pipeline, a cui fornisce i siti ospitanti candidati. Trigger tipici: "trova opportunità di link building per X", "scouting publisher / guest post per X", "dove prendo backlink per X", "analizza i backlink dei competitor e trovami siti nuovi", "link gap analysis per X". NON scrive l'articolo (c'è guest-post-pipeline) né valuta il tono del portale (host-site-analysis): individua DOVE ottenere link, non COSA scrivere.
---

# Link Building Scouting

Questa skill produce una **mappa di opportunità di link building** per un cliente: parte da un'analisi approfondita del dominio, ricostruisce il profilo backlink del cliente e dei competitor, e individua **portali candidati** dove ottenere un guest post o una menzione — portali di settore (o generalisti, su richiesta) che **accettano contributi esterni** e su cui **il cliente non è ancora linkato**. Per ogni candidato fornisce le metriche Ahrefs che contano per la link building e, dove disponibile, il prezzo di pubblicazione da Getfluence.

Produce indicazioni operative e decisionali — non un report descrittivo. Il destinatario è chi deve decidere dove investire l'attività di link building e poi passare i siti scelti alla scrittura.

**Posizione nel flusso Moca:** questa skill **precede** `guest-post-pipeline` (e le sue fasi `guest-post-brand-analysis` / `host-site-analysis`). Lo scouting individua *dove* ottenere link; la pipeline decide *cosa* scrivere e produce l'articolo.

---

## Come nasce la lista dei candidati (il modello mentale)

Getfluence **non scopre siti per argomento**: via MCP espone solo `search_offers`, che verifica domini che gli passi. Quindi **la scoperta dei candidati è responsabilità della skill, e il motore è Ahrefs** (più la ricerca di footprint e la SERP). Getfluence interviene **dopo**, come arricchimento: per i domini candidati dice se sono a catalogo e a che prezzo. Un dominio non a catalogo **resta comunque nella lista**, semplicemente senza prezzo Getfluence — non è un giudizio di qualità, è solo "non acquistabile lì".

Tre idee guida:
- **Il cliente non deve essere già linkato.** L'opportunità è dove c'è un *gap*: portali che linkano i competitor (o sono a tema) ma non ancora il cliente.
- **Pertinenza prima di tutto.** Un portale verticale e in-topic vale più di un generalista fortissimo ma fuori tema.
- **Le metriche di terze parti si leggono con giudizio.** DR/traffico/TF ecc. sono screening, non verdetti: vanno incrociati con la performance reale (traffico organico, keyword, stabilità). I criteri di dettaglio sono in **`references/qualita-link-building.md`** (6 segnali di qualità, come leggere le metriche, red flag/link tossici, menzioni, budget, mappa criterio→strumento): leggilo prima della qualificazione e dello scoring.

---

## Istruzioni di progetto (verifica SEMPRE all'inizio)

Se lavori dentro un progetto Claude, controlla se ci sono **istruzioni custom** o **knowledge di progetto** (linee guida di link building del cliente, settori vietati, publisher in blocklist/whitelist, tetti di spesa, brand safety). Se presenti hanno **precedenza** sui default di questa skill, restano subordinate alle scelte esplicite dell'utente in sessione, e in caso di conflitto con una buona pratica vanno segnalate, non ignorate. Se non ci sono, procedi con i default.

---

## Strumenti

- **Ahrefs** (MCP `Ahrefs`) — **motore principale**: analisi del cliente, profili backlink (cliente e competitor), metriche dei prospect. Prima di usare un tool Ahrefs per la prima volta chiama `doc` per lo schema esatto. I valori monetari Ahrefs sono in **centesimi di USD** (dividi per 100). Se una risposta indica `render_with`, usa il tool di render indicato.
- **Getfluence** (MCP `getfluence`) — fonte di **scoperta + prezzo/disponibilità**. Tool: `check_getfluence_status`, `search_offers` (verifica per dominio) e **`browse_catalog`** (sfoglia l'intero catalogo, ~10k offerte, filtrando per metriche/prezzo/dominio e ordinando per prezzo → è una vera **fonte di candidati** oltre che di prezzi). ⚠️ Verifica i **nomi esatti dei parametri** con la descrizione/`doc` del tool a runtime (tipicamente: filtri per tld/dominio, metriche minime — DR/TF/traffico —, prezzo massimo, ordinamento, paginazione; rispetta il rate limit ~4 req/s). Se non è collegato, la skill funziona lo stesso, dichiarandolo.
- **Catalogo prezzi fornitori bundled** (`assets/listini/comparativa-fornitori.csv`) — listini di **più fornitori** (Link Juice, Mauxa, Matteo Di Felice, AdHub Media) uniti in un CSV incluso come knowledge locale: si legge **da file, senza rete e senza pubblicare nulla**. Serve per il **prezzo**, per **confrontare i fornitori** (stesso dominio, prezzi diversi → si indica il più conveniente) e come fonte di **candidati** (filtrabile per categoria/paese). ⚠️ Salta le prime 2 righe; metriche/paese/categoria stanno dentro `NOTE`. In questo file il separatore decimale è `.` (`1305.50 €` = 1.305,50 €).
- **Script bundled** (`scripts/price_lookup.py`) — usa **questo** per leggere il catalogo, invece di re-implementare il parsing ogni volta: fa lookup per dominio (prezzo minimo + fornitore + alternative + metriche) e discover per categoria/paese/prezzo/metriche. Deterministico, gestisce celle multi-riga e formati prezzo. Es.: `python scripts/price_lookup.py lookup --domains a.it,b.it` · `python scripts/price_lookup.py discover --category finanza --country IT --max-price 400`. Richiede un ambiente con Python (Claude Code/Cowork); se sei in un ambiente senza esecuzione Python, applica manualmente la logica del `_manifest.md` filtrando **solo** i domini che ti servono, senza caricare l'intero CSV.
- **Ricerca web** (WebSearch) — per la **ricerca di footprint** dei siti che accettano guest post (vedi Fase 4), nella **lingua del mercato** target. Se non disponibile, salta quel canale e dichiaralo.
- **Semrush** (opzionale, se collegato) — conferma incrociata su backlink/traffico/competitor. Se non c'è, usa Ahrefs.

### Sanity check iniziale
All'avvio chiama `check_getfluence_status` (se il MCP c'è). Se risponde, potrai arricchire con i prezzi; se non risponde, prosegui comunque avvisando che mancheranno i prezzi Getfluence. Non bloccare il lavoro per l'assenza di Getfluence: è arricchimento, non prerequisito.

---

## Domande iniziali obbligatorie

Fai queste domande **sempre e rigorosamente** prima di partire. Se l'utente ne salta qualcuna, insisti (proponi i default tra parentesi ma chiedi conferma).

1. **Dominio del cliente** + **pagina/e target** da rafforzare (URL) e **topic/settore** di interesse.
2. **Competitor di riferimento** (URL): **sempre richiesti esplicitamente** all'utente — sono la fonte principale del bacino di prospect. Se l'utente non li ha, proponi di individuarli tu con Ahrefs (`site-explorer-organic-competitors`) e falli confermare prima di procedere.
3. **Ambito dei portali**: solo **verticali/di settore** o anche **generalisti**? (default: prioritizza i verticali, includi i generalisti solo se autorevoli e in-topic).
4. **Mercato/i e lingua** — la skill lavora su **qualsiasi mercato**, non solo l'Italia. Il **default è Italia / italiano (`it`)**, ma l'utente può indicare uno o più mercati (es. Spagna `es`, Francia `fr`, Germania `de`, UK `gb`, USA `us`, …) o un mix. Il mercato scelto si propaga a tutto il flusso: `country` nelle chiamate Ahrefs, filtro tld/paese su Getfluence e sul catalogo (campo `Paese`), e **lingua delle query di footprint** (es. `"escribe para nosotros" <settore>` per ES, `"écrire pour nous"` per FR, `"write for us"` per EN). Se richiede più mercati, gestiscili separatamente e indica il mercato di ogni prospect. Nota: il catalogo bundled è prevalentemente IT (con alcuni ES/FR/DE/UK/US); per mercati poco coperti, appoggiati di più ad Ahrefs, Getfluence `browse_catalog` e footprint nella lingua locale.
5. **Preferenze di scoring** — *domanda obbligatoria*: l'utente ha preferenze su **come ordinare/pesare i prospect** (es. dare più peso a traffico organico, DR, pertinenza tematica, prezzo Getfluence, o un ordinamento specifico), oppure **nessuna preferenza** e uso il default? Il default è: pertinenza tematica come fattore dominante, poi autorità reale (traffico + DR), poi efficienza di prezzo dove c'è Getfluence. Registra la risposta e applicala nella Fase 6.
6. **Eventuali soglie/budget** (opzionali): soglie minime di metriche (es. DR ≥ 30, traffico ≥ 5.000) e/o tetto € per link. Se fornite, filtrano/pesano; se non fornite, elenca tutto ordinato per valore.
7. **Blocklist/whitelist** eventuali (domini da escludere o da includere comunque).

Riepiloga i parametri raccolti prima di procedere.

---

## Flusso operativo

### Fase 1 — Analisi approfondita del dominio del cliente (Ahrefs)

Inquadra il cliente e il suo contesto SEO, così da giudicare la pertinenza dei prospect più avanti.
- **Autorità e traffico**: `site-explorer-domain-rating` (DR) e `site-explorer-metrics` (`target` = dominio, `mode` `subdomains`, `date` odierna, `country` del mercato) → DR, `org_traffic`, `org_keywords`, `org_keywords_1_3`.
- **Temi presidiati**: `site-explorer-organic-keywords` (`order_by` per traffico/volume, `limit` ~25) e `site-explorer-top-pages` → di cosa "parla" davvero il sito e quali pagine attraggono traffico/link.
- **Sintesi profilo backlink**: `site-explorer-backlinks-stats` per la fotografia (referring domains, backlink totali, dofollow ecc.).
Restituisci una sintesi breve: settore reale, temi forti, livello di autorità, pagine chiave. Serve da metro per la pertinenza.

### Fase 2 — Backlink esistenti del cliente (Ahrefs)

Ricostruisci **chi già linka il cliente**: `site-explorer-referring-domains` (`target` = dominio cliente, `mode` `subdomains`, `select`: `domain,domain_rating,traffic_domain,dofollow_links,is_spam`, `order_by` `domain_rating:desc`, `limit` alto per coprire il profilo).
Questo insieme è l'**inventario dei referring domain del cliente** e, soprattutto, la **lista di esclusione** per il prospecting: i domini che già linkano il cliente **non sono opportunità nuove**.

### Fase 3 — Backlink dei competitor (Ahrefs)

Per **ciascun competitor** confermato in intake, estrai i referring domains con `site-explorer-referring-domains` (stessi `select` della Fase 2, `order_by` `domain_rating:desc`, filtra già `is_spam=false` e `domain_rating ≥` soglia se fornita). Chi linka i competitor è un publisher che **accetta contenuti/link nel settore**: è il bacino primario di prospect.
Tattica ad alto rendimento (Ahrefs/Semrush): individua le **pagine dei competitor più linkate** con `site-explorer-pages-by-backlinks`, poi sulle 2–3 top usa `site-explorer-referring-domains` per catturare **chi linka contenuti simili ai nostri**.

### Fase 4 — Prospecting: costruzione della lista candidati

Unisci le fonti, poi **sottrai i già-linkati**:
- **a) Link gap competitor** — referring domains dei competitor (Fase 3) **meno** i referring domains del cliente (Fase 2). È il cuore: portali che linkano i competitor ma non ancora il cliente.
- **b) Chi ranka sul topic** — `serp-overview` sulla keyword primaria del topic (e 1–2 correlate), `country` coerente: raccogli i domini editoriali in prima pagina non già linkati al cliente.
- **c) Ricerca di footprint (WebSearch)** — allarga il bacino ai siti che dichiarano di accettare contributi. Query tipo: `"scrivi per noi" <settore>`, `"guest post" <settore>`, `"collabora con noi" <settore>`, `"linee guida guest post" <settore>`, adattate alla lingua/mercato. Raccogli i domini pertinenti, escludi i già-linkati. Distingui gli **host editoriali** dai **marketplace/servizi di link building** (etichettali come tali) e scarta gli articoli-spiegazione (pezzi "cos'è un guest post" che non sono offerte).
- **d) Catalogo fornitori (per categoria/paese)** — usa `scripts/price_lookup.py discover --category <settore> --country <mercato> [--max-price … --min-da …]` per estrarre dal catalogo i portali del tema e del mercato giusto (Categoria/Topic/Paese stanno in `NOTE`). Sono per definizione siti che accettano guest post, e arrivano **già con prezzo e fornitore**. Escludi i già-linkati. (Se l'utente vuole il catalogo **solo per il prezzo**, salta questo punto e usalo solo in Fase 5.)
- **e) Getfluence `browse_catalog`** — sfoglia il catalogo Getfluence filtrando per **mercato** (tld/paese), metriche minime e prezzo massimo, ordinando per prezzo: ottieni altri portali che vendono pubblicazioni, **già con prezzo**. Verifica i nomi esatti dei filtri col `doc` del tool; paginando rispetta il rate limit. Escludi i già-linkati. La pertinenza tematica di questi candidati va comunque verificata con Ahrefs (Fase 6).

**Segnale "accetta guest post"** per ogni candidato, da annotare:
- **presente nel catalogo fornitori** (d) o **su Getfluence** (e/Fase 5) → forte (vende pubblicazioni);
- **footprint esplicito** (c) → forte;
- **è referring domain editoriale di un competitor** (a) → medio (accetta link esterni).

**Consolidamento**: normalizza (togli `http(s)://`, `www.`, path → dominio registrabile), **deduplica**, escludi cliente/competitor, social/aggregatori/marketplace non pertinenti, blocklist di progetto e — filtro chiave — **tutti i domini che già linkano il cliente**. Applica l'ambito richiesto (solo verticali o anche generalisti). Ottieni la **lista prospect**.

### Fase 5 — Arricchimento prezzi (Getfluence + listini bundled)

Per ogni prospect raccogli il prezzo da **tutte le fonti disponibili** e fai il merge.

**a) Getfluence** — passa **tutta la lista prospect** a `search_offers` in **batch** (più domini in un'unica chiamata). Non fare loop di chiamate singole. (I candidati arrivati da `browse_catalog` in Fase 4e hanno già il prezzo Getfluence: non ri-verificarli.)
- `domains`: array dei prospect. `search_type`: `"wide"` (consigliato). `page`: da `1`, pagina se paginato (Hydra).
- Per i domini **a catalogo**: `url`, `formatType`, **`price`** (già in €, "a partire da"), metriche (`organicTraffic`, `trustFlow`, `citationFlow`, `domainAuthority`, `authorityScore`, `domainRating`), `id`, `createdAt`; in coda eventuali **crediti API rimanenti** (annotali, avvisa se bassi).
- **Rate limit / 429**: ~4 req/s + quote; su `429` backoff (2s/4s/8s), non ritentare a raffica. Il batch è la difesa principale.

**b) Catalogo fornitori bundled** — fai il lookup con `scripts/price_lookup.py lookup --domains <lista>` (o `--stdin`): per ogni dominio restituisce **prezzo minimo, fornitore, tutte le offerte** dei vari fornitori e le metriche/note (DA/TF/CF/DR/AS/ZA, Paese, nofollow). Gestisce già celle multi-riga, salto delle 2 righe di testa, formati prezzo e `Da concordare`→"su richiesta". Non caricare l'intero CSV nel contesto.

**c) Confronto e scelta del più conveniente** — per ogni dominio metti a confronto **tutti** i prezzi disponibili: i vari **fornitori** del catalogo **+ Getfluence**. Determina il **prezzo minimo** e — requisito chiave — indica **da quale fornitore/fonte** comprarlo (es. "349 € via Mauxa"). Riporta le **alternative** (gli altri fornitori con relativo prezzo) in nota, così l'utente vede il risparmio. Considera "su richiesta"/"n.d." come non confrontabili numericamente (elencali ma non possono vincere sul prezzo). Un dominio senza alcun prezzo resta in lista con **"n.d."** (né Getfluence né catalogo ≠ scadente): opportunità da contattare direttamente.

### Fase 6 — Metriche, qualificazione e scoring

Per ogni prospect componi la **scheda** con le metriche Ahrefs rilevanti per la LB (usa `doc` per gli schemi esatti; recupera le metriche costose solo sulla rosa che serve). Set di default (confermato):
- **Domain Rating** (`site-explorer-domain-rating`);
- **Traffico organico** e keyword (`site-explorer-metrics`: `org_traffic`, `org_keywords`);
- **Referring domains** del prospect (`site-explorer-backlinks-stats` o il campo relativo);
- **Pertinenza tematica** (top keyword/temi via `site-explorer-organic-keywords`) → **Alta / Media / Bassa** con motivazione di una riga;
- **`is_spam` / red flag** e, sul link verso il competitor, se è **dofollow** (dai dati di Fase 3);
- **Prezzo + fonte** dal merge di Fase 5 (Getfluence e/o listini); riporta anche le metriche del listino (DA/TF/ZA) e il flag **nofollow** se presente nelle note.

Applica i controlli di **salute/trust** e la **checklist red flag** del reference (§2–§3): DR alto + traffico ~0, `citationFlow` ≫ `trustFlow`, crolli di traffico, pattern "sito contenitore"/link farm. Non scartano da soli, ma abbassano la priorità o escludono se gravi.

**Scoring** — applica la preferenza raccolta in intake (domanda 5):
- se l'utente ha indicato pesi/priorità, **usa quelli** e dichiaralo;
- altrimenti default: **pertinenza (peso maggiore)** → **autorità reale** (traffico organico + DR) → **efficienza di prezzo** dove c'è Getfluence (**€ per 1.000 di traffico organico** `price/(organicTraffic/1000)` e/o **€ per punto DR** `price/domainRating`) → **trust/salute**.
Se sono state date soglie/budget, filtra di conseguenza. **Spiega sempre come hai ordinato.**

### Fase 7 — Output

Presenta i risultati come da formato qui sotto.

---

## Formato di output

### 1. Parametri dello scouting
Riga di sintesi: cliente, topic/settore, competitor usati, mercato/lingua, ambito (verticali/generalisti), preferenza di scoring applicata, eventuali soglie/budget.

### 2. Analisi del cliente
Sintesi della Fase 1: DR, traffico organico, temi/keyword forti, pagine chiave, fotografia del profilo backlink (n° referring domains, ecc.).

### 3. Profilo backlink dei competitor
Per competitor: n° referring domains, esempi di publisher rilevanti che li linkano, e i temi/pagine che attraggono più link. Evidenzia il **potenziale link gap** (quanti domini linkano i competitor ma non il cliente).

### 4. Opportunità di link building (tabella prospect)
Ordinata secondo lo scoring scelto (migliore in alto). Solo domini su cui il cliente **non è ancora linkato**.

| # | Dominio | Mercato | Pertinenza | DR | Traffico org. | Ref. domains | Guest post | Miglior prezzo € | Dove comprarlo | Cliente linkato | Note |
|---|---------|---------|-----------|----|--------------|--------------|-----------|------------------|----------------|-----------------|------|

- **Mercato**: paese/lingua del portale (utile con più mercati; ometti la colonna se il mercato è unico).
- **Pertinenza**: Alta/Media/Bassa + motivo (in Note se stretto). Fattore dominante di default.
- **Guest post**: segnale di accettazione (catalogo fornitori / Getfluence / footprint / linka competitor).
- **Miglior prezzo €**: il prezzo **minimo** tra tutte le fonti ("a partire da"); "su richiesta" se solo "Da concordare"; "n.d." se nessuna fonte ce l'ha (≠ scadente).
- **Dove comprarlo**: la **fonte/fornitore** del prezzo minimo (es. "Mauxa", "AdHub Media", "Getfluence"). È l'indicazione operativa: da chi comprare.
- **Cliente linkato**: sempre "No" per costruzione — garanzia che è un'opportunità nuova.
- **Note**: **prezzi alternativi degli altri fornitori** (per mostrare il risparmio), TF/CF/ZA e red flag di salute, nofollow/requisiti/Paese dal catalogo, tipologia offerta.

### 5. Riepilogo e prossimi passi
- Numeri: quanti prospect totali, quanti con prezzo disponibile (per fonte: Getfluence / listini, con range prezzi), quanti verticali vs generalisti.
- Se erano dati budget/soglie: come si colloca la lista, e una **shortlist consigliata** entro budget.
- **Handoff a `guest-post-pipeline`** per i siti scelti (sono i "siti ospitanti candidati" da passare alla scrittura).

---

## Principi di qualità (tienili sempre)

- **Solo opportunità nuove.** Escludi sempre i domini che già linkano il cliente: l'output è il *gap*, non l'esistente.
- **Prezzo = confronto multi-fonte, non filtro.** Metti sempre a confronto i **fornitori del catalogo** e **Getfluence**: indica il **prezzo minimo** e **da chi comprarlo**, con le alternative in nota. Un dominio senza prezzo resta in lista (≠ scadente).
- **Dati del catalogo = riservati.** Il catalogo contiene prezzi forniti da terzi: resta **locale alla skill**, non va pubblicato, incollato in servizi esterni o esposto oltre il necessario. Viaggia dentro il file `.skill`: condividilo solo internamente.
- **La pertinenza batte l'autorità nuda.** Un link in-topic su un sito medio vale più di uno fuori tema su un sito fortissimo.
- **Metriche di terze parti con giudizio.** DR/DA/AS/TF/CF sono screening, non verdetti: incrociali con la performance reale (traffico, keyword, stabilità). DR alto + traffico ~0 = red flag. Non sommare metriche di provider diversi.
- **Le menzioni e i nofollow hanno valore** (brand association, referral, AI Overview): non scartarli a priori.
- **Rispetta i rate limit.** Batch su `search_offers`, backoff sui `429`; su Ahrefs recupera le metriche costose solo sulla rosa che serve.
- **Trasparenza.** Mostra fonti dei prospect, criterio di scoring applicato e quanti domini cadono a ogni filtro.
- **Lingua di lavoro: italiano.**

---

## Esempio end-to-end (caso fittizio)

**Input:** «Cliente `mocainteractive.com`, pagina target la home, topic: digital advertising / marketing. Competitor? → l'utente fornisce `competitor-adv-1.it`, `competitor-adv-2.it`. Ambito: verticali marketing/ADV, generalisti solo se autorevoli. Mercato: Italia. Preferenza scoring? → "dai più peso al traffico organico e alla pertinenza". Budget: indicativo 300–500 €/link.»

**Come procede la skill:**
1. **Cliente (Ahrefs)** — DR, traffico, temi ("digital advertising", "seo", "email marketing"), top pages, profilo backlink.
2. **Backlink cliente** — referring domains del cliente = lista di esclusione.
3. **Competitor** — referring domains dei due competitor + pagine più linkate → bacino di publisher del settore.
4. **Prospecting** — link gap (competitor meno cliente) + domini che rankano su "agenzia digital advertising" ecc. + footprint (`"scrivi per noi" marketing`, `"guest post" pubblicità`) → ~30 prospect non ancora linkati, filtrati sui verticali marketing/ADV.
5. **Prezzi (confronto fonti)** — `search_offers` batch sui ~30 su Getfluence **e** lookup sul catalogo fornitori. Es. `notizie.it` risulta a 490 € (Getfluence), 470 € (Link Juice), 349 € (Mauxa) → **miglior prezzo 349 € via Mauxa**, alternative in nota. I domini senza alcun prezzo restano in lista come "n.d.".
6. **Metriche + scoring** — schede Ahrefs per prospect; ordinamento con peso extra su traffico e pertinenza (come richiesto); annotate red flag e €/1k traffico dove c'è prezzo.
7. **Output** — analisi cliente, profilo competitor con entità del gap, tabella dei ~30 prospect ordinata con **miglior prezzo e fornitore da usare** (alternative in nota), riepilogo (quanti con prezzo, per fonte/fornitore, range) e shortlist consigliata entro 300–500 €, con handoff a `guest-post-pipeline`.

Livello atteso: l'utente deve capire **dove** sono le opportunità nuove, **quanto valgono** per la LB e **da quale fornitore conviene comprarle**.
