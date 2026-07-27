---
name: guest-post-pipeline
description: >
  Orchestratore del flusso completo di scrittura di un articolo guest post per la link building. Chiama in sequenza guest-post-brand-analysis (cliente e pagina/e target), host-site-analysis (portale ospitante e suo tono di voce), guest-post-writer (stesura con link naturale) e guest-post-reviewer (controllo finale). Parte da domande obbligatorie iniziali: pagina/e target, anchor, sito ospitante, lingua, topic, formato di output e note di scrittura (es. termini da evitare). Usa questa skill quando l'utente vuole scrivere un guest post / articolo di link building da pubblicare su un sito terzo, con un link verso una pagina del cliente. Trigger tipici: "scrivi un guest post", "scrivimi un articolo di link building", "pubblicare un articolo con un link su un altro sito", "avvia il flusso guest-post-pipeline". NON è per articoli blog sul sito del cliente (per quelli usa seo-blog-pipeline): qui l'articolo è ospitato da un portale terzo e l'obiettivo è un link naturale in un pezzo editoriale credibile.
---

# Guest Post Pipeline

Questa skill orchestra il flusso completo di produzione di un **articolo guest post per la link building**: un contenuto editoriale che verrà pubblicato su un **sito terzo** (il portale ospitante) e che contiene uno o più link verso una pagina del cliente, inseriti in modo naturale.

La filosofia di fondo, derivata dalle migliori pratiche di link building, è una sola: **non stiamo piazzando un link, stiamo scrivendo un articolo vero**. Un pezzo che porta valore al lettore del portale ospitante, scritto nel tono di voce di quel portale, e che si potrebbe posizionare da solo. Il link è una conseguenza naturale del contenuto, non il suo unico scopo. Un articolo che non meriterebbe di esistere senza il link non è un buon guest post.

Chiama le sotto-skill in sequenza, passando l'output di ciascuna come input della successiva.

---

## Istruzioni di progetto (da verificare SEMPRE all'inizio)

Se il flusso viene eseguito all'interno di un progetto Claude, prima di partire controlla se il progetto contiene **istruzioni custom** e/o **knowledge di progetto** (brand book del cliente, linee guida editoriali, tone of voice, glossari, termini da usare o evitare, vincoli legali, requisiti di formato).

Se presenti, considerale parte integrante dei requisiti:

- Le istruzioni di progetto hanno **precedenza sui default generici** di queste skill.
- Restano subordinate a: (a) le scelte esplicite fatte dall'utente nella configurazione di questa sessione, e (b) il tono di voce del **portale ospitante**, che nel guest post è il riferimento primario per come si scrive (l'articolo deve sembrare nativo del portale, non del cliente).
- Se un'istruzione di progetto è in conflitto con il TOV del portale ospitante o con una buona pratica di link building, segnala il conflitto all'utente e chiedi come procedere.

Se non sei in un progetto o non ci sono istruzioni/knowledge, prosegui con i default delle skill.

---

## Configurazione di sessione (da chiedere SEMPRE all'inizio)

Prima di avviare la Fase 1, raccogli queste informazioni in un'unica richiesta concisa. Le prime quattro sono le domande obbligatorie del flusso; le ultime due completano la configurazione.

1. **Pagina/e target da linkare**: qual è l'URL della pagina principale del cliente verso cui deve puntare il link? **Chiedi sempre anche se c'è un secondo URL da inserire o se basta quello principale.** Se c'è un secondo URL, fatti indicare **URL e anchor** anche per quello. Distingui chiaramente **URL principale** e **secondo URL**: serviranno alla regola di posizionamento in scrittura (vedi Fase 3).
2. **Anchor text da utilizzare**: qual è il testo di ancoraggio richiesto per il link principale? Se c'è un secondo URL, associa a ciascun URL la propria anchor.
3. **Sito ospitante**: qual è l'URL del portale su cui verrà pubblicato l'articolo?
4. **Lingua**: in che lingua va scritto l'articolo? (L'articolo va scritto nativamente in quella lingua, non tradotto.)
5. **Topic dell'articolo**: qual è l'argomento (o il titolo di lavoro) dell'articolo? Lo fornisce l'utente.
6. **Formato dell'output** (da chiedere SEMPRE, non assumere mai): in che formato va consegnato l'articolo finale? Proponi `markdown` (consigliato per import su CMS), `HTML` (per editor visuale), `testo plain`, `documento Word (.docx)` o altro formato indicato dall'utente. Non consegnare mai il deliverable senza aver confermato il formato.
7. **Note e indicazioni per la scrittura** (da chiedere SEMPRE): ci sono note, indicazioni, vincoli o cose a cui stare attenti nella scrittura? In particolare: termini o espressioni da evitare, termini o claim da usare (o obbligatori), argomenti da non toccare, tono o angolazione preferiti, vincoli legali o di compliance, nomi di competitor da non citare, refusi ricorrenti da evitare, e qualsiasi altra istruzione specifica del cliente o del portale. È una domanda sempre presente: se l'utente non ha nulla da segnalare, accetta "nessuna nota" e prosegui. Riporta queste note per intero alle fasi di scrittura (Fase 3) e controllo (Fase 4): hanno valore vincolante e, dove sono in conflitto con un default generico delle skill, prevalgono (restano subordinate solo alla correttezza SEO/link building e alle scelte esplicite dell'utente). Se una nota è in conflitto con una buona pratica di link building o con il TOV del portale, segnala il conflitto e chiedi.

Domanda opzionale sulla modalità:
- **Modalità di esecuzione**: `interattiva` (default, mostra un mini‑riepilogo dopo ogni fase e chiede conferma) o `autonoma` (procede senza conferme intermedie, salvo i checkpoint obbligatori descritti sotto).

Se manca uno degli elementi 1–7, chiedilo prima di procedere (la domanda 7 va sempre posta, ma la sua risposta può essere "nessuna nota"). Non avviare il flusso con informazioni incomplete. In particolare, non inventare mai la pagina target, l'anchor o il portale.

Memorizza le scelte e applicale per tutta la sessione. Non ripetere le domande alle fasi successive.

---

## Flusso di esecuzione

Esegui le skill in questo ordine. Ogni fase riceve come contesto l'output di tutte le fasi precedenti.

### Fase 1 — BRAND ANALYSIS
*Skill: `guest-post-brand-analysis`*

Analizza il sito del cliente e la/e pagina/e target da linkare. Produce:
- Scheda brand: settore, cosa fa il cliente, prodotti/servizi, valori, elemento distintivo (il "perché" del brand), pubblico
- Scheda pagina/e target: cosa offre esattamente la pagina, contenuto, a chi si rivolge (serve a contestualizzare il link)
- Forme di citazione del brand (nome, varianti) da alternare nel testo
- Nota di coerenza anchor ↔ pagina target: l'anchor promette al lettore ciò che troverà nella pagina?

### Fase 2 — HOST SITE ANALYSIS
*Skill: `host-site-analysis`*

Analizza il portale ospitante per capire come si scrive per quel sito. Produce:
- Scheda portale: di cosa parla, verticale o generalista, pubblico, localizzazione
- Scheda tono di voce: registro, persona grammaticale (tu/voi/impersonale), tono, lessico
- Scheda formato: **lunghezza target** (media in parole dei guest post già presenti sul portale, con intervallo di riferimento), struttura degli heading, uso di grassetto/liste, tipo di articolo prevalente (news, guida, approfondimento, listicle)
- Indicazioni di stile che lo scrittore dovrà rispettare per rendere l'articolo nativo del portale

**Checkpoint di coerenza (obbligatorio):** con gli output delle Fasi 1 e 2, verifica che il **topic fornito dall'utente** sia coerente sia con la pagina/anchor target sia con la linea editoriale del portale. Se il topic è fuori tema (rispetto al cliente o rispetto al portale), o se l'anchor richiesta presenta un rischio di sovra-ottimizzazione (match esatto su keyword competitiva, specie in settori YMYL), **non procedere in silenzio**: segnala il problema all'utente, spiega il rischio e proponi un aggiustamento (topic riformulato o anchor più diluita/branded). Attendi la sua decisione. L'utente ha sempre l'ultima parola, ma deve decidere informato.

### Fase 3 — GUEST POST WRITER
*Skill: `guest-post-writer`*

Scrive la bozza dell'articolo. Si articola in due momenti con un checkpoint in mezzo:

**3a — Scaletta e piano del link.** La skill produce prima una scaletta: H1, angolo dell'introduzione, struttura H2/H3, e il **piano di inserimento del link** (in quale punto cade ogni link, su quale anchor, perché quel punto è naturale). Validazione dell'anchor inclusa.

**Checkpoint (obbligatorio):** mostra la scaletta e il piano del link all'utente e chiedi conferma esplicita prima di scrivere il testo completo. È l'ultimo momento per correggere struttura o strategia del link.

**3b — Stesura.** Approvata la scaletta, la skill scrive il testo completo: H1, introduzione, paragrafi H2/H3, grassetto con criterio, e inserimento del/i link in modo naturale seguendo le linee guida di link building. La lunghezza dell'articolo rispetta l'intervallo target rilevato dalla host-site-analysis (media dei guest post del portale). **Se ci sono due URL**, non vanno mai nello stesso paragrafo (paragrafi distinti) e l'URL principale va sempre più in alto del secondo, mai sotto. Se attivata la ricerca dati, ancora le statistiche a fonti verificabili. Produce anche una "Nota strategica" per chi pubblica.

### Fase 4 — GUEST POST REVIEWER
*Skill: `guest-post-reviewer`*

Controllo finale della bozza. Verifica:
- Qualità editoriale: è un articolo vero e utile, non una marchetta, scorrevole, coerente col TOV del portale
- SEO non forzata: keyword integrate e non stuffate, nessuna sovra-ottimizzazione
- Naturalezza del link: cade su un'anchor semanticamente sensata, nel contesto giusto, **mai** in frasi commerciali ("visita il sito…", "scopri i prodotti di…", "leggi la guida su…"); coerenza anchor ↔ pagina target
- Posizionamento con due URL: i due link non stanno nello stesso paragrafo (paragrafi distinti) e l'URL principale è più in alto del secondo
- Lunghezza: l'articolo rientra nell'intervallo target rilevato dalla host-site-analysis (media dei guest post del portale)
- Voce umana (de‑AI): niente trattini come punteggiatura, niente aperture da AI, niente sezione FAQ finale, titoli con capitalizzazione corretta
- Affidabilità dei dati: statistiche con fonte o marcate `[DATO DA VERIFICARE]`, nessun dato inventato
- Rispetto delle note dell'utente (termini da evitare assenti, vincoli onorati)

Produce un verdetto (pronto / da correggere) con lista puntuale di interventi.

**Loop di correzione:** se il reviewer segnala problemi, applica le correzioni (tornando a `guest-post-writer` per le riscritture puntuali) e rifai il controllo sui punti corretti. Non consegnare un articolo con un fail bloccante (link commerciale, SEO forzata, dato inventato) irrisolto.

---

## Gestione dei checkpoint

Il flusso prevede **due checkpoint obbligatori**, attivi sia in modalità interattiva sia autonoma:

1. **Dopo la Fase 2** (check di coerenza): se il topic è fuori tema o l'anchor è rischiosa, ferma e chiedi.
2. **Dentro la Fase 3** (dopo la scaletta, prima della stesura): mostra scaletta e piano del link e chiedi conferma esplicita.

**Mini‑checkpoint (solo in modalità interattiva):** dopo le Fasi 1, 2 e 4 mostra un mini‑riepilogo di 3‑5 bullet e chiedi se procedere. In modalità autonoma questi sono omessi.

---

## Modalità di esecuzione parziale

Il flusso può partire da uno stato avanzato se l'utente fornisce output già pronti:

- Se l'utente fornisce già un'analisi completa del brand e della pagina target, salta la Fase 1.
- Se fornisce già un'analisi del portale ospitante (TOV, formato), salta la Fase 2.
- Se fornisce già una bozza scritta e vuole solo il controllo, salta alle Fase 4.

**Fornire input grezzi non equivale a saltare una fase.** Dare l'URL del cliente o del portale sono input del flusso, non output di una fase: le analisi vanno comunque eseguite. Si salta una fase solo se l'utente fornisce l'**output completo** di quella fase.

---

## Output finale

L'utente riceve **un unico articolo finale** nel formato indicato (markdown, HTML, testo plain, .docx o altro), composto da:

1. **L'articolo** (H1, introduzione, H2/H3 con testo, grassetto, link del cliente inserito/i in modo naturale), scritto nel tono di voce del portale ospitante e nella lingua richiesta.
2. **Blocco "NOTA STRATEGICA"** accodato in fondo, per chi pubblica: dove cade ogni link e su quale anchor, perché la posizione è naturale, le forme di citazione del brand usate, eventuali dati inseriti con relativa fonte (o i `[DATO DA VERIFICARE]` rimasti), e l'esito del controllo finale.

Le analisi delle Fasi 1 e 2 restano nella conversazione come passaggi consultabili: non duplicarle nell'output finale.

---

## Regole critiche

- L'articolo deve essere un **pezzo editoriale vero**, utile al lettore del portale ospitante: se non meriterebbe di esistere senza il link, va ripensato.
- Il riferimento primario per **come si scrive** è il tono di voce del **portale ospitante**, non quello del cliente.
- Nell'articolo va **solo** il/i link verso la/e pagina/e target indicate dall'utente. Nessun altro link (né esterno né interno al portale) va inserito, salvo diversa indicazione esplicita dell'utente.
- Il link non va **mai** inserito in una frase commerciale ("visita il sito", "scopri i prodotti", "leggi la guida"): cade su un'anchor che ha già senso semantico nel testo.
- Non inventare mai la pagina target, l'anchor, il portale o il topic: sono input dell'utente.
- Chiedi sempre il formato dell'output all'inizio e attendi la risposta: non assumere il markdown di default.
- Il check di coerenza dopo la Fase 2 e il checkpoint sulla scaletta (Fase 3) sono obbligatori in entrambe le modalità.
- Non consegnare un articolo con un fail bloccante irrisolto (link in frase commerciale, SEO forzata, dato inventato).
- Non inventare dati o statistiche: usa fonti verificabili o marca `[DATO DA VERIFICARE]`.
- Se un sito (cliente o portale) non è leggibile con gli strumenti disponibili, non procedere a indovinare: chiedi all'utente di incollare i contenuti necessari.
