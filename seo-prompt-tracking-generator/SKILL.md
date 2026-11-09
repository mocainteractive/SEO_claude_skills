---
name: seo-prompt-tracking-generator
description: "Trasforma keyword SEO (export Google Search Console, lista incollata o connettore GSC) e info su brand e competitor in prompt conversazionali per il tracking GEO e la Sentiment Analysis su ChatGPT, Perplexity, Gemini e Claude. Applica la Matrice 4x4: 4 categorie (Brand Discovery, Comparative / Versus, Problem / Solution, Customer Care / Crisis) per 4 varianti di prompt per keyword. Restituisce i prompt in chat, in una tabella per categoria. Trigger: \"genera i prompt di tracking per il brand X\", \"trasforma queste keyword GSC in prompt per LLM\", \"prompt per monitorare il sentiment del brand su ChatGPT\", \"prompt set per GEO tracking\". Non esegue i prompt e non misura il sentiment."
---

# SEO PROMPT TRACKING GENERATOR

Questa skill converte keyword SEO "secche" (come le digita un utente su Google) in **domande naturali** come le porrebbe un utente a un assistente AI, organizzate per misurare due cose:

- **Visibilità GEO**: il brand viene citato, raccomandato o linkato come fonte quando l'utente chiede qualcosa sul settore?
- **Sentiment**: quando il brand viene citato, in che tono ne parla il modello (positivo, neutro, critico) e rispetto a quali competitor?

Il destinatario dell'output è il team SEO / GEO che deve caricare i prompt in un tool di monitoraggio (Peec AI, Profound, Otterly, Semrush AI Toolkit, SE Ranking AI, oppure un foglio di test manuale) e interrogare periodicamente ChatGPT, Perplexity, Gemini e Claude.

**Cosa NON fa questa skill:**

- Non interroga gli LLM e non calcola il sentiment: produce solo il set di prompt.
- Non inventa keyword: parte sempre da keyword reali fornite dall'utente o lette da GSC. Può solo derivare varianti conversazionali.
- Non inventa difetti, scandali o problemi del brand: i prompt della categoria Customer Care / Crisis si basano sui temi presenti nelle keyword o indicati dall'utente.

---

## FILE DELLA SKILL

| File | Quando leggerlo |
|---|---|
| `references/matrice-4x4.md` | Prima della Fase 4. Definisce le 4 categorie, le 4 varianti di prompt e i template per ciascuna cella. |
| `references/regole-conversione.md` | Prima delle Fasi 3 e 4. Regole per classificare le keyword e trasformarle da keyword secche a prompt conversazionali, con checklist di qualità. |
| `references/esempio-output.md` | Prima della Fase 5. Esempio completo di output (riepilogo e tabelle) da usare come riferimento di formato. |
| `templates/keyword-input-template.csv` | Da proporre all'utente se non ha un file pronto, come formato di input. |

---

## FASE 0, WIZARD DI BRIEF

Prima di generare qualsiasi prompt raccogli il brief. La **prima domanda è sempre lo Step 0.0** (quantità di prompt), da porre da sola e prima di ogni altra. Per gli step successivi, se un'informazione è già presente nel contesto (messaggio dell'utente, file allegato, conversazione precedente) **non richiederla**: riportala nel riepilogo della Fase 0.6 per conferma. Fai le domande mancanti in un unico blocco con AskUserQuestion, oppure in chat se servono risposte libere.

### STEP 0.0, QUANTITÀ DI PROMPT (SEMPRE LA PRIMA DOMANDA)

Prima di qualsiasi altra domanda, e anche se l'utente ha già fornito brand, keyword o file, chiedi quanti prompt vuole generare in totale. Unica eccezione: se l'utente ha già indicato il numero nel messaggio, non richiederlo e riportalo nel riepilogo.

Usa AskUserQuestion con queste opzioni (l'utente può sempre scrivere un numero diverso):

- **32 prompt**: set di prova, 2 keyword con matrice completa;
- **64 prompt**: set compatto, 4 keyword con matrice completa;
- **160 prompt**: set standard, 10 keyword con matrice completa;
- **400 prompt**: set esteso, 25 keyword con matrice completa.

Il numero scelto, chiamato **N**, guida tutta la generazione secondo le regole della sezione "Distribuzione dei prompt" della Fase 4. Ogni keyword con la matrice completa produce 16 prompt, quindi le keyword da lavorare sono **K = N / 16, arrotondato per eccesso**.

### STEP 0.1, BRAND PRINCIPALE

- Nome del brand (e varianti con cui viene scritto o cercato: acronimi, nome del dominio, nome del prodotto di punta).
- Dominio del sito.

### STEP 0.2, COMPETITOR

- Nomi dei competitor da includere (consigliati 3-5).
- Se l'utente non li ha pronti, proponi di ricavarli dalle keyword Versus del dataset o dalle query GSC che contengono nomi di altri brand, e chiedi conferma prima di usarli.

### STEP 0.3, SETTORE E CONTESTO

- Settore / nicchia di riferimento (es. "e-commerce arredamento outdoor", "software gestionale per studi dentistici").
- Target principale (B2C, B2B, professionisti, fascia di prezzo) se rilevante.
- Prodotti o servizi principali.
- Mercato geografico (paese, eventuale area locale).

### STEP 0.4, LINGUA DEI PROMPT

Chiedi **sempre** in che lingua generare i prompt. Non assumere un default. Se l'utente indica più lingue, genera un set completo per ciascuna lingua (non tradurre letteralmente: adatta formule e riferimenti al mercato, vedi `references/regole-conversione.md`).

### STEP 0.5, SORGENTE DELLE KEYWORD

Le keyword possono arrivare da tre fonti, anche combinate:

1. **File** (CSV o XLSX esportato da Google Search Console, Ahrefs, Semrush, SEOZoom). Leggi il file e individua le colonne utili: `query` / `keyword`, `clicks`, `impressions`, `position`, ed eventuale colonna di tipo (`Brand`, `Non-Brand`, `Versus`, `Long-tail`).
2. **Lista incollata** in chat, anche già suddivisa per tipo.
3. **Connettore Google Search Console** (tool `mcp__GSC-MCP__*`), solo se l'utente lo chiede o lo conferma:
   - usa `list_clients` / `resolve_client` per individuare la property del brand;
   - usa `get_search_queries` (o `get_search_analytics` con dimensione query) sugli ultimi 3 mesi, salvo diversa indicazione;
   - recupera query, click, impression e posizione media.

Se l'utente non ha un file, proponi il formato `templates/keyword-input-template.csv`.

**Selezione delle keyword.** Servono K keyword (calcolate dallo Step 0.0).

- Se il dataset contiene **più di K keyword**, chiedi all'utente come selezionarle:
  - top K per click o impression (default proposto);
  - un numero bilanciato per tipo (es. su 10 keyword: 2 Brand, 2 Versus, 4 Non-Brand, 2 Long-tail);
  - lista scelta a mano dall'utente.
- Se il dataset contiene **meno di K keyword**, il numero N non è raggiungibile senza ripetere prompt. Dillo all'utente con il massimo ottenibile (keyword disponibili x 16) e chiedi se preferisce ridurre N a quel valore oppure aggiungere altre keyword.

### STEP 0.6, RIEPILOGO E CONFERMA

Riassumi il brief e chiedi conferma prima di procedere:

```
BRIEF PROMPT TRACKING
- Prompt da generare: [N] (BD [..], CV [..], PS [..], CC [..])
- Brand: [...] (varianti: [...]) , dominio: [...]
- Competitor: [...]
- Settore / nicchia: [...]
- Mercato: [...]
- Lingua dei prompt: [...]
- Sorgente keyword: [file / lista / GSC, periodo]
- Keyword da lavorare: [K] (criterio di selezione: [...])
- LLM target: ChatGPT, Perplexity, Gemini, Claude

Procedo con la generazione? (sì/no)
```

---

## FASE 1, PULIZIA DEL DATASET

1. Normalizza le keyword: minuscolo, spazi singoli, rimozione di duplicati e varianti identiche (singolare/plurale, con o senza accento).
2. Escludi le query non utilizzabili e dichiaralo nel riepilogo finale:
   - query di navigazione pura senza contenuto (`login`, `area riservata`, `www.brand.it`);
   - query di altri brand non presenti nella lista competitor e non del settore;
   - query offensive, spam o non pertinenti.
3. Se presenti, conserva click, impression e posizione: servono a ordinare l'output.

---

## FASE 2, CLASSIFICAZIONE DELLE KEYWORD

Se il dataset non è già suddiviso, assegna a ciascuna keyword un **Tipo** applicando le regole di `references/regole-conversione.md` (sezione "Classificazione"):

| Tipo | Definizione |
|---|---|
| **Brand** | Contiene il nome del brand o una sua variante. |
| **Versus** | Contiene il brand e/o un competitor insieme a segnali di confronto (`vs`, `o`, `meglio`, `alternativa`, `differenza`, `confronto`). |
| **Non-Brand** | Keyword generica di settore, senza nomi di brand, con 1-3 parole. |
| **Long-tail** | Keyword generica di 4 o più parole, spesso in forma di domanda o con specificazioni (uso, prezzo, luogo, target). |

Assegna inoltre un **segnale di criticità** (Sì/No) se la keyword contiene termini da Customer Care / Crisis (`reso`, `rimborso`, `recensioni negative`, `truffa`, `non funziona`, `assistenza`, `reclamo`, `ritardo`, `opinioni`, `reddit`, `trustpilot`). Le keyword con segnale = Sì alimentano in via prioritaria la categoria Customer Care / Crisis.

Mostra all'utente un riepilogo compatto della classificazione (conteggio per tipo ed elenco delle keyword ambigue) e chiedi conferma solo sulle ambigue.

---

## FASE 3, MAPPATURA KEYWORD, CATEGORIA, INTENT

Ogni keyword genera prompt in **tutte e 4 le categorie** della matrice, ma con un peso diverso. La categoria **primaria** è quella più coerente con il tipo di keyword e determina l'ordine nell'output:

| Tipo keyword | Categoria primaria | Funnel / Intent |
|---|---|---|
| Brand | Brand Discovery & Awareness | Awareness, navigazionale/informativo |
| Brand + segnale criticità | Customer Care / Crisis | Post-acquisto, supporto |
| Versus | Comparative / Versus | Consideration, commerciale |
| Non-Brand | Problem / Solution | Awareness / Consideration, informativo |
| Long-tail | Problem / Solution (o Comparative se contiene "migliore", "quale scegliere") | Consideration / Decision |

Per le keyword Non-Brand e Long-tail le categorie Brand Discovery e Customer Care si costruiscono **innestando il brand sul tema della keyword** (es. keyword `divano da esterno resistente` diventa "[Brand] fa divani da esterno davvero resistenti?").

Le regole complete di mappatura sono in `references/regole-conversione.md`.

---

## FASE 4, GENERAZIONE DEI PROMPT (MATRICE 4x4)

Leggi `references/matrice-4x4.md` e, per ogni keyword selezionata, genera **4 prompt per ciascuna delle 4 categorie**, uno per ogni variante, rispettando il totale N scelto nello Step 0.0:

| Variante | Formula | Scopo |
|---|---|---|
| **V1, Domanda diretta** | Domanda secca, come la scriverebbe l'utente | Risposta base del modello |
| **V2, Raccomandazione** | Richiesta di consiglio, lista o classifica | Misura chi viene raccomandato e in che ordine |
| **V3, Scenario / persona** | Domanda calata in un caso d'uso concreto con vincoli (budget, uso, luogo) | Misura la pertinenza percepita del brand |
| **V4, Fonti e prova sociale** | Richiesta di opinioni, recensioni, esperienze, fonti | Misura sentiment e fonti citate (Reddit, Trustpilot, Google, stampa) |

### DISTRIBUZIONE DEI PROMPT

Il totale consegnato deve essere **esattamente N**, salvo duplicati accorpati da dichiarare nel riepilogo.

1. **Quota per categoria.** Dividi N in parti uguali tra le 4 categorie (N / 4). Se resta un avanzo, assegna i prompt in più in quest'ordine: Problem / Solution, Comparative / Versus, Brand Discovery, Customer Care / Crisis.
2. **Ordine delle keyword.** Lavora le K keyword in ordine di priorità (click, poi impression). Le prime keyword ricevono la matrice completa (16 prompt).
3. **Ultima keyword parziale.** Se N non è multiplo di 16, l'ultima keyword riceve solo i prompt che mancano per arrivare a N, scegliendo le categorie che non hanno ancora raggiunto la propria quota e, dentro ogni categoria, le varianti nell'ordine V1, V2, V3, V4.
4. **N inferiore a 16.** Usa una sola keyword per categoria, scegliendo per ciascuna categoria la keyword più coerente (vedi Fase 3), e assegna le varianti in ordine V1, V2, V3, V4 fino a esaurire la quota.
5. **Più lingue.** Se lo Step 0.4 indica più lingue, N vale per ciascuna lingua. Dichiaralo nel riepilogo dello Step 0.6 (es. 64 prompt x 2 lingue = 128 righe).

### REGOLE NON NEGOZIABILI

1. **Unbranded resta unbranded.** Nella categoria Problem / Solution i prompt **non contengono mai** il nome del brand né dei competitor: servono a misurare se il brand emerge spontaneamente (share of voice organico).
2. **Comparative.** Almeno 2 delle 4 varianti nominano esplicitamente brand e competitor; le altre usano formule aperte ("alternative a [Competitor]", "chi è meglio per [esigenza]") per misurare il posizionamento relativo.
3. **Customer Care / Crisis** è sempre branded e affronta solo temi plausibili per il settore o presenti nelle keyword: non inventare scandali o accuse.
4. **Linguaggio naturale.** Ogni prompt è una frase completa che un utente reale scriverebbe in chat: no elenchi di keyword, no operatori di ricerca, no virgolette forzate.
5. **Neutralità.** I prompt non devono suggerire la risposta né contenere giudizi a favore del brand ("perché [Brand] è il migliore?" è vietato; "[Brand] è una buona scelta per...?" è corretto).
6. **Lunghezza.** Tra 8 e 35 parole. Le varianti V3 possono arrivare a 45 parole.
7. **Niente duplicati.** Se due keyword simili producono lo stesso prompt, tienine uno e associa entrambe le keyword nella colonna Keyword SEO separate da ` | `.
8. **Niente trattino lungo** nei testi dei prompt: usa la virgola.
9. **Lingua e registro** coerenti con il mercato indicato nello Step 0.4.

Applica la checklist di qualità di `references/regole-conversione.md` prima di passare alla Fase 5.

---

## FASE 5, OUTPUT

Restituisci l'output **come testo in chat**, nell'ordine seguente. Usa `references/esempio-output.md` come riferimento di formato.

### 5.1, RIEPILOGO DEL SET

Un breve blocco con: numero di prompt richiesto (N) e consegnato, brand, competitor, lingua, numero di keyword lavorate per tipo, numero di prompt per categoria, keyword escluse e motivo.

### 5.2, TABELLE IN CHAT

Una tabella markdown per categoria (4 tabelle in totale), ciascuna preceduta dal titolo della categoria in maiuscolo, con **solo** queste colonne:

| Colonna | Contenuto |
|---|---|
| `Funnel / Intent` | Awareness, Consideration, Decision, Post-acquisto + intent (informativo, commerciale, transazionale, supporto) |
| `Keyword SEO` | Keyword di partenza (una o più, separate da barra verticale) |
| `Prompt` | Testo del prompt |
| `Branded` | Sì / No |

Non aggiungere altre colonne (niente ID, tipo di keyword, variante o metrica da monitorare). Le varianti V1-V4 della Fase 4 servono solo a costruire prompt diversi tra loro e non vanno mostrate.

Ordina le righe per keyword con più click (o impression se i click non ci sono) e, per la stessa keyword, nell'ordine delle varianti V1, V2, V3, V4.

**Niente CSV né file.** L'unico output è il testo in chat. Non generare blocchi CSV, file o artifact se l'utente non lo chiede esplicitamente.

### 5.3, VOLUMI GRANDI

Se il set supera i 200 prompt, consegna le tabelle **per categoria**, in messaggi successivi, annunciando all'inizio quanti blocchi arriveranno. Non troncare mai le tabelle e non usare "..." per abbreviare.

### 5.4, NOTE OPERATIVE (BREVI)

Chiudi con massimo 5 punti elenco su come usare il set:

- frequenza consigliata di esecuzione (es. settimanale per Customer Care / Crisis, mensile per le altre);
- esecuzione con cronologia e memoria disattivate, in sessione anonima;
- eseguire gli stessi prompt su tutti e 4 gli LLM per avere dati confrontabili;
- registrare per ogni risposta: menzione del brand (Sì/No), posizione, sentiment (positivo/neutro/negativo), competitor citati, fonti citate.

---

## FORMATO DI CONSEGNA

L'output di default è **solo testo in chat** (riepilogo, tabelle per categoria, note operative). Genera un CSV, un file (.csv, .xlsx), un Google Sheet o un artifact **solo se l'utente lo chiede esplicitamente**; in quel caso usa le stesse colonne delle tabelle più `Categoria`, e rispetta il brand Moca (font Figtree, palette Moca) per gli output visuali.
