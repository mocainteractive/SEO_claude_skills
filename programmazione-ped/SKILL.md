---
name: programmazione-ped
description: Programma un piano editoriale SEO a partire da un Google Sheet di coda (brand, dominio, cartella Drive, righe Nuovo o Revisione) e crea un'attività pianificata che, a ogni esecuzione, scrive o revisiona un contenuto con le skill SEO, lo salva come Google Doc nella cartella indicata e ne scrive il link nello Sheet, fino a esaurire le righe. Trigger: programmazione piano editoriale, programma un piano editoriale, programma un ped, programma la stesura di contenuti, programma la stesura di articoli, pianifica articoli, schedula i contenuti del ped, automatizza il piano editoriale.
---

# PROGRAMMAZIONE PIANO EDITORIALE

Questa skill non scrive i contenuti direttamente. Fa il setup: legge e valida lo Sheet di coda, controlla la cannibalizzazione, chiede la frequenza, mostra il calendario previsto e crea un'attività pianificata. È l'attività a produrre un contenuto per ogni esecuzione e a disattivarsi quando la coda è finita. I contenuti sono per uso interno: un SEO Specialist li rivede prima di passarli al cliente.

## STRUTTURA DELLO SHEET DI INPUT

- B1 = nome del brand (usato anche nella nomenclatura dei file)
- B2 = dominio del sito
- B3 = link della cartella Drive di destinazione
- Riga 4 = intestazione. I contenuti partono dalla riga 5.
- Colonne:
  - A Tipo: "Nuovo" oppure "Revisione"
  - B Keyword - vol/mese: solo per i Nuovi. Una keyword per riga nella cella, nel formato "keyword - volume". La prima è la primaria, le altre sono secondarie.
  - C URL da rivedere: solo per le Revisioni
  - D Note per il copy: indicazioni vincolanti
  - E Stato: Da fare (anche cella vuota), In lavorazione, Fatto, Saltato, Errore
  - F Link al Google Doc. Durante la lavorazione contiene "Avviata il gg/mm/aaaa - hh:mm"; in caso di Saltato o Errore contiene il motivo.
  - G Ora di lavorazione (AI): data e ora di completamento, nel formato gg/mm/aaaa - hh:mm

## FASE 1, RACCOLTA DELLO SHEET

1. Chiedi il link dello Sheet, se l'utente non l'ha già fornito, e ricava spreadsheetId e gid. Il nome del foglio lo ricavi con get_spreadsheet.
2. Leggi A1:G500 con il connettore Google Sheets. Se il connettore non è disponibile o lo Sheet non è accessibile, fermati e spiega cosa serve.
3. Controlla con list_triggers se esiste già un'attività su questo spreadsheetId. Se esiste, passa alla sezione GESTIONE SUCCESSIVA.

## FASE 2, VALIDAZIONE

Controlla e riporta all'utente in una tabella sintetica (riga, tipo, keyword primaria o URL, stato):

- B1, B2 e B3 compilati. La cartella in B3 deve esistere ed essere scrivibile, verificalo con get_file_metadata.
- La riga 4 corrisponde all'intestazione attesa (colonne da A a G).
- Per ogni riga con A valorizzata:
  - Nuovo: B non vuota e nel formato corretto. Se C è compilata, segnalalo e chiedi se va ignorata.
  - Revisione: C contiene un URL del dominio in B2 che risponde. B può restare vuota.
  - Tipo diverso da Nuovo o Revisione: segnalalo come errore.
- Una E vuota equivale a "Da fare": scrivi tu "Da fare" nelle righe valide con E vuota. Le righe già "Fatto" o "Saltato" non vengono toccate.
- Righe in "Errore": gestiscile come descritto in GESTIONE DEGLI ERRORI prima di proseguire.
- La proprietà GSC corrispondente a B2 deve esistere (GSC-MCP-SERVER, resolve_client). Se manca, avvisa: le revisioni e il controllo di cannibalizzazione useranno solo Ahrefs e DataForSEO.

Se ci sono errori bloccanti, chiedi all'utente di correggerli e rileggi lo Sheet. Le segnalazioni non bloccanti vanno solo riportate. Poi passa alla fase 2B.

## FASE 2B, CONTROLLO CANNIBALIZZAZIONE

È un controllo obbligatorio e va fatto su tutto il PED prima di qualsiasi programmazione. Due keyword cannibalizzano quando soddisfano lo stesso intento di ricerca, anche se sono formulate in modo diverso (per esempio "controlli auto usata" e "cosa verificare prima di comprare un'auto di seconda mano").

### 1. Keyword da verificare
Per ogni riga si verifica una sola keyword, perché le secondarie appartengono allo stesso intento di ricerca della primaria.
- Nuovi: la prima keyword della colonna B.
- Revisioni: la query con più impressioni per l'URL in C negli ultimi 3 mesi, presa da GSC (get_query_page_combinations o get_search_analytics filtrato per pagina). Se GSC non è disponibile, usa la keyword organica principale dell'URL da Ahrefs.
- Considera anche le righe "Fatto" della coda, con la loro keyword primaria: sono contenuti già scritti ma forse non ancora pubblicati.

### 2. Pagine esistenti del sito
- Recupera la sitemap in quest'ordine: da GSC (list_sitemaps e get_sitemap), da <dominio>/sitemap.xml, dalla riga Sitemap di <dominio>/robots.txt. Segui le sitemap index ed estrai tutti gli URL, almeno quelli del blog e delle pagine prodotto.
- Se non trovi la sitemap, fermati e chiedi esplicitamente allo specialist in chat il link della sitemap.xml, spiegando cosa hai provato. Attendi la risposta prima di proseguire.
- Solo se lo specialist conferma che la sitemap non esiste, prosegui con GSC e SERP. In quel caso dichiara nell'esito che il controllo sulle pagine del sito è parziale.

### 3. Verifica dell'intento
- Per ogni keyword del punto 1 scarica la SERP organica di Google Italia, lingua italiano, top 10 (DataForSEO serp_organic_live_advanced; se non risponde, Ahrefs serp-overview).
- Due keyword hanno lo stesso intento quando condividono almeno 4 URL nella top 10. Con 3 URL in comune il caso è limite: segnalalo e valutalo leggendo i title delle SERP.

### 4. Conflitti da cercare
- Tra righe del PED: la keyword di una riga ha lo stesso intento della keyword di un'altra riga. Vale tra Nuovo e Nuovo, tra Nuovo e Revisione, e tra Revisione e Revisione.
- Tra il PED e il sito, stessa keyword: una pagina del sito di qualsiasi tipo (blog, prodotto, categoria) si posiziona entro la 20ª posizione in GSC per la keyword della riga, oppure ha quella keyword come target evidente in title, H1 o slug. È sempre cannibalizzazione.
- Tra il PED e il sito, keyword diversa ma stesso intento (almeno 4 URL in comune nella top 10): tra pagine dello stesso tipo è cannibalizzazione. Tra un articolo e una pagina prodotto o di categoria è una segnalazione non bloccante: va nella tabella per lo specialist e diventa un link interno suggerito nel Doc.
- Per le Revisioni: un'altra pagina del dominio, diversa dall'URL in C, compete per la stessa query. In GSC lo vedi da due o più URL con impressioni sulla stessa query, entrambi entro la 20ª posizione.

### 5. Esito
- Nessun conflitto: riporta in una riga che il controllo è superato, con il numero di keyword e di pagine verificate, poi passa alla fase 3.
- Uno o più conflitti: INTERROMPI il flusso. Non chiedere la frequenza e non creare l'attività. Avvisa lo specialist in chat con una tabella:
  - riga del PED e keyword coinvolta
  - in conflitto con: riga del PED oppure URL del sito
  - evidenza: URL in comune nella top 10 (n su 10), posizione GSC della pagina esistente
  - azione suggerita: unire le due righe, trasformare il Nuovo in Revisione dell'URL esistente, cambiare keyword primaria, togliere la riga
- Chiedi allo specialist di correggere lo Sheet e di dirti quando è pronto. Poi ripeti tutta la fase 2 e la fase 2B da capo.

## FASE 3, FREQUENZA DI PUBBLICAZIONE

Con AskUserQuestion chiedi ogni quanto produrre un contenuto. Opzioni di esempio:
- Uno ogni giorno lavorativo alle 5:00
- Uno ogni lunedì alle 5:00
- Uno al giorno alle 20:00
- Uno ogni 3 ore

L'utente può rispondere in testo libero. Poi:

- Trasforma la risposta in una cron expression con fuso Europe/Rome (`CRON_TZ=Europe/Rome m h dom mon dow`).
- Se l'orario cade esattamente sull'ora (per esempio le 5:00), anticipalo di qualche minuto (per esempio 4:52) e dillo all'utente: le esecuzioni all'ora esatta possono subire ritardi.
- Intervallo minimo: ogni ora. Sotto le 2 ore avvisa che un contenuto completo richiede in genere 30-60 minuti. Due esecuzioni non lavorano mai la stessa riga grazie allo stato "In lavorazione" e all'orario in F, ma con intervalli molto stretti possono sovrapporsi.
- Chiedi la data di partenza, se diversa da subito.

## FASE 4, CALENDARIO E CONFERMA

Mostra il piano editoriale previsto: per ogni riga "Da fare", in ordine, la data e l'ora stimate di esecuzione, il tipo e la keyword primaria o l'URL. Indica la data dell'ultima esecuzione, quella che chiude il flusso. Chiedi conferma prima di creare l'attività.

## FASE 5, CREAZIONE DELL'ATTIVITÀ PIANIFICATA

1. Crea l'attività con create_trigger:
   - name: "[<Brand>] PED contenuti SEO, <frequenza in parole>"
   - cron_expression: quella della fase 3
   - initiation: human_request
   - notifications: {push: true}, così lo specialist riceve l'esito di ogni esecuzione, errori compresi
   - prompt: l'intero PROMPT DI ESECUZIONE qui sotto, copiato senza tagli, compresi il TEMPLATE HTML e lo SCRIPT DI CORREZIONE, con i segnaposto compilati
2. L'attività deve conoscere il proprio ID per potersi disattivare: subito dopo la creazione, aggiorna il prompt con update_trigger inserendo il trigger_id restituito.
3. Controlla l'impostazione di approvazione nella risposta (derived_state.permission_mode). Se non è "auto", spiega che un'attività non presidiata si blocca alla prima approvazione e va impostata su "Approva automaticamente" nelle impostazioni dell'attività.

## FASE 6, AVVIO

Con AskUserQuestion chiedi se partire subito con il primo contenuto o attendere il primo slot del calendario.
- Partire subito: lancia fire_trigger e avvisa che il primo Doc arriverà nella cartella e nello Sheet entro circa un'ora.
- Attendere: indica la data e l'ora della prima esecuzione.

Chiudi con un riepilogo: nome dell'attività, frequenza, numero di contenuti in coda, data prevista di chiusura e impostazione di approvazione.

## PROMPT DI ESECUZIONE (TEMPLATE)

Segnaposto: {SPREADSHEET_ID}, {SHEET_NAME}, {TRIGGER_ID}.

---
Sei in un'esecuzione automatica e non presidiata: nessuno risponde alle domande, quindi non fermarti a chiedere conferme, prendi decisioni ragionevoli e documentale. Scrivi in italiano, con la capitalizzazione italiana, e non usare mai il trattino lungo nei testi (usa la virgola). Considera come data di riferimento quella odierna, fuso Europe/Rome.

OBIETTIVO: produrre UN solo contenuto SEO prendendolo dalla coda nel Google Sheet, salvarlo come Google Doc nella cartella Drive indicata nello Sheet e scrivere il link nello Sheet.

RISORSE
- Google Sheet: spreadsheetId {SPREADSHEET_ID}, foglio "{SHEET_NAME}". B1 brand, B2 dominio, B3 cartella Drive. Riga 4 intestazione, contenuti dalla riga 5. Colonne: A Tipo, B Keyword - vol/mese (la prima riga della cella è la primaria), C URL da rivedere, D Note per il copy, E Stato, F Link al Google Doc, G Ora di lavorazione (AI).
- Google Search Console: la proprietà corrispondente al dominio in B2 (GSC-MCP-SERVER, resolve_client).

PROCEDURA
0. Leggi A1:G500. Controlla le righe in "In lavorazione": se in F c'è "Avviata il gg/mm/aaaa - hh:mm" e sono passate più di 3 ore, imposta Stato "Errore" e scrivi in F "Esecuzione interrotta, avviata il gg/mm/aaaa - hh:mm". Non ritentarle.
1. Prendi la PRIMA riga dalla 5 in giù con Tipo valorizzato e Stato "Da fare" o vuoto. Ignora sempre le righe in "Errore", "Saltato", "Fatto" e "In lavorazione": non ritentarle mai. Se non c'è nessuna riga da lavorare, la coda è finita: disattiva questa attività con update_trigger (trigger_id {TRIGGER_ID}, enabled=false), perché una sessione avviata dall'attività non può eliminarla. Nel resoconto finale elenca le eventuali righe in "Errore" rimaste da gestire, poi termina.
2. Scrivi "In lavorazione" in E e "Avviata il gg/mm/aaaa - hh:mm" in F (ora attuale, fuso Europe/Rome). Rileggi la riga: se in F c'è un orario diverso dal tuo, un'altra esecuzione l'ha presa prima di te, quindi torna al punto 1 e passa alla riga successiva. Memorizza numero di riga, Tipo e keyword primaria oppure URL: ti servono per ritrovare la riga alla fine.
3. Tipo "Nuovo": esegui il flusso completo della skill anthropic-skills:seo-blog-pipeline (keyword-analysis, serp-analysis, brand-analysis-and-connections, content-brief-builder, draft-writer, seo-optimizer, content-reviewer). Usa la prima keyword di B come primaria e le altre come secondarie, sul dominio in B2, rispettando le note in D.
   - Nel controllo di cannibalizzazione verifica l'intento di ricerca della sola keyword primaria: SERP in comune (almeno 4 URL nella top 10) e pagine del dominio posizionate per la keyword in GSC. Considera il sito online e anche le keyword primarie delle righe "Fatto" della stessa coda. Se una pagina del sito di qualsiasi tipo si posiziona per la stessa keyword, è cannibalizzazione. Con keyword diversa ma stesso intento, tra articolo e pagina prodotto o categoria è solo una segnalazione da riportare nei Punti da verificare.
   - Se trovi una cannibalizzazione, non scrivere il testo. Imposta Stato "Errore" e scrivi in F "Cannibalizzazione con: <URL o riga>, evidenza: <URL in comune in SERP o posizione GSC>".
   - Poi interrompi il flusso: disattiva questa attività con update_trigger (trigger_id {TRIGGER_ID}, enabled=false), così lo specialist può decidere in chat prima che si producano altri contenuti. Nel resoconto finale spiega il conflitto e termina.
4. Tipo "Revisione": esegui la skill anthropic-skills:existing-page-optimizer sull'URL in C. Individua le keyword con DataForSEO e Ahrefs, verifica su GSC per quali query la pagina si posiziona oggi e con quali performance, poi scegli primaria e secondarie. Rispetta le note in D. Se DataForSEO non risponde, prosegui con Ahrefs e GSC e annotalo.
   REGOLE DELLA REVISIONE (vincolanti, valgono anche se la colonna D è vuota):
   - L'obiettivo non è stravolgere la struttura del contenuto. Il testo online è la base di partenza e va mantenuto parola per parola dove non serve intervenire.
   - Modifiche e aggiunte solo dove migliorano davvero il testo, e solo con un'evidenza che le giustifica: query GSC non coperte o con posizioni da migliorare, gap rispetto alla SERP o all'AI Overview, errori, informazioni superate. Ogni intervento va nel changelog con la sua evidenza.
   - Non riscrivere da zero, non riformulare frasi corrette solo per stile, non cambiare l'ordine delle sezioni se non c'è un motivo preciso da riportare nel changelog.
   - Elimina solo ciò che è sbagliato, superato o fuori intento, e lascialo comunque visibile nel Doc come testo eliminato.
5. AI OVERVIEW RE-RANKING (obbligatorio): sul testo finale esegui la skill anthropic-skills:ai-overview-reranker su 1-3 keyword, la primaria più le secondarie più rilevanti con AI Overview in SERP. Applica al testo le raccomandazioni concrete (chunking, heading dichiarativi, risposte dirette, information gain, E-E-A-T) senza stravolgere la struttura e rispettando le note in D.
6. Dove le skill chiederebbero una scelta all'utente, scegli l'opzione più ragionevole e riportala nei Punti da verificare come "Scelta fatta in autonomia".
7. CONTENUTO DEL DOC. Struttura sempre in questo ordine. Non aggiungere, togliere, rinominare o riordinare sezioni. Se una sezione non ha contenuto, scrivi "Non applicabile".
   PARTE 1, NOTE PER LO SPECIALIST (da leggere prima dell'articolo)
     1. PUNTI DA VERIFICARE: tabella con 4 colonne, Tipo, Cosa, Dove nell'articolo, Azione richiesta. Una riga per punto. I tipi ammessi sono:
        - "Da confermare con il cliente": informazioni che solo il cliente conosce (condizioni di polizza, prezzi, dati interni);
        - "Da verificare": dati o affermazioni nel testo che non hai potuto confermare con una fonte ufficiale, comprese le correzioni di errori del testo online;
        - "Scelta fatta in autonomia": decisioni che di solito si chiedono allo specialist;
        - "Avviso tecnico": fonti dati non disponibili, segnalazioni di cannibalizzazione non bloccanti.
        "Dove nell'articolo" indica il titolo della sezione e il paragrafo (per esempio: H2 "Titolo", 3° paragrafo) oppure la sezione delle note. "Azione richiesta" dice cosa deve fare lo specialist; per gli avvisi solo informativi scrivi "Nessuna, solo informativo". Se non c'è nulla da segnalare, al posto della tabella scrivi "Nessun punto da verificare".
     2. Revisioni: SITUAZIONE ATTUALE, cioè keyword, posizioni, clic e impressioni da GSC e presenza nell'AI Overview, con una tabella delle query principali. Nuovi: KEYWORD E INTENTO DI RICERCA, con volumi e composizione della SERP.
     3. KEYWORD TARGET: primaria e secondarie con volume.
     4. Revisioni: CHANGELOG, cioè ogni intervento con l'evidenza che lo giustifica. Nuovi: PUNTEGGIO E-E-A-T, con voto e sintesi della review.
     5. LINK INTERNI: in uscita già inseriti nel testo, e in entrata da creare (pagina sorgente, punto del testo, anchor).
     6. AI OVERVIEW RE-RANKING: tabella keyword, punteggio prima (o bozza), dopo (o finale), miglior competitor; poi sotto-query coperte e scoperte, interventi applicati, raccomandazioni non applicate.
     7. NOTE DI LAVORAZIONE: tutto ciò che non rientra nei punti da verificare. Se non c'è nulla, "Nessuna nota".
   PARTE 2, ARTICOLO
     - Blocco "Metadati:" con le righe "Meta title:", "Meta description:" e "URL:" (Nuovi: "URL suggerito:"). Nelle Revisioni, se un valore non cambia, aggiungi " (invariato)".
     - H1, senza etichetta.
     - Testo completo dell'articolo, con H2 e H3 preceduti dall'etichetta del livello.
     - Se ci sono fonti, in fondo il titoletto "Riferimenti normativi" o "Fonti" seguito da un elenco.
   Nelle Revisioni, nella parte 2, il Doc serve anche al cliente per il data entry nel CMS: chi lo usa deve vedere a colpo d'occhio cosa aggiungere, cosa sostituire e cosa togliere. Quindi:
     - tutto ciò che è aggiunto o modificato è evidenziato in rosa Moca (classe "n"): i paragrafi nuovi per intero, e nei paragrafi modificati la parte cambiata, compresi titoli, voci di elenco, celle di tabella e metadati;
     - tutto ciò che è eliminato resta al suo posto, in grigio e barrato come testo cancellato (classe "d"): paragrafi interi, frasi o singole parole. Quando una frase viene sostituita, la versione eliminata in barrato precede subito quella nuova in rosa;
     - il testo invariato resta senza evidenziazione;
     - nessuna modifica deve restare senza segno: prima di creare il Doc confronta il testo finale con quello online e controlla che ogni differenza sia in rosa o in barrato.
   Nei Nuovi: nessuna evidenziazione e nessun barrato.
   Mai etichette come [NUOVO], [RISCRITTO] o [MODIFICATO], mai legende, mai emoji, mai righe vuote doppie.
8. CREAZIONE DEL DOC. Costruisci l'HTML usando ESATTAMENTE il TEMPLATE HTML qui sotto: stesso blocco <style>, stesso <body style="font-family:'Figtree'">, solo gli elementi e le classi indicati, grassetto sempre con <b>. Carica prima la skill anthropic-skills:google-workspace, poi crea il Doc con Drive create_file: title come sotto, parentId = ID della cartella in B3, contentMimeType "text/html", textContent = l'HTML.
   - Nome per i Nuovi: "[<Brand B1>] Articolo <keyword primaria> - GG.MM.AAAA"
   - Nome per le Revisioni: "[<Brand B1>] Revisione <slug della pagina> - GG.MM.AAAA"
9. CORREZIONE AUTOMATICA (obbligatoria). L'import HTML di Google Docs arrotonda i mezzi punti, non crea l'interruzione di pagina né la fascia azzurra e a volte non applica Figtree. Quindi:
   a. Leggi il Doc con read_doc. Il risultato è grande e viene salvato in un file: annota il percorso.
   b. Salva lo SCRIPT DI CORREZIONE qui sotto in postproc.py ed eseguilo: python3 postproc.py <percorso del read_doc>. Stampa {"rev": ..., "requests": [...]}.
   c. Chiama update_doc con requests = il campo "requests" e writeControl = {"requiredRevisionId": il campo "rev"}. Esegui la correzione una volta sola: rieseguirla aggiungerebbe una seconda interruzione di pagina.
   d. Verifica: esporta il Doc in PDF con Drive download_file_content (exportMimeType "application/pdf") e controlla le pagine. Le note devono stare prima dell'articolo, l'articolo deve iniziare su una pagina nuova, tutto deve essere in Figtree con i grassetti al loro posto, H2 e H3 devono avere l'etichetta, evidenziazione e barrato devono comparire solo nelle Revisioni. Correggi quello che non torna con update_doc; se non riesci, aggiungilo nei Punti da verificare come "Avviso tecnico".
10. Prima di scrivere nello Sheet, rileggi A:G e verifica che la riga memorizzata al punto 2 abbia ancora lo stesso Tipo e la stessa keyword o URL. Se lo Sheet è stato modificato e la riga si è spostata, ritrovala per contenuto. Poi scrivi il link del Doc in F (sostituendo "Avviata il..."), imposta Stato "Fatto" in E e scrivi in G data e ora di completamento nel formato gg/mm/aaaa - hh:mm (fuso Europe/Rome).
11. Se qualcosa fallisce in modo non recuperabile, imposta Stato "Errore" e scrivi in F una breve descrizione: cosa è fallito, in quale fase, ed eventualmente il link al Doc parziale. Non ritentare.

Elabora UN solo contenuto per esecuzione. Alla fine riporta in due righe la riga lavorata, l'esito e il link del Doc.

TEMPLATE HTML
Copia il blocco <head> senza modifiche. Il <body> mostra tutti gli elementi ammessi: sostituisci i testi tra parentesi graffe, ripeti gli elementi quanto serve, togli quelli che non servono (per esempio tabelle, evidenziazioni e barrati se non applicabili).

<html><head><meta charset="utf-8"><style>.part,h1{font-size:25.5pt;font-weight:bold;color:#00205B;margin:0 0 12pt 0;line-height:1.2;}.sec{font-size:13pt;font-weight:bold;color:#191919;margin:18pt 0 6pt 0;line-height:1.5;}p,li{font-size:13.5pt;color:#484848;margin:0 0 8pt 0;line-height:1.5;}li{margin:0 0 4pt 0;}.meta{font-size:12pt;color:#191919;margin:0 0 4pt 0;}h2{margin:18pt 0 7pt 0;line-height:1.5;}h3{margin:12pt 0 7pt 0;line-height:1.5;}.lab{font-size:9pt;font-weight:bold;color:#E52217;}.t2{font-size:15pt;font-weight:bold;color:#191919;}.t3{font-size:13pt;font-weight:bold;color:#191919;}.src{font-size:11pt;font-weight:bold;margin:12pt 0 6pt 0;}table{border-collapse:collapse;}td{font-size:10pt;color:#484848;text-align:center;border:1px solid #CCCCCC;padding:3pt 5pt;}td.l{text-align:left;vertical-align:top;}a{color:#E52217;text-decoration:underline;}.n{background-color:#FFE7E6;}.d{color:#A6A6A6;text-decoration:line-through;}</style></head><body style="font-family:'Figtree'">
<p class="part"><b>NOTE PER LO SPECIALIST</b></p>
<p class="sec"><b>1. PUNTI DA VERIFICARE</b></p>
<table><tr><td class="l"><b>Tipo</b></td><td class="l"><b>Cosa</b></td><td class="l"><b>Dove nell'articolo</b></td><td class="l"><b>Azione richiesta</b></td></tr>
<tr><td class="l"><b>{Tipo}</b></td><td class="l">{Cosa}</td><td class="l">{Dove}</td><td class="l">{Azione}</td></tr></table>
<p class="sec"><b>2. {SITUAZIONE ATTUALE oppure KEYWORD E INTENTO DI RICERCA}</b></p>
<p>{Paragrafo di testo, con <b>concetti chiave</b> e <a href="{url}">link</a>.}</p>
<table><tr><td><b>{Intestazione}</b></td><td><b>{Intestazione}</b></td></tr><tr><td><b>{Prima colonna}</b></td><td>{Valore}</td></tr></table>
<p class="sec"><b>3. KEYWORD TARGET</b></p>
<ul><li><b>Primaria:</b> {keyword} ({volume}/mese)</li><li><b>Secondarie:</b> {keyword} ({volume}/mese), ...</li></ul>
<p class="sec"><b>4. {CHANGELOG oppure PUNTEGGIO E-E-A-T}</b></p>
<ul><li>{Voce}</li></ul>
<p class="sec"><b>5. LINK INTERNI</b></p>
<ul><li><b>In uscita, inseriti nel testo:</b> {...}</li><li><b>In entrata, da creare:</b> {...}</li></ul>
<p class="sec"><b>6. AI OVERVIEW RE-RANKING</b></p>
<p class="sec"><b>7. NOTE DI LAVORAZIONE</b></p>
<p class="part"><b>Metadati:</b></p>
<p class="meta"><b>Meta title:</b> {meta title}</p>
<p class="meta"><b>Meta description:</b> <span class="n">{meta description modificata}</span></p>
<p class="meta"><b>URL:</b> <a href="{url}">{url}</a> (invariato)</p>
<h1><b>{Titolo H1} <span class="n">{parte modificata}</span></b></h1>
<p><span class="d">{Paragrafo o frase eliminati}</span></p>
<h2><span class="lab">H2</span>&nbsp;&nbsp;<span class="t2">{Titolo H2}</span></h2>
<p>{Testo invariato} <span class="n">{testo nuovo o modificato}</span> {testo invariato con <b>grassetto</b>}.</p>
<h3><span class="lab">H3</span>&nbsp;&nbsp;<span class="t3 n">{Titolo H3 nuovo; senza la classe n se invariato}</span></h3>
<ul><li>{Voce invariata}</li><li><span class="n">{Voce nuova}</span></li></ul>
<table><tr><td><b>{Intestazione}</b></td><td><b>{Intestazione}</b></td></tr><tr><td><b><span class="n">{Prima colonna}</span></b></td><td><span class="n">{Valore nuovo}</span></td></tr></table>
<p class="src"><b>{Riferimenti normativi oppure Fonti}</b></p>
<ul><li>{Fonte}</li></ul>
</body></html>

SCRIPT DI CORREZIONE (postproc.py)

import json,sys
d=json.load(open(sys.argv[1])); c=d.get('content',d)
body=c['tabs'][0]['documentTab']['body']['content']; END=body[-1]['endIndex']
def rgb(ts):
    x=ts.get('foregroundColor',{}).get('color',{}).get('rgbColor',{})
    return '#%02X%02X%02X'%tuple(round(x.get(k,0)*255) for k in ('red','green','blue'))
runs=[];paras=[]
def walk(els):
    for el in els:
        if 'paragraph' in el:
            p=el['paragraph']; paras.append((el['startIndex'],el['endIndex'],''.join(r.get('textRun',{}).get('content','') for r in p['elements']).strip(),p.get('paragraphStyle',{}).get('namedStyleType')))
            runs.extend(r for r in p['elements'] if 'textRun' in r)
        elif 'table' in el:
            for row in el['table']['tableRows']:
                for cell in row['tableCells']: walk(cell['content'])
walk(body)
FIX={(13,'#484848'):13.5,(25,'#00205B'):25.5}
m=[]
for r in runs:
    ts=r['textRun'].get('textStyle',{}); k=(ts.get('fontSize',{}).get('magnitude'),rgb(ts))
    if k in FIX:
        a,b,s=r['startIndex'],min(r['endIndex'],END-1),FIX[k]
        if m and m[-1][1]==a and m[-1][2]==s: m[-1][1]=b
        else: m.append([a,b,s])
req=[]
if any(r['textRun'].get('textStyle',{}).get('weightedFontFamily',{}).get('fontFamily')!='Figtree' for r in runs):
    req.append({"updateTextStyle":{"range":{"startIndex":1,"endIndex":END-1},"textStyle":{"weightedFontFamily":{"fontFamily":"Figtree"}},"fields":"weightedFontFamily"}})
    for r in runs:
        if r['textRun'].get('textStyle',{}).get('bold'):
            req.append({"updateTextStyle":{"range":{"startIndex":r['startIndex'],"endIndex":min(r['endIndex'],END-1)},"textStyle":{"bold":True},"fields":"bold"}})
req+=[{"updateTextStyle":{"range":{"startIndex":a,"endIndex":b},"textStyle":{"fontSize":{"magnitude":s,"unit":"PT"}},"fields":"fontSize"}} for a,b,s in m if b>a]
for a,b,t,st in paras:
    if t in ('NOTE PER LO SPECIALIST','Metadati:') or st=='HEADING_1':
        req.append({"updateParagraphStyle":{"range":{"startIndex":a,"endIndex":b},"paragraphStyle":{"shading":{"backgroundColor":{"color":{"rgbColor":{"red":0.922,"green":0.973,"blue":1}}}}},"fields":"shading"}})
for el in body:
    if 'table' in el:
        t=el['table']; first=''.join(x.get('textRun',{}).get('content','') for x in t['tableRows'][0]['tableCells'][0]['content'][0]['paragraph']['elements']).strip()
        if first=='Tipo' and t['columns']==4:
            for i,w in enumerate([100,170,100,98]):
                req.append({"updateTableColumnProperties":{"tableStartLocation":{"index":el['startIndex']},"columnIndices":[i],"tableColumnProperties":{"widthType":"FIXED_WIDTH","width":{"magnitude":w,"unit":"PT"}},"fields":"widthType,width"}})
req.append({"insertPageBreak":{"location":{"index":[a for a,b,t,s in paras if t=='Metadati:'][0]}}})
print(json.dumps({"rev":c['revisionId'],"requests":req},separators=(',',':')))
---

## GESTIONE DEGLI ERRORI

Le esecuzioni non ritentano mai una riga in "Errore". Decide lo specialist, in chat, quando richiama la skill. Per ogni riga in errore:
1. Mostra il tipo, la keyword o l'URL e il motivo scritto in F.
2. Se il motivo è una cannibalizzazione, prima di chiedere rifai per quella riga il controllo della fase 2B e mostra la tabella dei conflitti con l'azione suggerita.
3. Con AskUserQuestion chiedi cosa fare:
   - Rimettere in coda così com'è: E torna "Da fare", F e G vengono svuotate
   - Correggere note, keyword o URL e poi rimettere in coda
   - Segnare come "Saltato"
   - Lasciare in "Errore"
4. Se le keyword della riga sono cambiate, ripeti la fase 2B su tutto il PED prima di riattivare.
5. Se la coda era finita, o l'attività era stata disattivata per una cannibalizzazione, e almeno una riga torna "Da fare", riattiva l'attività con update_trigger (enabled=true).

## GESTIONE SUCCESSIVA

Se l'utente richiama la skill su uno Sheet che ha già un'attività:
- Mostra lo stato: attività attiva o disattivata, prossima esecuzione, righe Fatte, Saltate, in Errore e in coda.
- Righe in "Errore": gestiscile come descritto in GESTIONE DEGLI ERRORI.
- Righe aggiunte: validale come nella fase 2 e ripeti la fase 2B su tutto il PED, righe nuove comprese. Se l'attività era disattivata, riattivala con update_trigger (enabled=true) e mostra il nuovo calendario.
- Cambio di frequenza: update_trigger sulla cron_expression.
- Pausa o stop: update_trigger con enabled=false.
- Righe ferme in "In lavorazione" da più di 3 ore secondo l'orario in F: la prossima esecuzione le segna da sola come "Errore, esecuzione interrotta". Se l'attività è ferma, chiedi allo specialist se rimetterle in "Da fare".
