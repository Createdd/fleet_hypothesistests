## Hypothese 1 (H1): Servicequalität-Optimierung

Ziel: Optimierung der Servicequalität bei akzeptabler Kosteneffizienz.

## Testszenarien
- 8 Fahrzeuge (Kleine Flotte) - je 8 Sitzplätze
- 16 Fahrzeuge (Mittlere Flotte) - je 8 Sitzplätze
- 24 Fahrzeuge (Große Flotte) - je 8 Sitzplätze

## Zentrale Ergebnisse

### Serviceraten nach Flottengröße
| Szenario | Flottengröße | Kapazität | Bediente Anfragen | Servicerate | Ø Wartezeit | Fahrzeugauslastung |
|----------|--------------|-----------|-------------------|-------------|-------------|--------------------|
| Szenario 1 | 8  | 64 Sitze  | 41/100            | 41,0%       | 5,3 min     | 100%               |
| Szenario 2 | 16 | 128 Sitze | 70/100            | 70,0%       | 5,0 min     | 100%               |
| Szenario 3 | 24 | 192 Sitze | 92/100            | 92,0%       | 4,7 min     | 100%               |## Kategorisierung der Erkenntnisse

### Direkte Simulationsergebnisse
- Servicerate steigt mit Flottengröße; nicht-linear mit abnehmendem Grenznutzen ab 24 Fahrzeugen
- Wartezeiten reduzieren sich von 5,3 auf 4,7 Minuten (8 → 24 Fzg)
- Alle Szenarien erfüllen die 8-Minuten-Grenze
- **Kritischer Sprung**: 8→16 Fahrzeuge (+29% Servicerate), 16→24 Fahrzeuge (+22% Servicerate)

### Zentrale Erkenntnis: Räumliche Abdeckung wichtiger als Sitzplatzkapazität

**Überraschung:** Trotz doppelter Fahrzeugkapazität (8 statt 4 Sitze) brauchen wir **gleich viele Fahrzeuge** für gleiche Servicerate!

**Warum?** Im On-Demand-Ridepooling ist die räumliche Verteilung der Fahrzeuge entscheidend:
- Ein Fahrzeug in Zone A kann Anfrage in Zone F nicht bedienen - egal ob 4 oder 8 Sitze
- Zeitliche Constraints (max. 8 min Wartezeit, 40% Umweg) verhindern "Warten auf volle Fahrzeuge"
- Nachfragedichte zu niedrig (100 Anfragen / 2h / 12 Zonen) für konsistentes Vollauslastungs-Pooling
- Alonso-Mora findet unter den Constraints oft keine kompatiblen Pool-Partner

**Echter Vorteil der 8-Sitzer:**
- ✅ Geringere Kosten pro Sitzplatz (Anschaffung, Wartung)
- ✅ Flexibilität für gelegentliche Pooling-Gelegenheiten
- ✅ Skalierbar bei steigender Nachfrage

**Kein Vorteil bei:**
- ❌ Reduktion der Fahrzeuganzahl (räumliche Abdeckung bleibt Bottleneck)
- ❌ Drastische Servicerate-Verbesserung bei gleicher Flottengröße

### Abgeleitete Schlussfolgerungen
- 24 Fahrzeuge (je 8 Sitze) erreichen 92% Servicerate - empfohlenes Minimum
- 16 Fahrzeuge nur für kostenoptimierte Pilotphasen (70% Servicerate)
- **Wichtige Erkenntnis**: Verdopplung der Sitzplatzkapazität (4→8 Sitze) führt NICHT zu Halbierung der benötigten Fahrzeuge
  - Grund: **Räumliche Abdeckung** ist kritischer als Sitzplatzanzahl
  - Bei niedriger Nachfragedichte (100 Anfragen/2h/12 Zonen) fahren Fahrzeuge oft nicht voll
  - Zeitliche Constraints (8 min Wartezeit, 40% Umweg) verhindern "Warten auf volle Fahrzeuge"
  - Vorteil der 8-Sitzer: Geringere Kosten pro Sitzplatz, Flexibilität für gelegentliches Pooling

### Hypothesen für weitere Untersuchungen
- Dynamische Repositionierung in Randlagen
- Einfluss unterschiedlicher Zonen-/Zentroiden-Layouts

## Strategische Empfehlungen
- **24 Fahrzeuge (192 Sitze)** empfohlen für >90% Servicerate bei guter Effizienz
- **16 Fahrzeuge (128 Sitze)** nur für kostenoptimierte Pilotphasen (70% Servicerate akzeptabel)
- **8 Fahrzeuge (64 Sitze)** unzureichend (nur 41% Servicerate)
- Für >95% Servicerate siehe H2-Studie (32 Fahrzeuge empfohlen)

## Technische Details
- Zeitfenster: 7–9 Uhr (Morgenspitze), Nachfrage: 100 Anfragen
- Algorithmus: Alonso-Mora Batch Assignment, Reoptimierung alle 30s
- Parameter: max. Wartezeit 8 min, **Fahrzeugkapazität: 8 Sitzplätze**, Zonen: 12

### Simulation ausführen
```bash
python run_klagenfurt_h1_spitzenzeiten.py
jupyter notebook studies/klagenfurt_h1_spitzenzeiten_case_study/analysis/klagenfurt_h1_spitzenzeiten_analysis.ipynb
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

---

**Hinweis:** Diese Dokumentation wurde mithilfe von KI-Tools erstellt und unterstützt.