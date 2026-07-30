---
name: host-site-analysis
description: >
  Analizza il portale ospitante su cui verrà pubblicato un guest post di link building, per apprenderne il tono di voce e il contesto editoriale e permettere allo scrittore di produrre un articolo che sembri nativo di quel sito. Studia registro, persona grammaticale (tu/voi/impersonale), tono, lessico, formato tipico degli articoli (news, guida, approfondimento, listicle), lunghezza media, struttura degli heading, uso di grassetto e liste, e come il portale inserisce i link nei propri pezzi. Usa questa skill come seconda fase del flusso guest-post-pipeline, dopo guest-post-brand-analysis e prima di guest-post-writer. Trigger tipici: "analizza il sito che ospita l'articolo", "studia il tono di voce del portale", "capisci come scrivono su questo sito prima di scrivere il guest post". Questa skill NON valuta l'autorevolezza SEO del portale né decide se è un buon sito partner: serve solo a capire come si scrive per quel portale.
---

# Host Site Analysis

Questa skill studia il **portale ospitante** per rispondere a una sola domanda: *come si scrive per questo sito, così che l'articolo sembri scritto dalla sua redazione?* Nel guest post il tono di voce del portale è il riferimento primario: un pezzo che stona rispetto allo stile del sito è meno credibile per il lettore, per la redazione che deve accettarlo e per Google.

L'obiettivo è una scheda di stile operativa: le regole implicite del portale che lo scrittore dovrà rispettare.

---

## Input atteso

- **URL del portale ospitante**: il sito su cui verrà pubblicato l'articolo.
- **Topic dell'articolo**: l'argomento fornito dall'utente (serve a individuare la sezione/categoria più pertinente del portale e a trovare articoli vicini al tema).
- **Lingua**: la lingua dell'articolo (deve coincidere con quella del portale; se il portale è in un'altra lingua, segnalalo).
- **Output di `guest-post-brand-analysis`** (se disponibile): utile per valutare il contesto in cui il brand verrà inserito.

---

## Integrazione strumenti

Usa `WebFetch` e, se serve, `WebSearch` per leggere il portale:

1. **Homepage** del portale: per capire di cosa parla, se è verticale o generalista, il pubblico e la localizzazione.
2. **La sezione/categoria più vicina al topic**: per capire in che contesto verrà inserito l'articolo.
3. **3‑5 articoli rappresentativi**, preferibilmente della categoria pertinente al topic: sono la fonte principale per il tono di voce e il formato. Se il portale ha una linea editoriale disomogenea, privilegia gli articoli più simili per tipo a quello che scriveremo.

Per trovare articoli pertinenti puoi usare `WebSearch` con `site:` sul dominio del portale più il topic.

**Individua e misura i guest post già presenti.** Oltre agli articoli redazionali, cerca sul portale i contenuti che sono a loro volta **guest post / contributi ospitati** (spesso riconoscibili da: firma esterna o "guest author", diciture come "articolo sponsorizzato", "in collaborazione con", "contenuto promozionale", "guest post", box autore di un brand, presenza di link esterni a un sito commerciale con anchor branded). Raccogline 3‑5 se disponibili e **conta le parole** di ciascuno. Se sul portale non è possibile distinguere i guest post dagli articoli redazionali, ripiega sugli articoli dello stesso **tipo** di quello che scriveremo (stessa categoria/formato) e conta quelli. In entrambi i casi annota il conteggio parole per articolo, così da poterne calcolare la media (Step 3).

Se il portale non è raggiungibile con gli strumenti disponibili (blocco di rete, contenuto non leggibile), non inventarne lo stile: chiedi all'utente di incollare 2‑3 articoli rappresentativi del sito. Se meno della metà degli articoli è leggibile, segnalalo e procedi con ciò che è disponibile.

Non servono metriche SEO in questa fase.

---

## Processo di analisi

### Step 1 — Inquadramento del portale

Dalla homepage e dalla sezione pertinente, ricava:
- **Tipo di portale**: verticale (specializzato su un tema) o generalista (multi-tema). Se verticale, su quale tema.
- **Pubblico di riferimento**: consumatore finale, professionista, azienda B2B, appassionato di nicchia.
- **Localizzazione**: nazionale, locale, internazionale. Rilevante se il topic o il brand hanno una dimensione geografica.
- **Sezione di destinazione**: in quale categoria/rubrica sarà pubblicato l'articolo, e cosa si aspetta il lettore di quella sezione.

### Step 2 — Tono di voce

Leggendo gli articoli rappresentativi, individua:
- **Registro**: formale, informale, colloquiale, tecnico, giornalistico.
- **Persona grammaticale**: si rivolge al lettore con il "tu", con il "voi", o usa una forma impersonale? È un tratto decisivo: va replicato esattamente.
- **Tono**: divulgativo, autorevole, ironico, istituzionale, pratico/how-to.
- **Lessico**: usa tecnicismi? Li spiega? Usa forestierismi, gergo di settore, un linguaggio semplice?

### Step 3 — Formato e struttura

Sempre dagli articoli, ricava:
- **Lunghezza di riferimento (target in parole)**: calcola la **media in parole dei guest post già presenti** sul portale individuati nell'integrazione strumenti (o, se non distinguibili, degli articoli dello stesso tipo). Indica la media, il numero di articoli su cui è calcolata e un intervallo target (es. media ± 10‑15%). Questo valore è la **lunghezza a cui il nuovo articolo dovrà attenersi**: né più corto né più lungo dei contributi già ospitati, così da risultare in linea con quel portale. Se non è stato possibile misurare alcun contenuto, dichiaralo e usa come default un intervallo di **500‑900 parole** (minimo 500, massimo 900), segnalando che è una stima non basata su dati del portale.
- **Struttura degli heading**: usa H2/H3? Quanti? Titoli descrittivi o creativi?
- **Elementi ricorrenti**: grassetto (quanto, su cosa), liste puntate/numerate (frequenti o rare), citazioni, box, immagini, tabelle.
- **Tipo di articolo prevalente**: news, guida/how-to, approfondimento, intervista, listicle, opinione. È il modello a cui l'articolo dovrà somigliare.
- **Attacco e chiusura**: come iniziano e come finiscono i pezzi (utile a evitare aperture che stonano con il portale).

### Step 4 — Come il portale inserisce i link

Osserva come sono trattati i link **in uscita** negli articoli del portale:
- I link cadono su anchor contestuali dentro il testo, o in formule tipo "leggi anche", "fonte"?
- Con che frequenza compaiono link esterni? Verso che tipo di risorse?

Questo serve a inserire il link del cliente in un modo coerente con le abitudini del portale, così da renderlo il più naturale possibile. (Ricorda: nell'articolo andrà comunque solo il link del cliente, salvo diversa indicazione dell'utente.)

---

## Output

---

**ANALISI PORTALE OSPITANTE — [nome/dominio portale]**

**SCHEDA PORTALE**
- Tipo: [verticale su X / generalista]
- Pubblico: [chi legge]
- Localizzazione: [nazionale/locale/internazionale]
- Sezione di destinazione: [categoria in cui andrà l'articolo e aspettativa del lettore]

**TONO DI VOCE**
- Registro: [formale/informale/tecnico/giornalistico…]
- Persona grammaticale: [tu / voi / impersonale] *(da replicare esattamente)*
- Tono: [divulgativo/autorevole/ironico/pratico…]
- Lessico: [tecnicismi sì/no, come vengono trattati, livello di linguaggio]

**FORMATO**
- Lunghezza target: [media ~X parole su N guest post/articoli misurati → intervallo target ~X‑Y parole] *(il nuovo articolo deve stare in questo intervallo; se non misurabile, indicare "stima non basata su dati del portale")*
- Struttura heading: [uso di H2/H3, numero, stile dei titoli]
- Elementi ricorrenti: [grassetto, liste, citazioni, immagini, tabelle]
- Tipo di articolo prevalente: [news/guida/approfondimento/listicle/intervista/opinione]
- Attacco e chiusura tipici: [come iniziano e finiscono i pezzi]

**GESTIONE DEI LINK NEL PORTALE**
- [Come cadono i link in uscita: anchor contestuali / formule dedicate; frequenza; tipo di risorse linkate]

**INDICAZIONI DI STILE PER LO SCRITTORE**
- [3‑6 regole operative sintetiche che l'articolo deve rispettare per sembrare nativo del portale: es. "dai del tu al lettore", "paragrafi brevi con un H2 ogni ~150 parole", "tono pratico, niente accademia", "grassetto solo sui concetti chiave", "lunghezza ~800 parole"]

**NOTE** *(solo se necessario)*
[Segnalazioni concise: portale in lingua diversa da quella richiesta, linea editoriale disomogenea, articoli non leggibili, sezione pertinente assente. Massimo 2-3 righe.]

---

## Regole critiche

- Il portale ospitante è il riferimento primario per il tono di voce: l'articolo deve sembrare scritto dalla sua redazione, non dal cliente.
- La persona grammaticale (tu/voi/impersonale) va rilevata e replicata esattamente: è uno degli scarti più evidenti tra un pezzo nativo e un guest post posticcio.
- Non inventare lo stile del portale: se gli articoli non sono leggibili, chiedi all'utente di incollarne 2‑3 rappresentativi.
- Analizza articoli il più possibile vicini per tipo e tema a quello che scriveremo: uno stile campionato da articoli non pertinenti è fuorviante.
- Misura sempre la lunghezza in parole dei guest post già presenti (o, se non distinguibili, degli articoli dello stesso tipo) e calcolane la media: è la lunghezza target del nuovo articolo. Il pezzo non deve essere né sensibilmente più corto né più lungo dei contributi già ospitati dal portale.
- Non valutare l'autorevolezza SEO del portale né se sia un buon sito partner: non è il compito di questa skill (quella scelta è a monte, fatta dall'utente).
- Le indicazioni di stile devono essere operative e sintetiche: sono istruzioni per chi scrive, non una descrizione del sito.
- Se il portale è in una lingua diversa da quella richiesta per l'articolo, segnalalo subito: è un'incongruenza da chiarire con l'utente.
