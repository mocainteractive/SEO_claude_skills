# Catalogo prezzi fornitori — indice e mappatura colonne

Questo file descrive il **catalogo prezzi dei portali** incluso nella skill come knowledge locale (letto a runtime, mai pubblicato: nessun rischio di indicizzazione). Contiene i listini di **più fornitori** uniti in un solo CSV. La skill lo usa per: (1) **prezzo** di ogni prospect e (2) confronto tra fornitori per indicare **da chi conviene comprare**.

**Come leggerlo a runtime (importante):** usa lo script bundled **`scripts/price_lookup.py`** (`lookup` per dominio, `discover` per categoria/paese) — gestisce già tutto ciò che segue. Solo se non hai Python, filtra manualmente **senza** caricare l'intero CSV nel contesto, con un vero parser CSV (celle multi-riga tra virgolette presenti). Nota formato: in questo file il separatore **decimale è il punto** (`1305.50 €` = 1.305,50 €; `Su richiesta`/`Da concordare` = prezzo su richiesta). Alcuni valori molto bassi possono essere outlier del sorgente: verificali in fase d'ordine.

---

## comparativa-fornitori.csv
- **Cosa contiene:** ~6.939 righe · **4 fornitori:** Link Juice (~6197), Mauxa (~355), Matteo Di Felice (~351), AdHub Media (~36).
- **⚠️ Prime 2 righe = titolo/sottotitolo, da SALTARE.** L'intestazione vera è alla **riga 3**: `FORNITORE,SITO,PREZZO,NOTE`. Quando parsi, salta le prime 2 righe (`csv.DictReader(righe[2:])`).
- **Mappatura colonne:**
  - `FORNITORE` → **fornitore/fonte** della riga (è l'etichetta da citare: "compra da <FORNITORE>"). Un dominio può comparire per **più fornitori** a prezzi diversi → confrontali.
  - `SITO` → **dominio** (chiave di lookup/merge; normalizza: minuscolo, togli `www.`, spazi, `http(s)://`, path).
  - `PREZZO` → **prezzo**. Formati: `280 €` oppure formato italiano `€ 1.234,00` (togli `€`/spazi, `.`=migliaia, `,`=decimali → numero). `Da concordare` / vuoto → **"su richiesta"** (non 0, non escludere).
  - `NOTE` → testo con **campi strutturati** `chiave: valore` separati da `;`. Estraine (chiavi viste, variano per fornitore):
    - metriche: **DA** (Moz), **TF**/**CF** (Majestic), **DR** (Ahrefs), **AS** (Semrush), **ZA** (SEOZoom Zoom Authority);
    - contesto: **Categoria**, **Topic**, **Paese** (IT/ES/FR/DE/UK/US/LATAM → usa per il filtro mercato), **Servizio** (es. "pubblicazione GNews");
    - requisiti/red flag: **Info**, **Anchor accettate**, **Scrittura articolo**, **Testata registrata**, **Maggiorazione per** (settori a sovrapprezzo: gambling, finanza, ecc.), eventuale **nofollow**.
    Regola di parsing: split su `;`, poi su primo `:`; le chiavi non sono uniformi tra fornitori → estrazione tollerante (case-insensitive), campi mancanti = vuoti.
- **Note:** prezzi in €. Metriche del listino = aggiunta rapida, da incrociare con la performance reale via Ahrefs (vedi `references/qualita-link-building.md`). `Paese` diverso da IT segnala un portale estero: rispetta il mercato richiesto dall'utente.

### Come aggiungere/aggiornare fornitori
Se ricevi un nuovo file: se ha lo **stesso schema** (`FORNITORE,SITO,PREZZO,NOTE`), aggiungi le righe a questo CSV (o sostituiscilo) e aggiorna i conteggi qui. Se ha uno **schema diverso**, salvalo come file separato in questa cartella e aggiungi qui una voce con la sua mappatura colonne. Aggiorna la **data dell'ultimo aggiornamento**: (indicare quando sostituisci il file).
