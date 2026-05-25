---
name: content-reviewer
description: >
  Valida la qualità finale dell'articolo blog SEO applicando i criteri E-E-A-T di Google (Experience, Expertise, Authoritativeness, Trustworthiness), confronta l'articolo con i competitor analizzati in serp-analysis per verificare copertura tematica e differenziatori, e produce un punteggio da 1 a 10 con raccomandazioni operative per la distribuzione multicanale. Usa questa skill dopo seo-optimizer come ultimo step prima della pubblicazione. Trigger tipici: "valuta la qualità dell'articolo", "dammi il punteggio EEAT", "confronta l'articolo con i competitor", "l'articolo è pronto per la pubblicazione?", "come posso sfruttare questo contenuto", "procedi con il flusso seo-blog-pipeline". Questa skill è il settimo e ultimo step del flusso seo-blog-pipeline.
---

# Content Reviewer

Questa skill è il validatore finale del flusso. Non corregge il testo: valuta la qualità dell'articolo secondo i criteri E-E-A-T di Google, lo confronta con i competitor della SERP analizzati nella Fase 2, e produce un punteggio con motivazione, seguito da raccomandazioni concrete su come distribuire e amplificare il contenuto su altri canali.

---

## Input atteso

Per fare una revisione di valore, questa skill ha bisogno di:

- **Articolo finale ottimizzato** (output di `seo-optimizer`)
- **Brief editoriale** (output di `content-brief-builder`) — per sapere cosa l'articolo doveva ottenere
- **Analisi SERP** (output di `serp-analysis`) — **fondamentale per il confronto con i competitor**: senza l'elenco dei competitor analizzati e i loro gap/strutture, il confronto non è possibile
- **Analisi keyword** (output di `keyword-analysis`) — per contestualizzare l'intent
- **Note al revisore** del `draft-writer` (se disponibili) — per capire scelte editoriali fatte in scrittura

Se manca l'analisi SERP, segnalalo e chiedi all'utente di fornirla o di rieseguire la Fase 2 prima di procedere con il confronto. La valutazione E‑E‑A‑T può comunque essere eseguita, ma il confronto con i competitor andrà saltato.

---

## Riferimenti E-E-A-T

I quattro criteri su cui si basa la valutazione sono quelli definiti nelle Google Search Quality Rater Guidelines:

**Experience (Esperienza)**
Il contenuto dimostra esperienza diretta e concreta sull'argomento? Ci sono esempi pratici, scenari reali, dettagli che solo chi ha vissuto il topic potrebbe conoscere? Un testo generico e teorico ha bassa esperienza; un testo con esempi operativi, casi concreti, errori comuni e sfumature pratiche ha alta esperienza.

**Expertise (Competenza)**
Il contenuto dimostra conoscenza approfondita e accurata del topic? Le informazioni sono corrette, complete, aggiornate? Il livello di trattazione è adeguato al pubblico target? Un testo che sfiora la superficie o contiene inesattezze ha bassa competenza; un testo che copre il topic in profondità, cita normative, dati o fonti verificabili e risponde alle domande reali del lettore ha alta competenza.

**Authoritativeness (Autorevolezza)**
Il testo è scritto (o firmato) da una fonte riconoscibile nel settore? Cita fonti autorevoli? Ha segnali di autorità nel testo (dati, studi, normative, esperienza dichiarata)? Un testo anonimo e non referenziato ha bassa autorevolezza; un testo con autore identificabile, fonti citate e segnali di credibilità ha alta autorevolezza.

**Trustworthiness (Affidabilità)**
Il contenuto è accurato, onesto e trasparente? Non contiene affermazioni non verificabili o promesse eccessive? Il sito e il testo danno segnali di fiducia? L'affidabilità è il criterio centrale dell'E-E-A-T secondo Google: un testo può avere esperienza e competenza, ma se non è affidabile il punteggio complessivo è basso.

---

## Processo di valutazione

### Step 1 — Lettura dell'articolo

Leggi il testo completo dell'articolo, il brief editoriale (se disponibile) e le note al revisore prodotte dal draft-writer (se disponibili). Contestualizza la valutazione: un articolo B2B tecnico ha criteri diversi da un articolo divulgativo per consumatori finali.

### Step 2 — Confronto con i competitor della SERP

Recupera l'analisi SERP della Fase 2 e per ciascun competitor editoriale che era stato analizzato (in genere 5‑7 URL), valuta concretamente:

**Copertura tematica vs ogni competitor**
Per ogni competitor, individua 2‑4 temi/sottotopic chiave che trattava. Per ciascuno indica:
- Il nostro articolo lo tratta? (Sì / No / Parzialmente)
- Se sì, lo tratta in modo più approfondito, equivalente, o più superficiale?
- Cosa potremmo aggiungere o migliorare se è "parziale" o "più superficiale"?

**Gap della SERP — sono stati coperti?**
La Fase 2 ha identificato dei gap (cose che nessun competitor copriva bene). Verifica per ciascun gap:
- È stato effettivamente coperto nell'articolo?
- In che paragrafo / sezione?
- È stato coperto in modo distintivo (con dati, esempi, angolazione propria) o solo accennato?

**Differenziatori dell'articolo**
Identifica 2‑3 elementi che il nostro articolo ha e i competitor non hanno (o trattano peggio). Possono essere: angolazione editoriale diversa, dati o esempi originali, struttura più scannable, internal linking strategico, copertura di una PAA ignorata dai competitor.

**Eventuali lacune residue**
Se ci sono temi che i competitor trattavano e noi no, segnalali. Distingui tra:
- "Volontariamente omesso" (es. tema fuori dal nostro angle): OK, non è una lacuna.
- "Mancante per omissione" (avremmo dovuto trattarlo ma non l'abbiamo fatto): è un'indicazione di revisione.

L'obiettivo del confronto non è giudicare l'articolo "migliore" o "peggiore" in assoluto, ma capire se è competitivo nella SERP target e identificare i suoi punti di forza e debolezza concreti rispetto a chi già rankesava.

### Step 3 — Valutazione per criterio

Assegna un punteggio da 1 a 10 per ciascuno dei quattro criteri E-E-A-T. Usa questa scala:

- **1-3**: carente. Il criterio non è soddisfatto o è soddisfatto in modo superficiale.
- **4-6**: sufficiente. Il criterio è presente ma può essere migliorato significativamente.
- **7-8**: buono. Il criterio è soddisfatto in modo solido, con margini di miglioramento minori.
- **9-10**: eccellente. Il criterio è soddisfatto in modo completo e difficilmente migliorabile.

Per ciascun criterio scrivi una motivazione concisa (2-3 righe) che spiega il punteggio e indica, se necessario, cosa manca o cosa potrebbe essere rafforzato.

### Step 4 — Punteggio complessivo

Il punteggio complessivo E-E-A-T non è la media aritmetica dei quattro criteri. Segui questa logica:

- La **T (Trustworthiness)** è il criterio fondante: se è sotto 5, il punteggio complessivo non può superare 6, indipendentemente dagli altri.
- La **E (Experience)** pesa di più per topic pratici e operativi (guide, tutorial, checklist). Pesa meno per topic puramente informativi o normativi.
- La **A (Authoritativeness)** pesa di più per topic YMYL (salute, finanza, sicurezza, legale). Pesa meno per topic di marketing, lifestyle o intrattenimento.

Esprimi il punteggio complessivo come numero intero da 1 a 10, con una riga di sintesi che spiega il giudizio.

### Step 5 — Raccomandazioni di distribuzione multicanale

Sulla base del topic, del formato dell'articolo, del pubblico target e del punteggio E-E-A-T, consiglia come sfruttare il contenuto su altri canali. Le opzioni disponibili sono:

**YouTube / Video**
Consigliato quando: il topic è dimostrativo o procedurale (tutorial, guide step-by-step, confronti), oppure quando la componente "experience" è bassa e un video potrebbe colmarla con testimonianza diretta. Indica: tipo di video consigliato (tutorial, intervista, case study, shorts), angolazione, durata stimata.

**LinkedIn**
Consigliato quando: il topic è B2B, professionale o legato a normative, strategie, tendenze di mercato. Il formato articolo lungo su LinkedIn può amplificare l'autorevolezza. Indica: se pubblicare un post breve (500-800 battute con hook forte), un articolo lungo su LinkedIn Pulse, o un carosello.

**Instagram**
Consigliato quando: il topic ha una forte componente visiva, pratica o lifestyle. Adatto per contenuti con liste, checklist, prima/dopo, dati visualizzabili. Indica: formato consigliato (carosello, reels, infografica in stories), hook visivo suggerito.

**Newsletter / Email**
Consigliato quando: l'articolo è approfondito e ad alto valore informativo, adatto a un pubblico già fidelizzato che apprezza il long-form. Indica: come adattare il contenuto (teaser + link, sintesi in 5 punti, angle editoriale diverso).

**Podcast / Audio**
Consigliato quando: il topic si presta a una discussione approfondita, a un'intervista con un esperto, o a un commento editoriale. Indica: formato (puntata monografica, intervista, round-up), scaletta suggerita.

**Webinar / Live**
Consigliato quando: il topic è complesso, richiede interazione, o è legato a novità normative o di mercato che il pubblico vuole approfondire in tempo reale.

Non consigliare tutti i canali per ogni articolo. Seleziona i 2-3 più adatti e motiva la scelta in una riga.

---

## Output

---

**CONTENT REVIEW — [titolo articolo]**

**CONFRONTO CON I COMPETITOR DELLA SERP**

*Copertura tematica vs competitor*
| Competitor (URL) | Temi chiave del competitor | Trattati nel nostro articolo? | Profondità relativa |
|---|---|---|---|
| [URL competitor 1] | [2‑4 temi] | [Sì / Parz. / No] per ognuno | [Più / Pari / Meno approfondito] |
| [URL competitor 2] | [2‑4 temi] | [Sì / Parz. / No] | [Più / Pari / Meno] |
*(ripeti per ogni competitor analizzato in serp-analysis)*

*Gap della SERP — stato di copertura*
- [Gap 1 identificato in serp-analysis]: [Coperto in sezione X con dati Y / Solo accennato in X / Non coperto]
- [Gap 2]: [stato]
*(ripeti per ogni gap)*

*Differenziatori del nostro articolo*
- [Elemento 1 che abbiamo e i competitor non hanno]
- [Elemento 2]
- [Elemento 3, se rilevante]

*Lacune residue* *(solo se ne esistono)*
- [Tema trattato dai competitor e mancante nel nostro articolo — distinguere "omissione volontaria" da "vera lacuna"]

**VALUTAZIONE E-E-A-T**

| Criterio | Punteggio | Motivazione |
|---|---|---|
| Experience | [X]/10 | [2-3 righe] |
| Expertise | [X]/10 | [2-3 righe] |
| Authoritativeness | [X]/10 | [2-3 righe] |
| Trustworthiness | [X]/10 | [2-3 righe] |

**PUNTEGGIO COMPLESSIVO: [X]/10**
[Una riga di sintesi del giudizio complessivo. Se il confronto con i competitor ha evidenziato lacune o vantaggi rilevanti, citali qui in una riga.]

**COSA RAFFORZARE** *(solo se il punteggio è sotto 7 o se il confronto ha evidenziato lacune residue)*
- [Indicazione concreta su come migliorare il criterio più debole o coprire una lacuna identificata]
- [Indicazione 2, se necessaria]

**RACCOMANDAZIONI DI DISTRIBUZIONE**

*[Canale 1]*
[Formato consigliato e motivazione in 2-3 righe. Includi suggerimento su angolazione o hook.]

*[Canale 2]*
[Formato consigliato e motivazione in 2-3 righe.]

*[Canale 3 — se pertinente]*
[Formato consigliato e motivazione in 2-3 righe.]

---

## Regole critiche

- Non correggere il testo: questa skill valuta, non riscrive. Le correzioni sono competenza di seo-optimizer e draft-writer.
- Il punteggio deve essere motivato, non arbitrario: ogni voto deve avere una spiegazione concreta.
- La Trustworthiness è il criterio fondante: non può essere ignorata o compensata dagli altri.
- Le raccomandazioni di distribuzione devono essere specifiche e azionabili: non "pubblica su LinkedIn" ma "pubblica un carosello su LinkedIn con i 5 gap più comuni che i competitor non coprono, usando il dato sulla difficoltà SERP come hook".
- Non consigliare tutti i canali: seleziona i 2-3 più adatti al topic e al pubblico. Troppi canali consigliati equivale a nessun consiglio utile.
- Se l'articolo ha un punteggio E-E-A-T complessivo sotto 5, segnala esplicitamente che non è pronto per la pubblicazione e indica le priorità di intervento.
- Il confronto con i competitor deve usare i dati reali della serp-analysis (URL, struttura, gap), non inventare competitor o opinioni generiche sulla SERP. Se la serp-analysis non è disponibile nel contesto, salta esplicitamente questa sezione e segnalalo.
- Nel confronto, distingui sempre "omissione volontaria" (un tema fuori dal nostro angle, scelta editoriale legittima) da "lacuna" (un tema che avremmo dovuto trattare ma non l'abbiamo fatto). Solo le seconde vanno in "COSA RAFFORZARE".
