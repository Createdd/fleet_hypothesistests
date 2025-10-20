# 🔬 Hypothese 2 (H2): Minimale Flottengröße

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

| Szenario | Flottengröße | Bediente Anfragen | Servicerate | Ø Wartezeit | Gesamtzeit | Fahrzeugauslastung |
|----------|--------------|-------------------|-------------|-------------|-------------|-------------------|
| **H2-Szenario 1** | 8 Fahrzeuge | 41/100 | **41,0%** | 5,34 min | 19,82 min | ~100% |
| **H2-Szenario 2** | 16 Fahrzeuge | 70/100 | **70,0%** | 5,05 min | 18,48 min | ~100% |
| **H2-Szenario 3** | 24 Fahrzeuge | 92/100 | **92,0%** | 4,67 min | 18,24 min | ~100% |
| **H2-Szenario 4** | 32 Fahrzeuge | 95/100 | **95,0%** | 4,09 min | 17,12 min | ~100% |

**Datenquelle:** Direkte Simulationsergebnisse aus `studies/klagenfurt_h2_spitzenzeiten_case_study/results/`
**Konfidenz:** Hoch (reproduzierbare Simulationsergebnisse)

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

### Wartezeitenvergleich

| Flottengröße | Ø Wartezeit | Gesamtzeit | Max. Wartezeit | Verbesserung vs. vorherige Stufe |
|--------------|-------------|-------------|----------------|----------------------------------|
| 8 Fahrzeuge | 5,34 min | 19,82 min | ~8 min | - (Baseline) |
| 16 Fahrzeuge | 5,05 min | 18,48 min | ~8 min | -5,4% Wartezeit |
| 24 Fahrzeuge | 4,67 min | 18,24 min | ~8 min | -7,5% Wartezeit |
| 32 Fahrzeuge | 4,09 min | 17,12 min | ~8 min | -12,4% Wartezeit |

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
- **Fahrzeugkapazität**: 4 Passagiere
- **Max. Wartezeit**: 8 Minuten

### Simulation ausführen

```bash
# H2-Simulation starten
python run_klagenfurt_h2_spitzenzeiten.py

# Analyse durchführen
python klagenfurt_h2_spitzenzeiten_analysis.py
```

## Konfidenzlevel

### Hohe Konfidenz (>80%)
- Kritischer Schwellenwert existiert bei 16 Fahrzeugen
- Nicht-lineares Skalierungsverhalten
- Service-Einbruch unter 16 Fahrzeugen
- 24 Fahrzeuge als tragfähiges Minimum

### Mittlere Konfidenz (50-80%)
- Phasenmodell-Empfehlungen
- Nutzerakzeptanz-Schwellenwerte
- Wachstumsstrategie-Timing

### Niedrige Konfidenz (<50%)
- Reale Betriebskosten
- Langfristige Nachhaltigkeit
- Tatsächliche Marktakzeptanz

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

## Referenzen

- Alonso-Mora et al. (2017) PNAS 114(3): 462-467
- FleetPy Framework (TUM-VT)
- OpenStreetMap Netzwerkdaten