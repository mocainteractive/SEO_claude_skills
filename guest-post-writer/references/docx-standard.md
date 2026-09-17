# Standard unico per il deliverable in .docx (guest post)

Scopo: quando il guest post va consegnato in **Word (.docx)**, ogni documento deve avere **lo stesso identico formato**. Questo file è la specifica da rispettare sempre, così due guest post diversi producono due .docx graficamente coerenti.

**Come costruirlo:** usa la skill `docx` (python-docx) applicando **esattamente** i parametri qui sotto. Il contenuto del documento è **solo l'articolo**, dall'H1 alla chiusura: nessuna copertina, legenda, intestazione con metadati, nota, riepilogo, indice (TOC), header o footer.

## Pagina
- Formato **A4**, orientamento verticale.
- Margini **2,5 cm** su tutti i lati.
- Nessun header, footer, numero di pagina, copertina o indice.

## Font e colori (bianco e nero)
- **Font unico per tutto: Calibri** (fallback Arial se Calibri non disponibile).
- Testo, heading e grassetto in **nero** (RGB 000000), su sfondo bianco.
- **Nessun colore** su paragrafi o testo e **nessuna evidenziazione**. L'unica eccezione è l'anchor del link cliente (vedi sotto).

## Stili (fissi)
- **H1** (titolo articolo, uno solo, in cima): Calibri **20 pt**, grassetto, nero, allineato a sinistra, spazio dopo 12 pt. Maiuscola solo sulla prima parola e sui nomi propri (mai title case, mai maiuscolo).
- **H2**: Calibri **15 pt**, grassetto, nero. Spazio prima 14 pt, dopo 6 pt.
- **H3**: Calibri **13 pt**, grassetto, nero. Spazio prima 10 pt, dopo 4 pt.
- **Corpo**: Calibri **11 pt**, nero, allineato a **sinistra** (niente giustificato), interlinea **1,15**, spazio dopo **8 pt**, nessun rientro di prima riga.
- **Grassetto**: inline, nero, secondo i criteri di scrittura (max 1–2 elementi per paragrafo, mai intere frasi, mai sulle keyword).
- **Liste**: elenchi puntati/numerati nativi di Word, **solo** dove l'articolo li prevede davvero.

## Link del cliente (anchor)
- L'anchor è un **hyperlink reale** verso l'URL target del cliente.
- Stile anchor: **rosso (RGB FF0000), sottolineato**. È l'**unico** elemento colorato del documento (serve a rendere il link subito individuabile in revisione).
- Con **due URL**: link in **paragrafi distinti**, l'URL principale sempre **più in alto** del secondo (come da regole di scrittura).
- Eventuali link a **fonti autorevoli** (solo se la policy di sessione li ammette): hyperlink **neri sottolineati** (non rossi), per distinguerli dal link cliente.

## Nome file
- `guest-post_[dominio-portale]_[slug-topic].docx` — tutto minuscolo, senza spazi né accenti, parole separate da trattino. Esempio: `guest-post_ilportale-it_panettone-artigianale.docx`.

## Cosa NON includere (mai)
- Nessuna intestazione con lunghezza richiesta/consegnata, elenco keyword o metadati.
- Nessuna "Nota strategica", nota al revisore, commento, riepilogo o esito del controllo.
- Nessuna sezione finale "Domande frequenti"/"FAQ".
- Solo l'articolo: si parte dall'H1 e si finisce con la chiusura del pezzo.
