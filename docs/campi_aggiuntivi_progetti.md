## Campi dei progetti/attività aggiuntivi per piattaforma IT (15 campi)

| Campo | Tipo | Esempio (dal progetto 24) | Significato |
|---|---|---|---|
| `type` | string | `"Attività"` | Tipo: Progetto o Attività (progetti e attività hanno la stessa tabella perché differiscono solo in questo campo e nel campo bsw sottostante) |
| `latitude` / `longitude` | string (decimal) | `"45.322500"`, `"8.430000"` | Coordinate geografiche per il punto sulla mappa |
| `bsw` | string | `"2025"` | Anno della Biodiversity Sampling Week (si applica solo alle attività) |
| `provincia` | array di ID | `[65]` | Province italiane (molti a molti), la prima viene utilizzata per il punto sulla mappa in assenza di coordinate specifiche le altre sono descrittive sul dettaglio del progetto/Attività |
| `localita` | int (FK) | `1` | Riferimento alla regione, viene presa dalla prima provincia |
| `aree` | JSON/null | `null` | Aree geografiche con il GEOJson |
| `tipo_pubblico` | string | `"pubblico generico"` | Target audience |
| `tipo_pubblico_altro` | string/null | `null` | Altro target |
| `inaturalist` | string/null | `null` | Link iNaturalist |
| `risultati` | string/null | `null` | Risultati |
| `parent` | int/null | `null` | Progetto padre |
| `logo` / `logoCredit` | image/null | `null` | Logo, separato dalle immagini |