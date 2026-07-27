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

Lo Step 2 individua i contenuti da linkare **dal** nuovo articolo (link in uscita). Questo step fa il contrario: individua gli **articoli del blog già pubblicati** dove conviene inserire un link che punta al nuovo articolo (link in entrata). Serve a far ricevere al nuovo contenuto link interni da pagine già indicizzate, accelerandone il posizionamento ed evitando che nasca "orfano".

**Due vincoli rigidi:**

1. **Massimo 2 articoli.** Anche se ne trovi tanti candidati, seleziona solo i 2 in cui il rimando al nuovo articolo è più naturale e utile per il lettore. Meno rumore per chi pubblica, priorità sulle opportunità migliori. Se solo 1 articolo è davvero adatto, restituiscine 1; se nessuno lo è, restituisci l'elenco vuoto (indicalo).
2. **Solo articoli del blog.** Escludi pagine prodotto, pagine servizio, pagine categoria, casi studio, landing page, "chi siamo": la lista deve contenere esclusivamente articoli editoriali del blog/magazine.

**Procedura operativa (obbligatoria).** Parti dai contenuti correlati dello Step 2 filtrati per soli articoli del blog. Scegli fino a 4 candidati; poi, per ciascuno, **leggi il testo con `WebFetch`** (se non già letto nella Chiamata 2) e identifica la **frase esatta** dell'articolo esistente dove l'inserimento del link sarebbe naturale e migliorativo (paragrafo che tocca il topic del nuovo articolo di sfuggita, o dove il lettore trarrebbe beneficio dall'approfondimento). Da questi candidati letti, seleziona i 2 migliori.

Per ciascuno dei 2 articoli selezionati indica **esattamente** questi elementi:
- **URL**: URL completo dell'articolo esistente (assoluto, `https://dominio.tld/...`, mai solo path relativo)
- **Sezione**: heading (H2/H3) dell'articolo esistente in cui si trova la frase da modificare
- **Frase attuale**: la **frase esatta** (copiata verbatim dall'articolo esistente) da modificare per inserire il link
- **Frase nuova**: la **stessa frase riscritta** con il link inserito, mostrando **fra doppi asterischi o backtick l'anchor** cliccabile (es. "…grazie a **una guida completa sulla mindfulness**…")
- **Anchor**: il testo esatto dell'anchor usato nella frase nuova (deve coincidere con la porzione evidenziata sopra)

**Non aggiungere commenti, motivazioni o spiegazioni**: l'output è solo l'elenco operativo (le 2 voci come sopra), deve poter essere copiato e applicato senza altre informazioni.

Se `WebFetch` non riesce a leggere uno degli articoli candidati (403, paywall, corpo troncato, contenuto vuoto), scartalo e prova il candidato successivo. Se non riesci a leggere abbastanza articoli per selezionarne 2, restituisci quelli che sei riuscito a lavorare (anche 1 o 0) e segnalalo esplicitamente.

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

- [URL completo con https://dominio.tld/...] - anchor: "[anchor text naturale da usare nell'articolo]" - correlazione: [approfondisce / complementare / prerequisito]

*(un bullet per contenuto correlato. URL sempre assoluto - MAI solo path relativo tipo `/blog/...`. Anchor sempre obbligatoria.)*

**PAGINE STRATEGICHE DA COLLEGARE**

- [URL completo con https://dominio.tld/...] - anchor: "[anchor text naturale]" - rilevanza: [perché è pertinente]

*(un bullet per pagina strategica. URL sempre assoluto. Anchor sempre obbligatoria.)*

**LINK IN ENTRATA DA CREARE (verso il nuovo articolo)**

*Massimo 2 voci, esclusivamente articoli del blog.*

1. **URL**: https://dominio.tld/percorso-completo-articolo-esistente
   - **Sezione**: [heading H2/H3 in cui si trova la frase]
   - **Frase attuale**: "[copia esatta della frase esistente da modificare]"
   - **Frase nuova**: "[la stessa frase riscritta con il link inserito, con l'**anchor evidenziata in grassetto**]"
   - **Anchor**: "[testo esatto dell'anchor]"

2. **URL**: https://dominio.tld/percorso-completo-articolo-esistente
   - **Sezione**: [heading H2/H3 in cui si trova la frase]
   - **Frase attuale**: "[copia esatta della frase esistente da modificare]"
   - **Frase nuova**: "[la stessa frase riscritta con il link inserito]"
   - **Anchor**: "[testo esatto dell'anchor]"

*(Massimo 2 voci - se ne trovi solo 1 di davvero adatta, restituisci solo quella. Se nessuna: scrivi "Nessun articolo del blog adatto per un link in entrata naturale" in una riga. Niente commenti o motivazioni: l'output è solo la lista.)*

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
- **URL sempre assoluti** in tutti gli output (contenuti correlati, pagine strategiche, link in entrata): scrivi sempre `https://dominio.tld/percorso-completo`, **mai** il solo path relativo (`/blog/…`, `/prodotti/…`). Chi legge l'output deve poter copiare e cliccare il link senza doverlo ricomporre.
- **Anchor text sempre obbligatoria** in ogni output di link: per contenuti correlati (link in uscita), pagine strategiche (link in uscita) e link in entrata da creare. Non è mai facoltativa: se non riesci a proporne una naturale, l'articolo/pagina non va incluso.
- Non includere link a risorse esterne: solo link interni al sito del cliente.
- Tieni sempre separati i link in uscita (dal nuovo articolo, Step 2 e 3) dai link in entrata da creare (verso il nuovo articolo, Step 4): sono due liste distinte nell'output, con anchor text riferiti a documenti diversi.
- **Link in entrata (Step 4): tre vincoli rigidi.** (a) **Massimo 2 articoli**, mai di più; se solo 1 è davvero adatto restituiscine 1, se nessuno restituisci lista vuota. (b) **Esclusivamente articoli del blog** (mai pagine prodotto, servizio, categoria, casi studio, landing, "chi siamo"). (c) Per ciascuno serve la **frase esatta** dell'articolo esistente da modificare (copiata verbatim via WebFetch) e la **frase riscritta** con il link inserito e l'anchor evidenziata: non basta "sezione X". Se WebFetch non riesce a leggere abbastanza articoli candidati, restituisci solo quelli lavorati e segnalalo.
