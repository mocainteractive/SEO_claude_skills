---
name: serp-analysis
description: >
  Analizza la SERP per la keyword primaria identificata dalla skill keyword-analysis e produce indicazioni operative per il content-brief-builder. Prima dell'analisi competitor esegue un controllo di cannibalizzazione: verifica se il sito del cliente è già posizionato sulla keyword primaria o sulle correlate principali e, in caso affermativo, ferma il flusso per decidere se continuare, cambiare focus o aggiornare la pagina esistente. Usa questa skill dopo keyword-analysis e prima di brand-analysis-and-connections. Trigger tipici: "analizza la SERP per questa keyword", "cosa fanno i competitor su questo topic", "come sono strutturati i contenuti in prima pagina", "abbiamo già un contenuto su questa keyword?", "procedi con il flusso seo-blog-pipeline". Questa skill è il secondo step del flusso seo-blog-pipeline.
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

### Chiamata 0 — Controllo cannibalizzazione (Ahrefs MCP)

Prima di tutto, verifica se il sito del cliente ha già contenuti posizionati sulla keyword primaria o sulle correlate più importanti. Serve a evitare di creare un nuovo articolo che competa con una pagina esistente (cannibalizzazione).

Usa `site-explorer-organic-keywords` sul dominio del cliente.

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

Se il dominio non ha dati in Ahrefs o la chiamata non restituisce keyword, considera il controllo superato (nessuna cannibalizzazione rilevata) e procedi.

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

---

## Processo di analisi

### Step 0 — Controllo cannibalizzazione (prima di ogni altra cosa)

Analizza i risultati della Chiamata 0 (e il segnale incrociato della Chiamata 1). Per la keyword primaria e per le correlate importanti, verifica se esiste già una pagina del sito posizionata:

- Considera posizionamento rilevante un risultato con `best_position_kind` = `organic` e `best_position_url` valorizzato.
- Valuta la gravità in base alla posizione (`best_position`):
  - **Top 10** (≤ 10): cannibalizzazione forte. Un nuovo contenuto sulla stessa keyword competerebbe direttamente con una pagina che già ranka bene.
  - **Posizione 11-50**: cannibalizzazione potenziale. Il sito presidia già il tema; un nuovo contenuto rischia di disperdere autorità invece di concentrarla.
  - **Oltre 50 o assente**: nessun rischio concreto, procedi.

Se trovi almeno una pagina posizionata in **top 50** sulla keyword primaria o su una correlata ad alto volume:

1. **FERMA il flusso**: non procedere con la verifica SERP e l'analisi competitor.
2. Mostra all'utente, in modo conciso:
   - La/le keyword già presidiate dal sito
   - L'URL della pagina esistente che ranka, con posizione e traffico stimato (`sum_traffic`)
3. Chiedi esplicitamente come procedere, proponendo tre opzioni:
   - **Continuare comunque** con un nuovo articolo (accettando il rischio, es. se l'angolo è diverso o si vuole sostituire la vecchia pagina)
   - **Cambiare focus** su una keyword/angolazione diversa (tornando a `keyword-analysis`)
   - **Aggiornare la pagina esistente** invece di crearne una nuova

Non procedere allo Step 1 finché l'utente non ha scelto.

Se non viene rilevata cannibalizzazione, prosegui normalmente e segnala l'esito nel blocco dedicato dell'output (una riga).

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

---

## Output

L'output deve essere leggibile sia dal `content-brief-builder` (skill successiva) sia da un cliente o responsabile editoriale. Usa un linguaggio diretto e operativo.

---

**ANALISI SERP — [keyword primaria]**

**CONTROLLO CANNIBALIZZAZIONE**
[Esito del controllo. Due casi:
- *Nessun rischio*: una riga che conferma che il sito non ha pagine posizionate in top 50 sul tema.
- *Rischio rilevato*: elenco delle pagine già posizionate (keyword presidiata — URL — posizione — traffico stimato) e indicazione che il flusso è in pausa in attesa della decisione dell'utente (continuare / cambiare focus / aggiornare la pagina esistente). In questo caso non compilare le sezioni successive finché l'utente non ha scelto.]

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

**FORMATO CONSIGLIATO**
[Formato scelto] — [motivazione in una riga basata sui dati]

**NOTE OPERATIVE** *(solo se necessario)*
[Segnalazioni su SERP mista, AI Overview, frammentazione locale, pagine non leggibili, o altri elementi che impattano la strategia. Massimo 3 righe. Ometti se non ci sono note utili.]

---

## Regole critiche

- Il controllo di cannibalizzazione (Step 0) precede sempre l'analisi competitor. Se il sito ha già una pagina posizionata in top 50 sulla keyword primaria o su una correlata importante, ferma il flusso e chiedi all'utente se continuare, cambiare focus o aggiornare la pagina esistente. Non proseguire senza una sua decisione.
- Lo Step 0 richiede il dominio del cliente: se non è disponibile dal contesto, chiedilo prima di procedere. Non inventare o assumere il dominio.
- Non procedere se la SERP è dominata da contenuti transazionali. Segnala il problema e torna a `keyword-analysis`.
- Analizza solo risultati editoriali. Escludi pagine prodotto, e-commerce e directory.
- I gap devono essere concreti: specifica sempre cosa manca e come colmarlo, mai osservazioni generiche.
- Le domande PAA vanno recuperate dalla SERP reale, non inventate. Se non recuperabili, ometti la sezione.
- Il formato consigliato deve essere motivato dai dati, non dalla preferenza personale.
- L'output deve essere operativo: chi lo legge capisce immediatamente cosa fare.
- Non includere mai valutazioni sulle ads o sui risultati a pagamento.
- Non descrivere il processo di analisi nell'output: mostra solo i risultati.
