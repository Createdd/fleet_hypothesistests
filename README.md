# 🚌 FleetPy Klagenfurt Fallstudie

[![FleetPy](https://img.shields.io/badge/Framework-FleetPy-blue)](https://github.com/TUM-VT/FleetPy)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-green.svg)](https://www.python.org/downloads/)

## Überblick

Diese Studie analysiert die Machbarkeit und Leistung eines Ridepooling-Dienstes in Klagenfurt unter Verwendung des FleetPy-Simulationsframeworks. Die Analyse gliedert sich in zwei Haupthypothesentests:

### [Hypothese 1 (H1): Servicequalität-Optimierung](H1_service_quality.md)
- Fokus auf Optimierung der Servicequalität mit größeren Flotten
- Test von Flotten mit 20, 30 und 40 Fahrzeugen
- Schwerpunkt auf Maximierung der Servicerate und Minimierung der Wartezeiten

### [Hypothese 2 (H2): Minimale Flottengröße](H2_minimum_fleet.md)
- Fokus auf Bestimmung der minimal wirtschaftlich tragfähigen Flottengröße
- Test von Flotten mit 8, 16, 24 und 32 Fahrzeugen
- Schwerpunkt auf Ermittlung kritischer Schwellenwerte und Kosteneffizienz


### [Use Case 2 (UC2): Altersbasierte digitale Kompetenz](UC2_age_based.md)
- Zielgruppe: Ältere Personen mit geringerer digitaler Kompetenz
- Frage: Welche Begleitmaßnahmen (Telefon-Support, vereinfachte App, volle Unterstützung) erhöhen die Nutzbarkeit?
- Abbildung im Modell: Entscheidungsfenster, Wartezeit-Akzeptanzkurve, Boarding-/Assistenzzeiten, Gehfähigkeit

**Details zur Parametrisierung und Evaluationsmetriken siehe [UC2_age_based.md](UC2_age_based.md).**

### [Use Case 3 (UC3): Barrierefreiheit – Rollstuhl und Kinderwagen](UC3_accessibility.md)
- Zielgruppe: Personen mit Kindern/Kinderwagen und mobilitätseingeschränkte Personen (Rollstuhl)
- Frage: Welche Flottenzusammensetzung (Standard vs. barrierefreie Gelenkbusse) gewährleistet ausreichende Servicerate?
- Abbildung im Modell: Zwei Fahrzeugtypen (4-Sitzer vs. 8-Sitzer Gelenkbus), erhöhte Kapazitätsnutzung für Rollstuhl/Kinderwagen
- Szenarien: 0%, 20%, 30%, 50% barrierefreie Fahrzeuge

**Details zu Kostenanalyse und Trade-offs siehe [UC3_accessibility.md](UC3_accessibility.md).**

## Zentrale Ergebnisse

### Serviceraten-Vergleich
| Flottengröße | Servicerate | Wartezeit | Fahrzeugauslastung |
|--------------|-------------|------------|-------------------|
| 8 Fahrzeuge | 41,0% | 5,34 min | ~100% |
| 16 Fahrzeuge | 70,0% | 5,05 min | ~100% |
| 20 Fahrzeuge | 84,0% | 5,00 min | 100% |
| 24 Fahrzeuge | 92,0% | 4,67 min | ~100% |
| 30 Fahrzeuge | 95,0% | 4,20 min | 100% |
| 32 Fahrzeuge | 95,0% | 4,09 min | ~100% |
| 40 Fahrzeuge | 98,0% | 3,60 min | 92,5% |

**Kritische Schwellenwerte:**
- Unter 16 Fahrzeuge: Service bricht ein (<70% Servicerate)
- 24 Fahrzeuge: Optimale Mindestflotte (92% Servicerate)
- 30-32 Fahrzeuge: Optimaler Bereich für Servicequalität (95% Servicerate)
- Über 40 Fahrzeuge: Abnehmender Grenznutzen (minimaler Gewinn bei höheren Kosten)

## Systemkonfiguration

### Netzwerkparameter
- **Knoten:** 2.099 (Straßenkreuzungen und Haltestellen)
- **Kanten:** 5.658 (Straßenverbindungen)
- **Zonen:** 12 (K-Means-Clustering)
- **Zentroiden:** 103 (strategische Ein-/Ausstiegspunkte)

### Service-Beschränkungen
- **Maximale Wartezeit:** 8 Minuten
- **Maximaler Umwegfaktor:** 40% der direkten Fahrzeit
- **Einstiegszeit:** 30 Sekunden (konstant)
- **Fahrzeugkapazität:** 4 Passagiere

### Zeitparameter
- **Simulationszeitraum:** 7:00-9:00 (Morgenspitze)
- **Reoptimierungsintervall:** 30 Sekunden
- **Nachfrage:** 100 Mobilitätsanfragen

## Project Setup

## Projekt-Setup
- Python 3.10+
### Voraussetzungen
- Conda Environment

### Installation

### Installation
\`\`\`bash
git clone https://github.com/Createdd/fleet_hypothesistests.git
```bash
git clone https://github.com/Createdd/fleet_hypothesistests.git
cd fleet_hypothesistests
```
\`\`\`bash
conda env create -f environment.yml
conda activate fleetpy
\`\`\`

3. Install dependencies:

### Simulationen ausführen
\`\`\`bash
python run_klagenfurt_h1_spitzenzeiten.py
python klagenfurt_h1_spitzenzeiten_analysis.py
\`\`\`

For H2 (Minimum Fleet):
\`\`\`bash
python run_klagenfurt_h2_spitzenzeiten.py
python klagenfurt_h2_spitzenzeiten_analysis.py
\`\`\`

### Simulationen ausführen

#### H1 (Servicequalität)
```bash
python run_klagenfurt_h1_spitzenzeiten.py
python klagenfurt_h1_spitzenzeiten_analysis.py
```

#### H2 (Minimale Flotte)
```bash
python run_klagenfurt_h2_spitzenzeiten.py
python klagenfurt_h2_spitzenzeiten_analysis.py
```

#### UC2 (Digitale Kompetenz & Support-Maßnahmen)
```bash
conda activate fleetpy
python run_uc2_age_based.py
```
Die Simulation erzeugt Ergebnisdateien für alle vier Szenarien (baseline, phone_support, simple_ui, full_support).

Für die Analyse und Visualisierung:
```bash
jupyter notebook studies/uc2_age_based/studies/uc2_study/analysis/uc2_analysis.ipynb
```
Das Notebook aggregiert die Ergebnisse und zeigt die wichtigsten Kennzahlen und Vergleiche an.

#### UC3 (Barrierefreiheit – Flottenzusammensetzung)
```bash
conda activate fleetpy
python run_uc3_accessibility.py
```
Die Simulation testet 4 Flottenzusammensetzungen (baseline: 0% Gelenkbusse, mixed_20: 20%, mixed_30: 30%, mixed_50: 50%).

Für die Analyse und Visualisierung:
```bash
jupyter notebook studies/uc3_accessibility/studies/uc3_study/analysis/uc3_analysis.ipynb
```
Das Notebook zeigt Trade-offs zwischen Kosten und Servicerate für verschiedene Anteile barrierefreier Fahrzeuge.

## Kategorisierung der Erkenntnisse

## Glossar

- Servicerate: Anteil bedienter Anfragen an allen Anfragen (bedient/gesamt)
- Wartezeit: Zeit zwischen Anfrage und Abholung (Durchschnitt über alle bedienten Anfragen)
- Gesamtzeit: Summe aus Wartezeit und Fahrzeit bis Ziel (Durchschnitt)
- Fahrzeugauslastung: Anteil der Zeit, in der Fahrzeuge mit Fahrgästen unterwegs sind bzw. operativ genutzt werden

### Direkte Simulationsergebnisse
- Serviceraten steigen mit Flottengröße
- Nicht-lineare Skalierung existiert (kritischer Schwellenwert bei 16 Fahrzeugen)
- Abnehmender Grenznutzen über 24 Fahrzeuge
- Zonensystem ist kritisch für Algorithmuserfolg

### Abgeleitete Schlussfolgerungen
- 24 Fahrzeuge als optimale Mindestflotte
- Kosteneffizienz-Vergleiche
- Kurz- bis mittelfristige Betriebsempfehlungen

### Hypothesen für weitere Untersuchungen
- Absolute Kostenschätzungen (keine realen CAPEX/OPEX-Daten verfügbar)
- Reale Nutzerakzeptanz in Klagenfurt
- Langfristige betriebliche Auswirkungen
- Übertragbarkeit auf andere Städte

## Datenquellen
- Netzwerkdaten: OpenStreetMap (verifiziert)
- Algorithmus: Alonso-Mora et al. (2017) PNAS 114(3): 462-467
- Framework: FleetPy (TUM-VT)

## Lizenz
Dieses Projekt verwendet das FleetPy-Framework unter dessen Lizenz.
© Technische Universität München, Lehrstuhl für Verkehrstechnik