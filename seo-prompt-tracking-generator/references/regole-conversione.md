# REGOLE DI CONVERSIONE, DA KEYWORD SEO A PROMPT CONVERSAZIONALE

Una keyword SEO è una stringa compressa: l'utente toglie articoli, verbi e contesto perché sa che Google funziona così. Con un assistente AI lo stesso utente scrive frasi complete, aggiunge il proprio contesto e chiede un consiglio. Questa conversione ricostruisce la domanda completa che sta dietro la keyword.

---

## 1. CLASSIFICAZIONE DELLE KEYWORD

Applica le regole nell'ordine. La prima che corrisponde assegna il tipo.

| Ordine | Condizione | Tipo |
|---|---|---|
| 1 | Contiene brand e/o competitor **e** un segnale di confronto (`vs`, `contro`, `o`, `oppure`, `meglio`, `migliore di`, `alternativa`, `alternative`, `differenza`, `confronto`, `simile a`) | Versus |
| 2 | Contiene il nome del brand o una sua variante | Brand |
| 3 | Contiene solo il nome di un competitor senza segnale di confronto | Versus (da usare come "alternative a [Competitor]") |
| 4 | Generica, 4 o più parole, oppure in forma di domanda (`come`, `quale`, `perché`, `quanto`, `dove`, `cosa`) | Long-tail |
| 5 | Generica, 1-3 parole | Non-Brand |

**Segnale di criticità (Sì/No).** Sì se la keyword contiene, anche in altre lingue, termini come: `reso`, `resi`, `rimborso`, `recesso`, `reclamo`, `lamentele`, `truffa`, `affidabile`, `opinioni`, `recensioni`, `recensioni negative`, `non funziona`, `difettoso`, `assistenza`, `servizio clienti`, `contatti`, `ritardo`, `spedizione`, `garanzia`, `disdetta`, `reddit`, `trustpilot`.

Per le altre lingue applica gli equivalenti (es. EN: `refund`, `return policy`, `complaints`, `scam`, `legit`, `reviews`, `customer service`; ES: `devolución`, `reembolso`, `opiniones`, `estafa`; FR: `remboursement`, `retour`, `avis`, `arnaque`; DE: `Rückgabe`, `Erstattung`, `Erfahrungen`, `Betrug`).

---

## 2. INTENT E FUNNEL

| Segnale nella keyword | Intent | Funnel |
|---|---|---|
| `cos'è`, `come funziona`, `significato`, `guida`, `perché` | Informativo | Awareness |
| `migliore`, `migliori`, `top`, `classifica`, `vs`, `alternative`, `recensione`, `opinioni` | Commerciale | Consideration |
| `prezzo`, `costo`, `offerta`, `acquista`, `comprare`, `sconto`, `codice sconto`, `dove comprare` | Transazionale | Decision |
| `reso`, `rimborso`, `assistenza`, `garanzia`, `tracking ordine`, `disdetta` | Supporto | Post-acquisto |
| Solo nome del brand | Navigazionale | Awareness |

Quando un prompt viene generato in una categoria diversa da quella primaria, l'intent si adegua alla categoria (es. un prompt CC generato da una keyword Non-Brand è comunque Post-acquisto / Supporto).

---

## 3. LE 7 REGOLE DI CONVERSIONE

1. **Ricostruisci la frase completa.** Aggiungi verbo, articoli e soggetto. `preventivo fotovoltaico 6 kw` diventa "Quanto costa installare un impianto fotovoltaico da 6 kW?".
2. **Esplicita il bisogno implicito.** Chiediti perché l'utente cerca quella keyword. `materasso mal di schiena` contiene "ho mal di schiena e voglio dormire meglio".
3. **Aggiungi contesto realistico solo nelle varianti V3.** Budget, luogo, dimensione, esperienza. Il contesto deve essere plausibile per il target del brief, non inventato a caso.
4. **Chiedi nomi quando serve tracciare.** Nelle varianti V2 e V4 il prompt deve chiedere marche, aziende o siti, altrimenti la risposta non contiene entità misurabili.
5. **Mantieni il tema della keyword.** Il prompt deve restare semanticamente vicino alla keyword di partenza: se ci si allontana troppo, il collegamento con i dati SEO si perde.
6. **Scrivi come un utente, non come un SEO.** Niente "keyword", "ranking", "SERP" nei prompt. Niente maiuscole enfatiche, niente elenchi di termini.
7. **Una sola domanda principale per prompt.** Al massimo una domanda di approfondimento ("...e perché?"). Prompt con 3 domande producono risposte non confrontabili.

### ESEMPI DI CONVERSIONE

| Keyword SEO | Tipo | Prompt conversazionale (esempio) |
|---|---|---|
| `[brand] opinioni` | Brand + criticità | "Che opinioni hanno i clienti di [Brand]? Ci sono problemi ricorrenti?" |
| `[brand] vs [competitor]` | Versus | "Meglio [Brand] o [Competitor] per chi compra online per la prima volta?" |
| `software fatturazione elettronica` | Non-Brand | "Quali sono i migliori software di fatturazione elettronica per un libero professionista?" |
| `come scegliere un gestionale per ristorante` | Long-tail | "Ho un ristorante con 40 coperti, come scelgo un gestionale per ordini e magazzino?" |
| `[brand] reso` | Brand + criticità | "Come si fa un reso su [Brand] e in quanti giorni arriva il rimborso?" |

---

## 4. ADATTAMENTO ALLA LINGUA E AL MERCATO

- Non tradurre parola per parola: riformula come scriverebbe un madrelingua del mercato target.
- Adatta le fonti citate nei prompt V4 al mercato (es. Italia: Trustpilot, Google, Reddit, forum di settore; Germania: Trustpilot, Idealo; Francia: Avis Vérifiés, Trustpilot; USA: Reddit, BBB, Trustpilot).
- Adatta valute, unità di misura e riferimenti normativi (es. diritto di recesso UE di 14 giorni) al mercato.
- Usa il registro informale (tu) quando è naturale per quella lingua nelle chat con un assistente.

---

## 5. CHECKLIST DI QUALITÀ (PRIMA DELLA CONSEGNA)

Verifica ogni punto. Se uno fallisce, correggi prima di consegnare.

- [ ] Ogni keyword selezionata ha 16 prompt (4 categorie x 4 varianti), salvo duplicati accorpati e dichiarati.
- [ ] Nessun prompt della categoria Problem / Solution contiene il brand o un competitor.
- [ ] Nella categoria Comparative ogni competitor del brief compare almeno una volta.
- [ ] Nessun prompt suggerisce la risposta o contiene giudizi a favore del brand.
- [ ] I prompt Customer Care / Crisis trattano solo temi plausibili o presenti nelle keyword.
- [ ] Le varianti V2 e V4 chiedono nomi, marche, aziende o fonti.
- [ ] Lunghezza tra 8 e 35 parole (V3 fino a 45).
- [ ] Nessun prompt duplicato o quasi identico.
- [ ] Nessun trattino lungo nei testi.
- [ ] Lingua, valuta e fonti coerenti con il mercato.
- [ ] Il CSV contiene tutte le righe delle tabelle, con gli stessi ID.
