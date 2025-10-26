## Hypothese 1 (H1): Servicequalität-Optimierung

Ziel: Optimierung der Servicequalität bei akzeptabler Kosteneffizienz.

## Testszenarien
- 20 Fahrzeuge (Basisflotte)
- 30 Fahrzeuge (Balance Kosten/Service)
- 40 Fahrzeuge (Servicequalität priorisiert)

## Zentrale Ergebnisse

### Serviceraten nach Flottengröße
| Szenario | Flottengröße | Bediente Anfragen | Servicerate | Ø Wartezeit | Fahrzeugauslastung |
|----------|--------------|-------------------|-------------|-------------|--------------------|
| 20 Fzg   | 20           | 84/100            | 84,0%       | 5,0 min     | 100%               |
| 30 Fzg   | 30           | 95/100            | 95,0%       | 4,2 min     | 100%               |
| 40 Fzg   | 40           | 98/100            | 98,0%       | 3,6 min     | 92,5%              |

## Kategorisierung der Erkenntnisse

### Direkte Simulationsergebnisse
- Servicerate steigt mit Flottengröße; nicht-linear mit abnehmendem Grenznutzen >30 Fahrzeuge
- Wartezeiten reduzieren sich von 5,0 auf 3,6 Minuten (20 → 40 Fzg)
- Alle Szenarien erfüllen die 8-Minuten-Grenze

### Abgeleitete Schlussfolgerungen
- 30 Fahrzeuge als beste Kosten-Nutzen-Balance
- 40 Fahrzeuge nur bei Premium-Anspruch sinnvoll

### Hypothesen für weitere Untersuchungen
- Dynamische Repositionierung in Randlagen
- Einfluss unterschiedlicher Zonen-/Zentroiden-Layouts

## Strategische Empfehlungen
- 30 Fahrzeuge empfohlen für >95% Servicerate bei guter Effizienz
- 20 Fahrzeuge nur für kostenoptimierte Pilotphasen
- 40 Fahrzeuge für Premium-Service mit höherem Aufwand

## Technische Details
- Zeitfenster: 7–9 Uhr (Morgenspitze), Nachfrage: 100 Anfragen
- Algorithmus: Alonso-Mora Batch Assignment, Reoptimierung alle 30s
- Parameter: max. Wartezeit 8 min, Kapazität 4, Zonen: 12

### Simulation ausführen
```bash
python run_klagenfurt_h1_spitzenzeiten.py
python klagenfurt_h1_spitzenzeiten_analysis.py
```

## Hinweis zu Kostenanalyse

Diese Studie fokussiert auf **Servicequalität und Kapazitätsplanung**. Detaillierte Kostenanalysen werden in [UC3 (Barrierefreiheit)](UC3_accessibility.md) behandelt, da dort unterschiedliche Fahrzeugtypen mit verschiedenen Kostenstrukturen verglichen werden.

**Für H1 gilt:** Kosten skalieren **linear mit Flottengröße** (identische Fahrzeuge), daher ist die Kostenoptimierung implizit durch Minimierung der Flottengröße bei Zielvorgabe (z.B. >95% Servicerate) gegeben.

## Datenquelle
- Direkte Simulationsergebnisse aus `studies/klagenfurt_h1_spitzenzeiten_case_study/results/`

## Referenzen
- Alonso-Mora et al. (2017) PNAS 114(3): 462–467
- FleetPy Framework (TUM-VT)
- OpenStreetMap Netzwerkdaten