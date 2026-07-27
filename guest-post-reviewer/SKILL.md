---
name: guest-post-reviewer
description: >
  Controllo finale di un articolo guest post per la link building prima della consegna. Verifica che l'articolo sia scritto bene e sia un pezzo editoriale vero (non una marchetta), che la SEO non sia forzata (keyword non stuffate, nessuna sovra-ottimizzazione), che il link del cliente sia inserito in modo naturale su un'anchor coerente e MAI in frasi commerciali ("visita il sito…", "scopri i prodotti…", "leggi la guida…"), che rispetti il tono di voce del portale e la voce umana (niente trattini come punteggiatura, niente aperture da AI, niente FAQ finale, titoli capitalizzati bene) e che i dati siano verificabili o marcati. Usala come ultima fase del flusso guest-post-pipeline, dopo guest-post-writer. Trigger tipici: "controlla il guest post", "verifica che il link sia inserito bene", "l'articolo di link building è pronto?", "il link è naturale?". NON riscrive il testo: segnala i problemi e restituisce un verdetto con gli interventi; le correzioni le applica guest-post-writer.
---

# Guest Post Reviewer

Questa skill è il **controllo finale** del guest post. Non riscrive il testo: lo verifica rispetto ai criteri che rendono un articolo di link building efficace e sicuro, e restituisce un verdetto (pronto / da correggere) con una lista puntuale di interventi.

Il metro di giudizio è duplice: l'articolo deve essere **un buon pezzo editoriale** (utile, credibile, nel tono del portale) e **un buon veicolo di link** (link naturale, non commerciale, coerente, non forzato). Un articolo può essere ben scritto ma avere un link piazzato male, o avere un link perfetto ma essere una marchetta: entrambi i casi vanno segnalati.

---

## Input atteso

- **Bozza dell'articolo** (output di `guest-post-writer`), compresa la Nota strategica.
- **Output di `host-site-analysis`**: per verificare che il testo rispetti il tono di voce e il formato del portale.
- **Output di `guest-post-brand-analysis`**: per verificare la coerenza anchor ↔ pagina target e le forme di citazione del brand.
- **Pagina/e target e anchor** richieste dall'utente.
- **Note e indicazioni per la scrittura fornite dall'utente** (se presenti): termini da evitare, termini/claim obbligatori, argomenti da non toccare, competitor da non citare, vincoli legali o di compliance, tono/angolazione richiesti.

Se manca l'analisi del portale, la verifica del tono di voce sarà limitata: segnalalo. Se manca l'analisi del brand, il controllo di coerenza anchor ↔ target va fatto sulla base della pagina target fornita dall'utente.

---

## Processo di controllo

Scorri i sei blocchi in ordine. Per ciascun punto segna l'esito (OK / da correggere) e, se da correggere, l'intervento preciso.

### Step 1 — Qualità editoriale

- **È un articolo vero?** Risponde a un bisogno informativo reale del lettore del portale, o esiste solo per ospitare il link? Prova del nove: togliendo il link, l'articolo avrebbe ancora senso di esistere?
- **Non è una marchetta?** Il brand è trattato con misura, senza aggettivi promozionali gratuiti, senza toni da comunicato stampa. L'articolo non è auto-referenziale.
- **Scorre?** Il testo è leggibile, con frasi di lunghezza variabile, senza riempitivi né frasi vuote che suonano autorevoli ma non dicono nulla.
- **Rispetta il TOV del portale?** Registro, persona grammaticale (tu/voi/impersonale), tono, lessico e formato coincidono con quanto rilevato dalla host-site-analysis. Un pezzo che stona con il portale è un fail.
- **Lunghezza in linea col portale?** Il conteggio parole dell'articolo rientra nell'**intervallo target** rilevato dalla host-site-analysis (media dei guest post già presenti). Se l'articolo è sensibilmente più corto o più lungo, segnalalo come intervento (indica il conteggio attuale e il target).

### Step 2 — SEO non forzata

- **Keyword integrate, non stuffate.** Le parole chiave del topic scorrono naturalmente, non sono ripetute meccanicamente né ammassate a inizio paragrafo né evidenziate in grassetto per farsi notare.
- **Nessuna sovra-ottimizzazione.** Titoli non keyword-stuffed; densità delle keyword naturale; l'anchor non è un match esatto ripetuto e forzato (attenzione ai settori YMYL).
- **Grassetto e liste con criterio.** Il grassetto evidenzia concetti chiave, non decora né serve a marcare keyword. Le liste ci sono solo dove il contenuto è enumerabile.

### Step 3 — Naturalezza e correttezza del link (blocco critico)

- **Nessuna frase commerciale.** Il link **non** cade in costruzioni tipo "visita il sito…", "scopri i prodotti di…", "leggi la guida su…", "clicca qui", "vai su…". Se ne trovi anche una sola, è un **fail bloccante**: indica la frase e proponi come reinserire il link in un passaggio informativo.
- **Anchor con senso semantico.** L'anchor ha senso nel testo anche ignorando il link; la frase funziona come se il link non ci fosse.
- **Coerenza anchor ↔ pagina target.** L'anchor promette ciò che la pagina mantiene: chi clicca trova quel tipo di risorsa.
- **Posizione naturale.** Il link cade dove il discorso lo richiede, non forzato per stare in alto. Se i link sono più d'uno, verifica che la densità rispetto alla lunghezza non sia eccessiva.
- **Due URL: paragrafi distinti e ordine (blocco critico).** Se ci sono un URL principale e un secondo URL, verifica che **non** stiano nello stesso paragrafo (devono essere in due paragrafi diversi) e che l'**URL principale sia più in alto** del secondo nel testo. Se i due link sono nello stesso paragrafo, o se il secondo URL compare prima/sopra del principale, è un **fail bloccante**: indica la posizione e come correggere.
- **Citazione del brand variata.** Il brand non è nominato sempre con la stessa formula; le menzioni alternano nome, forme e menzioni generiche (dalla brand-analysis).
- **Solo i link del cliente.** Nel testo non ci sono link diversi da quelli richiesti dall'utente (salvo indicazione esplicita).

### Step 4 — Voce umana (de‑AI)

- **Niente trattini come punteggiatura** (`-`, `–`, `—`) tra clausole o per inciso. È il tell principale del testo AI. Se presenti, vanno sostituiti.
- **Niente aperture/chiusure da AI**: "Nel mondo di oggi…", "In un contesto sempre più…", "È fondamentale sottolineare…", "In conclusione, come abbiamo visto…".
- **Niente sezione "Domande frequenti" / "FAQ"** in fondo: le domande vanno integrate nel corpo.
- **Titoli capitalizzati correttamente**: maiuscola solo sulla prima parola e sui nomi propri, mai title case, mai tutto maiuscolo.
- **Niente ritmo robotico**: paragrafi tutti della stessa lunghezza, ripetizioni degli stessi termini, elenchi ovunque.

### Step 5 — Affidabilità dei dati

- **Dati verificabili.** Ogni dato/statistica citato ha una fonte reale (indicata nella Nota strategica) oppure è marcato `[DATO DA VERIFICARE]`.
- **Nessun dato inventato.** Se trovi un dato preciso senza fonte e non marcato, è un **fail bloccante**: va verificato o marcato.

### Step 6 — Rispetto delle note dell'utente

Se l'utente ha fornito note e indicazioni per la scrittura, verifica che siano state rispettate:
- **Termini/espressioni da evitare**: non compaiono da nessuna parte, nemmeno nei titoli o nell'anchor. La presenza di un termine vietato è un **fail bloccante**.
- **Termini/claim obbligatori**: sono effettivamente presenti dove richiesto.
- **Argomenti da non toccare / competitor da non citare**: rispettati.
- **Vincoli legali o di compliance, tono/angolazione richiesti**: rispettati.

Se non sono state fornite note, salta questo blocco e segnalo come non applicabile.

---

## Output

---

**CONTROLLO GUEST POST — [titolo articolo]**

**ESITO PER CRITERIO**

| Blocco | Esito | Note / interventi |
|---|---|---|
| Qualità editoriale | [OK / da correggere] | [se da correggere: cosa e dove] |
| SEO non forzata | [OK / da correggere] | [...] |
| Naturalezza del link | [OK / da correggere] | [...] |
| Voce umana (de‑AI) | [OK / da correggere] | [...] |
| Affidabilità dati | [OK / da correggere] | [...] |
| Rispetto note utente | [OK / da correggere / non applicabile] | [...] |

**FAIL BLOCCANTI** *(solo se presenti)*
- [Elenco dei problemi che impediscono la consegna: link in frase commerciale, SEO forzata, dato inventato, articolo-marchetta, TOV del portale non rispettato, due URL nello stesso paragrafo o secondo URL sopra il principale, termine "da evitare" presente o altra nota vincolante dell'utente violata. Per ciascuno: la frase/punto esatto e l'intervento richiesto.]

**INTERVENTI CONSIGLIATI** *(migliorie non bloccanti)*
- [Elenco puntuale di correzioni che alzerebbero la qualità senza essere indispensabili.]

**VERDETTO: [PRONTO PER LA CONSEGNA / DA CORREGGERE]**
[Una riga di sintesi. Se "da correggere", indica quali interventi vanno fatti prima di ripresentare l'articolo.]

---

## Regole critiche

- Questa skill valuta e segnala, non riscrive: le correzioni le applica `guest-post-writer`. Indica sempre l'intervento preciso, non un giudizio generico.
- Il link in una frase commerciale è un **fail bloccante**, sempre: "visita il sito", "scopri i prodotti", "leggi la guida", "clicca qui" e simili non sono ammessi.
- Anche la SEO forzata (keyword stuffing, sovra-ottimizzazione dell'anchor) e i dati inventati sono fail bloccanti: un articolo con un fail bloccante non è pronto.
- Le note vincolanti dell'utente vanno verificate: un termine "da evitare" presente nel testo (o altra istruzione vincolante violata) è un fail bloccante.
- Con due URL, il posizionamento è vincolante: mai nello stesso paragrafo e URL principale sempre più in alto del secondo. La violazione è un fail bloccante.
- La lunghezza va confrontata con l'intervallo target del portale (media dei guest post esistenti): fuori intervallo è un intervento da segnalare.
- Il tono di voce del portale ospitante è il riferimento: un pezzo ben scritto ma che stona con il portale va segnalato.
- Distingui i fail bloccanti (impediscono la consegna) dagli interventi consigliati (migliorie): non trattarli allo stesso modo.
- Verifica la coerenza anchor ↔ pagina target usando la pagina reale, non un'ipotesi: se l'anchor promette qualcosa che la pagina non offre, è da correggere.
- Non introdurre nel testo problemi che non ci sono: se un criterio è soddisfatto, segnalo OK e passa oltre. L'obiettivo è un articolo pronto, non una lista di rilievi a tutti i costi.
