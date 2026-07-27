---
name: guest-post-brand-analysis
description: >
  Analizza il sito del cliente e la/e pagina/e target da linkare per un guest post di link building. Apprende cosa fa il brand, i suoi prodotti/servizi, i valori e l'elemento distintivo, il pubblico, e soprattutto cosa contiene esattamente la pagina target, così da poter contestualizzare il link nel modo giusto. Verifica la coerenza tra l'anchor richiesta e la pagina target (l'anchor non deve promettere al lettore qualcosa di diverso da ciò che troverà) e individua le varianti con cui citare il brand nel testo. Usa questa skill come prima fase del flusso guest-post-pipeline, prima di host-site-analysis e guest-post-writer. Trigger tipici: "analizza il cliente per il guest post", "studia la pagina da linkare", "prepara l'analisi del brand per l'articolo di link building". Questa skill NON valuta il profilo backlink né fa keyword research: serve solo a capire il cliente e la pagina target per scrivere un articolo credibile e un link coerente.
---

# Guest Post Brand Analysis

Questa skill studia il **cliente** e la/e **pagina/e target** da linkare, per dare allo scrittore del guest post tutto ciò che serve a: (a) parlare del brand in modo accurato e non generico quando serve, (b) inserire il link in un contesto coerente, e (c) verificare che l'anchor richiesta non inganni il lettore.

L'obiettivo non è un dossier esaustivo sul cliente, ma una scheda operativa e sintetica, orientata alla scrittura di un singolo articolo.

---

## Input atteso

- **URL del sito del cliente**: il dominio del brand da promuovere. Di norma è ricavabile dalla/e pagina/e target. Se non è chiaro, chiedilo.
- **Pagina/e target da linkare**: l'URL (o gli URL) verso cui punterà il link nell'articolo.
- **Anchor text**: il testo di ancoraggio richiesto per ogni link (per il controllo di coerenza anchor ↔ pagina).
- **Topic dell'articolo**: l'argomento fornito dall'utente (per valutare la pertinenza del cliente rispetto al tema).
- **Lingua**: la lingua dell'articolo (l'analisi va condotta tenendo conto del mercato di quella lingua).

---

## Integrazione strumenti

Usa `WebFetch` per leggere le pagine del sito del cliente. Leggi in sequenza:

1. **La/e pagina/e target** indicata/e dall'utente: sono la fonte più importante, perché è lì che punta il link.
2. **La homepage** del sito: per inquadrare settore, posizionamento e tono generale del brand.
3. **La pagina "Chi siamo" / "About"** (se presente): per valori, storia, elemento distintivo del brand.

Se una pagina non è raggiungibile con gli strumenti disponibili (blocco di rete, contenuto non leggibile), non inventarne il contenuto: chiedi all'utente di incollare il testo della pagina (in particolare quello della pagina target, che è indispensabile). Se più della metà delle pagine non è leggibile, segnalalo e procedi con ciò che l'utente fornisce.

Non servono strumenti SEO in questa fase: qui si studia il contenuto e il senso del brand, non le metriche.

---

## Processo di analisi

### Step 1 — Comprensione del brand

Dalla homepage e dalla pagina "Chi siamo", ricava:
- **Settore e cosa fa**: in una frase, di cosa si occupa il cliente.
- **Prodotti / servizi principali**: cosa offre concretamente.
- **Elemento distintivo (il "perché")**: cosa rende riconoscibile il brand, il motivo per cui un cliente lo sceglie (non cosa fa o come, ma perché). Se non è esplicitato, deducilo con prudenza dai contenuti, senza inventare.
- **Valori e posizionamento**: artigianale/industriale, premium/accessibile, tecnico/divulgativo, B2B/B2C.
- **Pubblico di riferimento**: a chi si rivolge il brand.

### Step 2 — Analisi della pagina target

Per ciascuna pagina target da linkare, ricava:
- **Tipo di pagina**: prodotto, categoria, servizio, guida/articolo, landing, homepage.
- **Cosa offre esattamente**: il contenuto concreto che il lettore troverà cliccando il link.
- **A chi si rivolge**: il bisogno che quella pagina soddisfa.
- **Aggancio tematico con il topic dell'articolo**: qual è il ponte naturale tra l'argomento dell'articolo e ciò che offre la pagina. È il punto in cui il link potrà cadere in modo credibile.

### Step 3 — Coerenza anchor ↔ pagina target

Per ogni coppia anchor/pagina, verifica che **l'anchor prometta ciò che la pagina mantiene**: chi legge l'anchor e clicca deve trovare esattamente quel tipo di risorsa. Segnala se:
- L'anchor è generica o fuorviante rispetto al contenuto della pagina.
- L'anchor è un **match esatto** su una keyword commerciale/competitiva (rischio di sovra-ottimizzazione, specie in settori YMYL): annota il rischio, così che il writer e l'utente possano valutare una variante più diluita o branded. Non modificare l'anchor di tua iniziativa: la scelta resta dell'utente.

### Step 4 — Forme di citazione del brand

Individua i modi in cui il brand può essere nominato nel testo, per **variare** le menzioni ed evitare ripetizioni meccaniche:
- Nome del brand (come si scrive ufficialmente).
- Eventuali varianti (con/senza forma societaria, sigla, nome del prodotto/linea).
- Menzione generica ("l'azienda", "il produttore", "il negozio specializzato in…") utilizzabile come alternativa quando il nome è già stato usato di recente.

Nota anche il **tono con cui il brand parla di sé** (dalla homepage): serve come riferimento secondario, ma ricorda che nel guest post il tono primario resta quello del portale ospitante (fase successiva).

---

## Output

---

**ANALISI BRAND — [nome brand]**

**SCHEDA BRAND**
- Settore e attività: [una frase]
- Prodotti/servizi principali: [elenco sintetico]
- Elemento distintivo (il "perché"): [cosa rende riconoscibile il brand]
- Valori e posizionamento: [tratti chiave]
- Pubblico: [a chi si rivolge]

**PAGINA/E TARGET**

*[URL pagina target 1]*
- Tipo: [prodotto/categoria/servizio/guida/landing/home]
- Cosa offre: [contenuto concreto]
- A chi si rivolge: [bisogno soddisfatto]
- Aggancio con il topic dell'articolo: [il ponte tematico naturale per il link]

*(ripeti per ogni pagina target)*

**COERENZA ANCHOR ↔ TARGET**
- [anchor] → [pagina]: [coerente / attenzione: motivo] [eventuale nota su rischio di sovra-ottimizzazione]

*(ripeti per ogni coppia anchor/pagina)*

**FORME DI CITAZIONE DEL BRAND**
- Nome ufficiale: [brand]
- Varianti: [elenco]
- Menzioni generiche utilizzabili: [elenco]

**NOTE** *(solo se necessario)*
[Segnalazioni concise: pagina non leggibile, anchor rischiosa, brand con posizionamento ambiguo, elemento distintivo non deducibile. Massimo 2-3 righe.]

---

## Regole critiche

- Non inventare informazioni sul brand o sulla pagina target: se una pagina non è leggibile, chiedi all'utente di incollarne il contenuto. La pagina target in particolare è indispensabile.
- L'elemento distintivo ("perché") va dedotto solo se i contenuti lo permettono; se non emerge, dichiaralo, non inventarlo.
- Segnala sempre l'incoerenza anchor ↔ pagina e il rischio di sovra-ottimizzazione, ma non modificare l'anchor: la decisione è dell'utente (gestita nel checkpoint dell'orchestratore).
- Non fare keyword research né valutazioni sul profilo backlink: non è il compito di questa skill.
- Le forme di citazione del brand servono a variare le menzioni nel testo: raccoglile sempre, anche quando il brand ha un nome solo (in quel caso proponi almeno una menzione generica alternativa).
- Il tono del brand è un riferimento secondario: nel guest post prevale il tono del portale ospitante.
- Mantieni la scheda sintetica e operativa: serve a scrivere un articolo, non a fare un dossier aziendale.
