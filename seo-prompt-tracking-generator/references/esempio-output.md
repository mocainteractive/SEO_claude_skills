# ESEMPIO DI OUTPUT

Esempio di riferimento per il **formato** dell'output. Brand e competitor sono di fantasia e servono solo a mostrare la struttura: non usare questi nomi nei progetti reali.

**Brief dell'esempio**

- Brand: Verdeluce (dominio verdeluce.it), arredamento outdoor e-commerce
- Competitor: Giardino Plus, OutLiving
- Mercato e lingua: Italia, italiano
- Keyword di esempio (1 sola, per brevità): `divano da esterno resistente`, tipo Non-Brand, 140 click, 12.500 impression

Un set reale contiene tutte le keyword selezionate nella Fase 0.

---

## 5.1, RIEPILOGO DEL SET

- **Brand:** Verdeluce, **competitor:** Giardino Plus, OutLiving
- **Lingua:** italiano, **mercato:** Italia
- **Keyword lavorate:** 1 (Non-Brand: 1)
- **Prompt generati:** 16 (BD 4, CV 4, PS 4, CC 4)
- **Keyword escluse:** nessuna

---

## 5.2, TABELLE PER CATEGORIA

### BRAND DISCOVERY & AWARENESS

| ID | Funnel / Intent | Tipo KW | Keyword SEO | Variante | Prompt | Branded | Cosa monitorare |
|---|---|---|---|---|---|---|---|
| BD-001 | Awareness, informativo | Non-Brand | divano da esterno resistente | V1 | Verdeluce fa divani da esterno davvero resistenti a sole e pioggia? | Sì | Accuratezza, tono |
| BD-002 | Consideration, commerciale | Non-Brand | divano da esterno resistente | V2 | Quali sono i punti di forza e i punti deboli dei divani da esterno di Verdeluce? | Sì | Pro e contro citati |
| BD-003 | Consideration, commerciale | Non-Brand | divano da esterno resistente | V3 | Ho un terrazzo esposto a sud senza copertura e vorrei un divano da esterno sotto i 1.500 euro, quelli di Verdeluce sono adatti? | Sì | Pertinenza, tono |
| BD-004 | Consideration, commerciale | Non-Brand | divano da esterno resistente | V4 | Cosa dicono le recensioni dei clienti sui divani da esterno di Verdeluce dopo qualche anno di utilizzo? | Sì | Sentiment, fonti citate |

### COMPARATIVE / VERSUS

| ID | Funnel / Intent | Tipo KW | Keyword SEO | Variante | Prompt | Branded | Cosa monitorare |
|---|---|---|---|---|---|---|---|
| CV-001 | Consideration, commerciale | Non-Brand | divano da esterno resistente | V1 | Per un divano da esterno che duri nel tempo, meglio Verdeluce o Giardino Plus? | Sì | Brand vincente, criteri |
| CV-002 | Consideration, commerciale | Non-Brand | divano da esterno resistente | V2 | Quali sono le migliori alternative a OutLiving per comprare un divano da esterno resistente online? | Sì | Posizione del brand nella lista |
| CV-003 | Decision, commerciale | Non-Brand | divano da esterno resistente | V3 | Devo scegliere tra OutLiving, Verdeluce e Giardino Plus per un divano da esterno da lasciare fuori tutto l'anno al lago, quale mi consigli e perché? | Sì | Brand vincente, criteri |
| CV-004 | Consideration, commerciale | Non-Brand | divano da esterno resistente | V4 | Che differenze notano gli utenti tra i divani da esterno di Giardino Plus e quelli di Verdeluce? | Sì | Sentiment relativo, fonti |

### PROBLEM / SOLUTION

| ID | Funnel / Intent | Tipo KW | Keyword SEO | Variante | Prompt | Branded | Cosa monitorare |
|---|---|---|---|---|---|---|---|
| PS-001 | Awareness, informativo | Non-Brand | divano da esterno resistente | V1 | Come scelgo un divano da esterno che non si rovini con sole, pioggia e umidità? | No | Menzione spontanea, fonti |
| PS-002 | Consideration, commerciale | Non-Brand | divano da esterno resistente | V2 | Quali sono le migliori marche di divani da esterno resistenti in vendita in Italia? | No | Menzione, posizione, competitor |
| PS-003 | Consideration, commerciale | Non-Brand | divano da esterno resistente | V3 | Ho un giardino al mare con molta salsedine e un budget di circa 2.000 euro, che divano da esterno mi conviene comprare e da chi? | No | Menzione, posizione, competitor |
| PS-004 | Consideration, commerciale | Non-Brand | divano da esterno resistente | V4 | Quali divani da esterno resistenti vengono consigliati di più su forum e recensioni online? | No | Menzione, fonti citate |

### CUSTOMER CARE / CRISIS

| ID | Funnel / Intent | Tipo KW | Keyword SEO | Variante | Prompt | Branded | Cosa monitorare |
|---|---|---|---|---|---|---|---|
| CC-001 | Post-acquisto, supporto | Non-Brand | divano da esterno resistente | V1 | Come funziona il reso di un divano da esterno acquistato su Verdeluce, chi paga il ritiro? | Sì | Correttezza info, tono |
| CC-002 | Post-acquisto, supporto | Non-Brand | divano da esterno resistente | V2 | Quali sono le lamentele più comuni dei clienti Verdeluce sui divani da esterno? | Sì | Criticità ricorrenti, fonti |
| CC-003 | Post-acquisto, supporto | Non-Brand | divano da esterno resistente | V3 | Ho comprato un divano da esterno da Verdeluce e dopo una stagione il tessuto si è scolorito, come faccio a chiedere la garanzia? | Sì | Correttezza info, tono |
| CC-004 | Decision, supporto | Non-Brand | divano da esterno resistente | V4 | Cosa scrivono su Trustpilot e Reddit di Verdeluce? Ci sono esperienze negative con consegne o assistenza? | Sì | Sentiment, fonti negative |

---

## 5.3, BLOCCO CSV

```csv
"ID","Categoria","Funnel / Intent","Tipo KW","Keyword SEO","Variante","Prompt","Branded","Cosa monitorare","Lingua"
"BD-001","Brand Discovery & Awareness","Awareness, informativo","Non-Brand","divano da esterno resistente","V1","Verdeluce fa divani da esterno davvero resistenti a sole e pioggia?","Sì","Accuratezza, tono","it"
"BD-002","Brand Discovery & Awareness","Consideration, commerciale","Non-Brand","divano da esterno resistente","V2","Quali sono i punti di forza e i punti deboli dei divani da esterno di Verdeluce?","Sì","Pro e contro citati","it"
"BD-003","Brand Discovery & Awareness","Consideration, commerciale","Non-Brand","divano da esterno resistente","V3","Ho un terrazzo esposto a sud senza copertura e vorrei un divano da esterno sotto i 1.500 euro, quelli di Verdeluce sono adatti?","Sì","Pertinenza, tono","it"
"BD-004","Brand Discovery & Awareness","Consideration, commerciale","Non-Brand","divano da esterno resistente","V4","Cosa dicono le recensioni dei clienti sui divani da esterno di Verdeluce dopo qualche anno di utilizzo?","Sì","Sentiment, fonti citate","it"
"CV-001","Comparative / Versus","Consideration, commerciale","Non-Brand","divano da esterno resistente","V1","Per un divano da esterno che duri nel tempo, meglio Verdeluce o Giardino Plus?","Sì","Brand vincente, criteri","it"
"CV-002","Comparative / Versus","Consideration, commerciale","Non-Brand","divano da esterno resistente","V2","Quali sono le migliori alternative a OutLiving per comprare un divano da esterno resistente online?","Sì","Posizione del brand nella lista","it"
"CV-003","Comparative / Versus","Decision, commerciale","Non-Brand","divano da esterno resistente","V3","Devo scegliere tra OutLiving, Verdeluce e Giardino Plus per un divano da esterno da lasciare fuori tutto l'anno al lago, quale mi consigli e perché?","Sì","Brand vincente, criteri","it"
"CV-004","Comparative / Versus","Consideration, commerciale","Non-Brand","divano da esterno resistente","V4","Che differenze notano gli utenti tra i divani da esterno di Giardino Plus e quelli di Verdeluce?","Sì","Sentiment relativo, fonti","it"
"PS-001","Problem / Solution","Awareness, informativo","Non-Brand","divano da esterno resistente","V1","Come scelgo un divano da esterno che non si rovini con sole, pioggia e umidità?","No","Menzione spontanea, fonti","it"
"PS-002","Problem / Solution","Consideration, commerciale","Non-Brand","divano da esterno resistente","V2","Quali sono le migliori marche di divani da esterno resistenti in vendita in Italia?","No","Menzione, posizione, competitor","it"
"PS-003","Problem / Solution","Consideration, commerciale","Non-Brand","divano da esterno resistente","V3","Ho un giardino al mare con molta salsedine e un budget di circa 2.000 euro, che divano da esterno mi conviene comprare e da chi?","No","Menzione, posizione, competitor","it"
"PS-004","Problem / Solution","Consideration, commerciale","Non-Brand","divano da esterno resistente","V4","Quali divani da esterno resistenti vengono consigliati di più su forum e recensioni online?","No","Menzione, fonti citate","it"
"CC-001","Customer Care / Crisis","Post-acquisto, supporto","Non-Brand","divano da esterno resistente","V1","Come funziona il reso di un divano da esterno acquistato su Verdeluce, chi paga il ritiro?","Sì","Correttezza info, tono","it"
"CC-002","Customer Care / Crisis","Post-acquisto, supporto","Non-Brand","divano da esterno resistente","V2","Quali sono le lamentele più comuni dei clienti Verdeluce sui divani da esterno?","Sì","Criticità ricorrenti, fonti","it"
"CC-003","Customer Care / Crisis","Post-acquisto, supporto","Non-Brand","divano da esterno resistente","V3","Ho comprato un divano da esterno da Verdeluce e dopo una stagione il tessuto si è scolorito, come faccio a chiedere la garanzia?","Sì","Correttezza info, tono","it"
"CC-004","Customer Care / Crisis","Decision, supporto","Non-Brand","divano da esterno resistente","V4","Cosa scrivono su Trustpilot e Reddit di Verdeluce? Ci sono esperienze negative con consegne o assistenza?","Sì","Sentiment, fonti negative","it"
```

---

## 5.5, NOTE OPERATIVE

- Eseguire i prompt Customer Care / Crisis ogni settimana, gli altri ogni mese.
- Usare sessioni anonime, con cronologia e memoria disattivate.
- Lanciare gli stessi prompt su ChatGPT, Perplexity, Gemini e Claude per avere dati confrontabili.
- Per ogni risposta registrare: menzione del brand (Sì/No), posizione, sentiment, competitor citati, fonti citate.
