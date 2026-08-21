# Criteri di qualità per lo scouting di link building

Riferimento operativo per le fasi di **qualificazione** e **scoring** della skill `link-building-scouting`. Sintetizza i criteri convergenti di quattro guide (Ahrefs, Ahrefs Academy, Semrush, SEOZoom) e li traduce in controlli eseguibili con gli strumenti disponibili (Ahrefs + le metriche restituite da Getfluence).

Leggi questo file quando devi qualificare i domini a catalogo (Fase 3) e assegnare il punteggio (Fase 4).

## Indice
1. Cosa rende un sito "di qualità" (i 6 segnali che contano)
2. Come leggere le metriche senza farti ingannare
3. Checklist red flag / link tossici
4. Il ruolo delle menzioni e dei nofollow
5. Benchmark di budget (mercato italiano)
6. Mappa criterio → strumento

---

## 1. Cosa rende un sito "di qualità" (i 6 segnali che contano)

Le guide concordano su questi segnali, in ordine di peso decrescente per lo scouting. Il primo è il più importante.

1. **Rilevanza tematica (topical relevance).** È il segnale più forte e va pesato per primo. Un link/menzione da un sito **verticale** e in-topic vale molto più di uno da un generalista, e un link off-topic è il caso peggiore (segnale debole e confuso per Google). Non basta che il sito sia "forte in generale": deve essere autorevole **proprio nel tema** del cliente. Distingui sempre **verticale** (specializzato, approfondisce un tema) da **generalista/contenitore** (pubblica un po' di tutto).
   *Euristica veloce (Semrush):* chiediti "cercherei questo link anche se Google non esistesse?". Se sì (il sito è davvero frequentato dal pubblico del cliente), è pertinente; se lo vuoi solo per il ranking, non lo è. La pertinenza è comunque un concetto elastico (Ahrefs): temi adiacenti e complementari sono legittimi, purché il legame non sia forzato.

2. **Performance reale in SERP.** L'autorevolezza vera si misura su come il sito rende davvero su Google: **traffico organico** stabile, ampiezza e qualità delle **keyword posizionate** (quante in top 3/top 10), stabilità dei ranking nel tempo. È l'idea dietro la Zoom Authority di SEOZoom e la logica "page/site-level traffic" di Ahrefs: una pagina/sito con traffico ~0 passa pochissimo valore, **a prescindere dal DR**.

3. **Autorità del dominio (come riferimento, non come verdetto).** DR (Ahrefs), DA (Moz), AS (Semrush), TF/CF (Majestic), Zoom Authority (SEOZoom) sono utili come screening rapido, ma sono **calcoli proprietari basati sui backlink e manipolabili** (network artificiali, link spazzatura). Usali come soglia d'ingresso, mai come unica ragione per scegliere un sito.

4. **Salute e stabilità del dominio (affidabilità).** Crescita organica costante, pubblicazione **regolare**, presenza di una **redazione vera** che produce contenuti originali. Segnali di affidabilità elementari (Semrush): il sito esiste da tempo, ha HTTPS/SSL, ha attività social reale, genera un traffico mensile stabile. Campanelli d'allarme: oscillazioni anomale di traffico, penalizzazioni storiche, picchi sospetti, sito fermo da mesi.

5. **Contesto editoriale del link.** Il valore è massimo quando il link è **editoriale**, nel corpo di un contenuto utile, in posizione rilevante — non in liste di link, footer, sidebar o pagine riempitive. (Questo si verifica soprattutto in fase di pubblicazione, ma un sito il cui modello è "link in calce a contenuti riempitivi" è già un segnale di bassa qualità.)

6. **Naturalezza e varietà del profilo.** Un buon sito ospitante ha a sua volta un profilo backlink e un profilo di anchor **vari e naturali**; un sito che vende link in massa mostra pattern innaturali (anchor in uscita sovraottimizzate verso molti domini commerciali scollegati).

---

## 2. Come leggere le metriche senza farti ingannare

- **Non sommare metriche di provider diversi.** DR, DA, AS, TF/CF misurano cose diverse su scale diverse. Scegli **1–2 metriche primarie** (DR + traffico organico) e usa le altre come conferma/trust, mai come addendi di un totale.
- **Privilegia la performance reale alla metrica di autorità.** A parità di prezzo, un sito con traffico organico solido e keyword in top 10 batte un sito con DR più alto ma traffico modesto: il secondo può avere il DR gonfiato.
- **TF/CF come check di trust, non come punteggio.** Un **Citation Flow molto maggiore del Trust Flow** (rapporto TF/CF basso) indica un profilo link quantitativamente ampio ma poco affidabile: segnalalo.
- **DR alto + traffico ~0 = red flag.** È il pattern tipico del dominio con autorità artificiale. Da segnalare sempre, spesso da escludere.
- **Guarda l'andamento, non solo il valore puntuale.** Un traffico in calo strutturale o con crolli improvvisi (possibile penalizzazione) vale meno di un traffico stabile o in crescita, anche se il valore odierno è simile.

---

## 3. Checklist red flag / link tossici

Segnala (e, se gravi, escludi) i domini che mostrano questi segnali. Nessuno da solo è una condanna automatica, ma più segnali insieme abbassano molto la qualità:

- **Fuori tema**: il sito non presidia il topic del cliente (relevance debole).
- **Traffico organico vicino allo zero** o in crollo, soprattutto se il DR è alto.
- **Oscillazioni/penalizzazioni**: cali improvvisi di traffico, storia di ranking instabile.
- **Pattern da "sito contenitore"**: nessuna redazione riconoscibile, contenuti riempitivi, esiste palesemente solo per ospitare guest post / vendere link.
- **Anchor in uscita sovraottimizzate**: il sito linka molti domini esterni con anchor a corrispondenza esatta (keyword secche commerciali) → tipico dei link farm.
- **Crescita di backlink innaturale**: picchi improvvisi di referring domains da fonti mai collegate prima.
- **Profilo di referring domains spammoso** (flag `is_spam`), TLD sospetti, network.
- **Eccesso di link esterni per pagina**: pagine che sono liste di collegamenti.

---

## 4. Il ruolo delle menzioni e dei nofollow

- **Non scartare un sito solo perché offre nofollow o una menzione senza link.** Oggi Google tratta gli attributi come "hint" e legge le **menzioni** (citazioni testuali del brand, anche senza collegamento) come segnale di autorevolezza, con peso crescente per la presenza nelle **AI Overview**. Una menzione autentica su un sito verticale autorevole può valere più di un link forzato su un generalista.
- **Valuta il ritorno complessivo**: brand association, traffico referral qualificato, presenza tra le fonti citate dall'AI. Una menzione/nofollow su testata prestigiosa e in-topic va tenuta in shortlist, annotando l'attributo.
- **In pratica per lo scouting**: se un'offerta Getfluence è una menzione in un articolo esistente (non un nuovo articolo), non penalizzarla a priori — pesala su rilevanza e autorità del sito come le altre, segnalando la tipologia.

---

## 5. Benchmark di budget (mercato italiano)

Usali per un **sanity check** del budget dichiarato dall'utente, non come prezzi da imporre:
- Azioni "entry level": da **poche centinaia di euro** a singola pubblicazione.
- Progetti strutturati / multicanale: **diverse migliaia di euro al mese**, specie nei settori competitivi.
- Principio: acquistare link economici su generalisti/network è un falso risparmio (rischio penalizzazione, valore reale nullo). Meglio pochi link pertinenti e sani che molti scadenti.
- Se il budget per link è molto sotto la fascia di mercato per le soglie richieste, **dillo all'utente** e proponi di alzare il budget, abbassare le soglie o ridurre il numero di siti.

---

## 6. Mappa criterio → strumento

Con Getfluence, **per i soli domini a catalogo**, ottieni già: `organicTraffic`, `trustFlow`, `citationFlow`, `domainAuthority`, `authorityScore`, `domainRating`. **Usale come arricchimento** (evitano una chiamata Ahrefs per quelle metriche); per i domini non a catalogo e per i controlli più profondi usa Ahrefs. Riserva le chiamate Ahrefs costose alla rosa che serve.

| Criterio | Strumento e campi |
|---|---|
| Rilevanza tematica | Ahrefs `site-explorer-organic-keywords` (su cosa ranka il sito) e `site-explorer-top-pages` (quali contenuti fanno traffico) → confronta con il topic del cliente |
| Performance reale | Ahrefs `site-explorer-metrics` (`org_traffic`, `org_keywords`, `org_keywords_1_3`) + le metriche Getfluence |
| Autorità | Ahrefs `site-explorer-domain-rating` (DR) + DA/AS/DR da Getfluence |
| Salute/stabilità | Ahrefs `site-explorer-metrics-history` o `site-explorer-domain-rating-history` (trend traffico/DR, crolli sospetti); `site-explorer-refdomains-history` (crescita innaturale di referring domains) |
| Pattern "contenitore"/link farm | Ahrefs `site-explorer-linked-domains` e `site-explorer-linked-anchors-external` (a chi linka in uscita e con quali anchor); `site-explorer-outlinks-stats` |
| Trust del profilo | Ahrefs `site-explorer-referring-domains` con `is_spam`; `site-explorer-backlinks-stats` |

Nota unità Ahrefs: alcuni campi (traffico, refdomains) costano più unità API. Batcha e limita le chiamate profonde ai soli domini candidati seri. Valori monetari Ahrefs in **centesimi di USD** (dividi per 100).
