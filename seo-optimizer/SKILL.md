---
name: seo-optimizer
description: >
  Controlla e ottimizza la bozza dell'articolo blog SEO prodotta dal draft-writer. Verifica keyword, struttura, metadati e link interni, controlla che il testo sia scritto in modo umano e non riconoscibile come AI-generated (frasi fatte, riempitivi, ritmo robotico) riscrivendo le frasi problematiche, poi corregge direttamente il testo o produce un report di modifiche in base all'entità degli interventi necessari. Usa questa skill dopo draft-writer e prima di content-reviewer. Trigger tipici: "ottimizza l'articolo per la SEO", "controlla la SEO del testo", "rendi il testo più umano", "verifica che non sembri scritto da un'AI", "procedi con il flusso seo-blog-pipeline". Questa skill è il sesto step del flusso seo-blog-pipeline.
---

# SEO Optimizer

Questa skill esegue il controllo SEO completo della bozza dell'articolo e restituisce il testo corretto oppure un report di modifiche, in base all'entità degli interventi necessari.

L'obiettivo è un articolo che rispetti i criteri SEO fondamentali senza sembrare ottimizzato: keyword ben distribuite, struttura leggibile, metadati efficaci, link interni tutti inseriti correttamente.

---

## Input atteso

- Bozza completa dell'articolo prodotta da `draft-writer`
- Brief editoriale (per verificare keyword list, link interni e metadati attesi)
- Note al revisore prodotte dal draft-writer (se disponibili)

---

## Processo di controllo

Esegui i seguenti controlli in sequenza. Per ciascuno registra internamente: OK, da correggere (modifica puntuale), o problema esteso (richiede interventi su più sezioni).

### Controllo 1 — Keyword primaria

Verifica che la keyword primaria sia presente:
- Nel titolo H1
- Nella prima parte dell'introduzione (idealmente nel primo o secondo paragrafo, non oltre)
- In almeno 2-3 H2 principali, in modo naturale
- Nel meta title
- Nella meta description

Verifica che la keyword primaria non sia ripetuta in modo meccanico o eccessivo. La soglia è qualitativa, non numerica: se leggendo il testo la keyword si sente forzata o ripetuta più volte nello stesso paragrafo, è troppa. Se è distribuita naturalmente nel testo, va bene anche se appare molte volte.

### Controllo 2 — Keyword secondarie e correlate

Verifica che le keyword secondarie siano distribuite nel testo nei paragrafi indicati dal brief. Non devono essere tutte presenti (alcune potrebbero non trovare contesto naturale), ma quelle ad alto volume o quelle associate a H2 specifici devono esserci.

Verifica che non ci siano ripetizioni anomale di keyword secondarie nello stesso paragrafo o in paragrafi adiacenti.

### Controllo 3 — Struttura e leggibilità

Verifica:
- Gerarchia heading corretta: H1 unico, H2 per sezioni principali, H3 per sottosezioni. Nessun salto di livello (es. H1 → H3 senza H2).
- Paragrafi non eccessivamente lunghi: un paragrafo di testo continuo che supera le 120-150 parole è un segnale di leggibilità ridotta. Segnalarlo se presente.
- Frasi non eccessivamente complesse: periodi con più di 3 subordinate consecutive o frasi superiori a 35-40 parole sono difficili da leggere su schermo. Segnalarli se presenti.
- Copertura tematica: tutti gli H2 del brief sono stati sviluppati in modo sostanziale? Se un paragrafo è troppo superficiale (meno di 80-100 parole per un H2 che richiedeva approfondimento), segnalarlo.

### Controllo 4 - Metadati

Verifica:
- **H1**: contiene la keyword primaria (possibilmente nella parte iniziale)? È chiaro e leggibile? L'H1 **non ha un limite rigido di caratteri**: non segnalarlo mai come "troppo lungo" per motivi di title tag - sono elementi distinti. L'unica correzione ammessa sulla lunghezza è se supera i ~110-120 caratteri risultando illeggibile, oppure se manca la keyword primaria (in quel caso proponi una variante).
- **Meta title**: è un elemento **distinto dall'H1**, non un doppione. Contiene la keyword primaria nella prima parte del titolo? È **simile ma non identico** all'H1 (se coincide alla lettera, va riscritto perché sfrutti diversamente lo spazio: variazione di ordine, aggiunta di keyword secondaria, elemento differenziante come "guida 2026", brand)? **È entro i 60 caratteri?**
- **Meta description**: contiene la keyword primaria? È scritta in italiano fluente come una frase compiuta, non come un elenco di keyword? **È entro i 160 caratteri?** Stimola il clic?

**Misurazione dei caratteri via script - obbligatoria.** Non stimare la lunghezza a occhio: esegui un breve script Python con la Bash tool per misurare meta title e meta description e per verificare che H1 e meta title non siano identici. Esempio:

```python
h1 = "..."  # il titolo H1 attuale dell'articolo
mt = "..."  # il meta title
md = "..."  # la meta description

# H1 non ha limite rigido; misurazione solo informativa
print(f"H1: {len(h1)} caratteri (nessun limite rigido)")

# Meta title e meta description hanno limite rigido
for nome, testo, limite in [("Meta title", mt, 60), ("Meta description", md, 160)]:
    n = len(testo)
    stato = "OK" if n <= limite else f"SFORATO di {n - limite}"
    print(f"{nome}: {n}/{limite} -> {stato}")

# H1 e meta title devono essere simili ma non identici
if h1.strip().lower() == mt.strip().lower():
    print("PROBLEMA: H1 e Meta title coincidono. Riscrivere il meta title.")
else:
    print("H1 vs Meta title: distinti (OK)")
```

Se meta title o meta description sforano il limite, riscrivili, applica la modifica al testo e ri-esegui lo script per confermare il rientro. Se H1 e meta title coincidono, riscrivi il meta title mantenendo la stessa idea centrale ma variando la formulazione (l'H1 resta com'è, salvo problemi propri). Riporta nel report finale solo le versioni verificate.

Se la meta description è solo una concatenazione di keyword o è scritta in modo meccanico, va riscritta anche se tecnicamente contiene le parole giuste.

### Controllo 5 — Link interni

Confronta i link indicati nella nota SEO del brief con quelli presenti nel testo:
- Tutti i link indicati sono stati inseriti?
- Ogni link è sull'**anchor text** indicato (o su una variante semanticamente equivalente)? L'anchor è **obbligatoria** su ogni link, mai omessa.
- Ogni `href` è un **URL assoluto** (`https://dominio.tld/percorso-completo`)? Se qualche link punta solo a un path relativo (es. `/blog/...`), correggilo con l'URL assoluto ricavato dal dominio del sito.
- Nessun link usa anchor text generici ("clicca qui", "scopri di più", "leggi qui")?
- Nessun link punta a una landing page (non previsto dalla brand-analysis)?
- I link sono inseriti in modo naturale nel testo, non spezzano il flusso?

Se un link del brief non è stato inserito, va aggiunto nel punto più naturale del testo più vicino al topic del link.

### Controllo 6 — Tell stilistici da AI

Verifica e correggi tre pattern che svelano una scrittura AI‑generated:

**Trattini come punteggiatura inline**
Cerca nel testo ogni occorrenza di `-`, `–`, `—` usata come segno di interpunzione tra clausole o per inciso (es. "il marketing è cambiato — i contenuti contano di più"). Sostituiscila con virgola, punto e virgola o punto, oppure riscrivi la frase. I trattini restano legittimi solo all'interno di parole composte ("post‑pandemia") e in intervalli numerici.

**Sezione "Domande frequenti" / "FAQ"**
Se l'articolo contiene una sezione finale (H2 o equivalente) intitolata "Domande frequenti", "FAQ", "Le domande più comuni" o simili, e questa sezione raccoglie domande e risposte in elenco, va eliminata. Le domande vanno ridistribuite nel corpo dell'articolo: o come heading dei paragrafi esistenti, o come domande implicite a cui un paragrafo già risponde.

**Titolo "Conclusione" (e sinonimi) sull'H2 finale**
Cerca l'ultimo H2 dell'articolo. Se il suo titolo è "Conclusione", "Conclusioni", "In sintesi", "Per concludere", "Considerazioni finali", "Tirando le somme", "In definitiva", "Ultima parola" o qualunque variante equivalente vuota di significato, **riscrivilo** in forma utile alla SEO: rifocalizza la keyword primaria o l'angolo del pezzo (es. "Come iniziare oggi con [keyword]", "[Keyword]: cosa fare prima di partire", "Quali passi seguire per [obiettivo]"). Il paragrafo conclusivo e la CTA devono restare, cambia solo l'heading. Se l'H2 non esiste o è già utile, nessuna azione.

**Capitalizzazione dei titoli**
H1, H2 e H3 devono avere la maiuscola solo sulla prima parola e sui nomi propri. Se un titolo è in title case all'inglese ("Come Fare la Pasta con la Pancetta") o tutto maiuscolo ("COME FARE LA PASTA AL RAGÙ"), correggilo. Forma corretta: "Come fare la pasta con la pancetta", "Come preparare un antipasto coi carciofi".

Questi quattro controlli sono di tipo binario: o il pattern è presente e va corretto, o non lo è.

### Controllo 7 — Scrittura umana (de‑AI)

Oltre ai tre tell binari del Controllo 6, verifica che il testo non "suoni" generato da un'AI. I modelli tendono a produrre frasi fatte, costruzioni retoriche a stampino, riempitivi privi di contenuto e un ritmo uniforme. Individua questi pattern e **riscrivi le frasi interessate** rendendole più naturali, concrete e specifiche, mantenendo significato, fatti e keyword previste.

Pattern da cercare e correggere (elenco non esaustivo, usa il giudizio):

**Frasi fatte e aperture/chiusure cliché**
- "Nel mondo di oggi", "Nell'era digitale", "In un mondo sempre più [aggettivo]", "Al giorno d'oggi", "Nel panorama attuale"
- Chiusure vuote: "In conclusione", "In sintesi", "Per concludere", "Tirando le somme", "In definitiva"
- Premesse inutili: "È importante sottolineare/notare che", "Vale la pena ricordare che", "Va detto che", "Come ben sai"

**Costruzioni retoriche tipiche dell'AI**
- Antitesi a stampino: "Non si tratta solo di X, ma di Y", "X non è (solo) ..., è ..."
- Regola del tre meccanica: triplette di aggettivi o sostantivi interscambiabili ("veloce, efficace e affidabile")
- "Che tu sia un [profilo] o un [profilo], ..."
- Domande retoriche di riempimento all'inizio dei paragrafi

**Riempitivi e marketing vuoto**
- Intensificatori generici: "fondamentale", "cruciale", "essenziale", "rivoluzionario", "all'avanguardia", "di altissimo livello", "soluzione completa", "a 360 gradi"
- Verbi-ombrello usati a vuoto, senza un "come" concreto: "permette di", "consente di", "aiuta a"
- Generalizzazioni senza dati né esempi: "sempre più aziende", "molti esperti concordano", "negli ultimi anni"

**Ritmo e struttura robotici**
- Paragrafi tutti della stessa lunghezza e con la stessa struttura (frase tema + due di supporto + chiusura)
- Connettivi ripetuti in apertura di paragrafi consecutivi ("Inoltre", "Tuttavia", "Infatti")
- Liste puntate con elementi costruiti tutti in modo identico e parallelo all'eccesso
- Grassetto applicato a termini a caso, senza criterio

Per ogni pattern trovato **riscrivi la frase**, non limitarti a segnalarla: taglia il riempitivo, sostituisci la frase fatta con un'affermazione concreta, varia la lunghezza e il ritmo delle frasi, e dove rende il testo più credibile aggiungi un dettaglio specifico o un esempio. Diversamente dal Controllo 6, questo è un controllo di giudizio: la soglia è qualitativa (il testo suona autentico quando lo leggi ad alta voce?).

Mantieni invariati: significato, keyword previste, fatti e dati, struttura H2/H3, link interni.

---

## Decisione: testo corretto vs report

Dopo aver completato tutti i controlli, valuta l'entità complessiva delle modifiche necessarie:

**Modifica diretta del testo** (restituisci il testo corretto completo):
- Le modifiche riguardano al massimo 2 paragrafi
- Si tratta di interventi puntuali: aggiunta/spostamento di una keyword, riscrittura di una frase, inserimento di un link mancante, correzione di un meta tag

**Report di modifiche** (restituisci un report senza riscrivere tutto):
- Le modifiche riguardano 3 o più paragrafi
- Ci sono problemi strutturali o di copertura tematica estesi
- La meta description va riscritta interamente
- Più link interni mancano o sono inseriti in modo scorretto

**Eccezione per le riscritture de‑AI (Controllo 7):** se le uniche modifiche estese sono riscritture di frasi per renderle più umane (nessun problema strutturale, di copertura o di link), **applicale direttamente e restituisci il testo completo corretto**, anche se toccano più di 2 paragrafi. Lo scopo del controllo è consegnare il testo umanizzato, non un elenco di frasi da sistemare a mano. Riserva il report ai problemi SEO/strutturali. Se coesistono riscritture de‑AI diffuse *e* problemi strutturali, usa il report e includi le riscritture de‑AI suggerite al suo interno.

---

## Output — Testo corretto

Se le modifiche sono poche (massimo 2 paragrafi), restituisci il testo completo dell'articolo con le correzioni già applicate. **Mantieni in cima il blocco "KEYWORD UTILIZZATE"** prodotto dal draft-writer (aggiornato se durante l'ottimizzazione hai aggiunto/rimosso keyword), seguito dal corpo dell'articolo, seguito dalla nota delle modifiche applicate:

```
**KEYWORD UTILIZZATE**
- [keyword primaria] — [volume]/mese
- [keyword secondaria] — [volume]/mese
...

---

[Testo completo dell'articolo corretto, dall'H1 alla CTA finale]

---

**MODIFICHE APPLICATE**
- [Modifica 1: descrizione in una riga]
- [Modifica 2: descrizione in una riga]
```

Se il draft-writer non ha incluso il blocco "KEYWORD UTILIZZATE", ricostruiscilo tu partendo dal brief e dall'analisi keyword, segnando solo le keyword effettivamente presenti nel testo finale dopo le tue correzioni.

---

## Output — Report di modifiche

Se le modifiche sono estese, restituisci un report strutturato senza riscrivere il testo completo:

---

**REPORT SEO OPTIMIZER**

**Stato generale:** [Buono con interventi puntuali / Richiede revisione estesa]

**KEYWORD**
- [OK / Problema]: [descrizione]
- [OK / Problema]: [descrizione]

**STRUTTURA E LEGGIBILITÀ**
- [OK / Problema]: [descrizione e punto del testo da correggere]

**METADATI**
- Meta title: [OK / testo corretto suggerito]
- Meta description: [OK / testo corretto suggerito]

**LINK INTERNI**
- [Link presente e corretto / Link mancante: dove inserirlo e su quale anchor / Link con anchor errato: correzione suggerita]

**TELL STILISTICI DA AI**
- Trattini inline: [Nessuno / N occorrenze da rimuovere con correzioni puntuali]
- Sezione FAQ finale: [Assente / Presente — da ridistribuire nei paragrafi]
- Capitalizzazione titoli: [Corretta / N titoli da riscrivere — elenco]

**SCRITTURA UMANA (DE‑AI)**
- [Naturale / Pattern AI rilevati]: per ciascun pattern indica la frase originale, il tipo (frase fatta, riempitivo, antitesi a stampino, ritmo robotico, ecc.) e la riscrittura più umana proposta.

**INTERVENTI RICHIESTI IN ORDINE DI PRIORITÀ**
1. [Intervento più critico]
2. [Intervento]
3. [Intervento meno critico]

---

## Regole critiche

- Non modificare la struttura H2/H3 dell'articolo: questo non è il momento per cambiare l'architettura del testo.
- Non riscrivere paragrafi interi per pure preferenze di stile: le correzioni devono essere motivate da criteri SEO oggettivi o dalla de‑AI (Controllo 7). Fa eccezione la de‑AI, che è un intervento richiesto: lì la riscrittura a livello di frase è ammessa e dovuta, ma non spingerti a riscrivere interi paragrafi quando basta correggere le frasi problematiche.
- I pattern di scrittura AI (frasi fatte, riempitivi, antitesi a stampino, ritmo robotico) vanno riscritti in forma umana, non solo segnalati: la de‑AI è un intervento obbligatorio, non opzionale.
- La riscrittura de‑AI non deve mai alterare significato, fatti, dati o keyword previste, né toccare la struttura H2/H3 e i link interni.
- La densità keyword è qualitativa, non numerica: non forzare inserimenti meccanici se il testo scorre già bene.
- Un meta title o una meta description che contengono la keyword ma sono scritti male vanno corretti: la keyword da sola non basta.
- **H1 e meta title sono elementi distinti**: l'H1 non ha limite rigido di caratteri (mai segnalarlo "troppo lungo" per motivi di title), il meta title sì (60). Se un H1 lungo viene passato dal draft-writer o dall'utente, non tentare di accorciarlo per far posto nel title: sono due campi separati. Se coincidono alla lettera, riscrivi solo il meta title.
- I link mancanti vanno sempre segnalati o inseriti: sono indicazioni del brief e non possono essere ignorati.
- Nessun link su anchor generici: se un link è stato inserito su "clicca qui" o equivalenti, va corretto.
- I trattini come punteggiatura inline vanno sempre rimossi: è una correzione obbligatoria, non stilistica.
- Una sezione finale "Domande frequenti" / "FAQ" va sempre smontata e ridistribuita nel corpo dell'articolo.
- Un H2 finale intitolato "Conclusione" (o sinonimi vuoti di significato) va **sempre** riscritto in forma utile alla SEO (rifocalizzando keyword primaria o angolo del pezzo). Il paragrafo conclusivo resta, cambia solo l'heading.
- Ogni link nel testo deve avere anchor esplicita (mai "clicca qui" e simili) e `href` con **URL assoluto** (`https://dominio.tld/...`, mai solo path relativo). Se manca uno dei due, correggi.
- I titoli in title case o tutto maiuscolo vanno sempre corretti in "maiuscola solo sulla prima parola e sui nomi propri".
- Se l'articolo supera tutti i controlli senza problemi significativi, dillo esplicitamente: "Nessuna modifica necessaria" è un output valido.
