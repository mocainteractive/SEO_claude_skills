---
name: link-building-scouting
description: >
  Scouting e qualificazione di siti editori (publisher) per la link building: dato un cliente e un topic da coprire, produce una shortlist ordinata di siti su cui pubblicare un guest post o ottenere una menzione, con disponibilità e prezzo reali da Getfluence, metriche di autorità e pertinenza tematica, filtrata per budget e soglie. È la fase di discovery + qualificazione che sta a monte del flusso guest-post-pipeline: gli fornisce i siti ospitanti candidati. Usa questa skill quando l'utente vuole trovare dove fare link building. Trigger tipici: "trova siti per link building", "scouting publisher per il cliente X", "shortlist guest post con budget Y", "su quali siti pubblico un guest post per X", "quali siti sono a catalogo Getfluence", "dammi una lista di siti dove comprare un link". NON scrive l'articolo (per quello c'è guest-post-pipeline) e NON valuta il tono di voce del singolo portale (host-site-analysis): serve a decidere DOVE pubblicare, non COSA scrivere.
---

# Link Building Scouting

Questa skill costruisce la **shortlist di siti editori** su cui il cliente può ottenere un backlink (guest post o menzione), partendo da un cliente e da un topic e arrivando a una tabella ordinata con **prezzo e disponibilità reali** presi da Getfluence, **metriche di autorità**, **pertinenza tematica** e un **punteggio trasparente** che bilancia qualità e costo.

Produce indicazioni operative e decisionali — non un report descrittivo. Il destinatario è chi deve decidere dove investire il budget di link building e poi passare i siti scelti al flusso di scrittura.

**Posizione nel flusso Moca:** questa skill **precede** `guest-post-pipeline` (e le sue fasi `guest-post-brand-analysis` / `host-site-analysis`). Lo scouting decide *dove* pubblicare; la pipeline decide *cosa* scrivere e produce l'articolo.

---

## Principio che regge tutta la skill (leggilo prima di iniziare)

**Getfluence non scopre siti per argomento.** Risponde solo su domini che gli passi tu: dice se un dominio noto è a catalogo, a che prezzo e con quali metriche. Non esiste una query "dammi siti di cucina" su Getfluence.

Di conseguenza la skill lavora in due tempi:
1. **La scoperta dei domini candidati la fai TU** con Ahrefs (e SERP / lista del cliente). Questo è il vero lavoro creativo dello scouting.
2. **Getfluence serve solo a verificare disponibilità e prezzo** sui domini che hai già scoperto.

Se inverti l'ordine o ti aspetti che Getfluence "trovi" i siti, la skill fallisce. Tienilo presente in ogni fase.

Un secondo principio: **l'assenza di un sito dal catalogo Getfluence NON è un giudizio di qualità.** Significa solo "non acquistabile via Getfluence in questo momento". Un sito ottimo può non esserci (magari si tratta direttamente, o è su un altro marketplace). Comunicalo sempre così all'utente, senza sminuire quei domini.

---

## Istruzioni di progetto (verifica SEMPRE all'inizio)

Se lavori dentro un progetto Claude, controlla se ci sono **istruzioni custom** o **knowledge di progetto** (linee guida di link building del cliente, settori vietati, publisher in blocklist/whitelist, tetti di spesa, requisiti di brand safety). Se presenti:
- hanno **precedenza** sui default di questa skill (soglie, criteri di scoring, filtri);
- restano subordinate alle scelte esplicite fatte dall'utente in questa sessione e ai vincoli di budget dichiarati;
- se un'istruzione di progetto è in conflitto con una buona pratica (es. accettare siti con red flag di trust), non ignorarla in silenzio: segnala il conflitto e chiedi come procedere.

Se non sei in un progetto o non ci sono istruzioni, procedi con i default della skill.

---

## Strumenti richiesti

- **Getfluence** (MCP `getfluence`) — availability + prezzo + metriche per dominio. Tool: `check_getfluence_status`, `search_offers`. **Necessario** per la fase di availability/pricing; senza, la skill può solo fare discovery e stimare metriche via Ahrefs (dichiaralo all'utente).
- **Ahrefs** (MCP `Ahrefs`) — motore di **discovery** dei domini candidati e di **validazione** delle metriche. È lo strumento principale della fase 1. Prima di usare un tool Ahrefs per la prima volta chiama `doc` per lo schema esatto; ricorda che i valori monetari Ahrefs sono in **centesimi di USD** (dividi per 100).
- **Semrush** (opzionale, se collegato in sessione) — overview dominio / keyword organiche / competitor, come fonte complementare o di conferma incrociata su pertinenza e traffico. Se non è disponibile, **non è un problema**: usa Ahrefs. Non bloccare il flusso per l'assenza di Semrush.
- (GA4/GSC sono disponibili ma poco rilevanti per lo scouting: ignorali salvo richiesta specifica.)

### Sanity check iniziale
Chiama `check_getfluence_status` una volta all'inizio. Se le credenziali non sono configurate o il server non risponde, avvisa l'utente e chiedi se vuole comunque procedere con la sola discovery Ahrefs (shortlist senza prezzi reali) o fermarsi. Non lanciarti in decine di chiamate se il connettore è giù.

---

## Domande iniziali obbligatorie

Fai queste domande **sempre e rigorosamente** prima di partire. Sono i parametri che rendono lo scouting utile invece che generico: senza budget e soglie qualunque lista è inservibile. Se l'utente ne salta qualcuna, insisti — proponi i default indicati tra parentesi ma chiedi conferma.

1. **Cliente e pagina/e target da linkare** (URL) e **topic da coprire**: di cosa deve parlare l'articolo/menzione che ospiterà il link. Serve a guidare discovery e pertinenza.
2. **Lingua e mercato/geo** di interesse (default: italiano / Italia `it`).
3. **Budget**: massimo € per singolo link e/o budget totale, e **numero di siti desiderati** nella shortlist.
4. **Soglie minime di metriche** (default proposti: DR ≥ 30, Trust Flow ≥ 15, traffico organico ≥ 5.000/mese). Adattali al mercato: su nicchie piccole o lingue minori possono essere troppo alte.
5. **Requisito di pertinenza tematica**: settori/nicchie ammessi e, se ci sono, quelli da escludere (brand safety).
6. **Eventuale lista di domini già candidati** dal cliente (verranno uniti ai candidati scoperti da te).
7. **Competitor di riferimento noti** (URL): accelerano molto la discovery. Se l'utente non li ha, li ricavi tu da Ahrefs (`site-explorer-organic-competitors`) partendo dal sito del cliente e/o dal topic.

Riepiloga i parametri raccolti prima di procedere, così l'utente vede su quali criteri stai per lavorare.

---

## Flusso operativo

### Fase 1 — Discovery dei domini candidati (Ahrefs + lista utente)

Obiettivo: costruire una **lista unica e deduplicata di domini candidati** il più ampia e pertinente possibile. Più il bacino è buono qui, migliore sarà la shortlist finale. Usa più angoli di scoperta e poi unisci:

**a) Referring domains dei competitor** — chi già linka i competitor è un publisher che accetta contenuti nel settore.
Per ogni competitor noto o individuato, usa `site-explorer-referring-domains`:
- `target`: il dominio del competitor, `mode`: `subdomains`
- `select`: `domain,domain_rating,traffic_domain,links_to_target,is_spam`
- `order_by`: `domain_rating:desc`
- `where`: filtra già qui per alzare la qualità, es. `domain_rating ≥` soglia e `is_spam = false`
- `limit`: 50–100 per competitor
Nota unità: `traffic_domain` costa più unità API per riga — se vuoi risparmiare, prima gira senza e recuperalo solo per la rosa ristretta.

**b) Chi posiziona per le keyword del topic** — chi ranka in prima pagina sul topic è un sito a tema e potenzialmente ospitante.
Usa `serp-overview` sulla keyword primaria del topic (e 1–2 correlate), `country` coerente col mercato, e raccogli i domini dei risultati organici. In alternativa/complemento, `site-explorer-organic-competitors` sul sito del cliente per trovare siti tematicamente affini.

**c) Lista fornita dal cliente** (domanda 6) — includila sempre così com'è.

**d) (Opzionale) Semrush** — se collegato, usa la sua vista competitor/organic per aggiungere domini che Ahrefs non ha intercettato.

**Consolidamento:** normalizza i domini (togli `http(s)://`, `www.`, path → dominio registrabile), **deduplica**, ed escludi da subito: il dominio del cliente e dei competitor, aggregatori/social/e-commerce marketplace non pertinenti, e i domini in eventuale blocklist di progetto. Il risultato è la **lista candidati** per la Fase 2.

### Fase 2 — Availability + pricing (Getfluence)

Passa la lista candidati a `search_offers`. **In batch**: Getfluence accetta più domini in una sola chiamata, e più domini = una sola richiesta HTTP. Non fare un loop di chiamate singole (bruci il rate limit inutilmente).

Ricetta `search_offers`:
- `domains`: **array** di domini candidati (obbligatorio). Passane molti in una chiamata.
- `search_type`: `"wide"` (**consigliato** — copre dominio e sottodomini via `registrableDomainSearch`). Usa `"strict"` solo se ti serve il match esatto del dominio/sottodominio, `"flexible"` per matching più permissivo sull'URL.
- `page`: parti da `1`; se la risposta è paginata (Hydra) e ti servono più risultati, richiedi le pagine successive.

Gestione del risultato:
- Per ogni dominio **presente a catalogo** ottieni: `url`, `formatType` (es. `article-website`), **`price`** (già in €), le metriche SEO (`organicTraffic`, `trustFlow`, `citationFlow`, `domainAuthority`, `authorityScore`, `domainRating`), `id`, `createdAt`. In coda la risposta può includere i **crediti API rimanenti**: annotali e, se sono bassi, avvisa l'utente.
- I domini **non presenti** semplicemente non compaiono. Mettili da parte in un elenco separato "non a catalogo Getfluence" (≠ scadenti, vedi principio iniziale).
- Il `price` è un **"a partire da"** per un nuovo articolo o una menzione in un articolo esistente: può variare in fase di trattativa. Dillo nell'output.

**Rate limit e 429.** Il limite è ~4 richieste/secondo più quote giornaliera e mensile. Il server traduce già `401/403/429` in messaggi chiari. Se ricevi un `429`, **non ritentare a raffica**: aspetta e riprova con backoff (es. 2s, 4s, 8s), e se persiste segnala all'utente che la quota è esaurita e proponi di riprendere più tardi o di ridurre il batch. Batchare i domini è la difesa principale: preferisci 1 chiamata da 40 domini a 40 chiamate da 1.

### Fase 3 — Qualificazione e filtri

Sui soli domini a catalogo, applica in ordine:

1. **Budget**: scarta chi supera il tetto per singolo link. Tieni conto del budget totale nel comporre la shortlist (Fase 4).
2. **Soglie metriche** (domanda 4): applica i minimi su DR e traffico organico come filtri primari; usa TF come soglia di trust. Non essere rigido al punto da svuotare la lista: se restano pochissimi siti, segnala all'utente che le soglie sono probabilmente troppo alte per il mercato e proponi di allentarle.
3. **Pertinenza tematica**: è il criterio che distingue un buon link da uno inutile. Verifica di cosa parla davvero il sito con le sue keyword organiche — `site-explorer-organic-keywords` (`target` = dominio, `mode` `subdomains`, `country` coerente, `order_by` traffico/volume, `limit` ~20–30) — e valuta se il topic del cliente è coerente con i temi presidiati dal sito. Classifica la pertinenza in **Alta / Media / Bassa** con una motivazione di una riga (es. "Alta — ranka su 'ricette dolci', 'dessert'; topic cliente = pasticceria"). Per non spendere unità inutilmente, fai questo controllo **solo sui domini che hanno già passato budget e soglie**.
4. **Red flag di qualità** (non scartano da soli, ma annotali): `citationFlow` molto maggiore di `trustFlow` (rapporto TF/CF basso) può indicare un profilo link gonfiato e poco affidabile; traffico organico molto basso rispetto a un DR alto è un altro campanello. Segnala in colonna Note.

### Fase 4 — Scoring & ranking

Ordina i siti sopravvissuti con un punteggio **trasparente** che bilancia due cose che al cliente interessano davvero: **quanto è pertinente** il sito e **quanta autorità/traffico compri per ogni euro**.

Linee guida (non sommare ingenuamente metriche di provider diversi — scegli poche metriche primarie e usa le altre come check):
- **Metriche primarie**: Domain Rating (DR) e traffico organico. Sono i due segnali più robusti e confrontabili.
- **Efficienza di spesa**: calcola **€ per punto DR** (`price / domainRating`) e, se utile, **€ per 1.000 di traffico organico** (`price / (organicTraffic/1000)`). Più basso = più efficiente. È l'indicatore che rende comparabili siti di prezzo diverso.
- **Pertinenza**: è il moltiplicatore. Un sito Bassa pertinenza, per quanto economico e autorevole, vale poco: penalizzalo o escludilo. Un sito Alta pertinenza a prezzo ragionevole va in cima anche se non è il più autorevole in assoluto.
- **Trust**: TF/CF sani confermano; red flag di trust abbassano la posizione.

Costruisci un punteggio complessivo 0–100 (o un ranking ordinale) combinando pertinenza (peso maggiore) ed efficienza autorità/prezzo, e **spiega in output come l'hai calcolato**. Non serve una formula esoterica: serve che l'utente capisca perché il sito #1 è il #1.

### Fase 5 — Output

Presenta la shortlist come **tabella ordinata** dal miglior candidato al peggiore, seguita dai riepiloghi. Vedi il formato qui sotto.

---

## Formato di output

Usa questa struttura.

### 1. Parametri dello scouting
Una riga di riepilogo: cliente, topic, mercato/lingua, budget (per link + totale), soglie applicate, n° siti richiesti. Così i criteri sono trasparenti.

### 2. Shortlist qualificata
Tabella ordinata per punteggio (migliore in alto):

| # | Dominio | Prezzo € | DR | TF/CF | DA | AS | Traffico org. | Pertinenza | € per punto DR | Punteggio | Note |
|---|---------|---------|----|-------|----|----|--------------|-----------|----------------|-----------|------|

- **Prezzo €**: dal `price` Getfluence, indicando che è "a partire da".
- **TF/CF**: Trust Flow / Citation Flow (es. `28/35`).
- **Pertinenza**: Alta / Media / Bassa + motivazione breve (può stare in Note se la tabella è stretta).
- **€ per punto DR**: efficienza di spesa.
- **Note**: red flag di trust, formato offerta, o altre osservazioni.

### 3. Riepilogo budget
- Costo totale della shortlist proposta e come si colloca rispetto al budget totale.
- Numero di siti proposti vs richiesti; costo medio per link; ventaglio prezzi (min–max).
- Se il budget non basta per il numero di siti desiderato alle soglie date, dillo e proponi opzioni (alzare budget, abbassare soglie, meno siti ma migliori).

### 4. Candidati non acquistabili via Getfluence
Elenco dei domini scoperti in Fase 1 ma **non a catalogo**, con una riga che ricorda che l'assenza non è un giudizio di qualità e che, se interessano, possono essere valutati per contatto diretto o su altri canali.

### 5. Prossimo passo
Suggerisci esplicitamente l'**handoff a `guest-post-pipeline`** per i siti scelti: la pipeline analizzerà cliente e portale ospitante e scriverà l'articolo con il link naturale. Indica che i siti della shortlist sono i "siti ospitanti candidati" da passare a quel flusso.

---

## Principi di qualità (tienili sempre)

- **Assenza da Getfluence ≠ sito scadente.** Ripetilo in output ogni volta che elenchi i non-a-catalogo.
- **Non sommare metriche di provider diversi.** DR (Ahrefs), DA (Moz), AS (Semrush), TF/CF (Majestic) misurano cose diverse su scale diverse. Scegli 1–2 primarie (DR + traffico) e usa le altre come conferma/trust, non come addendi di un totale.
- **Rispetta i rate limit.** Batch dei domini in `search_offers`, niente loop di chiamate singole, backoff sui `429`. Su Ahrefs, recupera le metriche costose (traffico, refdomains) solo sulla rosa che serve.
- **Rendi trasparenti criteri e filtri.** Mostra soglie applicate, come hai calcolato il punteggio, e quanti domini sono caduti a ogni filtro. Una shortlist di cui non si capisce la logica non è azionabile.
- **La pertinenza batte l'autorità nuda.** Un link tematicamente coerente su un sito medio vale più di un link fuori tema su un sito fortissimo.
- **Lingua di lavoro: italiano**, coerente con le altre skill Moca.

---

## Esempio end-to-end (caso fittizio)

**Input utente:** «Cliente: *Dolci del Sole*, pasticceria artigianale, pagina target `dolcidelsole.it/panettone-artigianale`. Topic: panettone e lievitati natalizi. Mercato: Italia, italiano. Budget: max 300 €/link, totale 1.000 €, voglio 4 siti. Soglie: DR ≥ 30, TF ≥ 15, traffico ≥ 5.000. Nicchie ammesse: food, lifestyle, cucina. Nessuna lista mia. Competitor: `fiaschetterialievita.it`.»

**Come procede la skill:**
1. **Sanity check** — `check_getfluence_status`: ok.
2. **Discovery (Ahrefs)** — `site-explorer-referring-domains` su `fiaschetterialievita.it` (DR desc, `is_spam=false`) → una decina di referring domains food/lifestyle. `serp-overview` su "panettone artigianale" / "migliori panettoni" → altri domini editoriali che rankano. Unione + dedup → ~15 domini candidati (es. `gamberorosso.it`, `dissapore.com`, `foodblog-esempio.it`, `magazinecucina-esempio.it`, …).
3. **Availability (Getfluence)** — `search_offers` con tutti i ~15 domini in **una** chiamata, `search_type: "wide"`. Risultano a catalogo 9; 6 non compaiono → lista "non a catalogo".
4. **Qualificazione** — filtro budget (scarta 2 sopra 300 €), soglie DR/TF/traffico (scarta 1), pertinenza via `site-explorer-organic-keywords` sui restanti 6 → 4 Alta, 1 Media, 1 Bassa (esclusa). Un dominio ha CF≫TF → red flag annotata.
5. **Scoring** — calcolo € per punto DR e ordino i 5 pertinenti; i migliori 4 stanno nel budget totale (somma ≈ 940 €).
6. **Output** — tabella dei 4 (+ il Media come alternativa), riepilogo budget (4 siti, 940 € su 1.000, media 235 €/link), elenco dei 6 non a catalogo con la nota, e suggerimento di passare i 4 siti a `guest-post-pipeline`.

Questo è il livello di trasparenza e concretezza atteso: l'utente deve poter dire "compro questi 4" e sapere esattamente perché.
