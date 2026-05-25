---
name: draft-writer
description: >
  Scrive la bozza completa dell'articolo blog SEO a partire dal brief editoriale prodotto dal content-brief-builder. Usa questa skill dopo content-brief-builder e prima di seo-optimizer. Trigger tipici: "scrivi l'articolo", "sviluppa la bozza", "scrivi il testo seguendo il brief", "procedi con il flusso seo-blog-pipeline". Questa skill è il quinto step del flusso seo-blog-pipeline. Può essere usata anche in autonomia se l'utente fornisce direttamente un brief editoriale.
---

# Draft Writer

Questa skill scrive la bozza completa dell'articolo blog SEO a partire dal brief editoriale. Produce un testo pronto per la revisione: strutturato, ottimizzato SEO, scritto con voce umana e con i link interni già inseriti nel modo corretto.

L'obiettivo non è riempire una pagina con parole, ma rispondere in modo completo e autentico al bisogno informativo di chi ha fatto quella ricerca.

---

## Input atteso

**Fonte primaria (obbligatoria):** il brief editoriale prodotto da `content-brief-builder`, che contiene:
- Metadati (H1, meta title, meta description)
- Keyword list con volumi
- Istruzioni di scrittura generali (TOV, stile, registro)
- Scaletta H2/H3 con istruzioni per ciascun paragrafo e keyword da integrare
- Nota SEO con link interni, anchor text, CTA e fonti

**Fonte integrativa (se disponibile nel contesto):** output delle skill precedenti (keyword-analysis, serp-analysis, brand-analysis-and-connections). Se presenti, usali per arricchire le scelte editoriali: sapere quali gap coprire, quali domande PAA rispondere e qual è il TOV del brand aiuta a scrivere un testo più preciso. Se non sono presenti, il brief è sufficiente.

**Istruzioni e knowledge di progetto (se il flusso gira dentro un progetto Claude):** linee guida editoriali, brand book, tone of voice, glossari, termini da usare/evitare, vincoli di formato o legali. Rispettale durante la scrittura: prevalgono sui default generici di questa skill. Se sono in conflitto con il brief approvato o con una buona pratica SEO, non procedere a senso: segnala il conflitto e chiedi all'utente come comportarti.

---

## Processo di scrittura

### Step 1 — Lettura completa del brief

Prima di scrivere qualsiasi parola, leggi il brief per intero. Identifica:
- Il pubblico target: chi sta leggendo questo articolo, con quale competenza, con quale bisogno
- Il tono di voce: formale/informale, tecnico/divulgativo, registro e persona grammaticale (tu/voi)
- I vincoli fissi: struttura H2/H3 che non va modificata (salvo aggiunta di 1-2 capitoli, vedi sotto)
- I link interni con anchor text: vanno inseriti esattamente dove indicato, nel modo più naturale possibile
- Le CTA: vanno inserite nei punti indicati, con il testo suggerito o una variante equivalente

### Step 2 — Struttura e libertà editoriale

La struttura H2/H3 del brief è fissa. Il copywriter non la modifica. L'unica eccezione: se durante la scrittura emerge un aspetto genuinamente utile per il lettore e rilevante per SEO che il brief non copre, è possibile aggiungere un massimo di 1-2 H2 aggiuntivi. In questo caso:
- L'aggiunta deve coprire un gap reale, non essere un'espansione generica
- Va posizionata dove è più utile per il flusso del testo, non in fondo per allungare
- Va segnalata nell'output con una nota: *(H2 aggiunto: [motivazione in una riga)*

Le istruzioni di scrittura per ciascun paragrafo sono indicative sul contenuto, non sulla forma. Se il brief dice "inizia con un aggancio empatico" ma un approccio diverso è più efficace per quel paragrafo, usalo. Quello che conta è rispettare l'obiettivo del paragrafo, non la formula.

### Step 3 — Scrittura del testo

Scrivi il testo seguendo questo ordine: introduzione, H2 in sequenza con i relativi H3, conclusione/CTA finale.

**Criteri di qualità che guidano la scrittura:**

**Voce umana, non da AI**
Il testo deve sembrare scritto da un professionista del settore, non da un sistema automatico. Questo significa:
- Niente aperture con "Nel mondo di oggi...", "In un contesto sempre più...", "È fondamentale sottolineare che..."
- Niente conclusioni con "In conclusione, come abbiamo visto..."
- Niente ripetizioni di termini tecnici o di settore che un umano non userebbe tre volte nello stesso paragrafo
- Niente frasi vuote che suonano autorevoli ma non dicono nulla ("è importante considerare tutti gli aspetti")
- Frasi di lunghezza variabile: alcune brevi e dirette, alcune più articolate. Non tutte dello stesso stampo

**Niente trattini come punteggiatura inline**
L'uso del trattino (`-`, `–`, `—`) come punteggiatura tra clausole o per inciso è uno dei segnali più riconoscibili di testo generato da AI. Va evitato in modo assoluto. Sostituisci con virgola, punto e virgola o punto, oppure riscrivi la frase.

Esempi di cosa NON scrivere:
- "Il marketing digitale è in continua evoluzione — capire le nuove tendenze è essenziale."
- "Tre fattori contano davvero: contenuto, link, esperienza utente — e tutti vanno presidiati."

Versioni corrette:
- "Il marketing digitale è in continua evoluzione. Capire le nuove tendenze è essenziale."
- "Tre fattori contano davvero: contenuto, link, esperienza utente. Tutti vanno presidiati."

I trattini restano legittimi solo all'interno di parole composte ("post‑pandemia", "anti‑stress") e in intervalli numerici. Mai come segno di interpunzione tra frasi.

**Niente sezione "Domande frequenti" o "FAQ"**
Le domande PAA del brief devono essere risolte all'interno del corpo dell'articolo: o come heading H2/H3, o come domanda implicita a cui un paragrafo risponde naturalmente. Non creare mai un blocco a fine articolo intitolato "Domande frequenti", "FAQ" o equivalenti che raccolga domande e risposte in elenco. Se il brief contenesse erroneamente una sezione FAQ, ridistribuisci le domande nel testo e segnalalo nelle note al revisore.

**Capitalizzazione dei titoli (H1, H2, H3)**
I titoli si scrivono con la maiuscola **solo sulla prima parola** e sui nomi propri. Mai title case all'inglese, mai tutto maiuscolo.

Corretto:
- "Come ha fatto Sinner a vincere la partita"
- "Come preparare un antipasto coi carciofi"
- "Pasta alla carbonara: la ricetta originale romana"

Sbagliato:
- "Come Fare la Pasta con la Pancetta" (title case)
- "COME FARE LA PASTA AL RAGÙ" (tutto maiuscolo)
- "Come Preparare Un Antipasto Coi Carciofi" (title case)

**Risposta al bisogno, non riempimento**
La lunghezza non è un obiettivo. Ogni paragrafo deve rispondere a una domanda reale che il lettore si sta ponendo. Se una sezione del brief è esaurita in 80 parole perché non c'è altro di utile da dire, si chiude lì. Non si dilata per raggiungere una word count.

**Integrazione naturale delle keyword**
Le keyword vanno inserite dove scorrono in modo naturale nel testo. Non si forzano all'inizio di ogni paragrafo, non si ripetono meccanicamente, non si evidenziano in grassetto solo per farle notare. Un testo ottimizzato SEO non si legge come tale.

**Liste con giudizio**
Le liste puntate e numerate si usano solo quando il contenuto è effettivamente enumerabile (es. una checklist, una serie di step, una comparazione). Non si usano per spezzare testo narrativo che scorre bene in prosa. Un articolo pieno di elenchi puntati è un segnale di testo AI-generated, non di qualità editoriale.

**Grassetto con criterio**
Il grassetto si usa per evidenziare concetti chiave, non per decorare. Massimo 1-2 elementi in grassetto per paragrafo, mai intere frasi.

### Step 4 — Inserimento link interni

I link interni vanno inseriti esattamente nei punti indicati dal brief, sull'anchor text specificato. Se l'anchor text suggerito non scorre naturalmente nel contesto esatto del testo scritto, trova la variante più vicina che mantiene la keyword semantica. Mai usare:
- "clicca qui"
- "leggi la nostra guida su"
- "scopri di più"
- "visita questa pagina"

Il link deve cadere su parole che hanno già senso semantico nel testo, come se il link non ci fosse e la frase funzionasse ugualmente.

### Step 5 — CTA

Inserisci le CTA nei punti indicati dal brief. Le CTA devono essere:
- Coerenti con il tono del testo (non gridare se l'articolo ha un tono misurato)
- Connesse tematicamente al paragrafo in cui sono inserite (non spezzano il flusso)
- Orientate al beneficio del lettore, non alla vendita

Se il brief indica un testo CTA specifico, usalo o una variante che mantiene lo stesso messaggio.

---

## Output

L'output è il testo completo dell'articolo, formattato con gli heading corretti (H1, H2, H3), pronto per essere incollato nel CMS o consegnato per revisione. **Prima del testo dell'articolo**, anteponi un blocco "KEYWORD UTILIZZATE" con l'elenco delle keyword principali e secondarie effettivamente inserite nell'articolo, con il relativo volume di ricerca mensile (preso dal brief / keyword-analysis).

Struttura dell'output:

```
**KEYWORD UTILIZZATE**
- [keyword primaria] — [volume]/mese
- [keyword secondaria] — [volume]/mese
- [keyword secondaria] — [volume]/mese
- [keyword long-tail] — [volume]/mese
...

---

# [H1 — titolo articolo]

[Introduzione]

## [H2]

[Testo paragrafo]

### [H3] *(se previsto)*

[Testo sottoparagrafo]

## [H2]

[Testo paragrafo]

...

[CTA finale]
```

Inserisci nell'elenco solo le keyword effettivamente integrate nel testo (non l'intera lista del brief), con il volume reale del brief. Se una keyword del brief non è stata inserita perché non scorreva naturalmente, NON va nell'elenco e va invece segnalata nelle note al revisore.

Dopo il testo dell'articolo, aggiungi una sezione separata:

---

**NOTE AL REVISORE**
- Keyword primaria: [keyword] — inserita in: [elenco punti: H1, primo paragrafo, H2 X, ecc.]
- Link interni inseriti: [elenco con URL e anchor text usato]
- CTA inserite: [numero e posizione]
- H2 aggiunti rispetto al brief: [nessuno / titolo e motivazione]
- Eventuali scelte editoriali che si discostano dal brief: [nessuna / descrizione]

---

## Regole critiche

- Non modificare la struttura H2/H3 del brief. Massimo 1-2 H2 aggiuntivi se giustificati, con nota al revisore.
- Non inventare dati, statistiche o citazioni. Se il brief indica fonti, usale come riferimento ma non riprodurre testo da esse.
- Non inserire link non presenti nel brief. I link interni sono solo quelli forniti dalla brand-analysis-and-connections e riportati nel brief.
- Non usare frasi di apertura da AI: "Nel mondo di oggi", "In un contesto sempre più", "È fondamentale sottolineare".
- Non abusare di liste puntate: usarle solo dove il contenuto è genuinamente enumerabile.
- Non scrivere per la word count: scrivere per il lettore.
- L'anchor text dei link deve essere semanticamente naturale: mai "clicca qui" o costruzioni simili.
- Le keyword vanno integrate, non forzate. Un testo che si legge come ottimizzato SEO non è ottimizzato SEO.
- Il tono deve rispecchiare le istruzioni di scrittura del brief in ogni paragrafo, non solo nell'introduzione.
- Aggiungi sempre la sezione "Note al revisore" dopo il testo: serve al processo di revisione successivo.
- Mai trattini (`-`, `–`, `—`) come punteggiatura tra clausole o per inciso. Sono il principale tell di testo AI‑generated. Usa virgola, punto e virgola o punto, oppure riscrivi la frase.
- Mai una sezione finale "Domande frequenti" / "FAQ": le PAA si integrano come heading o come risposte inline nei paragrafi.
- H1, H2 e H3 sempre con maiuscola solo sulla prima parola e sui nomi propri. Mai title case, mai tutto maiuscolo.
