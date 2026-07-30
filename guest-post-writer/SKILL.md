---
name: guest-post-writer
description: >
  Scrive la bozza completa di un articolo guest post per la link building a partire dal topic fornito dall'utente, dall'analisi del brand/pagina target (guest-post-brand-analysis) e del portale ospitante (host-site-analysis). Produce prima una scaletta con il piano del link, poi il testo completo (H1, introduzione, H2/H3, grassetto con criterio) nel tono di voce del portale e nella lingua richiesta, con il/i link del cliente inserito/i in modo naturale secondo le linee guida di link building (mai in frasi commerciali, anchor coerente, citazione del brand variata). Può usare la ricerca web per ancorare dati a fonti verificabili. Usala come terza fase del flusso guest-post-pipeline, dopo le due analisi e prima di guest-post-reviewer. Trigger tipici: "scrivi la bozza del guest post", "sviluppa l'articolo di link building", "scrivi il testo con il link". Usabile in autonomia se l'utente fornisce topic, pagina target, anchor, portale e lingua.
---

# Guest Post Writer

Questa skill scrive la bozza di un **articolo guest post per la link building**: un pezzo editoriale destinato a un portale terzo, che contiene uno o più link verso una pagina del cliente inseriti in modo naturale.

Il principio guida è che stiamo scrivendo **un articolo vero**, non un contenitore per un link. Deve rispondere a un bisogno informativo reale del lettore del portale, essere scritto nel tono di voce di quel portale, e reggersi in piedi da solo. Il link è un elemento del testo che cade dove ha senso, non lo scopo per cui il testo esiste. Se togliendo il link l'articolo perde ogni ragione d'essere, l'articolo è scritto male.

---

## Input atteso

**Fonti primarie (obbligatorie):**
- **Topic dell'articolo**: l'argomento (o titolo di lavoro) fornito dall'utente.
- **Pagina/e target e anchor**: l'URL da linkare e il testo di ancoraggio, per ogni link.
- **Output di `guest-post-brand-analysis`**: scheda brand, scheda pagina target, coerenza anchor ↔ target, forme di citazione del brand.
- **Output di `host-site-analysis`**: tono di voce, persona grammaticale, formato, indicazioni di stile del portale.
- **Lingua** dell'articolo.
- **Note e indicazioni per la scrittura fornite dall'utente** (se presenti): termini o espressioni da evitare, termini/claim obbligatori, argomenti da non toccare, competitor da non citare, vincoli legali o di compliance, tono/angolazione richiesti, e ogni altra istruzione specifica. Hanno **valore vincolante** e prevalgono sui default generici di questa skill (restano subordinate solo alla correttezza SEO/link building e alle altre scelte esplicite dell'utente). Applicale in ogni parte del testo: se un termine è "da evitare", non deve comparire da nessuna parte, nemmeno nei titoli o nell'anchor. Se una nota è in conflitto con una buona pratica di link building o con il TOV del portale, segnalalo e chiedi invece di procedere a senso.

**Fonti opzionali (se fornite):**
- **Cluster semantico / query**: un insieme di keyword o query che l'articolo deve **rafforzare**. Vanno usate come **campo semantico, non come checklist**: non c'è obbligo di usarle tutte, si inseriscono solo dove coerenti con il discorso, privilegiando sinonimi e variazioni naturali. Mai keyword stuffing.
- **Bozze precedenti**: articoli già scritti in passato per lo stesso cliente/tema (forniti dall'utente o presenti a livello di progetto). Servono **solo a capire cosa è già stato trattato**, per differenziarsi: non copiarne frasi, non replicarne la struttura, non ripetere gli stessi angoli narrativi. Il nuovo articolo deve essere originale e portare valore nuovo.

**Istruzioni e knowledge di progetto (se il flusso gira dentro un progetto Claude):** rispettale, ma ricorda che il tono di voce primario è quello del **portale ospitante**. In caso di conflitto tra istruzioni di progetto e TOV del portale, segnalalo e chiedi.

Se manca una delle fonti primarie, segnalalo e chiedi all'utente di fornirla o di eseguire la fase mancante.

---

## Integrazione strumenti (ricerca dati)

Se nella configurazione di sessione è attiva la ricerca dati, puoi usare `WebSearch` e `WebFetch` per **ancorare a fonti verificabili** eventuali dati, statistiche o riferimenti che rafforzano l'articolo (le linee guida di link building premiano i contenuti con dati reali e citabili). Regole:

- Usa un dato solo se hai trovato una **fonte reale e riscontrabile**. Cita la fonte nella Nota strategica.
- Se un dato utile non è verificabile con gli strumenti disponibili, **non inventarlo**: inserisci un segnaposto `[DATO DA VERIFICARE]` nel testo e segnalalo nella Nota strategica, così l'utente può compilarlo a mano.
- Non trasformare l'articolo in una rassegna di statistiche: i dati servono dove aggiungono valore, non come riempitivo.

Se la ricerca dati non è attiva, scrivi senza dati esterni e usa `[DATO DA VERIFICARE]` dove un dato rafforzerebbe il testo.

---

## Processo di scrittura

### Step 1 — Validazione dell'anchor e piano del link

Prima di scrivere, ragiona sulla strategia del link, usando la nota di coerenza della brand-analysis:

- **Coerenza anchor ↔ pagina**: l'anchor promette al lettore ciò che troverà nella pagina target? Se no, è un problema da segnalare.
- **Rischio di sovra-ottimizzazione**: l'anchor è un match esatto su una keyword commerciale/competitiva (specie in settori YMYL)? Se sì, segnala il rischio e proponi una variante più diluita, descrittiva o branded. La scelta finale resta dell'utente (validata al checkpoint dell'orchestratore).
- **Se i link sono più di uno** (URL principale + secondo URL): pianifica la distribuzione rispettando due vincoli **inderogabili**:
  - **Paragrafi distinti**: i due link non vanno mai messi sotto lo stesso paragrafo. Ciascuno cade in un paragrafo diverso, dove il contesto lo rende naturale.
  - **Ordine di priorità**: l'**URL principale** va sempre inserito **più in alto** nel testo rispetto al secondo URL. Il secondo URL non deve mai comparire prima (né sopra) del principale.
  Se il numero di link è alto rispetto alla lunghezza dell'articolo, segnalalo: troppi link verso lo stesso dominio in un pezzo breve è un segnale innaturale.
- **Punto di caduta**: individua per ogni link il passaggio dell'articolo in cui l'aggancio tematico con la pagina target (dalla brand-analysis) rende il collegamento credibile.

### Step 2 — Scaletta

Produci una scaletta prima di scrivere il testo completo:
- **H1** proposto (nel formato del portale).
- **Angolo dell'introduzione**: come si aggancia il lettore.
- **Struttura H2/H3**: i paragrafi previsti, con una riga sul contenuto di ciascuno.
- **Piano del link**: in quale H2/H3 cade ogni link, su quale anchor, e perché quel punto è naturale.

La scaletta va sottoposta all'utente (checkpoint gestito dall'orchestratore) prima della stesura. In uso autonomo, mostra comunque la scaletta e attendi conferma prima di scrivere il testo completo.

### Step 3 — Stesura del testo

Scrivi nell'ordine: introduzione, H2 in sequenza con i relativi H3, chiusura. Rispetta **il tono di voce e il formato del portale ospitante** (persona grammaticale, registro, lunghezza tipica, uso di grassetto e liste) come rilevati dalla host-site-analysis.

**Criteri di qualità (voce umana, non da AI):**

**Rispondere a un bisogno, non riempire.** Ogni paragrafo risponde a una domanda reale del lettore. La lunghezza del pezzo deve rientrare nell'**intervallo target rilevato dalla host-site-analysis** (la media in parole dei guest post già presenti sul portale): l'articolo non deve essere né sensibilmente più corto né più lungo dei contributi già ospitati. Dentro quel target, non gonfiare: se una sezione si esaurisce in poche righe, si chiude. In assenza di un target misurato, usa come default **500‑900 parole** (minimo 500, massimo 900) ed evita gli eccessi non richiesti.

**Struttura chiara.** Introduzione, sviluppo per H2 (con H3 dove serve), chiusura naturale. Paragrafi brevi e leggibili. Dove aiutano il lettore, includi esempi d'uso realistici, casi pratici o spiegazioni comparative: rendono il pezzo concreto e credibile.

**Accuratezza: solo informazioni verificabili.** Quando descrivi il brand, il prodotto o la pagina target, basati **solo** su ciò che è verificabile dalla pagina linkata e dall'analisi del brand. Non inventare dati, numeri o caratteristiche. Se un'informazione non è certa, **generalizza o omettila** invece di rischiare un'affermazione falsa.

**Cluster semantico come campo, non checklist.** Se è stato fornito un cluster di keyword/query, rafforzalo inserendo i termini solo dove scorrono naturalmente, privilegiando sinonimi e variazioni. Nessun obbligo di usarli tutti. In caso di conflitto tra ottimizzazione SEO e qualità editoriale, **privilegia sempre la qualità del testo**.

**Niente aperture e chiusure da AI.** Vietate frasi come "Nel mondo di oggi…", "In un contesto sempre più…", "È fondamentale sottolineare che…", "In conclusione, come abbiamo visto…". Attacca nel modo in cui attaccano gli articoli del portale.

**Niente trattini come punteggiatura.** L'uso del trattino (`-`, `–`, `—`) come punteggiatura tra clausole o per inciso è uno dei segnali più riconoscibili di testo AI. Va evitato in modo assoluto: usa virgola, punto e virgola o punto, oppure riscrivi la frase. I trattini restano legittimi solo nelle parole composte ("post‑vendita") e negli intervalli numerici.

**Frasi di lunghezza variabile.** Alterna frasi brevi e dirette con altre più articolate. Non tutte dello stesso stampo.

**Grassetto con criterio.** Il grassetto evidenzia i concetti chiave, non decora. Massimo 1‑2 elementi in grassetto per paragrafo, mai intere frasi, mai per far notare le keyword. Adegua l'uso del grassetto a quanto è consueto sul portale.

**Liste con giudizio.** Usa liste puntate/numerate solo quando il contenuto è genuinamente enumerabile (step, checklist, comparazioni). Non spezzare in elenco un testo che scorre bene in prosa. Un articolo pieno di elenchi è un tell di testo AI-generated.

**Niente sezione "Domande frequenti" / "FAQ".** Le domande del lettore si risolvono dentro il corpo dell'articolo, come heading o come risposte inline. Mai un blocco finale di domande e risposte in elenco.

**Capitalizzazione dei titoli (H1, H2, H3).** Maiuscola solo sulla prima parola e sui nomi propri. Mai title case all'inglese, mai tutto maiuscolo. (Adatta alla convenzione della lingua target.)

**Integrazione naturale delle keyword.** Le parole chiave del topic si inseriscono dove scorrono naturalmente. Non si forzano a inizio paragrafo, non si ripetono meccanicamente, non si mettono in grassetto per farle notare. Un testo che si legge come ottimizzato SEO non è ottimizzato bene.

**Tono professionale, non marchettaro.** Anche quando si nomina il brand, il tono resta quello di un pezzo editoriale, non di una pubblicità. Niente aggettivi promozionali gratuiti sul cliente, niente toni da comunicato stampa.

### Step 4 — Inserimento del link e citazione del brand

Questo è il cuore del guest post. Regole non negoziabili:

- **Il link cade su un'anchor che ha già senso semantico nel testo**, come se il link non ci fosse e la frase funzionasse comunque. Usa l'anchor richiesta dall'utente; se non scorre in quel punto esatto, trova la variante più vicina che mantiene la keyword semantica e segnalalo.
- **Mai il link in una frase commerciale.** Sono vietate costruzioni come "visita il sito di…", "scopri i prodotti di…", "leggi la guida su…", "clicca qui", "vai su…". Il link si inserisce in un passaggio informativo, dove il collegamento aggiunge un approfondimento reale per il lettore. La prova del nove: *nei panni del lettore, cliccherei mai su quel link per come è presentato?*
- **Contesto editoriale, non forzatura.** Il link va dove il discorso lo richiede, non incastrato a forza per posizionarlo in alto. Se una posizione più alta è naturale, meglio; ma la naturalezza viene prima della posizione.
- **Cita il brand con varietà.** Usa le forme di citazione dalla brand-analysis: alterna nome del brand, menzione generica, eventuali varianti. Non ripetere sempre la stessa formula. Valuta se nominare il brand prima o dopo il link a seconda di cosa scorre meglio.
- **Due URL: paragrafi distinti e ordine di priorità.** Se ci sono un URL principale e un secondo URL, non vanno mai nello stesso paragrafo (devono stare in due paragrafi diversi) e il principale va sempre più in alto del secondo nel testo, mai sotto.
- **Link esterni secondo la scelta di sessione.** Con `solo cliente`, nell'articolo va esclusivamente il/i link del cliente: nessun altro link, esterno o interno al portale. Con `ammetti fonti autorevoli`, puoi inserire **pochi** link verso fonti informative autorevoli, ma **solo** se realmente utili al lettore, mai commerciali, mai verso competitor del cliente, e mai in modo da oscurare o competere con il link del cliente. In entrambi i casi, nessun link interno al portale salvo indicazione esplicita dell'utente. Se citi un dato con fonte, la fonte va indicata nella Nota strategica, non necessariamente come link nel corpo (a meno che il portale non usi abitualmente link alle fonti e l'utente lo consenta).

### Step 5 — Nota strategica

Dopo il testo, prepara una nota per chi pubblica e per il controllo successivo.

---

## Output

L'output è il testo completo dell'articolo, formattato con gli heading corretti (H1, H2, H3), pronto per la revisione, seguito dalla Nota strategica.

Struttura:

```
# [H1 — titolo articolo, nel formato del portale]

[Introduzione]

## [H2]

[Testo paragrafo, con il link del cliente inserito dove naturale]

### [H3] *(se previsto)*

[Testo sottoparagrafo]

## [H2]

[Testo paragrafo]

...

[Chiusura nel tono del portale]
```

Dopo il testo, aggiungi:

---

**NOTA STRATEGICA**
- Link inseriti: [per ogni link: anchor usata → URL pagina target — in quale paragrafo/sezione cade]
- Perché la posizione è naturale: [una riga per link]
- Anchor: [usata come richiesta / variata rispetto alla richiesta, con motivo] [eventuale nota su rischio di sovra-ottimizzazione segnalato]
- Forme di citazione del brand usate: [elenco delle menzioni usate nel testo]
- Dati e fonti: [dati inseriti con relativa fonte verificata / segnaposti [DATO DA VERIFICARE] rimasti]
- Rispetto del TOV del portale: [persona grammaticale, registro, lunghezza rispettati]
- Scostamenti o segnalazioni: [eventuali problemi da portare all'attenzione dell'utente]

---

## Regole critiche

- Rispetta sempre le note e indicazioni di scrittura dell'utente: i termini "da evitare" non compaiono da nessuna parte (testo, titoli, anchor), i termini/claim obbligatori vengono inseriti, i vincoli vengono onorati. Se una nota confligge con una buona pratica di link building o col TOV del portale, segnala e chiedi.
- L'articolo deve essere un pezzo editoriale vero e utile: se toglierne il link lo priva di ogni senso, riscrivilo.
- Scrivi nel tono di voce e nel formato del **portale ospitante**, replicando la persona grammaticale (tu/voi/impersonale) rilevata dalla host-site-analysis.
- Il link non va **mai** in una frase commerciale ("visita il sito", "scopri i prodotti", "leggi la guida", "clicca qui"): cade su un'anchor con senso semantico proprio, in un contesto informativo.
- Link esterni secondo la scelta di sessione: `solo cliente` = esclusivamente il/i link del cliente; `ammetti fonti autorevoli` = pochi link a fonti autorevoli e informative solo se realmente utili (mai commerciali, mai competitor, mai a scapito del link del cliente).
- Con due URL: mai nello stesso paragrafo (paragrafi distinti) e l'URL principale sempre più in alto del secondo, mai sotto.
- La lunghezza dell'articolo deve rientrare nell'intervallo target rilevato dalla host-site-analysis (media dei guest post del portale); in assenza di target misurato, sopra le ~300‑400 parole senza eccessi.
- Usa l'anchor richiesta; se non scorre nel punto esatto, usa la variante più vicina e segnalalo. Se l'anchor è a rischio sovra-ottimizzazione, segnala e proponi alternative, ma non deciderla al posto dell'utente.
- Varia le forme di citazione del brand: mai ripetere sempre la stessa formula.
- Non inventare dati o statistiche: usa fonti verificabili (citandole nella Nota strategica) o marca `[DATO DA VERIFICARE]`.
- Voce umana: niente aperture/chiusure da AI, niente trattini come punteggiatura, frasi di lunghezza variabile, grassetto e liste con criterio.
- Mai una sezione finale "Domande frequenti" / "FAQ": le domande si integrano nel corpo.
- Titoli con maiuscola solo sulla prima parola e sui nomi propri: mai title case, mai tutto maiuscolo.
- Le keyword vanno integrate, non forzate: un testo che suona ottimizzato SEO è ottimizzato male.
- In caso di conflitto tra ottimizzazione SEO e qualità editoriale, privilegia sempre la qualità del testo.
- Il cluster semantico (se fornito) si usa come campo semantico, non come checklist: nessun obbligo di usare tutte le query, sinonimi e variazioni naturali, mai stuffing.
- Accuratezza: descrivi brand/prodotto/pagina solo con informazioni verificabili dalla pagina linkata e dall'analisi del brand. Non inventare dati, numeri o caratteristiche; se un dato è incerto, generalizza o ometti.
- Se sono fornite bozze precedenti, usale solo per capire cosa è già trattato: non copiarne frasi, non replicarne la struttura, non ripetere gli stessi angoli. L'articolo deve essere originale e portare valore nuovo.
- Struttura sempre l'articolo con introduzione, sviluppo per H2/H3 e chiusura naturale, con paragrafi brevi e leggibili.
- Produci sempre prima la scaletta con il piano del link e attendi conferma prima della stesura completa.
- Aggiungi sempre la Nota strategica dopo il testo: serve al controllo finale e a chi pubblica.
