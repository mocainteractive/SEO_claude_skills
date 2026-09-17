# Standard unico per il deliverable in .docx (guest post)

Scopo: quando il guest post va consegnato in **Word (.docx)**, ogni documento deve avere **lo stesso identico formato**, con il **font di Moca (Figtree)**. Questo file è la specifica da rispettare sempre.

**Regola ferrea sul contenuto:** il documento contiene **solo il testo dell'articolo**, dall'H1 alla chiusura. **Nessuna nota** di alcun tipo nel file: eventuali note, avvertenze, `[DATO DA VERIFICARE]`, riepiloghi o esiti del controllo vanno **nella chat di risposta**, mai nel .docx. Niente copertina, legenda, metadati (lunghezza/keyword), "Nota strategica", commenti, indice (TOC), header, footer, sezione FAQ.

**Come costruirlo:** usa la skill `docx` (python-docx) applicando **esattamente** i parametri sotto. Imposta il font **sia sui run sia sugli stili**, e **sovrascrivi il colore degli heading a nero**: gli stili "Titolo/Heading" predefiniti di Word sono blu (es. `2E74B5`) — non usarli così, altrimenti i titoli escono blu e in Times New Roman. Ogni titolo va in **Figtree nero**.

## Pagina
- Formato **A4**, verticale. Margini **2,5 cm** su tutti i lati.
- Nessun header, footer, numero di pagina, copertina o indice.

## Font (Moca) e colori
- **Font unico per tutto: Figtree** (body, H1, H2, H3, grassetto, liste). Fallback: Arial/Helvetica se Figtree non è installato.
  - Per garantire la resa ovunque, **incorpora il font** nel .docx se il file Figtree è disponibile (embed TrueType). Se non è disponibile, imposta comunque il nome "Figtree" (renderà dove il font è installato, con fallback altrove).
- **Tutto in nero** (RGB 000000), sfondo bianco. **Heading compresi** (nessun blu). Nessun colore sui paragrafi, nessuna evidenziazione. Unica eccezione: l'anchor del link cliente (sotto).

## Stili (fissi)
- **H1** (titolo articolo, uno solo, in cima): Figtree **18 pt**, grassetto, nero, allineato a sinistra, spazio dopo 12 pt. Maiuscola solo sulla prima parola e sui nomi propri (mai title case, mai maiuscolo).
- **H2**: Figtree **14 pt**, grassetto, nero. Spazio prima 14 pt, dopo 6 pt.
- **H3**: Figtree **12 pt**, grassetto, nero. Spazio prima 10 pt, dopo 4 pt.
- **Corpo**: Figtree **11 pt**, nero, allineato a **sinistra** (niente giustificato), interlinea **1,15**, spazio dopo **8 pt**, nessun rientro di prima riga.
- **Grassetto**: inline, nero, secondo i criteri di scrittura (max 1–2 per paragrafo, mai intere frasi, mai sulle keyword).
- **Liste**: elenchi puntati/numerati nativi di Word, **solo** dove l'articolo li prevede davvero.

## Link del cliente (anchor)
- L'anchor è un **hyperlink reale** verso l'URL target del cliente.
- Stile anchor: **rosso (RGB FF0000), sottolineato**. È l'**unico** elemento colorato del documento (rende il link individuabile in revisione).
- Con **due URL**: link in **paragrafi distinti**, l'URL principale sempre **più in alto** del secondo.
- Eventuali link a **fonti autorevoli** (solo se la policy di sessione li ammette): hyperlink **neri sottolineati** (non rossi).

## Nome file
- `guest-post_[dominio-portale]_[slug-topic].docx` — minuscolo, senza spazi né accenti, parole separate da trattino. Es. `guest-post_ideegreen-it_arredo-modulare-bambini.docx`.

## Checklist prima di consegnare
1. Solo articolo, **zero note** nel file (le note stanno in chat).
2. Font **Figtree** ovunque, **tutto nero**, heading inclusi (nessun blu/Times New Roman residuo dagli stili default).
3. Anchor = hyperlink rosso sottolineato; secondo URL più in basso, in paragrafo distinto.
4. Nessun header/footer/copertina/TOC/FAQ.
