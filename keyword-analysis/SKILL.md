---
name: keyword-analysis
description: "Analizza una keyword seme o un topic generico e produce un set di keyword ottimizzato per la scrittura di un articolo blog SEO. Usa questa skill ogni volta che l'utente fornisce un argomento, una keyword o un tema su cui vuole scrivere un articolo, anche se non la chiama esplicitamente \"analisi keyword\". Trigger tipici: \"voglio scrivere un articolo su X\", \"dammi le keyword per X\", \"analizza la keyword X\", \"sto scrivendo su X, da dove parto?\". Questa skill è il primo step del flusso seo-blog-pipeline e deve sempre essere eseguita prima delle skill successive."
---

# Keyword Analysis

Questa skill analizza un punto di partenza (keyword seme, topic generico o frase) e produce un set di keyword focalizzato e pronto all'uso per la scrittura di un articolo blog informativo ottimizzato SEO.

L'obiettivo non è un report esaustivo, ma una lista chirurgica che orienta il copywriter (o le skill successive del flusso) senza disorientarlo.

---

## Input atteso

L'utente fornisce uno dei seguenti:
- Una keyword semplice ("meditazione")
- Una frase ("come fare meditazione")
- Un tema più ampio ("alimentazione vegana per sportivi")
- Una o più keyword già scelte (una lista che l'utente ha già in mente)

Di norma non si parte da un cluster già formato: il cluster è l'output di questa skill. Ma l'utente può comunque fornire delle keyword di partenza già selezionate.

**Se l'utente fornisce già una o più keyword**, prima di procedere chiedigli quale dei due percorsi preferisce:
- **Cercare anche keyword correlate** (consigliato): esegui l'analisi completa qui sotto usando le sue keyword come seme e ampliando il set con varianti semantiche, domande, long‑tail e termini LSI.
- **Procedere solo con le keyword fornite**: salta la costruzione del cluster (Step 4) e non aggiungere nuove keyword. Recupera comunque da Ahrefs volume e intent delle keyword fornite (Chiamata 1) per popolare i dati richiesti dal brief, e individua tra quelle la keyword primaria.

Rispetta la scelta dell'utente. In entrambi i casi questa è solo la Fase 1: gli step successivi del flusso (serp-analysis, brand-analysis-and-connections) vanno comunque eseguiti.

---

## Integrazione Ahrefs MCP

Prima di avviare il processo di analisi, recupera i dati reali tramite i tool Ahrefs MCP. Esegui le seguenti chiamate in sequenza.

### Chiamata 1 — Overview della keyword seme
Usa `keywords-explorer-overview` sulla keyword seme per ottenere i dati di base.

Parametri:
- `keywords`: la keyword seme fornita dall'utente
- `country`: "it" (default, salvo diversa indicazione)
- `select`: "keyword,volume,difficulty,intents,traffic_potential,parent_topic,serp_features,clicks,cpc"

Dati che ottieni: volume mensile, difficulty (0-100), intent (informational/navigational/commercial/transactional come oggetto boolean), traffic potential, parent topic, SERP features presenti.

### Chiamata 2 — Matching terms (cluster di keyword)
Usa `keywords-explorer-matching-terms` per trovare tutte le keyword che contengono i termini della keyword seme.

Parametri:
- `keywords`: la keyword seme
- `country`: "it"
- `select`: "keyword,volume,difficulty,intents,traffic_potential,parent_topic"
- `limit`: 50
- `order_by`: "volume:desc"

Filtra i risultati mantenendo solo keyword con intent informazionale o commerciale. Scarta quelle transazionali.

### Chiamata 3 — Search suggestions (domande e long-tail)
Usa `keywords-explorer-search-suggestions` per ottenere suggerimenti correlati, utili per domande frequenti e long-tail.

Parametri:
- `keywords`: la keyword seme
- `country`: "it"
- `select`: "keyword,volume,difficulty,intents"
- `limit`: 30
- `order_by`: "volume:desc"

### Chiamata 4 — Volume storico (solo se stagionalità sospetta)
Se il topic potrebbe avere picchi stagionali, usa `keywords-explorer-volume-history` per verificare.

Parametri:
- `keyword`: la keyword primaria selezionata
- `country`: "it"
- `date_from`: 12 mesi fa dalla data attuale

Usa i dati raccolti per alimentare i 5 step del processo di analisi qui sotto.

---

## Processo di analisi

Segui questo ordine preciso. Ogni step usa i dati Ahrefs recuperati sopra.

### Step 1 — Search intent

Leggi il campo `intents` restituito da Ahrefs per la keyword seme: è un oggetto con campi boolean (`informational`, `navigational`, `commercial`, `transactional`). Usa questo dato come base, integrandolo con il tuo ragionamento sulla SERP.

- **Informazionale**: compatibile con articolo blog.
- **Commerciale**: compatibile con articolo blog solo se `informational` è anch'esso true o se le SERP features non mostrano prevalenza di shopping/paid.
- **Transazionale** (con `informational` false): un articolo blog non ha chances. Segnala il problema e chiedi conferma prima di procedere.
- **Navigazionale**: irrilevante per i nostri scopi.

Nota anche le `serp_features` presenti: snippet, ai_overview, question, video danno indicazioni sul formato di contenuto più premiato da Google per quella query.

### Step 2 — Volume e opportunità

Usa il campo `volume` (medio mensile) e `traffic_potential` (traffico totale che riceve la pagina #1 per quella keyword).

Il volume è un dato informativo, non un filtro. Anche keyword con volume zero o molto basso sono valide se coerenti con il tema richiesto: possono intercettare ricerche emergenti, nicchie specifiche o query a coda lunga sottostimate dagli strumenti. Il `traffic_potential` è spesso più indicativo del volume: mostra quante ricerche totali potrebbe intercettare un contenuto che rankasse al primo posto.

### Step 3 — Difficoltà e competitività della SERP

Usa il campo `difficulty` (scala 0-100):
- 0-20: bassa competitività, buone chance per siti nuovi o di nicchia
- 21-50: competitività media, serve un contenuto solido e autorevole
- 51-70: alta competitività, serve un approccio differenziante
- 71+: molto alta, valuta se esiste una variante long-tail con difficulty inferiore

Nota anche `serp_domain_rating_top10_min` se disponibile: indica il DR minimo tra i siti in top 10, utile per capire se ci sono siti "normali" già posizionati.

### Step 4 — Selezione keyword primaria e costruzione del cluster

Con i dati delle chiamate 2 e 3, costruisci il cluster:

- **Keyword primaria**: quella con il miglior equilibrio tra volume, intent informativo e difficulty. Non necessariamente la più cercata, ma quella più scalabile.
- **Varianti semantiche**: keyword dal matching terms con stesso parent topic della primaria.
- **Domande frequenti**: keyword dal matching terms o suggestions che iniziano con "come", "cosa", "quando", "perché", "qual è", "quanto". Ottime per H2/H3.
- **Long-tail specifiche**: keyword con 4+ parole, volume basso ma intent molto preciso.
- **Termini LSI**: concetti semanticamente correlati attesi da Google su quel topic. Derivali dal cluster e dal tuo ragionamento tematico.

Criteri di esclusione: scarta keyword con intent transazionale, keyword fuori tema, keyword troppo generiche. Massimo 20-30 keyword secondarie.

### Step 5 — Stagionalità (quando rilevante)

Se hai eseguito la chiamata 4, analizza l'andamento mensile del volume storico. Se ci sono picchi ricorrenti negli stessi mesi, segnala i mesi di picco e la raccomandazione su quando pubblicare o aggiornare.

Ometti questo step se il topic è evergreen e i dati storici non mostrano stagionalità.

---

## Output

Usa sempre questa struttura:

---

**KEYWORD PRIMARIA**
[keyword] - [volume mensile stimato] - [intent: informazionale / commerciale / misto]

**KEYWORD SECONDARIE E CORRELATE**

*Varianti semantiche*
- [keyword] - [volume mensile stimato] - [intent: informazionale / commerciale / misto]
- [keyword] - [volume mensile stimato] - [intent: informazionale / commerciale / misto]

*Domande frequenti degli utenti*
- [domanda — ottima per H2/H3]
- [domanda]

*Long-tail e angolazioni specifiche*
- [keyword long-tail] - [volume mensile stimato] - [intent: informazionale / commerciale / misto]
- [keyword long-tail] - [volume mensile stimato] - [intent: informazionale / commerciale / misto]

*Termini semantici correlati (LSI)*
- [termine]
- [termine]

**NOTE** *(solo se necessario)*
[Eventuali segnalazioni concise su intent ambiguo, stagionalità rilevante, o suggerimento su formato del contenuto. Massimo 2-3 righe. Ometti questa sezione se non ci sono note utili.]

---

## Regole critiche

- Non includere mai keyword transazionali in un'analisi orientata a contenuti blog informativi.
- Non gonfiare la lista: 20-30 keyword secondarie sono sufficienti. Qualità > quantità.
- Non produrre un report decisionale sul "vale la pena scrivere questo articolo": la decisione di scrivere è già stata presa. Questa skill fornisce la base per farlo bene.
- Le note sono eccezioni, non la norma. Usale solo quando c'è qualcosa di concretamente utile da segnalare.
- Se l'intent è chiaramente transazionale, segnalalo esplicitamente e chiedi conferma prima di procedere.
- Scarta le keyword geolocalizzate (es. "manutenzione cancelli automatici Roma"): sono irrilevanti per un articolo nazionale. Se sono molto presenti nei risultati, segnalarlo nelle note come indicatore di mercato frammentato localmente.