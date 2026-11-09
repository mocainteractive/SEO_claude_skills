# MATRICE 4X4, CATEGORIE E VARIANTI DI PROMPT

La matrice incrocia **4 categorie di tracking** con **4 varianti di formulazione**. Ogni keyword selezionata produce fino a 16 prompt; il numero totale di prompt e quindi di keyword dipende dalla quantità N scelta dall'utente nello Step 0.0. Le categorie misurano tipi diversi di sentiment; le varianti misurano come cambia la risposta del modello al variare della formulazione.

Segnaposto usati nei template:

- `[Brand]`: brand principale (o una sua variante, alternandole tra i prompt).
- `[Competitor]`, `[Competitor2]`: competitor indicati nel brief.
- `[tema]`: il tema estratto dalla keyword (prodotto, servizio, problema), riscritto in forma naturale.
- `[esigenza]`: bisogno concreto dell'utente dedotto dalla keyword (es. "resistere alla pioggia", "gestire 3 sedi").
- `[vincolo]`: budget, luogo, dimensione, livello di esperienza, tempistica.
- `[settore]`: settore / nicchia indicato nel brief.

I template sono **punti di partenza**: riformulali per ogni keyword in modo che suonino naturali. Non usare lo stesso template identico per tutte le keyword, altrimenti il set misura la formula e non il tema.

---

## LE 4 VARIANTI

| Variante | Nome | Struttura | Cosa misura |
|---|---|---|---|
| V1 | Domanda diretta | Domanda breve e secca | Risposta di base, menzione spontanea |
| V2 | Raccomandazione | "Consigliami", "quali sono i migliori", "fammi una classifica" | Presenza e posizione in liste e raccomandazioni |
| V3 | Scenario / persona | Caso d'uso concreto con almeno un vincolo | Pertinenza percepita del brand per un bisogno specifico |
| V4 | Fonti e prova sociale | Opinioni, recensioni, esperienze, "cosa dicono su..." | Sentiment aggregato e fonti citate dal modello |

---

## CATEGORIA 1, BRAND DISCOVERY & AWARENESS (BD)

**Sentiment diretto.** Misura cosa sa il modello del brand, come lo descrive, quali pro e contro associa, quanto lo ritiene affidabile.

- **Branded:** sempre.
- **Funnel:** Awareness / Consideration iniziale.
- **Cosa monitorare:** accuratezza delle informazioni, tono (positivo/neutro/negativo), pro e contro citati, fonti.

| Variante | Template |
|---|---|
| V1 | "Cos'è [Brand] e di cosa si occupa?" / "[Brand] è affidabile per [tema]?" |
| V2 | "Quali sono i punti di forza e i punti deboli di [Brand]?" |
| V3 | "Sto valutando [Brand] per [esigenza] con [vincolo]. È una scelta sensata?" |
| V4 | "Cosa dicono le recensioni dei clienti su [Brand]? Che reputazione ha?" |

**Innesto su keyword Non-Brand e Long-tail:** collega il brand al tema della keyword. Keyword `scarpe da trail running ammortizzate` diventa V1 "[Brand] fa buone scarpe da trail running ammortizzate?".

---

## CATEGORIA 2, COMPARATIVE / VERSUS (CV)

**Sentiment relativo.** Misura come il modello posiziona il brand rispetto ai competitor: chi vince il confronto, su quali criteri, chi viene proposto come alternativa.

- **Branded:** almeno 2 varianti su 4 nominano brand e competitor; le altre possono nominare solo il competitor o il tema.
- **Funnel:** Consideration / Decision.
- **Cosa monitorare:** brand vincente nel confronto, criteri citati, posizione del brand nelle liste di alternative, competitor emergenti non previsti.

| Variante | Template |
|---|---|
| V1 | "Meglio [Brand] o [Competitor] per [tema]?" |
| V2 | "Quali sono le migliori alternative a [Competitor] per [tema]?" |
| V3 | "Devo scegliere tra [Brand], [Competitor] e [Competitor2] per [esigenza] con [vincolo]. Quale mi consigli e perché?" |
| V4 | "Che differenze ci sono tra [Brand] e [Competitor] secondo chi li ha usati entrambi?" |

**Regole:**

- Ruota i competitor tra le keyword, così che ogni competitor compaia almeno una volta per categoria.
- Alterna l'ordine dei nomi ("[Brand] o [Competitor]" e "[Competitor] o [Brand]") per ridurre il bias di posizione.
- Per le keyword Versus che contengono già un competitor, usa quel competitor in V1 e V4.

---

## CATEGORIA 3, PROBLEM / SOLUTION (PS)

**Unbranded e mid-funnel.** Misura se il brand emerge **spontaneamente** quando l'utente descrive un problema o un bisogno del settore. È la categoria più importante per la GEO: indica lo share of voice organico.

- **Branded:** mai. Nessun nome di brand o competitor nel prompt.
- **Funnel:** Awareness / Consideration.
- **Cosa monitorare:** il brand viene citato (Sì/No), in che posizione, con quale descrizione, quali competitor emergono al suo posto, quali fonti/domini vengono citati.

| Variante | Template |
|---|---|
| V1 | "Come posso [risolvere il problema / soddisfare l'esigenza]?" |
| V2 | "Quali sono i migliori [prodotti / servizi / aziende] per [esigenza] in [mercato]?" |
| V3 | "Ho [situazione concreta] e [vincolo]. Cosa mi consigli di fare o di comprare?" |
| V4 | "Quali [prodotti / servizi] per [tema] vengono consigliati di più su forum e recensioni?" |

**Regole:**

- Parti dal problema implicito nella keyword: `divano esterno che non si rovina con la pioggia` contiene il problema "durata all'aperto".
- V2 e V4 devono sempre chiedere nomi, marche o aziende, altrimenti il modello risponde in modo generico e non c'è nulla da tracciare.
- Inserisci il mercato geografico quando la keyword è locale o quando il settore ha player diversi per paese.

---

## CATEGORIA 4, CUSTOMER CARE / CRISIS (CC)

**Sentiment critico.** Misura cosa risponde il modello quando l'utente cerca problemi, lamentele o informazioni post-acquisto: resi, rimborsi, assistenza, recensioni negative su Reddit, Trustpilot, Google My Business.

- **Branded:** sempre.
- **Funnel:** Post-acquisto / Decisione finale (verifica di affidabilità prima dell'acquisto).
- **Cosa monitorare:** presenza di criticità ricorrenti, fonti negative citate, correttezza delle informazioni su resi e assistenza, tono complessivo.

| Variante | Template |
|---|---|
| V1 | "Come funziona il reso con [Brand]? È facile ottenere un rimborso?" |
| V2 | "Quali sono le lamentele più comuni dei clienti di [Brand]?" |
| V3 | "Ho ordinato [tema] da [Brand] e [problema plausibile]. Come devo muovermi e quali sono i miei diritti?" |
| V4 | "Cosa scrivono su Reddit e Trustpilot di [Brand]? Ci sono esperienze negative?" |

**Regole:**

- Usa solo problemi plausibili per il settore (ritardo nella consegna, prodotto non conforme, difficoltà a contattare l'assistenza, garanzia) o presenti nelle keyword con segnale di criticità.
- Non inserire accuse non verificate ("[Brand] è una truffa?" va usato **solo** se la keyword esiste nel dataset).
- Se il settore non prevede resi (es. servizi B2B), adatta a disdetta, contratto, SLA, supporto tecnico.

---

## RIEPILOGO DELLA MATRICE

| | V1 Domanda diretta | V2 Raccomandazione | V3 Scenario / persona | V4 Fonti e prova sociale |
|---|---|---|---|---|
| **BD, Brand Discovery** | Cos'è / è affidabile | Pro e contro | È adatto al mio caso | Reputazione e recensioni |
| **CV, Comparative** | X o Y | Alternative a Y | Scelta tra 3 con vincolo | Differenze secondo gli utenti |
| **PS, Problem / Solution** | Come risolvo | Migliori per esigenza | Caso concreto con vincolo | Più consigliati su forum |
| **CC, Customer Care** | Resi e rimborsi | Lamentele comuni | Problema post-acquisto | Esperienze negative |
