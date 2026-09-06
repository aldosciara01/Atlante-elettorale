# Atlante elettorale

Sito statico (GitHub Pages) con la mappa della proiezione per le politiche 2027 e approfondimenti sulle elezioni italiane.

- `index.html` — pagina iniziale
- `mappa/index.html` — mappa interattiva; legge `data/unita.json` (basi 2022 e geometrie) e `data/scenario.json` (valori nazionali correnti, coalizioni)
- `approfondimenti/` — analisi; ogni articolo è una pagina HTML che usa `assets/site.css`
- `data/scenario.json` — l'unico file da riscrivere per aggiornare la proiezione
- `CLAUDE.md` — convenzioni per gli aggiornamenti automatici

Pubblicazione: GitHub Pages dal ramo `main`, cartella radice.
