---
name: brand-analysis-and-connections
description: >
  Analizza il tono di voce del sito per cui si sta scrivendo l'articolo, individua i contenuti interni rilevanti da collegare (pagine prodotto/categoria, servizi, casi studio, articoli correlati) e produce indicazioni operative per il content-brief-builder. Usa questa skill dopo serp-analysis e prima di content-brief-builder. Trigger tipici: "analizza il sito del cliente", "dammi il TOV del sito", "cosa posso linkare nell'articolo", "procedi con il flusso seo-blog-pipeline". Questa skill è il terzo step del flusso seo-blog-pipeline.
---

# Brand Analysis and Connections

Questa skill analizza il sito web del progetto editoriale su tre livelli: tono di voce, contenuti esistenti correlati al topic dell'articolo, e pagine interne da collegare strategicamente nel testo. Produce indicazioni operative che alimentano direttamente il content-brief-builder.

---

## Input atteso

- URL del sito da analizzare (fornito dall'utente o noto dal contesto del progetto)
- Keyword primaria e topic dell'articolo (dall'output di keyword-analysis)
- **Ambito per l'internal linking** (dalla configurazione di sessione del flusso seo-blog-pipeline, se disponibile):
  - `automatico` (default): esplora l'intero sito e seleziona i contenuti correlati ovunque si trovino.
  - `cartella/sezione specifica`: uno o più percorsi/URL di sezione (es. `/blog/marketing/`) su cui concentrare in modo esaustivo la ricerca dei contenuti correlati, per non perdere articoli più nascosti nei siti con blog multi‑categoria.
  Se questa preferenza non è nota dal contesto e la skill viene usata in autonomia, chiedila all'utente o assume `automatico`.

Se il dominio non è chiaro dal contesto (ad esempio l'azienda gestisce più siti), chiedi conferma all'utente prima di procedere.

---

## Integrazione tool

Usa WebFetch in sequenza sulle sezioni del sito rilevanti per l'analisi. La prima chiamata è la discovery via `robots.txt` + sitemap, che rende la mappatura del sito molto più affidabile rispetto al tirare a indovinare gli URL.

### Chiamata 0 — Discovery via robots.txt + sitemap

Prima di tutto, recupera `https://<dominio>/robots.txt` con WebFetch. Il file robots.txt dichiara quasi sempre l'URL della sitemap XML in una riga tipo `Sitemap: https://esempio.it/sitemap.xml` (a volte più di una). Estrai tutti gli URL di sitemap presenti.

Per ciascuna sitemap dichiarata, esegui WebFetch sull'URL. Una sitemap può essere:
- Una **sitemap‑index** (contiene a sua volta puntatori ad altre sitemap, tipicamente divise per tipo di contenuto: `post-sitemap.xml`, `page-sitemap.xml`, `product-sitemap.xml`, ecc.). In questo caso scendi al livello successivo e recupera anche le sub‑sitemap rilevanti per l'analisi (pagine, blog, prodotti/servizi, casi studio).
- Una **sitemap di URL** (elenco diretto di pagine). Estrai gli URL e categorizzali per pattern: about/azienda, blog/articoli, prodotti/servizi, casi studio, landing page.

Usa la lista di URL ottenuta dalla sitemap come fonte primaria di verità per le chiamate successive: niente più tentativi a indovinare gli URL tipici, ma selezione mirata dalle pagine effettivamente esistenti sul sito.

**Se è stato indicato un ambito per l'internal linking (cartella/sezione specifica):** dalla lista della sitemap, isola ed enumera **tutti** gli URL che ricadono sotto i percorsi indicati (es. tutti gli URL sotto `/blog/marketing/`). Questa enumerazione esaustiva è la base per la ricerca dei contenuti correlati dello Step 2: in quella sezione non limitarti a un campione, ma considera l'intero elenco. Se nessuna sitemap è disponibile, naviga la sezione partendo dalla sua pagina indice (e dalle eventuali pagine di paginazione) per raccogliere gli URL. La scansione delle pagine strategiche (prodotti/servizi/casi studio) resta sull'intero sito anche in questa modalità.

Se `robots.txt` non è raggiungibile o non dichiara sitemap, prova comunque gli URL standard `/sitemap.xml`, `/sitemap_index.xml`, `/sitemap-index.xml`. Se anche questi falliscono, segnalalo nell'output e procedi con il fallback degli URL tipici descritti nelle chiamate seguenti.

### Chiamata 1 — Pagina About / Chi siamo

Recupera la pagina "Chi siamo", "About", "La nostra storia" o equivalente. Questa pagina è la fonte primaria per capire posizionamento, valori e registro comunicativo del brand.

Se hai la sitemap dalla Chiamata 0, scegli l'URL preciso da lì (cerca pattern come `/chi-siamo`, `/about`, `/azienda`, `/about-us`, `/la-nostra-storia` tra gli URL della sitemap). Altrimenti usa gli URL tipici come tentativi: `/chi-siamo`, `/about`, `/azienda`, `/about-us`, `/la-nostra-storia`.

### Chiamata 2 — Blog / News

Recupera la pagina principale del blog o news e poi leggi 3-5 articoli recenti o rappresentativi. Scegli articoli di lunghezza media o lunga, non comunicati stampa. Questi contenuti rivelano il livello di approfondimento atteso, il vocabolario usato, la struttura narrativa e il pubblico a cui si rivolgono.

Se hai la sitemap, seleziona articoli reali dagli URL elencati (preferendo quelli con date recenti se la sitemap riporta `lastmod`, o con slug attinenti al topic dell'articolo da scrivere). Altrimenti usa gli URL tipici: `/blog`, `/news`, `/articoli`, `/magazine`, `/insights`.

### Chiamata 3 — Pagine prodotto e servizio (categorie)

Recupera le pagine di categoria prodotto o servizio principali, non le schede del singolo prodotto. Le pagine categoria hanno più valore SEO e sono quelle da collegare nell'articolo.

Se hai la sitemap, identifica le pagine categoria filtrando gli URL per pattern (es. sub‑sitemap dedicate ai prodotti, oppure URL con path tipo `/prodotti/<categoria>` senza ulteriori segmenti). Altrimenti usa gli URL tipici: `/prodotti`, `/servizi`, `/soluzioni`, `/categorie`.

### Chiamata 4 — Casi studio (se presenti)

Recupera la pagina elenco dei casi studio o portfolio. Leggi 1-2 casi studio che abbiano attinenza con il topic dell'articolo.

Se hai la sitemap, cerca URL con slug `casi-studio`, `case-study`, `portfolio`, `clienti`, `progetti`, `success-stories`. Altrimenti prova gli URL tipici diretti.

Se una pagina non è accessibile o restituisce errore, salta e passa alla successiva. Segnala nell'output quali sezioni non erano disponibili.

---

## Processo di analisi

### Step 1 — Analisi del tono di voce

Sulla base delle pagine lette (about, blog, pagine servizio), ricava le seguenti dimensioni del TOV:

**Registro linguistico**
- Formale, semi-formale o informale?
- Usa il "tu" o il "voi" per rivolgersi al lettore?
- Il linguaggio è tecnico/specialistico o divulgativo/accessibile?
- Ci sono parole chiave o espressioni ricorrenti che identificano il brand?

**Tono narrativo**
- È più autorevole/esperto, empatico/vicino, o neutro/informativo?
- Usa storytelling o preferisce un approccio diretto e fattuale?
- Mette in evidenza i benefici per il cliente o le caratteristiche tecniche del prodotto?

**Pubblico percepito**
- A chi si rivolge prevalentemente il sito? (consumatore finale, professionista, azienda B2B, istituzione)
- Il livello di competenza assunto nel lettore è alto, medio o basso?

**Segnali di brand identity**
- Ci sono claim, tagline o frasi ricorrenti da preservare?
- Ci sono argomenti o valori su cui il brand insiste particolarmente? (es. sostenibilità, innovazione, made in Italy, certificazioni)

Se dall'analisi del sito il TOV risulta vago, generico o contraddittorio tra sezioni diverse, segnalalo e chiedi all'utente di fornire 3-5 esempi di post social (LinkedIn, Instagram, o altro canale rilevante) per integrare l'analisi.

### Step 2 — Contenuti correlati esistenti

Identifica articoli del blog già pubblicati che trattano argomenti vicini al topic dell'articolo da scrivere. Valuta la correlazione in base a quanti elementi hanno in comune con il topic (stesso settore, stesso pubblico, stessa categoria di prodotto/servizio, stesse keyword semantiche).

**Ambito della ricerca:**
- Se è stato indicato un ambito `automatico` (default): cerca i contenuti correlati su tutto il sito, usando la lista di URL della sitemap e gli slug attinenti al topic.
- Se è stata indicata una **cartella/sezione specifica**: dai priorità all'elenco esaustivo di URL di quella sezione (raccolto nella Chiamata 0) e passali in rassegna tutti, senza fermarti a un campione di articoli recenti. È il modo per non perdere articoli più nascosti nei blog con molte categorie. Puoi comunque includere contenuti correlati molto pertinenti trovati fuori dalla sezione, segnalandolo.

Per ciascun contenuto correlato indica:
- Titolo e URL
- Perché è correlato (elemento in comune con il topic)
- Tipo di relazione: approfondisce un aspetto del topic, tratta un argomento complementare, è un prerequisito concettuale

Questi contenuti sono candidati per i link interni "editoriali" nell'articolo, quelli che collegano concetti tra loro.

### Step 3 — Pagine interne da collegare strategicamente

Identifica le pagine prodotto (categorie), servizio e casi studio che hanno attinenza con il topic dell'articolo. Questi sono i link interni "commerciali/strategici" dell'articolo, quelli che collegano il contenuto informativo alle offerte del brand.

Criteri di selezione:
- Collega pagine di categoria prodotto, non schede del singolo prodotto (maggiore valore SEO)
- Collega pagine servizio rilevanti per il topic
- Collega casi studio che dimostrano competenza sul topic
- Non collegare mai landing page

Per ciascuna pagina da collegare indica:
- Titolo e URL
- Perché è rilevante per l'articolo
- Suggerimento di anchor text naturale (la parola o frase nel testo su cui inserire il link)

### Step 4 — Pagine esistenti da cui linkare il nuovo articolo (link in entrata)

Lo Step 2 individua i contenuti da linkare **dal** nuovo articolo (link in uscita). Questo step fa il contrario: individua gli articoli del blog **già pubblicati e correlati dove conviene inserire un link che punta al nuovo articolo** (link in entrata). Serve a far ricevere al nuovo contenuto link interni da pagine già indicizzate, accelerandone il posizionamento ed evitando che nasca "orfano".

Parti dai contenuti correlati identificati nello Step 2 e seleziona quelli in cui un rimando al nuovo articolo sarebbe naturale e utile per il lettore (es. articoli che toccano il topic di sfuggita e che potrebbero approfondirlo linkando il nuovo pezzo).

Per ciascuno indica:
- Titolo e URL dell'articolo esistente
- Contesto: perché è un buon punto da cui linkare e in quale passaggio dell'articolo esistente comparirebbe il rimando
- Anchor text suggerito: la parola o frase, **all'interno dell'articolo esistente**, su cui inserire il link verso il nuovo articolo

Se il sito ha pochi contenuti correlati, segnala che le opportunità di link in entrata sono limitate.

---

## Gestione siti con pochi contenuti

Se il sito ha un blog scarso, pochi articoli o contenuti datati, la skill procede comunque con quello che trova. Non blocca l'analisi. Segnala nell'output che la base di contenuti esistenti è limitata, indicando che i link interni disponibili saranno principalmente verso pagine prodotto/servizio piuttosto che articoli correlati.

---

## Output

---

**BRAND ANALYSIS — [nome sito / dominio]**

**TONO DI VOCE**

*Registro:* [formale / semi-formale / informale — tu / voi — tecnico / divulgativo]
*Tono narrativo:* [autorevole / empatico / neutro — orientato al beneficio / alla caratteristica]
*Pubblico percepito:* [chi è il lettore tipo del sito, livello di competenza assunto]
*Elementi di brand identity da preservare:* [claim, valori ricorrenti, espressioni tipiche del brand]
*Vocabolario ricorrente:* [termini, aggettivi o costruzioni sintattiche che caratterizzano la comunicazione]

**NOTE TOV** *(solo se necessario)*
[Segnala se il TOV è stato difficile da rilevare, contraddittorio tra sezioni, o se è stata richiesta integrazione con i social. Ometti se non ci sono note.]

**CONTENUTI CORRELATI DA COLLEGARE**

*[Titolo articolo] — [URL]*
- Correlazione: [perché è correlato al topic]
- Tipo: [approfondisce / complementare / prerequisito]

*(ripeti per ciascun contenuto correlato trovato)*

**PAGINE STRATEGICHE DA COLLEGARE**

*[Titolo pagina] — [URL]*
- Rilevanza: [perché è pertinente per l'articolo]
- Anchor text suggerito: [parola o frase naturale su cui inserire il link]

*(ripeti per ciascuna pagina strategica)*

**LINK IN ENTRATA DA CREARE (verso il nuovo articolo)**

*[Titolo articolo esistente] — [URL]*
- Contesto: [perché linkare da qui e in quale passaggio dell'articolo esistente]
- Anchor text suggerito: [parola o frase nell'articolo esistente su cui mettere il link al nuovo articolo]

*(ripeti per ciascun articolo esistente da cui linkare. Se non ce ne sono di adatti, indicalo esplicitamente.)*

**PAGINE NON ACCESSIBILI** *(solo se necessario)*
[Elenco delle sezioni del sito non raggiungibili durante l'analisi. Ometti se tutte le pagine erano accessibili.]

---

## Regole critiche

- Chiedi conferma del dominio se non è chiaro dal contesto o se l'azienda gestisce più siti.
- Se l'utente ha indicato una cartella/sezione specifica per l'internal linking, enumera ed esamina in modo esaustivo gli articoli di quella sezione: non limitarti a un campione. È il punto chiave per non perdere contenuti nascosti nei blog multi‑categoria.
- Non collegare mai landing page: solo pagine utili fronte SEO (categorie prodotto, servizi, casi studio, articoli).
- Preferisci sempre le pagine di categoria prodotto alle schede del singolo prodotto.
- Se il TOV non è rilevabile con certezza dal sito, chiedi esempi social prima di produrre l'output. Non inventare un TOV.
- Se il sito ha pochi contenuti, segnalalo ma procedi comunque con quello che è disponibile.
- L'anchor text suggerito deve essere naturale nel contesto dell'articolo: mai anchor text generici come "clicca qui" o "scopri di più".
- Non includere link a risorse esterne: solo link interni al sito del cliente.
- Tieni sempre separati i link in uscita (dal nuovo articolo, Step 2 e 3) dai link in entrata da creare (verso il nuovo articolo, Step 4): sono due liste distinte nell'output, con anchor text riferiti a documenti diversi.
