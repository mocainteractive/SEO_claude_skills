# Listini prezzi bundled — indice e mappatura colonne

Questo file elenca i **listini prezzi dei portali** inclusi nella skill come knowledge locale (letti a runtime, mai pubblicati). Per ogni listino sono indicati: etichetta della fonte, mercato/lingua, file, mappatura delle colonne e note di parsing. Quando aggiungi un nuovo listino, copia il CSV in questa cartella e aggiungi qui una voce.

**Come leggere i listini a runtime (importante):** i file possono avere migliaia di righe. **Non caricarli interi nel contesto**: usa codice (analysis tool / Python / bash) per **caricarli e filtrarli** — per dominio (lookup di prezzo) o per categoria (fonte di candidati). Parsali con un vero parser CSV (celle multi-riga tra virgolette presenti).

**Normalizzazione comune a tutti i listini:**
- **Dominio**: minuscolo, togli spazi, `http(s)://`, `www.`, eventuale path → dominio registrabile. Alcune celle hanno maiuscole/spazi (es. `Gattipersiani.it`, `ANIMALI `).
- **Prezzo**: formato italiano `€ 1.157,00` → `1157.00` (togli `€`/spazi, `.` migliaia, `,` decimali). Valori come `DA CONCORDARE` / vuoto → prezzo **"su richiesta"** (non 0, non escludere: il portale è comunque disponibile).
- **Fonte**: usa l'etichetta indicata sotto (non il nome file).

---

## link-juice-italiano.csv
- **Fonte (etichetta):** Link Juice
- **Mercato/lingua:** Italia / italiano
- **Righe:** ~6.280 portali · **Categorie:** 44 · **Aggiornato al:** (indicare la data dell'export quando lo aggiorni)
- **Mappatura colonne:**
  - `SITO` → **dominio** (chiave di lookup/merge)
  - `PREZZO` → **prezzo** (formato `€ 1.234,00`; può essere `DA CONCORDARE`)
  - `CATEGORIA` → **settore** (per filtrare i candidati per tema; contiene duplicati per accenti/spazi/refusi, es. `ECONOMIA E FINANZA` vs `ECONOMIA FINANZA`, `SALUTE BENESERE BELLEZZA` vs `SALUTE BENESSERE BELLEZZA` → confronta in modo tollerante: minuscolo, senza accenti, trim)
  - `TOPIC` → temi trattati dal sito (utile per la pertinenza fine)
  - `INFORMAZIONI PER CLIENTE ` → **note** (attenzione allo spazio finale nel nome colonna): requisiti editoriali, `NO FOLLOW`, diciture, ecc. → estrai in particolare il flag **nofollow** e i vincoli di anchor/lunghezza
  - `DA` → Domain Authority (Moz) · `TF` → Trust Flow (Majestic) · `ZA` → Zoom Authority (SEOZoom)
  - `IP` → IP del server (utile solo come segnale di footprint/PBN: più domini stesso IP/blocco = possibile network)
- **Note:** prezzi già in €. `DA CONCORDARE` = trattativa. Le metriche DA/TF/ZA del listino sono un'aggiunta; restano da incrociare con la performance reale via Ahrefs (vedi reference qualità).
