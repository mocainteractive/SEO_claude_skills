---
name: seo-blog-pipeline
description: >
  Orchestratore del flusso completo di creazione di un articolo blog SEO. Chiama in sequenza le skill keyword-analysis, serp-analysis, brand-analysis-and-connections, content-brief-builder, draft-writer, seo-optimizer e content-reviewer. Usa questa skill quando l'utente vuole avviare il flusso completo di produzione di un articolo blog SEO dall'analisi keyword alla pubblicazione, MA ANCHE quando chiede solo un content brief: la produzione del brief è l'obiettivo `brief` di questo flusso e richiede comunque le fasi a monte (keyword-analysis, serp-analysis, brand-analysis-and-connections), quindi una richiesta di brief deve attivare questo orchestratore e non la sola content-brief-builder. Trigger tipici: "avvia il flusso SEO per questo topic", "crea un articolo su X per il sito Y", "procedi con il flusso seo-blog-pipeline", "voglio un articolo completo su X", "crea un content brief per X", "voglio un brief per un articolo su X", "dammi il brief editoriale per X".
---

# SEO Blog Pipeline

Questa skill orchestra il flusso completo di produzione di un articolo blog SEO. Chiama le skill atomiche in sequenza, passando l'output di ciascuna come input della successiva. Il risultato finale è un articolo pronto per la pubblicazione, validato SEO e con raccomandazioni di distribuzione multicanale.

---

## Istruzioni di progetto (da verificare SEMPRE all'inizio)

Se il flusso viene eseguito all'interno di un progetto Claude, prima di partire controlla se il progetto contiene **istruzioni custom** e/o **knowledge di progetto** (documenti caricati: linee guida editoriali, brand book, tone of voice, glossari, liste di termini da usare o evitare, vincoli legali, requisiti di formato, ecc.).

Se presenti, considerale parte integrante dei requisiti e adatta brief e articolo di conseguenza, in tutte le fasi:

- Le istruzioni di progetto hanno **precedenza sui default generici** di queste skill (es. registro, formattazione, lunghezza, struttura, vocabolario, CTA, disclaimer).
- Restano comunque subordinate a: (a) le scelte esplicite fatte dall'utente nella configurazione di sessione di questa specifica esecuzione, e (b) la correttezza SEO e i checkpoint critici del flusso.
- Se un'istruzione di progetto è in **conflitto** con una buona pratica SEO o con una scelta di sessione, non ignorarla in silenzio: segnala il conflitto all'utente e chiedi come procedere.
- Quando il TOV o le linee guida sono già definiti dalle istruzioni/knowledge di progetto, usali come fonte primaria nella Fase 3 (brand-analysis-and-connections), integrando l'analisi del sito solo per ciò che manca.

Se non sei in un progetto o non ci sono istruzioni/knowledge, prosegui normalmente con i default delle skill.

---

## Input richiesto

Prima di avviare il flusso, verifica di avere:

1. **Topic o keyword seme**: l'argomento su cui scrivere l'articolo (una parola, una frase, un tema)
2. **URL del sito**: il dominio per cui si scrive l'articolo (necessario per brand-analysis-and-connections)
3. **Lingua target**: default italiano, salvo indicazione diversa
4. **Paese target**: default Italia (it), usato per le chiamate Ahrefs
5. **Brief iniziale (opzionale)**: eventuali note del cliente, angolazione preferita, vincoli editoriali. Se fornito, revisionalo e proponi miglioramenti prima di passare alla Fase 1.

Se uno di questi elementi (1–4) manca, chiedi conferma all'utente prima di procedere. Non avviare il flusso con informazioni incomplete.

---

## Configurazione di sessione (da chiedere SEMPRE all'inizio)

Prima di partire con la Fase 1, chiedi all'utente quattro cose in un'unica domanda concisa:

1. **Obiettivo finale**: dove vuole fermarsi il flusso?
   - `brief` → il flusso si ferma dopo la Fase 4 (content brief approvato). Utile quando l'articolo verrà scritto da un copywriter umano e serve solo il brief editoriale come deliverable.
   - `articolo completo` (default) → il flusso procede fino alla Fase 7 e consegna l'articolo finale ottimizzato e validato E‑E‑A‑T.

2. **Modalità di esecuzione**:
   - `interattiva` (default): tra una fase e l'altra mostra un mini‑riepilogo (3‑5 bullet) e chiede conferma esplicita per proseguire. Adatta quando l'utente vuole supervisionare il flusso passo per passo.
   - `autonoma`: il flusso procede senza chiedere conferme intermedie, salvo i due checkpoint critici dopo la Fase 3 e dopo la Fase 4, che restano sempre obbligatori (sono i punti di non ritorno).

3. **Formato finale del deliverable**: in che formato deve essere consegnato il deliverable (brief o articolo, a seconda dell'obiettivo)? Le opzioni più comuni sono:
   - `markdown` (default, comodo per CMS che importano MD)
   - `html` (per incollare direttamente in editor visuale)
   - `testo plain` (senza alcuna formattazione)
   - `documento Word (.docx)`
   - Altro formato indicato dall'utente

4. **Ambito per l'internal linking**: come deve cercare i contenuti interni da collegare nell'articolo (usato nella Fase 3, brand-analysis-and-connections)?
   - `automatico` (default): Claude mappa l'intero sito tramite robots.txt + sitemap e seleziona i contenuti correlati più rilevanti, ovunque si trovino.
   - `cartella/sezione specifica`: l'utente indica uno o più percorsi o URL di sezione (es. `/blog/marketing/`, `/magazine/guide/`). Claude esplora in modo esaustivo quella/e sezione/i, così non perde articoli più nascosti. Utile nei siti con blog suddiviso in molte categorie, dove la scansione automatica rischia di campionare solo una parte dei contenuti. La scansione del resto del sito per le pagine strategiche (prodotti/servizi/casi studio) resta comunque attiva.

Memorizza le scelte e applicale per tutto il resto della sessione. Non ripetere la domanda alle fasi successive.

Se l'obiettivo è `brief`, salta le Fasi 5, 6 e 7. Al checkpoint dopo la Fase 4 consegna il brief nel formato richiesto e termina lì il flusso.

---

## Flusso di esecuzione

Esegui le skill in questo ordine preciso. Ogni skill riceve come contesto l'output di tutte le skill precedenti.

### Fase 1 — KEYWORD ANALYSIS
*Skill: `keyword-analysis`*

Analizza il topic fornito. Produce:
- Keyword primaria con volume e intent
- Set di keyword secondarie e correlate (varianti semantiche, domande, long-tail, LSI)
- Eventuale nota su stagionalità o intent ambiguo

**Checkpoint**: se l'intent risulta transazionale, avvisa l'utente e chiedi conferma prima di procedere con le fasi successive.

---

### Fase 2 — SERP ANALYSIS
*Skill: `serp-analysis`*

Prima dell'analisi competitor, esegue un **controllo di cannibalizzazione** (Step 0): verifica tramite Ahrefs se il sito del cliente è già posizionato sulla keyword primaria o sulle correlate più importanti. Per questo, passa a questa skill anche l'URL del sito (input globale del flusso). Poi analizza la SERP per la keyword primaria identificata nella Fase 1. Produce:
- Esito del controllo di cannibalizzazione (pagine del sito già posizionate sul tema, se presenti)
- Panoramica SERP con verifica intent
- Analisi dei 5-7 competitor editoriali in prima pagina
- Gap di contenuto identificati
- Domande PAA da coprire
- Formato consigliato per l'articolo

**Checkpoint cannibalizzazione**: se il sito ha già una pagina posizionata in top 50 sulla keyword primaria o su una correlata importante, ferma il flusso e chiedi all'utente se continuare con un nuovo articolo, cambiare focus o aggiornare la pagina esistente. È un punto di stop obbligatorio in entrambe le modalità.

**Checkpoint**: se la SERP è dominata da contenuti transazionali in contrasto con l'analisi keyword, avvisa l'utente e chiedi conferma prima di procedere.

---

### Fase 3 — BRAND ANALYSIS AND CONNECTIONS
*Skill: `brand-analysis-and-connections`*

Analizza il sito del cliente. Applica l'**ambito per l'internal linking** scelto nella configurazione di sessione: se l'utente ha indicato una cartella/sezione specifica, esplora quella sezione in modo esaustivo per i contenuti correlati; altrimenti procede in automatico sull'intero sito. Produce:
- Tono di voce (registro, tono narrativo, pubblico percepito, vocabolario)
- Contenuti correlati esistenti da collegare
- Pagine strategiche da linkare nell'articolo (categorie prodotto, servizi, casi studio)

**Checkpoint**: se il TOV non è rilevabile con sufficiente chiarezza dal sito, pausa il flusso, chiedi all'utente di fornire esempi di post social, poi riprendi.

---

### Fase 4 — CONTENT BRIEF BUILDER
*Skill: `content-brief-builder`*

Costruisce il brief editoriale completo integrando gli output delle Fasi 1, 2 e 3. Produce:
- Metadati (H1, meta title, meta description)
- Keyword list con volumi
- Istruzioni di scrittura generali
- Scaletta H2/H3 con istruzioni per paragrafo e keyword da integrare
- Nota SEO con link interni, CTA e fonti

Il brief è il documento pivot del flusso: tutte le fasi successive lo usano come riferimento principale.

**Checkpoint**: prima di procedere alla scrittura, mostra il brief all'utente e chiedi conferma esplicita. Il brief è l'unico punto in cui l'utente può modificare la struttura dell'articolo prima che venga scritto.

---

### Fase 5 — DRAFT WRITER
*Skill: `draft-writer`*

Scrive la bozza completa dell'articolo seguendo il brief approvato. Produce:
- Testo completo dell'articolo con H1, H2, H3
- Link interni inseriti sugli anchor text indicati
- CTA posizionate nei punti indicati
- Note al revisore (keyword inserite, link usati, scostamenti dal brief)

---

### Fase 6 — SEO OPTIMIZER
*Skill: `seo-optimizer`*

Controlla e ottimizza la bozza prodotta nella Fase 5. Produce:
- Testo corretto (se modifiche ≤ 2 paragrafi, o se le modifiche estese sono solo riscritture de‑AI) oppure report di modifiche (se modifiche estese strutturali/SEO)
- Verifica keyword distribution, metadati, struttura, link interni
- Controllo di scrittura umana (de‑AI): rileva frasi fatte, riempitivi e ritmo robotico tipici dei testi AI-generated e riscrive le frasi problematiche in forma umana

---

### Fase 7 — CONTENT REVIEWER
*Skill: `content-reviewer`*

Valida la qualità finale dell'articolo ottimizzato. Produce:
- Punteggio E-E-A-T per criterio (Experience, Expertise, Authoritativeness, Trustworthiness)
- Punteggio complessivo da 1 a 10
- Raccomandazioni di distribuzione multicanale (2-3 canali selezionati)

---

## Gestione dei checkpoint

Il flusso prevede **due checkpoint obbligatori** che restano attivi in entrambe le modalità (interattiva e autonoma):

1. **Dopo la Fase 3** (prima di costruire il brief): mostra all'utente un riepilogo degli output delle prime tre fasi e chiedi conferma per procedere. Questo permette di correggere eventuali problemi nell'analisi prima di investire tempo nella scrittura.

2. **Dopo la Fase 4** (prima di scrivere): mostra il brief completo e chiedi conferma esplicita. È l'ultimo momento utile per modificare la struttura dell'articolo.

**Mini‑checkpoint aggiuntivi (solo in modalità interattiva):** dopo ogni altra fase (1, 2, 5, 6), mostra un mini‑riepilogo di 3‑5 bullet di cosa è emerso e chiedi all'utente se procedere. In modalità autonoma questi mini‑checkpoint sono omessi e il flusso prosegue automaticamente.

**Checkpoint di emergenza (sempre attivi):**
- Se in Fase 1 l'intent risulta chiaramente transazionale, ferma il flusso e chiedi conferma.
- Se in Fase 2 (Step 0) il sito ha già una pagina posizionata in top 50 sulla keyword primaria o su una correlata importante, ferma il flusso e chiedi se continuare, cambiare focus o aggiornare la pagina esistente.
- Se in Fase 2 la SERP è dominata da contenuti transazionali in contrasto con la keyword, ferma il flusso e chiedi conferma.
- Se in Fase 3 il TOV non è rilevabile, chiedi all'utente esempi di post social prima di proseguire.

Questi tre stop non dipendono dalla modalità: sono problemi che invalidano le fasi successive se ignorati.

---

## Modalità di esecuzione parziale

Il pipeline può essere avviato anche in modo parziale, saltando le fasi già completate in sessioni precedenti:

- Se l'utente fornisce già un output completo di keyword-analysis, salta la Fase 1 e parti dalla Fase 2.
- Se l'utente fornisce già un brief editoriale completo, salta le Fasi 1-4 e parti dalla Fase 5.
- Se l'utente fornisce già un articolo scritto, salta le Fasi 1-5 e parti dalla Fase 6.

**Attenzione: fornire input grezzi non equivale a saltare una fase.** Dare delle keyword seme o l'URL del sito sono semplicemente gli input del flusso, non l'output di una fase. Le Fasi 1-3 vanno comunque eseguite. Si salta una fase solo quando l'utente fornisce l'**output completo** di quella fase (un set keyword già analizzato con volumi e intent, un'analisi SERP completa con gap e PAA, un brief editoriale finito).

In particolare, **una richiesta di solo content brief NON deve mai eseguire la sola Fase 4**: esegui sempre prima le Fasi 1, 2 e 3, poi costruisci il brief (Fase 4) e fermati lì. Questo vale anche se l'utente ha già fornito keyword e/o URL.

**Se l'utente fornisce delle keyword (non un'analisi keyword completa):** prima di eseguire la Fase 1 chiedi se vuole che vengano cercate anche keyword correlate o se procedere solo con quelle fornite, poi esegui la Fase 1 di conseguenza. Le Fasi 2 e 3 restano comunque obbligatorie.

In ogni caso, le skill successive devono avere accesso agli output delle fasi precedenti per funzionare correttamente. Se mancano, segnalalo e chiedi all'utente di fornirli o di tornare alla fase mancante.

---

## Output finale

L'output finale dipende dall'obiettivo scelto all'inizio della sessione:

**Obiettivo `articolo completo`** (default):
L'utente riceve un **unico articolo finale** nel formato indicato (markdown, HTML, testo plain, .docx o altro). La struttura del deliverable è:

1. **Blocco "KEYWORD UTILIZZATE"** in testa: elenco delle keyword (primaria + secondarie + long‑tail) effettivamente integrate nell'articolo, ciascuna con il volume di ricerca mensile. È un blocco di metadati per chi pubblicherà l'articolo, sempre presente prima del corpo del testo.
2. **L'articolo ottimizzato** (versione finale dalla Fase 6, comprensiva di H1, corpo e CTA finale).
3. **Blocco "LINK INTERNI IN ENTRATA DA CREARE"** come blocco separato accodato dopo l'articolo: elenco degli URL di articoli del blog già esistenti e correlati dove inserire un link che punta a questo nuovo articolo, ciascuno con l'anchor text suggerito (dallo Step 4 di brand-analysis-and-connections). È un blocco operativo per chi pubblica: indica dove aggiungere i rimandi al nuovo contenuto aggiornando i vecchi articoli. Se non ci sono articoli adatti, indicalo in una riga.
4. **Report E‑E‑A‑T** (Fase 7) come blocco separato accodato in fondo: punteggi per criterio, punteggio complessivo, confronto con i competitor della SERP, raccomandazioni di distribuzione multicanale.

**Obiettivo `brief`**:
L'utente riceve il **content brief editoriale** prodotto in Fase 4, nel formato indicato. Niente articolo, niente report E‑E‑A‑T (la Fase 7 non viene eseguita). Il brief include anche l'elenco dei **link in entrata da creare** (URL di articoli esistenti dove linkare il nuovo articolo). Il brief deve essere autosufficiente: un copywriter umano deve poter scrivere l'articolo leggendo solo quel documento.

In entrambi i casi, le analisi delle fasi precedenti (keyword, SERP, brand) restano nella conversazione come passaggi intermedi consultabili. Non duplicare questi materiali nell'output finale.

---

## Regole critiche

- Se il flusso gira dentro un progetto Claude con istruzioni custom o knowledge di progetto, rispettale e adatta brief e articolo: hanno precedenza sui default delle skill, ma restano subordinate alle scelte di sessione dell'utente e alla correttezza SEO. In caso di conflitto, segnalalo e chiedi.
- Non saltare fasi senza esplicita indicazione dell'utente.
- Una richiesta di content brief attiva sempre le Fasi 1-4, mai la sola Fase 4. Fornire keyword e/o URL non autorizza a saltare le Fasi 1-3: sono input, non output di fase.
- Se l'utente fornisce delle keyword, chiedi se cercarne anche di correlate o procedere solo con quelle prima di eseguire la Fase 1.
- Non avviare la scrittura (Fase 5) senza approvazione esplicita del brief.
- Non procedere oltre la Fase 1 se l'intent è chiaramente transazionale senza conferma dell'utente.
- Non procedere oltre il controllo di cannibalizzazione (Fase 2, Step 0) se il sito ha già un contenuto posizionato in top 50 sulla keyword primaria o su una correlata importante: ferma e chiedi all'utente se continuare, cambiare focus o aggiornare la pagina esistente.
- Se il TOV del sito non è rilevabile, non inventarlo: pausa e chiedi input social all'utente.
- Ogni fase deve ricevere in contesto gli output di tutte le fasi precedenti.
- Il checkpoint dopo la Fase 3 è obbligatorio: non costruire il brief senza aver mostrato il riepilogo delle analisi.
- Il checkpoint dopo la Fase 4 è obbligatorio: non scrivere l'articolo senza approvazione esplicita del brief.
- Se il punteggio E-E-A-T finale è sotto 5, segnala all'utente che l'articolo non è pronto per la pubblicazione e indica le priorità di intervento prima di procedere.
