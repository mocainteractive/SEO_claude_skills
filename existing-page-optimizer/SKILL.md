---
name: existing-page-optimizer
description: >
  Orchestratore del flusso di ottimizzazione di un articolo del blog GIÀ esistente (non la creazione di uno nuovo). Usa questa skill quando l'utente vuole migliorare, aggiornare o far posizionare meglio una pagina già pubblicata di cui fornisce l'URL. Riusa le skill del flusso seo-blog-pipeline (keyword-analysis, serp-analysis, brand-analysis-and-connections, draft-writer, seo-optimizer, content-reviewer) adattandole all'ottimizzazione invece che alla scrittura da zero. I 5 step: 1) inquadra il perimetro (posizionamento attuale da Ahrefs + Google Search Console, link interni da e verso l'articolo, top 3 competitor); 2) verifica intento di ricerca e cosa cercano gli utenti; 3) individua o valuta le keyword target; 4) costruisce una scaletta di modifiche; 5) scrive il contenuto nuovo e ottimizza l'esistente. Trigger tipici: "ottimizza questo articolo del blog", "aggiorna/migliora la pagina [URL]", "far posizionare meglio questo articolo", "rilancia questo contenuto già pubblicato".
---

# Existing Page Optimizer

Questa skill orchestra il flusso di **ottimizzazione di un articolo blog già pubblicato**. A differenza di `seo-blog-pipeline` (che crea un articolo nuovo partendo da un topic), qui si parte da una pagina che esiste già: la si inquadra, si capisce perché non rende quanto potrebbe, e la si migliora intervenendo sul testo esistente e aggiungendo ciò che manca.

Riusa le skill atomiche del flusso esistente, ma con un'ottica diversa: non "cosa scrivo" ma "cosa cambio rispetto a quello che c'è già". Il risultato finale è l'articolo aggiornato più un changelog delle modifiche applicate.

---

## Quando usare questa skill (e quando no)

- **Usa `existing-page-optimizer`** quando esiste già una pagina/articolo pubblicato e l'obiettivo è migliorarne il posizionamento, l'attualità o la copertura. L'utente fornisce un URL.
- **Usa `seo-blog-pipeline`** quando l'articolo non esiste ancora e va creato da zero a partire da un topic o una keyword.

Connessione con il flusso di creazione: il controllo di cannibalizzazione di `serp-analysis` (Step 0 del seo-blog-pipeline) può concludersi con la decisione di **aggiornare/consolidare una pagina esistente** invece di crearne una nuova. Quando l'utente sceglie quella strada, il punto di ingresso naturale è proprio questa skill, usando come URL la pagina esistente individuata.

---

## Istruzioni di progetto (da verificare SEMPRE all'inizio)

Se il flusso viene eseguito all'interno di un progetto Claude, prima di partire controlla se il progetto contiene **istruzioni custom** e/o **knowledge di progetto** (linee guida editoriali, brand book, tone of voice, glossari, liste di termini da usare o evitare, vincoli legali, requisiti di formato, ecc.).

Se presenti, considerale parte integrante dei requisiti e applicale in tutte le fasi:

- Le istruzioni di progetto hanno **precedenza sui default generici** di queste skill (registro, formattazione, lunghezza, struttura, vocabolario, CTA, disclaimer).
- Restano subordinate a: (a) le scelte esplicite fatte dall'utente nella configurazione di sessione, e (b) la correttezza SEO e i checkpoint critici del flusso.
- In caso di **conflitto** tra un'istruzione di progetto e una buona pratica SEO o una scelta di sessione, non ignorarla in silenzio: segnala il conflitto all'utente e chiedi come procedere.
- Quando il TOV è già definito dalle istruzioni/knowledge di progetto, usalo come fonte primaria, integrando l'analisi del sito (e la voce dell'articolo esistente) solo per ciò che manca.

Se non sei in un progetto o non ci sono istruzioni/knowledge, prosegui con i default delle skill. In ogni caso, ricorda che l'articolo da ottimizzare ha già una sua voce: rispettala, salvo che sia in contrasto con il TOV del brand o con le istruzioni di progetto.

---

## Input richiesto

Prima di avviare il flusso, verifica di avere:

1. **URL dell'articolo da ottimizzare** (obbligatorio): l'indirizzo completo della pagina già pubblicata. È l'input centrale di tutto il flusso.
2. **Dominio del sito**: ricavato dall'URL dell'articolo. Serve per le chiamate Ahrefs/GSC a livello di dominio e per l'internal linking.
3. **Lingua target**: default italiano, salvo indicazione diversa (di norma coincide con la lingua dell'articolo esistente).
4. **Paese target**: default Italia (`it` per Ahrefs, `"Italy"` per DataForSEO), salvo diversa indicazione.
5. **Keyword target (opzionale)**: se l'utente ha già in mente la/le keyword su cui vuole far rendere l'articolo. Se non le fornisce, le ricava la Fase 3.
6. **Obiettivo/motivo dell'ottimizzazione (opzionale ma utile)**: es. "ha perso posizioni", "non ha mai performato", "è datato", "vogliamo intercettare anche la keyword X". Orienta le priorità della scaletta di modifiche.

Se manca l'URL dell'articolo (punto 1), chiedilo: senza non si può procedere. Se mancano lingua/paese, assumi i default e segnalalo.

---

## Configurazione di sessione (da chiedere SEMPRE all'inizio)

Prima della Fase 1, chiedi all'utente in un'unica domanda concisa:

1. **Obiettivo finale**: dove si ferma il flusso?
   - `scaletta di modifiche` → il flusso si ferma dopo la **Fase 4**: consegna la lista operativa di interventi, che applicherà un copywriter umano. Utile quando la riscrittura la fa una persona.
   - `articolo ottimizzato` (default) → il flusso procede fino alla **Fase 5** e consegna l'articolo aggiornato più il changelog.

2. **Validazione E‑E‑A‑T finale** (solo se l'obiettivo è `articolo ottimizzato`): eseguire anche la Fase 6 (`content-reviewer`) per ottenere punteggio E‑E‑A‑T, confronto con i competitor e raccomandazioni di distribuzione? `sì` (consigliato) / `no` (si ferma dopo l'ottimizzazione). Se l'obiettivo è `scaletta di modifiche`, questa domanda non si pone.

3. **Modalità di esecuzione**:
   - `interattiva` (default): tra una fase e l'altra mostra un mini‑riepilogo (3‑5 bullet) e chiede conferma per proseguire.
   - `autonoma`: procede senza conferme intermedie, salvo i checkpoint critici obbligatori (vedi sotto), che restano sempre attivi.

4. **Formato finale del deliverable** (da chiedere SEMPRE, non assumere mai): in che formato consegnare il deliverable (scaletta o articolo)? Proponi `markdown` (consigliato), `html`, `testo plain`, `documento Word (.docx)`, o altro indicato dall'utente. Usa `markdown` come fallback solo se l'utente dichiara di non avere preferenze. Non consegnare mai senza aver confermato il formato.

5. **Ambito per l'internal linking** (usato nella Fase 3, `brand-analysis-and-connections`):
   - `automatico` (default): mappa l'intero sito via robots.txt + sitemap e seleziona i contenuti correlati ovunque si trovino.
   - `cartella/sezione specifica`: l'utente indica uno o più percorsi (es. `/blog/marketing/`) da esplorare in modo esaustivo, così non si perdono articoli nascosti nei blog multi‑categoria. La scansione del resto del sito per le pagine strategiche resta attiva.

Memorizza le scelte e applicale per tutta la sessione. Non ripetere le domande nelle fasi successive.

---

## Flusso di esecuzione

Esegui le fasi in quest'ordine. Ogni fase riceve come contesto l'output di tutte le precedenti.

### Fase 1 — INQUADRAMENTO DEL PERIMETRO DEL CONTENUTO

Obiettivo: fotografare lo stato attuale dell'articolo e del suo contesto competitivo. È la base su cui si decidono tutte le modifiche. Si compone di cinque rilevazioni.

#### 1a — Lettura dell'articolo esistente (WebFetch)

Recupera l'URL dell'articolo con `WebFetch` ed estrai lo **stato attuale**:
- Metadati: title tag e meta description attuali, H1.
- Struttura: gerarchia completa degli heading (H1/H2/H3) e di cosa parla ogni sezione.
- Lunghezza stimata in parole.
- Argomenti coperti e profondità di ciascuno.
- **Link interni in uscita** già presenti nel corpo: destinazione e anchor text (sono i link "da" l'articolo).
- CTA presenti e loro posizione.
- Segnali di freschezza: data di pubblicazione/aggiornamento, dati o riferimenti temporali potenzialmente datati.

Questa lettura è la "versione di partenza" con cui confronterai tutto il resto.

#### 1b — Posizionamento attuale su Ahrefs (per la singola pagina)

Usa `site-explorer-organic-keywords` puntando **esattamente all'URL dell'articolo**:
- `target`: l'URL completo dell'articolo
- `mode`: `"exact"` (analizza la singola pagina, non tutto il dominio)
- `country`: `"it"` (default)
- `date`: data odierna (YYYY-MM-DD)
- `date_compared`: una data di 3‑6 mesi fa (YYYY-MM-DD), per leggere il **trend**
- `select`: `"keyword,best_position,best_position_diff,best_position_prev,volume,sum_traffic,keyword_difficulty,serp_features,is_informational,is_commercial,is_transactional"`
- `order_by`: `"sum_traffic:desc"`
- `limit`: 100

Da qui ricava:
- Le keyword per cui l'articolo **già rankka** e con quale posizione.
- Il **trend** (`best_position_diff`): l'articolo sta salendo, è stabile o sta perdendo posizioni?
- Le **keyword "quasi in prima pagina"** (posizioni circa 11‑20): sono le opportunità più immediate, spesso bastano interventi mirati per portarle in top 10.
- Il traffico stimato (`sum_traffic`) e la difficoltà (`keyword_difficulty`).

Opzionale: `site-explorer-url-rating-history` sull'URL per vedere l'andamento dell'autorità della pagina nel tempo.

#### 1c — Posizionamento reale su Google Search Console (gsc-moca, fonte primaria)

GSC dà i dati di **prima parte** (impression, clic, CTR, posizione media reali) per la pagina: più affidabili di qualsiasi stima. Usa il MCP `gsc-moca` sulla proprietà legata al dominio.

**a) Risolvi la proprietà.** Chiama `get_properties` e individua la proprietà che corrisponde al dominio (priorità `sc-domain:` > `https://www.` > `https://` > `http://`). Se l'utente ha dato un nome cliente, usa `resolve_client` con `autoSelectMain: true`. Se nessuna proprietà è accessibile, **salta la parte GSC**, segnalalo e prosegui con i soli dati Ahrefs (1b).

**b) Estrai le query della pagina.** Usa `get_query_page_combinations` filtrando sull'URL dell'articolo:
- `siteUrl`: la proprietà risolta
- `startDate`/`endDate`: ultimi **3 mesi** (oggi − 90 giorni → oggi)
- filtra le righe sulla pagina target (l'URL dell'articolo)
- `minImpressions`: `10`
- `includeFreshData`: `true`

Da qui ricava, per la pagina:
- Le **query reali** che le portano impression e clic (il linguaggio vero degli utenti).
- Le query con **molte impression ma pochi clic / CTR basso**: segnale che il title/meta non sono abbastanza attraenti, oppure che la posizione media è troppo bassa. Sono candidate a ottimizzazione di metadati e/o contenuto.
- Le query in **posizione media 5‑15**: opportunità di spinta verso la prima pagina/top 3.

**Lettura corretta dei dati GSC:** per i totali della pagina usa gli strumenti dedicati (es. `get_property_stats` per il contesto sito); **non sommare** le righe di `get_query_page_combinations` (le query anonimizzate rendono la somma inferiore al reale). La `position` è una **media** del periodo, non la posizione attuale. Con `includeFreshData: true` gli ultimi 2‑3 giorni possono ancora cambiare.

Incrocia GSC (primario) e Ahrefs (complemento): GSC dice cosa succede davvero, Ahrefs aggiunge keyword che GSC non mostra e il contesto competitivo.

#### 1d — Internal linking da e verso l'articolo

Due direzioni distinte:

- **Link in entrata (verso l'articolo).** Usa `site-explorer-pages-by-internal-links` con `target` = URL dell'articolo, `mode` = `"exact"`, `select` = `"url_from_plain,anchor,is_content,is_dofollow,links_to_target,title_source"`, `order_by` = `"links_to_target:desc"`, `limit` 100. Ottieni le pagine del sito che già linkano l'articolo, con anchor text e se il link è dentro il contenuto. **Pochi o nessun link interno in entrata = articolo poco supportato** dal resto del sito: è una delle leve più sottovalutate per farlo salire.
- **Link in uscita (dall'articolo).** Prendili dalla lettura di 1a (i link interni presenti nel corpo). Valuta se sono pochi, datati, o se puntano a pagine poco pertinenti.

Tieni separate le due liste: descrivono lo **stato attuale** dei collegamenti. Le **nuove** opportunità di link (in entrata e in uscita) le produce la Fase 3 con `brand-analysis-and-connections`.

#### 1e — Top 3 competitor sulla keyword principale + controllo consolidamento

Richiama la skill **`serp-analysis`** sulla keyword principale dell'articolo (quella desunta da 1a/1b/1c o fornita dall'utente), con due adattamenti per questo flusso:

- **Competitor: bastano i primi 3** risultati editoriali organici sulla keyword principale (non 5‑7). Per ciascuno raccogli, come da `serp-analysis`: formato, struttura degli heading, lunghezza, contenuti visivi, angolazione, gap. Servono come termine di paragone per capire cosa manca al nostro articolo.
- **Controllo consolidamento (reinterpretazione dello Step 0 cannibalizzazione).** Qui non stiamo creando una pagina nuova: la pagina è quella che vogliamo far rankare. Il rischio rilevante è l'**opposto**: che il sito abbia **altre pagine in competizione con questa** sulla stessa keyword. Usa GSC (`get_query_page_combinations` con `analyzeCannibalization: true`, oppure più pagine sulla stessa query) e Ahrefs per verificarlo. Se emergono più pagine del sito che competono sulla keyword target, è un **checkpoint**: segnalalo e chiedi se consolidare (unire i contenuti concorrenti in questo articolo, reindirizzare le pagine deboli, o de‑ottimizzarle). La decisione cambia la scaletta di modifiche.

Mantieni anche, da `serp-analysis`, il controllo della presenza di **AI Overview** sulla keyword principale (DataForSEO, `serp_organic_live_advanced` con `load_async_ai_overview: true`): le osservazioni servono in Fase 2 e nella scaletta.

**Checkpoint critico (consolidamento):** se il sito ha più pagine in competizione sulla keyword target, fermati e chiedi all'utente come procedere prima di continuare. È un punto di stop obbligatorio in entrambe le modalità.

---

### Fase 2 — INTENTO DI RICERCA E COSA CERCANO GLI UTENTI

Obiettivo: verificare che l'articolo risponda all'intento giusto e mappare cosa cercano davvero gli utenti sul tema. Si appoggia agli output di `serp-analysis` (Fase 1e) e ai dati GSC (Fase 1c), integrati dalla logica di `keyword-analysis`.

1. **Verifica dell'intento.** Confronta l'intento dominante della SERP attuale (da `serp-analysis`) con ciò che l'articolo esistente fa. Tre casi:
   - L'articolo è allineato all'intento della SERP → si ottimizza nel merito.
   - L'articolo è disallineato (es. è informativo ma la SERP è ormai transazionale, o viceversa) → **segnalalo come checkpoint**: forse non basta ottimizzare, va ripensato l'angolo. Chiedi conferma prima di proseguire.
   - L'intento è misto → si procede, segnalando come bilanciare le sezioni.
2. **Cosa cercano gli utenti.** Combina tre fonti:
   - **Query reali da GSC** (Fase 1c): è la domanda concreta che già intercetta la pagina. È la fonte più preziosa perché riflette utenti veri.
   - **Domande PAA** raccolte da `serp-analysis` sulla keyword principale.
   - **Search suggestions / correlate** (via `keyword-analysis`, Chiamata 3) per cogliere sfaccettature non ancora coperte.
3. **AI Overview.** Se presente sulla keyword (rilevato in Fase 1e), riporta le osservazioni operative: l'articolo deve offrire più valore della sintesi AI, essere strutturato per essere citato (risposta diretta in apertura di sezione, dati verificabili, heading formulati come la domanda), e coprire i sotto‑aspetti che l'AIO considera centrali.

Output della fase: intento confermato o rivisto + una mappa di "cosa cercano gli utenti" (domande e sotto‑temi) che alimenta sia la selezione keyword (Fase 3) sia la scaletta di modifiche (Fase 4).

---

### Fase 3 — KEYWORD TARGET SU CUI LAVORARE

Obiettivo: definire le keyword su cui spingere l'articolo. Usa la skill **`keyword-analysis`**, con un comportamento che dipende da cosa ha fornito l'utente.

- **Se l'utente NON ha fornito keyword**: esegui `keyword-analysis` completa, usando come seme il topic dell'articolo **e** le keyword che la pagina già intercetta (da Fase 1b Ahrefs e 1c GSC). Produci keyword primaria, secondarie, correlate, domande e long‑tail, con volumi e intent.
- **Se l'utente HA già fornito una o più keyword**: non saltare l'analisi. **Valuta** le keyword fornite recuperandone volume, intent e difficoltà (Ahrefs, Chiamata 1 di `keyword-analysis`), conferma quale può essere la primaria, e — se servono per coprire il tema o colmare gap — **proponi keyword secondarie** aggiuntive. Se una keyword fornita ha intento incompatibile con un articolo blog (es. puramente transazionale), segnalalo.

**Priorità specifiche di questo flusso (incrocio con la Fase 1):**
- Le keyword su cui l'articolo è **già "quasi in prima pagina"** (pos. 11‑20 su Ahrefs, o posizione media 5‑15 su GSC) sono **priorità alta**: piccoli interventi mirati possono produrre i guadagni più rapidi.
- Le keyword con **molte impression e pochi clic** su GSC indicano un problema di metadati o di match contenuto/intento: vanno indirizzate.
- Identifica i **gap di keyword**: termini pertinenti per cui i top 3 competitor rankano e questo articolo no (dai dati di `serp-analysis` e dalle correlate). Sono i candidati per nuove sezioni.

**Opportunità di internal linking (riuso di `brand-analysis-and-connections`).** In questa fase esegui anche `brand-analysis-and-connections` sull'URL del sito, applicando l'ambito di internal linking scelto in configurazione, per ottenere:
- il **TOV** del brand, da usare come riferimento per le riscritture (insieme alla voce già presente nell'articolo);
- **nuovi link in uscita** da aggiungere nell'articolo (contenuti correlati + pagine strategiche), con anchor text suggeriti (Step 2‑3 della skill);
- **nuovi link in entrata da creare** verso l'articolo, cioè altri articoli del blog dove conviene inserire un rimando a questo (Step 4 della skill).

Distingui sempre questi **nuovi** link (Fase 3) dai link **già esistenti** rilevati in Fase 1d.

---

### Fase 4 — SCALETTA DI MODIFICHE

Obiettivo: tradurre tutto ciò che è emerso in una **lista operativa e prioritizzata di interventi** sull'articolo. È il documento pivot del flusso, l'equivalente del brief ma orientato alla modifica: dice esattamente cosa cambiare, dove e perché. Sostituisce `content-brief-builder` (che serve a costruire un articolo nuovo).

Costruisci la scaletta confrontando lo **stato attuale** (Fase 1a) con lo **stato ideale** (gap e formato dai competitor, intento e domande utenti dalla Fase 2, keyword target dalla Fase 3, opportunità di link dalla Fase 3).

Organizza gli interventi per tipo:

1. **Metadati**
   - H1, title tag, meta description: confermare o riscrivere. Riscrivi quando non contengono la keyword primaria, quando GSC mostra CTR basso su query ad alte impression, o quando non sono orientati al clic.
   - **Verifica via script obbligatoria**: dopo aver proposto nuovi H1/title/meta, esegui un breve script Python (Bash tool) per misurarne la lunghezza esatta (H1 ≤ 55, meta title ≤ 55, meta description ≤ 160 caratteri). Riscrivi e ri‑esegui finché rientrano. Non riportare versioni non verificate.

2. **Struttura del contenuto** — per ogni intervento indica: **azione**, **punto** (quale sezione/H2 esistente), **perché**, **priorità** (alta/media/bassa).
   - `AGGIUNGI`: nuove sezioni per coprire gap, PAA o sotto‑temi non trattati (e keyword target non presidiate).
   - `ESPANDI`: sezioni troppo superficiali rispetto ai competitor o all'intento.
   - `RISCRIVI`: sezioni datate, fuori tono, deboli su keyword, o con scrittura da AI da umanizzare.
   - `UNISCI`/`RIMUOVI`: sezioni ridondanti, fuori tema, o (in caso di consolidamento) contenuti da assorbire da altre pagine del sito.
   - `RIORDINA`: se la sequenza attuale non segue l'intento o non mette in apertura la risposta diretta (utile anche per l'AI Overview).
   - `AGGIORNA`: dati, cifre, riferimenti temporali, screenshot datati.

3. **Keyword da integrare**: per ciascuna, dove inserirla naturalmente (in quale sezione/heading). Dai priorità alle keyword "quasi in prima pagina" della Fase 3.

4. **Link interni** (solo nuovi, dalla Fase 3, separati per direzione):
   - *In uscita da aggiungere*: contenuto/pagina di destinazione + anchor text + punto di inserimento.
   - *In entrata da creare*: articolo esistente da cui linkare + anchor text (nell'articolo esistente) verso questo articolo.

5. **CTA e conversione**: CTA da aggiungere, spostare o riscrivere, collegate alle pagine strategiche della Fase 3.

6. **Freschezza / E‑E‑A‑T**: segnali da rafforzare (autore, fonti, dati recenti), specie se c'è AI Overview o il topic è YMYL.

Ogni voce deve essere concreta e azionabile: non "migliorare l'introduzione" ma "riscrivere l'introduzione mettendo in apertura la risposta diretta alla query 'come fare X', inserendo la keyword primaria entro le prime 2 righe — priorità alta perché GSC mostra 1.200 impression/mese in pos. media 8".

**Checkpoint critico (approvazione scaletta):** mostra la scaletta completa all'utente e chiedi conferma esplicita prima di toccare il testo. È l'ultimo momento per cambiare strategia prima della riscrittura. Punto di stop obbligatorio in entrambe le modalità.

Se l'obiettivo di sessione è `scaletta di modifiche`, **consegna qui** la scaletta nel formato richiesto e termina il flusso.

---

### Fase 5 — SCRITTURA DEL NUOVO E OTTIMIZZAZIONE DELL'ESISTENTE

Obiettivo: applicare la scaletta approvata producendo l'articolo aggiornato. Combina due skill:

- **`draft-writer`** per i contenuti **nuovi**: scrive le sezioni da `AGGIUNGI` ed `ESPANDI` seguendo il TOV (Fase 3) e la voce dell'articolo esistente, integrando keyword e link come da scaletta. Valgono tutte le sue regole di qualità: voce umana, niente trattini come punteggiatura inline, niente sezione "FAQ" finale (le PAA si integrano come heading o risposte inline), capitalizzazione corretta dei titoli, keyword integrate e non forzate.
- **`seo-optimizer`** per il contenuto **esistente**: applica gli interventi `RISCRIVI`/`AGGIORNA`/`RIORDINA`, la de‑AI (umanizzazione delle frasi), la distribuzione keyword, i metadati (con verifica caratteri via script), e l'inserimento dei link mancanti sugli anchor corretti.

Mantieni la coerenza stilistica: il testo nuovo e quello esistente devono leggersi come scritti dalla stessa mano. Non riscrivere sezioni che la scaletta non ha toccato, salvo per de‑AI evidente.

**Output della Fase 5 — articolo aggiornato + changelog.** Consegna nel formato richiesto, con questa struttura:

1. **Blocco "KEYWORD UTILIZZATE"** in testa: keyword (primaria + secondarie + long‑tail) effettivamente presenti nell'articolo aggiornato, ciascuna con volume mensile.
2. **L'articolo completo aggiornato** (versione integrale già modificata, dall'H1 alla CTA finale), pronto da incollare nel CMS.
3. **Blocco "CHANGELOG MODIFICHE"** accodato: elenco di cosa è stato fatto, voce per voce, riprendendo la scaletta (sezioni aggiunte/espanse/riscritte/unite/rimosse/aggiornate, metadati cambiati, keyword integrate, link aggiunti). Una riga per intervento, così chi pubblica sa esattamente cosa è cambiato rispetto alla versione online.
4. **Blocco "LINK IN ENTRATA DA CREARE"** accodato: articoli esistenti dove aggiungere un link verso questo articolo, con anchor text suggerito (dalla Fase 3). È un'azione operativa post‑pubblicazione. Se non ce ne sono di adatti, indicalo in una riga.

---

### Fase 6 — VALIDAZIONE E‑E‑A‑T (opzionale)

*Solo se l'obiettivo è `articolo ottimizzato` e l'utente ha scelto la validazione finale.*

Esegui la skill **`content-reviewer`** sull'articolo aggiornato, passandole come contesto la keyword‑analysis (Fase 3), la serp‑analysis con i competitor (Fase 1e) e la scaletta di modifiche (Fase 4, in luogo del brief). Produce, come blocco separato accodato in fondo:
- punteggio E‑E‑A‑T per criterio + complessivo;
- confronto con i competitor della SERP (copertura, gap coperti, differenziatori);
- raccomandazioni di distribuzione multicanale.

Se il punteggio complessivo è sotto 5, segnala che l'articolo non è ancora pronto e indica le priorità di intervento.

---

## Gestione dei checkpoint

**Checkpoint critici (sempre attivi, in entrambe le modalità):**
1. **Disallineamento di intento (Fase 2):** se l'articolo risponde a un intento diverso da quello che la SERP premia oggi, fermati e chiedi se ottimizzare comunque o ripensare l'angolo.
2. **Consolidamento / cannibalizzazione interna (Fase 1e):** se il sito ha più pagine in competizione sulla keyword target, fermati e chiedi se consolidare prima di proseguire.
3. **Approvazione della scaletta (Fase 4):** non toccare il testo senza approvazione esplicita della scaletta di modifiche.

**Mini‑checkpoint (solo in modalità interattiva):** dopo le Fasi 1, 2, 3 e 5 mostra un mini‑riepilogo di 3‑5 bullet e chiedi se procedere. In modalità autonoma questi sono omessi; i tre checkpoint critici restano.

---

## Modalità di esecuzione parziale

- Se l'utente fornisce già un'analisi di posizionamento completa (Ahrefs + GSC) della pagina, puoi alleggerire la Fase 1 ma esegui comunque la lettura dell'articolo (1a) e il confronto competitor (1e).
- Se l'utente fornisce già le keyword target con volumi e intent, in Fase 3 valuta e integra invece di rifare l'analisi da zero (vedi sopra).
- Se l'utente vuole solo la scaletta di modifiche, imposta l'obiettivo su `scaletta` e fermati alla Fase 4.

Fornire l'URL e/o le keyword **non** equivale a saltare le fasi di analisi: sono input, non output di fase. Le Fasi 1‑3 vanno comunque eseguite per produrre una scaletta fondata.

---

## Regole critiche

- L'input centrale è l'**URL di una pagina esistente**: senza, non si parte. Questa skill non crea articoli nuovi (per quello c'è `seo-blog-pipeline`).
- GSC (`gsc-moca`) è la fonte primaria del posizionamento reale della pagina (impression, clic, CTR, posizione media); Ahrefs è complemento e fallback. Se la proprietà GSC non è accessibile, segnalalo e prosegui con Ahrefs.
- Per l'analisi della singola pagina usa Ahrefs in `mode: "exact"` sull'URL dell'articolo, con `date_compared` per leggere il trend di posizione.
- Tieni sempre separati i link **già esistenti** (Fase 1d, stato attuale) dai link **nuovi da creare** (Fase 3, `brand-analysis-and-connections`), e tra questi i link in uscita da quelli in entrata.
- Dai priorità alle keyword su cui la pagina è già "quasi in prima pagina" e alle query ad alte impression/basso CTR: sono i guadagni più rapidi.
- Il controllo di consolidamento (Fase 1e) è obbligatorio: se più pagine del sito competono sulla stessa keyword, fermati e chiedi come procedere.
- Chiedi sempre il formato dell'output all'inizio e attendi la risposta: non assumere mai il markdown di default.
- Non toccare il testo prima dell'approvazione della scaletta (Fase 4): è il checkpoint di non ritorno.
- Rispetta la voce dell'articolo esistente e il TOV del brand; le riscritture non devono stravolgere lo stile salvo conflitto con TOV o istruzioni di progetto.
- Non riscrivere sezioni non previste dalla scaletta, salvo de‑AI evidente. Non allungare per allungare: ogni aggiunta deve coprire un bisogno reale (gap, PAA, keyword, intento).
- Mai una sezione finale "Domande frequenti"/"FAQ" come elenco: le PAA si integrano nel corpo. Mai trattini come punteggiatura inline. Titoli con maiuscola solo sulla prima parola e sui nomi propri.
- Se il flusso gira in un progetto Claude con istruzioni/knowledge, rispettale: prevalgono sui default ma restano subordinate alle scelte di sessione e alla correttezza SEO. In caso di conflitto, segnala e chiedi.
- Consegna sempre, nell'obiettivo `articolo ottimizzato`, l'articolo completo aggiornato **più** il changelog delle modifiche: il changelog è parte del deliverable, non un opzionale.
