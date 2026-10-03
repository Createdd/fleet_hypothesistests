# Hypothese 2 (H2): Minimale Flottengröße

## Forschungsfrage

**Ziel:** Bestimmung der **minimal wirtschaftlich vertretbaren Flottengröße** für akzeptable Servicequalität (>85% Servicerate als Zielwert)

**Testszenarien:**
1. **Szenario 1 - Mikroflotte:** 8 Fahrzeuge (absolute Untergrenze)
2. **Szenario 2 - Kleine Flotte:** 16 Fahrzeuge (doppelte Mikroflotte)
3. **Szenario 3 - Basisflotte:** 24 Fahrzeuge (kritischer Schwellenwert)
4. **Szenario 4 - Standardflotte:** 32 Fahrzeuge (Komfortzone)

**Hypothese:** Es existiert ein kritischer Schwellenwert, unterhalb dessen die Servicerate drastisch einbricht (nicht-lineare Skalierung)

## Zentrale Ergebnisse

### Serviceraten nach Flottengröße (kleine Flotten)

| Szenario | Flottengröße | Gesamtkapazität | Bediente Anfragen | Servicerate | Ø Wartezeit | Gesamtzeit | Fahrzeugauslastung |
|----------|--------------|-----------------|-------------------|-------------|-------------|-------------|-------------------|
| **H2-Szenario 1** | 8 Fahrzeuge | 64 Sitze | 41/100 | **41,0%** | 5,34 min | 19,82 min | ~100% |
| **H2-Szenario 2** | 16 Fahrzeuge | 128 Sitze | 70/100 | **70,0%** | 5,05 min | 18,48 min | ~100% |
| **H2-Szenario 3** | 24 Fahrzeuge | 192 Sitze | 92/100 | **92,0%** | 4,67 min | 18,24 min | ~100% |
| **H2-Szenario 4** | 32 Fahrzeuge | 256 Sitze | 95/100 | **95,0%** | 4,09 min | 17,12 min | ~100% |

**Datenquelle:** Direkte Simulationsergebnisse aus `studies/klagenfurt_h2_spitzenzeiten_case_study/results/`

### Skalierungsverhalten-Analyse

**Kritischer Schwellenwert identifiziert:**
- ❌ **8 Fahrzeuge**: Unterversorgung (41% Servicerate) - **nicht vertretbar**
- ⚠️ **16 Fahrzeuge**: Kritischer Bereich (70% Servicerate) - **grenzwertig akzeptabel**
- ✅ **24 Fahrzeuge**: **Optimale Minimalflotte** (92% Servicerate) - **erreicht Akzeptanzgrenze**
- ✅ **32 Fahrzeuge**: Komfortzone (95% Servicerate) - **hohe Zuverlässigkeit**

**Skalierungssprünge (Servicerate-Verbesserung):**
- **8→16 Fahrzeuge** (+100% Flotte): +29% Servicerate (+71% relativer Sprung) → **Größter Effekt!**
- **16→24 Fahrzeuge** (+50% Flotte): +22% Servicerate (+31% relativer Sprung)
- **24→32 Fahrzeuge** (+33% Flotte): +3% Servicerate (+3% relativer Sprung) → **Abnehmender Grenznutzen**

**Wichtige Erkenntnis: Kapazität vs. Räumliche Abdeckung**

Trotz Verdopplung der Sitzplatzkapazität (4→8 Sitze in dieser Studie) bleiben die kritischen Schwellenwerte bei **gleichen Fahrzeuganzahlen**:
- Warum? **Räumliche Verteilung** ist der Hauptlimitierungsfaktor, nicht Sitzplatzanzahl
- Bei 100 Anfragen über 2h auf 12 Zonen: Zu wenig simultane, kompatible Anfragen für konsistentes Pooling
- Zeitliche Constraints (8 min Wartezeit, 40% Umweg) verhindern "Warten bis Fahrzeug voll ist"
- **Bottleneck**: Anzahl Fahrzeuge für räumliche Abdeckung, nicht Sitze pro Fahrzeug
- **Vorteil 8-Sitzer**: Geringere Kosten pro Sitzplatz; Flexibilität für gelegentliches Pooling; Skalierbar bei steigender Nachfrage

### Wartezeitenvergleich

| Flottengröße | Ø Wartezeit | Gesamtzeit | Max. Wartezeit | Verbesserung vs. vorherige Stufe |
|--------------|-------------|-------------|----------------|----------------------------------|
| 8 Fahrzeuge | 5,34 min | 19,82 min | ~8 min | - (Baseline) |
| 16 Fahrzeuge | 5,05 min | 18,48 min | ~8 min | -5,4% Wartezeit |
| 24 Fahrzeuge | 4,67 min | 18,24 min | ~8 min | -7,5% Wartezeit |
| 32 Fahrzeuge | 4,09 min | 17,12 min | ~8 min | -12,4% Wartezeit |

## Strategische Empfehlungen

### Wichtige Erkenntnis: Kapazität vs. Räumliche Abdeckung

**Überraschender Befund:**
Trotz **Verdopplung der Fahrzeugkapazität** (4→8 Sitze) bleiben die **Serviceraten identisch** bei gleicher Fahrzeuganzahl:

- 16 Fahrzeuge × 8 Sitze (128 Gesamtkapazität) = 70% Servicerate
- 24 Fahrzeuge × 8 Sitze (192 Gesamtkapazität) = 92% Servicerate

**Warum ist das so?**

Im On-Demand-Ridepooling ist **räumliche Abdeckung wichtiger als Sitzplatzkapazität**:

1. **Räumliche Verteilung**: Ein Fahrzeug in Zone A kann Anfrage in Zone F nicht bedienen (unabhängig von freien Sitzen)
2. **Zeitliche Constraints**: Max. 8 min Wartezeit und 40% Umweg → Fahrzeuge können nicht "warten bis sie voll sind"
3. **Niedrige Nachfragedichte**: 100 Anfragen über 2h auf 12 Zonen = zu wenig simultane, kompatible Anfragen für konsistentes Pooling
4. **Alonso-Mora Optimierung**: Findet unter gegebenen Constraints oft keine Pool-Partner, auch wenn Sitze frei sind

**Echter Vorteil der 8-Sitzer:**
- ✅ Niedrigere **Kosten pro Sitzplatz** (Anschaffung/Wartung)
- ✅ **Flexibilität** für gelegentliche Pooling-Gelegenheiten
- ✅ **Skalierbar** bei zukünftig höherer Nachfrage

**KEIN Vorteil:**
- ❌ Weniger Fahrzeuge nötig (brauchen immer noch 24 für 92% Service)
- ❌ Drastisch höhere Servicerate bei gleicher Flottengröße

**Konsequenz:** Die minimale Flottengröße wird durch **räumliche Abdeckung** bestimmt, nicht durch Gesamtkapazität.

---

## Zentrale Erkenntnis: Warum doppelte Sitzplatzkapazität nicht die Fahrzeuganzahl halbiert

**Wichtige Beobachtung:** Obwohl die Fahrzeuge jetzt 8 statt 4 Sitze haben (doppelte Kapazität), brauchen wir **gleich viele Fahrzeuge** für die gleiche Servicerate.

### Warum ist räumliche Abdeckung wichtiger als Sitzplatzkapazität?

**Im On-Demand-Ridepooling bestimmt die räumliche Verteilung der Fahrzeuge die Servicerate:**

1. **Räumliches Matching-Problem**
   - 12 Zonen × ~8 Anfragen pro Zone
   - Fahrzeug in Zone A kann Anfrage in Zone F nicht bedienen
   - → Mindestens 1-2 Fahrzeuge pro Zone nötig = 12-24 Fahrzeuge minimum

2. **Zeitliche Constraints**
   - Max. Wartezeit: 8 Minuten (harte Grenze)
   - Max. Umweg: 40% der direkten Fahrzeit
   - → Fahrzeuge können nicht "warten bis voll" ohne Constraints zu verletzen

3. **Niedrige Nachfragedichte**
   - 100 Anfragen über 2 Stunden = 0,83 Anfragen/Minute
   - Räumlich verteilt über 12 Zonen
   - → Geringe Wahrscheinlichkeit für simultane, kompatible Pool-Anfragen
   - → Fahrzeuge fahren oft mit 1-3 Passagieren (nicht voll ausgelastet)

4. **Alonso-Mora Optimierung unter Constraints**
   - Sucht beste Zuordnung unter gegebenen Zeit-/Umweg-Limits
   - Mehr Sitze helfen NUR wenn Anfragen kompatibel sind (gleiche Richtung, Zeitfenster)
   - Bei aktueller Nachfrage: findet oft keine Pool-Partner trotz freier Sitze

### Was bedeutet das konkret?

**Bottleneck ist NICHT Sitzplatzkapazität, sondern:**
- ❌ Zu wenige Fahrzeuge → schlechte räumliche Abdeckung → lange Wartezeiten → niedrige Servicerate
- ✅ Genug Fahrzeuge → gute räumliche Abdeckung → kurze Wartezeiten → hohe Servicerate

**Vorteil der 8-Sitzer liegt woanders:**
- ✅ **Kosteneffizienz**: Geringere Fixkosten pro Sitzplatz
- ✅ **Flexibilität**: Kann gelegentliche Pool-Möglichkeiten nutzen
- ✅ **Skalierbarkeit**: Bei höherer Nachfrage (>200 Anfragen/2h) würden 8-Sitzer deutliche Vorteile bringen

**Praktische Konsequenz:**
- Mit 4-Sitzern: ~24 Fahrzeuge für 92% Servicerate
- Mit 8-Sitzern: ~24 Fahrzeuge für 92% Servicerate
- Unterschied: Niedrigere Kosten/Sitzplatz, nicht weniger Fahrzeuge!

---

## Strategische Empfehlungen

### Kostenoptimierte Betriebsführung

**Phase 1 - Start-up/Pilot (3-6 Monate):**
- **Empfehlung:** 24 Fahrzeuge
- **Servicerate:** 92% (über Mindestziel von 85%)
- **Vorteile:**
  - ✅ Niedrige Anfangsinvestition (60% vs. 40 Fahrzeuge)
  - ✅ Akzeptable Servicequalität für Early Adopters
  - ✅ Testphase für Nachfragevalidierung
  - ✅ 4,67 min durchschnittliche Wartezeit
- **Risiken:**
  - ⚠️ 8% unbediente Anfragen (Reputationsrisiko)
  - ⚠️ Wenig Puffer bei Nachfragespitzen

**Phase 2 - Wachstum (6-12 Monate):**
- **Empfehlung:** 32 Fahrzeuge
- **Servicerate:** 95% (hervorragend)
- **Vorteile:**
  - ✅ Hohe Zuverlässigkeit (nur 5% Ablehnung)
  - ✅ 4,09 min Wartezeit (Premium-Niveau)
  - ✅ Puffer für Nachfrageschwankungen
  - ✅ Wettbewerbsfähig mit ÖPNV

**Phase 3 - Reife (>12 Monate):**
- **Empfehlung:** H1-Szenarien (30-40 Fahrzeuge)
- **Servicerate:** 95-98%
- **Ziel:** Etablierung als Premium-Service

**Kritische Grenze:**
⚠️ **NIEMALS unter 16 Fahrzeuge** (70% Service unakzeptabel für Nutzerakzeptanz)

## Servicequalitäts-Kategorien

| Kategorie | Servicerate | Flottengröße | Bewertung | Anwendungsfall |
|-----------|-------------|--------------|-----------|----------------|
| **Unterversorgung** | <70% | <16 Fahrzeuge | ❌ Nicht vertretbar | Keine |
| **Kritisch** | 70-85% | 16-20 Fahrzeuge | ⚠️ Grenzwertig | Nur im Notfall |
| **Akzeptabel** | 85-95% | 24-32 Fahrzeuge | ✅ Betreibbar | **Minimalbetrieb empfohlen** |
| **Optimal** | >95% | >30 Fahrzeuge | ✅ Hervorragend | Premium-Service |

## Technische Details

### Simulationsparameter
- **Zeitfenster**: 7:00-9:00 Uhr (Morgenspitze)
- **Nachfrage**: 100 Mobilitätsanfragen
- **Algorithmus**: Alonso-Mora Batch Assignment
- **Reoptimierung**: Alle 30 Sekunden
- **Fahrzeugkapazität**: 8 Passagiere (doppelte Kapazität im Vergleich zu älteren 4-Sitzer-Studien)
- **Max. Wartezeit**: 8 Minuten

### Simulation ausführen

```bash
# H2-Simulation starten
python run_klagenfurt_h2_spitzenzeiten.py

# Analyse durchführen
python studies/klagenfurt_h2_spitzenzeiten_case_study/klagenfurt_h2_spitzenzeiten_analysis.py
```

## Kategorisierung der Erkenntnisse

### Direkte Simulationsergebnisse
- Kritischer Schwellenwert bei 16 Fahrzeugen nachgewiesen
- Nicht-lineares Skalierungsverhalten gemessen
- Service-Einbruch unter 16 Fahrzeugen dokumentiert
- Leistungsdaten für 24 Fahrzeuge als Mindestflotte

### Abgeleitete Schlussfolgerungen
- Empfehlungen für Betriebsphasen
- Servicequalitäts-Schwellenwerte
- Wachstumsstrategie-Timing

### Hypothesen für weitere Untersuchungen
- Reale Betriebskosten im Praxisbetrieb
- Langfristige wirtschaftliche Nachhaltigkeit
- Tatsächliche Marktakzeptanz und Nachfrage
- Skalierbarkeit in verschiedenen Marktphasen

## Bekannte Einschränkungen

1. **Synthetische Nachfrage (keine realen Daten)**
   - **Auswirkung:** Mittel
   - **Abschwächung:** Räumliche Verteilung über Zonen, realistische zeitliche Modellierung

2. **Keine Kostendaten (theoretische Schätzungen)**
   - **Auswirkung:** Hoch
   - **Abschwächung:** Fokus auf Servicequalität und Effizienzmetriken

3. **Nur Morgenspitze (keine Tagesvariationen)**
   - **Auswirkung:** Mittel
   - **Abschwächung:** Morgenspitze ist dimensionierungs-kritisch (konservative Schätzung)

## Hinweis zu Kostenanalyse

Diese Studie fokussiert auf **Mindestkapazität und kritische Schwellenwerte**. Detaillierte Kostenanalysen werden in [UC3 (Barrierefreiheit)](UC3_accessibility.md) behandelt, da dort unterschiedliche Fahrzeugtypen mit verschiedenen Kostenstrukturen verglichen werden.

**Für H2 gilt:** Kosten skalieren **linear mit Flottengröße** (identische Fahrzeuge). Die Kostenoptimierung erfolgt implizit durch Bestimmung der **minimalen Flottengröße**, die noch akzeptable Servicequalität (>85% Servicerate) liefert. Ergebnis: **24 Fahrzeuge** als kostenoptimales Minimum.

## Referenzen

- Alonso-Mora et al. (2017) PNAS 114(3): 462-467
- FleetPy Framework (TUM-VT)
- OpenStreetMap Netzwerkdaten

---

**Hinweis:** Diese Dokumentation wurde mithilfe von KI-Tools erstellt und unterstützt.