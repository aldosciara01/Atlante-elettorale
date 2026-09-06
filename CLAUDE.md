# Atlante elettorale — istruzioni per le sessioni di aggiornamento

Sito statico pubblicato con GitHub Pages dal ramo `main` (cartella radice). Nessun build step: ogni file HTML è completo e autonomo.

## Struttura
- `index.html`: pagina iniziale con le schede degli approfondimenti (aggiungere una scheda `.card` per ogni nuovo articolo).
- `mappa/index.html`: mappa interattiva D3. Non modificarla per aggiornare i dati.
- `data/scenario.json`: valori nazionali correnti. È l'UNICO file da riscrivere per l'aggiornamento periodico. Campi: `version` (intero, incrementare), `updatedAt` (ISO), `updatedLabel` (data in italiano), `supermedia` {`date` ISO, `label` in italiano, `url` dell'articolo, `lists` nome lista → percentuale}, `adjustments` {CasaRif, Centro}, `targets` (chiavi esattamente FdI, PD, M5S, FN, FI, AVS, Lega, CasaRif, Centro, NM, Altri; somma 100), `coalitions` (perimetri, NON cambiare finché non saranno depositate le liste ufficiali).
- `data/unita.json`: basi 2022 e geometrie delle 186 unità. Non toccare.
- `approfondimenti/`: un file HTML per articolo, più `index.html` (elenco) e `metodo.html`.
- `assets/site.css`: stile condiviso.

## Regola di traduzione Supermedia → targets
FdI = Fratelli d'Italia; PD; M5S; FN = Futuro Nazionale; FI = Forza Italia; AVS; Lega; NM = Noi Moderati (0,8 se assente); CasaRif = Italia Viva + +Europa + adjustments.CasaRif (se la Supermedia riporta già "Casa Riformista", usare quel valore senza aggiunta); Centro = Azione + adjustments.Centro (se compaiono PLD o una lista unica di centro, sommarli ad Azione al posto dell'aggiunta); Altri = 100 − somma degli altri dieci, arrotondato a un decimale, mai sotto 1,0 (in tal caso ridurre le aggiunte). Aggiornare solo se la Supermedia trovata è successiva a `supermedia.date`; verificare che la somma delle liste lette sia tra 92 e 100.

## Nuovo articolo
Copiare la struttura di `approfondimenti/scenari-2027.html` (head con `site.css`, `nav.site-nav`, `main.prose`, `footer.site-footer`, script finale che legge `scenario.json`). Prosa accademica, niente elenchi puntati; tabelle solo per numeri. Aggiungere la scheda in `approfondimenti/index.html` e, se rilevante, in `index.html`.

## Commit
Messaggi in italiano, brevi: "Supermedia del 17 settembre 2026" per gli aggiornamenti dati, "Approfondimento: <titolo>" per gli articoli.
