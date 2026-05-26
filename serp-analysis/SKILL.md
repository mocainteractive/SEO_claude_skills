---
name: serp-analysis
description: >
  Analizza la SERP per la keyword primaria identificata dalla skill keyword-analysis e produce indicazioni operative per il content-brief-builder. Prima dell'analisi competitor esegue un controllo di cannibalizzazione: verifica se il sito del cliente è già posizionato sulla keyword primaria o sulle correlate principali, usando come fonte primaria i dati di prima parte di Google Search Console (MCP gsc-moca, proprietà legata all'URL/dominio fornito a inizio chat) e Ahrefs come complemento/fallback; in caso affermativo ferma il flusso per decidere se continuare, cambiare focus o aggiornare la pagina esistente. Verifica inoltre, tramite DataForSEO MCP, la presenza dell'AI Overview sulla keyword primaria e sulle due secondarie più pertinenti, producendo osservazioni per la scrittura. Usa questa skill dopo keyword-analysis e prima di brand-analysis-and-connections. Trigger tipici: "analizza la SERP per questa keyword", "cosa fanno i competitor su questo topic", "come sono strutturati i contenuti in prima pagina", "abbiamo già un contenuto su questa keyword?", "c'è l'AI Overview su questa keyword?", "procedi con il flusso seo-blog-pipeline". Questa skill è il secondo step del flusso seo-blog-pipeline.
---

# SERP Analysis

Questa skill analizza la SERP per la keyword primaria e i contenuti dei competitor organici in prima pagina. Produce indicazioni operative — non un report descrittivo — che alimentano direttamente il content-brief-builder e che possono essere lette anche dal cliente o dal responsabile editoriale.

L'obiettivo è capire il formato vincente, identificare i gap di contenuto e definire come differenziarsi dai competitor con un articolo più completo o con un angolo editoriale diverso.

---

## Input atteso

- L'output della skill `keyword-analysis`: in particolare la keyword primaria, le keyword secondarie/correlate con i rispettivi volumi, l'intent e le SERP features già rilevate da Ahrefs.
- L'URL (dominio) del sito del cliente, necessario per il controllo di cannibalizzazione dello Step 0. È un input globale del flusso seo-blog-pipeline. Se non è disponibile dal contesto, chiedilo all'utente prima di procedere.

---

## Integrazione tool

Usa i seguenti tool in sequenza.

### Chiamata 0 — Controllo cannibalizzazione (GSC primario + Ahrefs fallback)

Prima di tutto, verifica se il sito del cliente ha già contenuti posizionati sulla keyword primaria o sulle correlate più importanti. Serve a evitare di creare un nuovo articolo che competa con una pagina esistente (cannibalizzazione). La fonte primaria è Google Search Console (dati di prima parte: pagine, query, posizioni reali del sito); Ahrefs è il complemento e il fallback quando la proprietà GSC non è accessibile.

#### Chiamata 0.1 — GSC (fonte primaria, MCP gsc-moca)

Usa i tool del MCP Google Search Console (`gsc-moca`) sulla proprietà legata all'URL/dominio fornito dall'utente a inizio chat.

**a) Risolvi la proprietà GSC.** Chiama `get_properties` e individua la proprietà che corrisponde al dominio fornito. Gestisci le varianti: una `sc-domain:esempio.com` copre tutto il dominio ed è preferibile; altrimenti scegli tra `https://www.`, `https://`, `http://` con la priorità `sc-domain:` > `https://www.` > `https://` > `http://`. Se l'utente ha dato un nome cliente invece di un URL, usa `resolve_client` (con `autoSelectMain: true`) per ottenere la proprietà principale.

Se nessuna proprietà corrisponde o non è accessibile (l'account autenticato non ha i permessi), **salta la parte GSC** e usa solo la Chiamata 0.2 (Ahrefs). Segnalalo nell'output.

**b) Estrai le combinazioni query × pagina.** Usa `get_query_page_combinations` sulla proprietà risolta:
- `siteUrl`: la proprietà risolta (es. `sc-domain:esempio.com`)
- `startDate` / `endDate`: ultimi **3 mesi** (finestra robusta per posizionamenti stabili; oggi − 90 giorni → oggi, in formato YYYY-MM-DD)
- `query`: il termine radice della keyword primaria (il tool filtra lato API con operatore `contains`). Esegui la chiamata una volta per la keyword primaria e, se utile, ripetila per le 2-3 correlate ad alto volume.
- `minImpressions`: `10` (taglia il rumore di code lunghissime con pochissime impression)
- `includeFreshData`: `true`

In parallelo, esegui una chiamata con `analyzeCannibalization: true` (stessa proprietà e periodo, senza filtro `query` o con il filtro sul termine radice): restituisce direttamente le query per cui **2 o più pagine** del sito competono, raggruppate per query. È il segnale più forte di cannibalizzazione già in atto.

**Lettura corretta dei dati GSC (importante):**
- Per i totali reali del sito usa `get_property_stats`: i numeri di GSC **non** sono la somma delle righe per query. Non sommare mai le righe di `get_search_queries`, `get_top_pages` o `get_query_page_combinations` per ricavare un totale: le query anonimizzate da Google fanno sì che la somma sia sempre inferiore al reale.
- `includeFreshData: true` (`dataState: "all"`) include gli ultimi giorni ancora in elaborazione: il response segnala `first_incomplete_date`. Per il controllo di cannibalizzazione va bene, ma tienine conto: gli ultimi ~2-3 giorni possono cambiare.
- La `position` di GSC è una **media** sul periodo, non la posizione attuale: una media bassa (vicina a 1) indica presidio stabile.
- I dati GSC riguardano solo le query per cui il sito ha già ottenuto impression: se una keyword non compare, il sito non riceve impression per quel termine nel periodo (segnale di assenza di cannibalizzazione su quel fronte).

#### Chiamata 0.2 — Ahrefs (complemento e fallback)

Usa `site-explorer-organic-keywords` sul dominio del cliente. È sempre utile come complemento (Ahrefs vede anche keyword senza dati GSC) ed è il fallback quando la proprietà GSC non è accessibile.

Parametri:
- `target`: il dominio del sito del cliente (es. "esempio.it")
- `mode`: "subdomains"
- `country`: "it" (default, salvo diversa indicazione)
- `date`: la data odierna (formato YYYY-MM-DD)
- `select`: "keyword,best_position,best_position_url,best_position_kind,volume,sum_traffic"
- `order_by`: "best_position:asc"
- `limit`: 50
- `where`: filtro che isola le keyword della famiglia tematica. Costruiscilo come `or` di condizioni `isubstring` sui termini centrali della keyword primaria e delle 3-5 correlate più importanti (quelle a volume più alto dall'output di keyword-analysis). Esempio per keyword primaria "meditazione": `{"or":[{"field":"keyword","is":["isubstring","meditazione"]},{"field":"keyword","is":["isubstring","meditare"]}]}`

Usa `isubstring` sui termini radice (non `eq` sulla frase esatta) per catturare anche le varianti con cui il sito potrebbe già rankare.

Se il dominio non ha dati in Ahrefs o la chiamata non restituisce keyword, considera questa parte come priva di segnali (non blocca da sola il controllo).

### Chiamata 1 — SERP overview (Ahrefs MCP)

Usa `serp-overview` per ottenere i dati strutturali sui risultati organici in prima pagina.

Parametri:
- `keyword`: la keyword primaria
- `country`: "it" (default, salvo diversa indicazione)
- `select`: "url,title,position,traffic,domain_rating,refdomains,page_type,backlinks"

Dalla lista risultante, identifica i risultati editoriali organici (escludi homepage aziendali, e-commerce puri, pagine prodotto, directory). Tieni nota delle posizioni e dei domini per abbinarli ai dati del passaggio successivo.

Controlla anche se il dominio del cliente compare tra gli URL posizionati: è un secondo segnale (oltre alla Chiamata 0) che il sito presidia già la keyword primaria. Tienine conto nello Step 0.

### Chiamata 2 — Ricerca Google (WebSearch)

Esegui una ricerca web con la keyword primaria usando il tool `WebSearch`. Questo passaggio serve a due scopi:
1. Recuperare gli URL degli articoli in formato leggibile da `WebFetch`
2. Estrarre le domande PAA ("le persone chiedono anche") visibili direttamente nella SERP Google

Query da usare: la keyword primaria così com'è, in italiano.

Abbina gli URL ottenuti dalla ricerca con i dati Ahrefs (posizione, DR, traffico). Seleziona i 5-7 risultati editoriali da leggere.

### Chiamata 3 — Lettura contenuto competitor (WebFetch)

Per ciascuno degli URL editoriali selezionati, usa `WebFetch` per leggere il contenuto della pagina.

Per ogni pagina estrai:
- Struttura degli heading (H1, H2, H3 presenti nel testo)
- Tipo e presenza di contenuti visivi (immagini, video, tabelle, infografiche, callout, box)
- Link interni presenti nel testo: destinazione (articolo informativo, pagina prodotto/servizio, landing page, risorsa esterna) e anchor text rappresentativo
- Lunghezza stimata del contenuto
- Angolazione editoriale: a chi si rivolge, tono, punto di vista (generico, tecnico, fai-da-te, professionale, commerciale)

Leggi le pagine in sequenza. Se una pagina restituisce errore o contenuto non leggibile, saltala e passa alla successiva. Se più della metà delle pagine non è leggibile, segnalalo nell'output e procedi con i dati Ahrefs disponibili.

### Chiamata 4 — Presenza AI Overview (DataForSEO MCP)

Verifica se Google mostra un **AI Overview** sulle keyword più importanti del tema. L'AI Overview cambia il modo in cui l'articolo va scritto (vedi Step 5), quindi è un controllo da fare sempre.

**Keyword da controllare:** la **keyword primaria** + le **2 keyword secondarie più pertinenti e legate al tema** (scelte dall'output di keyword-analysis per vicinanza tematica al topic dell'articolo, non solo per volume). Totale: 3 chiamate.

Usa il tool `serp_organic_live_advanced` del MCP DataForSEO, una chiamata per keyword.

Parametri per chiamata:
- `keyword`: la keyword da analizzare
- `location_name`: il paese target del flusso (default `"Italy"`; in alternativa `location_code` 2380)
- `language_name`: la lingua target (default `"Italian"`; in alternativa `language_code` `"it"`)
- `device`: `"desktop"` (l'AI Overview può variare per device; usa desktop come riferimento salvo diversa indicazione)
- `load_async_ai_overview`: `true` — **importante**: Google carica spesso l'AI Overview in modo asincrono; senza questo flag l'elemento risulta presente ma vuoto. Con `true` il tool esegue la richiesta aggiuntiva per recuperarne contenuto e fonti (comporta un piccolo costo extra per chiamata).

Nella risposta, cerca nell'array `items` un elemento con `type` = `ai_overview`:
- la presenza dell'elemento = **AI Overview presente** per quella keyword; la sua assenza = non presente.
- `references` (array di `ai_overview_reference`): le **fonti citate** dall'AI Overview, ciascuna con `domain`, `title`, `url`. Sono le pagine che Google usa per comporre la risposta.
- i blocchi di testo dell'elemento sintetizzano **cosa risponde** Google e quali sotto-aspetti tocca.

Se DataForSEO non è disponibile o la chiamata fallisce, segnalalo nell'output e prosegui senza bloccare il flusso: il controllo AI Overview è informativo, non è un checkpoint di stop.

---

## Processo di analisi

### Step 0 — Controllo cannibalizzazione (prima di ogni altra cosa)

Combina i segnali raccolti nella Chiamata 0, dando **precedenza ai dati GSC** (prima parte, più affidabili) e usando Ahrefs come conferma/complemento. Considera anche il segnale incrociato della Chiamata 1 (il dominio del cliente compare già nella SERP della keyword primaria?).

**Segnali GSC (Chiamata 0.1) — prioritari:**
- **Più pagine sulla stessa query** (output di `analyzeCannibalization: true`, oppure 2+ righe con la stessa query e URL diversi in `get_query_page_combinations`): è cannibalizzazione **già in atto**. Segnale forte a prescindere dalla posizione media.
- **Una pagina con impression/clic sulla keyword primaria o su una correlata ad alto volume**: il sito presidia già il tema. Valuta la gravità con la `position` media GSC:
  - posizione media ≤ 10 → presidio forte
  - posizione media 11-50 → presidio potenziale
  - posizione media > 50 ma con clic reali → comunque rilevante
- Se la proprietà GSC non era accessibile, basati sui segnali Ahrefs.

**Segnali Ahrefs (Chiamata 0.2) — conferma/fallback:**
- Posizionamento rilevante = `best_position_kind` `organic` con `best_position_url` valorizzato.
  - **Top 10**: cannibalizzazione forte. **11-50**: potenziale. **Oltre 50 o assente**: nessun rischio concreto da questa fonte.

**Decisione.** Se almeno una fonte indica una pagina del sito che presidia la keyword primaria o una correlata ad alto volume (pagina in top 50 su Ahrefs, oppure impression/clic in GSC, oppure più pagine in competizione su GSC):

1. **FERMA il flusso**: non procedere con la verifica SERP e l'analisi competitor.
2. Mostra all'utente, in modo conciso:
   - La/le keyword già presidiate dal sito
   - L'URL (o gli URL, se più pagine competono) della pagina esistente, con la posizione media e — se da GSC — impression e clic nel periodo; se da Ahrefs, posizione e traffico stimato (`sum_traffic`)
   - La fonte del segnale (GSC e/o Ahrefs)
3. Chiedi esplicitamente come procedere, proponendo le opzioni:
   - **Continuare comunque** con un nuovo articolo (accettando il rischio, es. se l'angolo è diverso o si vuole sostituire la vecchia pagina)
   - **Cambiare focus** su una keyword/angolazione diversa (tornando a `keyword-analysis`)
   - **Aggiornare/consolidare la pagina esistente** invece di crearne una nuova (particolarmente indicato quando GSC mostra più pagine già in competizione)

Non procedere allo Step 1 finché l'utente non ha scelto.

Se nessuna fonte rileva cannibalizzazione, prosegui normalmente e segnala l'esito nel blocco dedicato dell'output (una riga, indicando che il controllo GSC + Ahrefs è stato superato).

### Step 1 — Verifica della SERP

Prima di analizzare i competitor, verifica che la SERP sia compatibile con un articolo blog informativo.

Controlla cosa domina la prima pagina dai risultati Ahrefs:
- Se la maggioranza dei risultati sono articoli o guide informative: procedi normalmente.
- Se la maggioranza sono pagine prodotto, e-commerce o landing page commerciali: la keyword ha un intent prevalentemente transazionale, anche se Ahrefs l'aveva classificata come informazionale. Segnala il problema, suggerisci di tornare alla skill `keyword-analysis` per valutare una keyword alternativa, e non procedere finché non c'è conferma.
- Se la SERP è mista (articoli + pagine commerciali): segnalalo nelle note operative dell'output, ma procedi con l'analisi dei risultati editoriali presenti.

Nota anche le SERP features già rilevate da `keyword-analysis`:
- **Snippet in evidenza / featured snippet**: Google premia risposte dirette e strutturate. L'articolo dovrà avere almeno una sezione con risposta sintetica e chiara.
- **"Le persone chiedono anche" (PAA)**: raccogli le domande mostrate. Sono ottime per H2/H3 e sezione FAQ.
- **Video**: se presenti, il formato video è premiato su questo topic. Non blocca la scrittura, ma va segnalato.
- **Local pack**: segnala frammentazione locale del mercato. Irrilevante per un articolo nazionale.
- **AI Overview**: Google sta già sintetizzando risposte automatiche. L'articolo dovrà puntare su profondità e differenziazione per emergere.

### Step 2 — Analisi dei competitor

Usa i dati letti con WebFetch per ciascun competitor. Per ogni risultato editoriale analizza:

**Formato e struttura del contenuto**
- Che tipo di articolo è? (guida completa, confronto, raccolta dati/statistiche, tutorial step-by-step, FAQ, listicle, analisi/opinione esperta)
- Come è strutturato? (numero e gerarchia di H2/H3, presenza di tabelle, elenchi, callout, box informativi)
- Lunghezza stimata in parole

**Contenuto visivo e multimediale**
- Usa immagini? Di che tipo? (foto, grafici, infografiche, screenshot, illustrazioni)
- Usa video incorporati?
- Ha elementi interattivi? (calcolatori, widget, quiz, tool)

**Link interni nel testo**
- A che tipo di contenuti linka? (altri articoli informativi, pagine prodotto/servizio, landing page, risorse esterne)
- La strategia prevalente è approfondire o convertire?

**Angolazione editoriale**
- A chi si rivolge? (consumatore finale, professionista, azienda B2B)
- Punto di vista: generico/divulgativo, tecnico/specialistico, orientato al fai-da-te, orientato all'acquisto

### Step 3 — Identificazione dei gap

Dopo aver analizzato tutti i competitor, rispondi a queste domande:

- **Gap di contenuto**: quali aspetti del topic non sono coperti, sono trattati superficialmente, o sono coperti in modo generico quando potrebbero essere approfonditi?
- **Gap di formato**: tutti usano testo lungo e generico? Un articolo con tabelle, dati, o struttura più scannable si differenzierebbe.
- **Gap di angolazione**: tutti si rivolgono al consumatore finale? Se l'obiettivo è B2B o professionale, l'angolazione specialistica è già un differenziatore concreto.
- **Gap di risposta**: le domande PAA presenti in SERP trovano risposta chiara negli articoli competitor? Se no, rispondere meglio è un vantaggio diretto.

I gap devono essere concreti e sfruttabili. Non scrivere osservazioni generiche: specifica cosa manca e come può essere coperto.

### Step 4 — Formato vincente consigliato

Sulla base dell'analisi, indica il formato più adatto per l'articolo da scrivere tra:
- Guida completa
- Tutorial step-by-step
- Confronto / comparazione
- Raccolta dati e statistiche
- FAQ strutturata
- Listicle
- Analisi / opinione esperta
- Formato ibrido (specificare la combinazione)

Motiva la scelta in una riga, basandoti su cosa manca nella SERP o su cosa funziona meglio per l'intent e il pubblico target.

### Step 5 — AI Overview: presenza e osservazioni per la scrittura

Analizza i risultati della Chiamata 4 per la keyword primaria e le due secondarie più pertinenti. Per ciascuna registra se l'AI Overview è presente o assente.

Se l'AI Overview **non** è presente su nessuna delle tre keyword, segnalalo in una riga e non aggiungere osservazioni.

Se è presente su una o più keyword, ricava osservazioni concrete da tenere a mente in fase di scrittura. In particolare:

- **L'articolo deve offrire più valore dell'AI Overview.** Quando Google risponde già in SERP, il clic organico cala: il contenuto deve dare profondità, dati, esempi o un punto di vista che la sintesi AI non offre, altrimenti non ha motivo di essere cliccato.
- **Punta a farti citare come fonte.** Struttura il testo perché sia facilmente estraibile dall'AI Overview: risposta diretta e sintetica in apertura di sezione (BLUF), definizioni chiare, elenchi e tabelle, dati verificabili, heading formulati come la domanda dell'utente.
- **Copri i sotto-aspetti sintetizzati dall'AIO.** Dai blocchi di testo dell'AI Overview emerge quali sfaccettature Google considera centrali: assicurati che l'articolo le tratti tutte, meglio dei competitor.
- **Analizza le fonti citate (`references`).** I domini/pagine citati dall'AI Overview sono i competitor di fatto per la citazione: nota quali sono, se il sito del cliente è già tra questi, e cosa fanno quelle pagine che potremmo fare meglio. Se compaiono fonti diverse dai competitor organici dello Step 2, tienine conto.
- **E-E-A-T conta di più.** Le fonti citate dagli AI Overview tendono a essere autorevoli e aggiornate: segnala di rafforzare segnali di expertise, dati recenti e attribuzione (autore, fonti).

Le osservazioni vanno riportate in modo operativo: ciascuna deve dire al copywriter cosa fare concretamente. Confluiscono nel content-brief-builder come indicazioni di scrittura.

---

## Output

L'output deve essere leggibile sia dal `content-brief-builder` (skill successiva) sia da un cliente o responsabile editoriale. Usa un linguaggio diretto e operativo.

---

**ANALISI SERP — [keyword primaria]**

**CONTROLLO CANNIBALIZZAZIONE**
[Esito del controllo, indicando la/le fonte/i (GSC e/o Ahrefs) e se la proprietà GSC era accessibile. Due casi:
- *Nessun rischio*: una riga che conferma che il sito non presidia il tema (nessuna pagina in top 50 su Ahrefs, nessuna impression/clic rilevante su GSC, nessuna query con più pagine in competizione).
- *Rischio rilevato*: elenco delle pagine già posizionate (keyword presidiata — URL — posizione media — impression/clic se da GSC o traffico stimato se da Ahrefs — fonte). Se GSC mostra più pagine in competizione sulla stessa query, evidenzialo come cannibalizzazione già in atto. Indica che il flusso è in pausa in attesa della decisione dell'utente (continuare / cambiare focus / aggiornare-consolidare la pagina esistente). In questo caso non compilare le sezioni successive finché l'utente non ha scelto.]

**PANORAMICA SERP**
[2-3 righe: cosa domina la prima pagina, intent confermato o rivisto rispetto a keyword-analysis, SERP features rilevanti e cosa implicano per il contenuto da scrivere]

**COMPETITOR ANALIZZATI**

*[Posizione] — [Titolo articolo] — [Dominio]*
- Formato: [tipo di articolo]
- Struttura: [gerarchia heading, elementi di formattazione, lunghezza stimata]
- Contenuto visivo: [immagini, video, elementi interattivi]
- Link interni: [verso articoli / prodotti / landing page — strategia prevalente]
- Angolazione: [a chi si rivolge, punto di vista]

*(ripeti per ciascun competitor analizzato)*

**GAP IDENTIFICATI**
- [Gap 1: cosa manca e come può essere coperto]
- [Gap 2]
- [Gap 3]
*(massimo 5 gap, solo quelli concretamente sfruttabili nell'articolo)*

**DOMANDE PAA DA COPRIRE**
- [Domanda 1]
- [Domanda 2]
*(domande "le persone chiedono anche" presenti in SERP. Vanno integrate come H2/H3 dell'articolo o risposte direttamente all'interno dei paragrafi pertinenti. NON vanno mai raccolte in una sezione "Domande frequenti" / "FAQ" a fine articolo. Ometti questa sezione dell'output se le PAA non sono recuperabili.)*

**AI OVERVIEW**
[Per keyword primaria + 2 secondarie più pertinenti: presente / assente (fonte: DataForSEO). Se presente almeno su una:
- elenco delle keyword con AI Overview
- fonti citate rilevanti (`references`: dominio + pagina), segnalando se il sito del cliente è già citato
- osservazioni operative per la scrittura (estraibilità/risposta diretta, sotto-aspetti da coprire, E-E-A-T, opportunità di citazione)
Se assente su tutte e tre, una riga. Se DataForSEO non era disponibile, segnalalo.]

**FORMATO CONSIGLIATO**
[Formato scelto] — [motivazione in una riga basata sui dati]

**NOTE OPERATIVE** *(solo se necessario)*
[Segnalazioni su SERP mista, AI Overview, frammentazione locale, pagine non leggibili, o altri elementi che impattano la strategia. Massimo 3 righe. Ometti se non ci sono note utili.]

---

## Regole critiche

- Il controllo di cannibalizzazione (Step 0) precede sempre l'analisi competitor. Se una qualsiasi fonte (GSC o Ahrefs) indica che il sito presidia già la keyword primaria o una correlata importante, ferma il flusso e chiedi all'utente se continuare, cambiare focus o aggiornare/consolidare la pagina esistente. Non proseguire senza una sua decisione.
- GSC è la fonte primaria del controllo (dati di prima parte). Per la cannibalizzazione a livello di pagina usa `get_query_page_combinations` (con `analyzeCannibalization: true` per le query con più pagine in competizione). Ahrefs è complemento e fallback quando la proprietà GSC non è accessibile.
- Per i totali GSC usa sempre `get_property_stats`: non sommare mai le righe di `get_search_queries`, `get_top_pages` o `get_query_page_combinations` (le query anonimizzate rendono la somma inferiore al reale). La `position` GSC è una media di periodo, non la posizione attuale.
- Lo Step 0 richiede il dominio del cliente: se non è disponibile dal contesto, chiedilo prima di procedere. Non inventare o assumere il dominio. Se la proprietà GSC non è accessibile, segnalalo e prosegui il controllo con i soli dati Ahrefs.
- Non procedere se la SERP è dominata da contenuti transazionali. Segnala il problema e torna a `keyword-analysis`.
- Analizza solo risultati editoriali. Escludi pagine prodotto, e-commerce e directory.
- I gap devono essere concreti: specifica sempre cosa manca e come colmarlo, mai osservazioni generiche.
- Le domande PAA vanno recuperate dalla SERP reale, non inventate. Se non recuperabili, ometti la sezione.
- Il controllo AI Overview (Chiamata 4 / Step 5) va eseguito sempre su keyword primaria + 2 secondarie più pertinenti, con `load_async_ai_overview: true` per recuperare contenuto e fonti. Non è un checkpoint di stop: se DataForSEO non è disponibile, segnalalo e prosegui. Le osservazioni AI Overview devono essere operative e confluire nel brief.
- Il formato consigliato deve essere motivato dai dati, non dalla preferenza personale.
- L'output deve essere operativo: chi lo legge capisce immediatamente cosa fare.
- Non includere mai valutazioni sulle ads o sui risultati a pagamento.
- Non descrivere il processo di analisi nell'output: mostra solo i risultati.
