# Atlante elettorale — istruzioni per le sessioni di aggiornamento

Sito statico pubblicato con GitHub Pages dal ramo `main` (cartella radice). Nessun build step: ogni file HTML è completo e autonomo.

## Struttura
- `index.html`: pagina iniziale con le schede degli approfondimenti (aggiungere una scheda `.card` per ogni nuovo articolo).
- `mappa/index.html`: mappa interattiva D3. Non modificarla per aggiornare i dati.
- `data/scenario.json`: valori nazionali correnti. È l'UNICO file da riscrivere per l'aggiornamento periodico. Campi: `version` (intero, incrementare), `updatedAt` (ISO), `updatedLabel` (data in italiano), `media` {`date` ISO dell'ultimo sondaggio incluso, `label` della finestra (es. "1–7 settembre 2026"), `name`, `method`, `polls` (array: `ist`, `comm`, `field`, `pub`, `scarto`, `peso`, `url`), `lists` nome lista → percentuale media}, `previous` {`date`, `label`, `name`, `lists`} con la media precedente, `adjustments` {CasaRif, Centro}, `targets` (chiavi esattamente FdI, PD, M5S, FN, FI, AVS, Lega, CasaRif, Centro, NM, Altri; somma 100), `prevTargets` (stesse chiavi, valori della media precedente: servono alle frecce di variazione in home), `coalitions` (perimetri, NON cambiare finché non saranno depositate le liste ufficiali).
  Ad ogni aggiornamento: PRIMA copiare `media` in `previous` (tenendo solo `date`, `label`, `name`, `lists`) e `targets` in `prevTargets`, POI scrivere i nuovi valori.
- `data/unita.json`: basi 2022 e geometrie delle 186 unità. Non toccare.
- `data/sicilia.json`: proiezione delle regionali siciliane per provincia e circoscrizione di Palermo, generata da `build_sicilia.py` (scenario di liste e candidati definito in testa allo script; rieseguirlo con `python3 build_sicilia.py` dopo ogni modifica dello scenario, quindi aggiornare a mano la tabella e i numeri nel testo di `approfondimenti/regionali-sicilia-2027.html`). Richiede il pacchetto Python `shapely`.
- `approfondimenti/amministrative-2027.html`: contiene la mappa per municipio delle sei città al voto con dati infracomunali (Roma, Milano, Napoli, Torino, Bologna, Palermo). Legge `data/unita.json` e `data/scenario.json` e rifà la proiezione nel browser: si aggiorna da sola con la media, ma i numeri citati in prosa (municipi vinti, primi partiti, punte percentuali) vanno riletti quando la media cambia in modo sensibile.
- `approfondimenti/`: un file HTML per articolo, più `index.html` (elenco) e `metodo.html`. Le simulazioni degli appuntamenti elettorali (`regionali-sicilia-2027.html`, `amministrative-2027.html`, `primarie-centrosinistra-2027.html`) vanno aggiornate quando escono candidature ufficiali o nuovi sondaggi.
- `data/appuntamenti.json`: gli appuntamenti mostrati nella colonna laterale della home (tipo, luogo, `date` ISO se fissata altrimenti `null` con `periodo` stimato, nota, link, forma). Il markup della colonna in `index.html` va rigenerato a mano quando cambia il file: card con silhouette SVG, titolo, conto alla rovescia (solo se `date` è valorizzata) oppure periodo stimato.
- `assets/site.css`: stile condiviso.

## Come si costruisce la media ponderata
Ogni settimana si raccolgono tutte le rilevazioni nazionali di intenzioni di voto di lista pubblicate nei sette giorni precedenti (registro sondaggipoliticoelettorali.it, siti degli istituti, politpro.eu, rassegne). Si tiene **una sola rilevazione per istituto**, la più recente pubblicata nella finestra. **Lab21 è sempre escluso.** Ogni sondaggio viene prima tradotto nelle chiavi dello scenario, poi entra nella media con peso pari a 1/scarto medio dell'istituto (i pesi vengono normalizzati a 100). Scarti medi 2022-2024: Ipsos 11,4; Eumetra 13,2; Cluster17 13,2; SWG 13,3; Ixè 14,0; YouTrend (Quorum) 14,1; BiDiMedia 14,2; Noto 14,4; EMG 14,5; Demopolis 14,8; Euromedia 15,5; Tecnè 15,8; CISE 16,9; Termometro Politico 17,4; Piepoli 18,1; Lab21 23,8 (escluso). Istituti non in tabella (Only Numbers, Izi, Winpoll…): scarto 14,7, la media del gruppo.

Traduzione di ogni sondaggio in `targets`: FdI = Fratelli d'Italia; PD; M5S; FN = Futuro Nazionale; FI = Forza Italia; AVS; Lega; NM = Noi Moderati (0,8 se assente); CasaRif = Italia Viva + +Europa + adjustments.CasaRif (se la rilevazione riporta già "Casa Riformista", usare quel valore senza aggiunta); Centro = Azione + PLD se rilevato, altrimenti Azione + adjustments.Centro; Altri = 100 − somma degli altri dieci, mai sotto 1,0 (in tal caso ridurre le aggiunte). La media dei valori così ottenuti si arrotonda a un decimale e la differenza di arrotondamento si scarica su Altri, perché la somma faccia esattamente 100. Aggiornare solo se sono usciti sondaggi successivi a `media.date`.

Dopo l'aggiornamento vanno riviste anche le simulazioni che citano numeri nazionali: `approfondimenti/scenari-2027.html` (cifre utili e tabelle dei seggi nei due scenari), la frase sugli aggregati regionali in `regionali-sicilia-2027.html` e i valori Nord/Centro/Sud in `primarie-centrosinistra-2027.html`. I seggi si calcolano con la stessa funzione `computeSeats` di `index.html`.

## Nuovo articolo
Copiare la struttura di `approfondimenti/scenari-2027.html` (head con `site.css`, `nav.site-nav`, `main.prose`, `footer.site-footer`, script finale che legge `scenario.json`). Prosa accademica, niente elenchi puntati; tabelle solo per numeri. Aggiungere la scheda in `approfondimenti/index.html` e, se rilevante, in `index.html`.

## Commit
Messaggi in italiano, brevi: "Media ponderata dei sondaggi del 15–21 settembre 2026" per gli aggiornamenti dati, "Approfondimento: <titolo>" per gli articoli.
