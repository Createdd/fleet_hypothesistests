# 🚌 FleetPy Klagenfurt Fallstudie (8-Sitzer-Studie)

[![FleetPy](https://img.shields.io/badge/Framework-FleetPy-blue)](https://github.com/TUM-VT/FleetPy)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-green.svg)](https://www.python.org/downloads/)

## Überblick

Diese Studie analysiert die Machbarkeit und Leistung eines Ridepooling-Dienstes in Klagenfurt unter Verwendung des FleetPy-Simulationsframeworks mit **8-Sitzer Standard-Fahrzeugen** und **12-Sitzer barrierefreien Fahrzeugen**. Die Analyse gliedert sich in vier Hauptstudien:

**💡 Wichtige Erkenntnis:** Diese Studie verwendet realistische Fahrzeugkonfigurationen (8/12 Sitze) und validiert Erkenntnisse der vorherigen [4-Sitzer-Studie](comparison_previous_study.md). Trotz **Verdopplung der Sitzplatzkapazität** bleiben Service-Raten identisch - dies beweist, dass **räumliche Abdeckung wichtiger ist als absolute Kapazität**.

---

## Studien-Übersicht

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
- Abbildung im Modell: Zwei Fahrzeugtypen (**8-Sitzer Standard** vs. **12-Sitzer Gelenkbus**), erhöhte Kapazitätsnutzung für Rollstuhl/Kinderwagen
- Szenarien: 0%, 20%, 30%, 50% barrierefreie Fahrzeuge

**Details zu Kostenanalyse und Trade-offs siehe [UC3_accessibility.md](UC3_accessibility.md).**

### [📊 Vergleich: 8-Sitzer vs. 4-Sitzer-Studie](comparison_previous_study.md)
- Validierung der vorherigen Konsortium-Studie (4-Sitzer-Konfiguration)
- Empirischer Beweis: Räumliche Abdeckung > Kapazität
- Methodologische Verbesserungen und neue Erkenntnisse
- Offene Forschungsfragen zu UC3 (Barrierefreiheits-Matching)

## Zentrale Ergebnisse

### H1/H2: Serviceraten-Vergleich (Flottengrößen-Variation)
| Flottengröße | Servicerate | Wartezeit | Fahrzeugauslastung | Studie |
|--------------|-------------|-----------|-------------------|--------|
| 8 Fahrzeuge | 41,0% | 5,34 min | ~100% | H2 |
| 16 Fahrzeuge | 70,0% | 5,05 min | ~100% | H2 |
| 20 Fahrzeuge | 84,0% | 5,00 min | 100% | H1 |
| 24 Fahrzeuge | 92,0% | 4,67 min | ~100% | H2 |
| 30 Fahrzeuge | 95,0% | 4,20 min | 100% | H1 |
| 32 Fahrzeuge | 95,0% | 4,09 min | ~100% | H2 |
| 40 Fahrzeuge | 98,0% | 3,60 min | 92,5% | H1 |

**Kritische Schwellenwerte:**
- Unter 16 Fahrzeuge: Service bricht ein (<70% Servicerate)
- 24 Fahrzeuge: Optimale Mindestflotte (92% Servicerate)
- 30-32 Fahrzeuge: Optimaler Bereich für Servicequalität (95% Servicerate)
- Über 40 Fahrzeuge: Abnehmender Grenznutzen (minimaler Gewinn bei höheren Kosten)

### UC2: Digitale Kompetenz & Altersgruppen-Vergleich (20 Fahrzeuge)

#### Ältere Nutzer (65+) - Support-Maßnahmen

| Szenario | Maßnahme | Servicerate | Ø Wartezeit | Entscheidungszeit | Interpretation |
|----------|----------|-------------|-------------|-------------------|----------------|
| baseline | Keine Unterstützung | **42%** | 2,8 min | 60s | Niedrige digitale Kompetenz |
| phone_support | Telefon-Hotline | *Simuliert* | *Simuliert* | 240s | Mehr Entscheidungszeit |
| simple_ui | Vereinfachte App | **63%** | 3,7 min | 120s | Höhere Toleranz |
| full_support | Volle Unterstützung | *Simuliert* | *Simuliert* | 300s | Kombination aller Maßnahmen |

#### Junge Nutzer - Altersgruppen-Vergleich

| Altersgruppe | Servicerate | Ø Wartezeit | Entscheidungszeit | Gehgeschwindigkeit | Boarding-Zeit |
|--------------|-------------|-------------|-------------------|-------------------|---------------|
| **Studenten (21-30)** | **77%** | 4,1 min | 25s | 1,5 m/s | 12s |
| **Schüler (15-20)** | *Parametrisiert* | *Simuliert* | 20s | 1,4 m/s | 15s |
| **Ältere (65+) Baseline** | **42%** | 2,8 min | 60s | 1,0 m/s | 60s |

**💡 Zentrale Erkenntnis:** Studenten (77%) nutzen Service deutlich erfolgreicher als Ältere ohne Support (42%). Digitale Kompetenz-Gap: 3-6x langsamere Entscheidungen bei Älteren.

### UC3: Barrierefreiheit (20 Fahrzeuge, Variable Flottenzusammensetzung)

| Szenario | Standard (8 Sitze) | Barrierefrei (12 Sitze) | Anteil Barrierefrei | Servicerate Gesamt | Kosten |
|----------|-------------------|------------------------|---------------------|-------------------|--------|
| baseline | 20 | 0 | 0% | **45%** | €40k fix + €5,3k var |
| mixed_20 | 16 | 4 | 20% | **45%** | Moderat |
| mixed_30 | 14 | 6 | 30% | **45%** | €49k fix + €6,1k var |
| mixed_50 | 10 | 10 | 50% | **45%** | Hoch |

**⚠️ Wichtige Erkenntnis:** Identische 45% Service-Raten über alle Szenarien zeigen **FleetPy-Modellierungslücke**. Das Framework kann keine expliziten Barrierefreiheits-Anforderungen simulieren. Die **räumliche Verteilung** barrierefreier Fahrzeuge ist kritisch - 30% (6 Fahrzeuge) empfohlen für bessere geografische Abdeckung über 12 Zonen.

**Empfehlung bleibt:** 30% barrierefreie Fahrzeuge aus **rechtlichen/ethischen Gründen** (ÖNORM B 1600, EU 1107/2006), nicht aus Simulationsergebnissen. Siehe [comparison_previous_study.md](comparison_previous_study.md) für Details.

## Systemkonfiguration

### Netzwerkparameter
- **Knoten:** 6.394 (Straßenkreuzungen und Haltestellen)
- **Kanten:** 8.277 (Straßenverbindungen)
- **Zonen:** 12 (K-Means-Clustering)
- **Zentroiden:** 314 (strategische Ein-/Ausstiegspunkte)
- **Netzwerk-Extension:** Erweitert um Lakeside Park/Universität Klagenfurt (Zone 9) für UC2-Studenten-Szenarien

**⚠️ Wichtiger Hinweis zur Netzwerk-Regeneration:**
Das Netzwerk wurde von 2.099 auf 6.394 Knoten erweitert, um die Universität Klagenfurt/Lakeside Park einzuschließen. Nach jeder Netzwerk-Änderung müssen **Demand-Dateien neu generiert werden**, da alte Knoten-IDs ungültig werden. Dies erfolgt durch Neuausführung von `klagenfurt_h1_spitzenzeiten_map_all.py` oder manuell mit:
```python
# Demand regenerieren (100 zufällige O-D-Paare)
python -c "import pandas as pd; import numpy as np; nodes = pd.read_csv('data/networks/klagenfurt_h1_spitzenzeiten/base/nodes.csv'); np.random.seed(42); demand = pd.DataFrame([{'Unnamed: 0': float(i), 'request_id': float(i), 'rq_time': float(np.random.randint(25200,32400)), 'start': float(np.random.choice(nodes['node_index'])), 'end': float((e:=np.random.choice(nodes['node_index'])) if e != (s:=np.random.choice(nodes['node_index'])) else np.random.choice(nodes['node_index'])), 'earliest_pickup_time': float(np.random.randint(25200,32400))} for i in range(100)]); demand.to_csv('data/demand/klagenfurt_h1_spitzenzeiten/matched/klagenfurt_h1_spitzenzeiten/demand_requests.csv', index=False)"
```

### Service-Beschränkungen
- **Maximale Wartezeit:** 8 Minuten
- **Maximaler Umwegfaktor:** 40% der direkten Fahrzeit
- **Einstiegszeit:** 30-60 Sekunden (variiert nach Altersgruppe)
- **Fahrzeugkapazität:**
  - **Standard:** 8 Passagiere
  - **Barrierefrei:** 12 Passagiere
  - **Rollstuhl/Kinderwagen:** 2 Sitzplätze (Platzbedarf-Proxy)

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

## 🔬 Wissenschaftliche Erkenntnisse

### Validiert (aus 4-Sitzer-Studie)
- ✅ **24-30 Fahrzeuge optimal** für Klagenfurt (92-95% Service-Rate)
- ✅ **Kritischer Schwellenwert bei 16 Fahrzeugen** (<70% Service inakzeptabel)
- ✅ **Nicht-lineare Skalierung** mit abnehmendem Grenznutzen
- ✅ **Support-Maßnahmen für Ältere** wirksam (+50% Verbesserung)

### Neue Erkenntnisse (8-Sitzer-Studie)
- 🆕 **Räumliche Abdeckung > Kapazität** (empirisch bewiesen durch identische Service-Raten trotz verdoppelter Sitze)
- 🆕 **Altersgruppen-Unterschiede** quantifiziert (77% Studenten vs. 42% Ältere)
- 🆕 **Digitale Kompetenz-Gap** gemessen (3-6x langsamere Entscheidungen bei Älteren)
- 🆕 **Modellierungslücken** transparent dokumentiert (UC3 Barrierefreiheits-Matching fehlt)

### Offene Forschungsfragen
- 🔬 Explizite Barrierefreiheits-Anforderungen in FleetPy implementieren
- 🔬 Empirische Validierung mit echten Nutzern in Klagenfurt
- 🔬 Langzeit-Studien über gesamten Tagesverlauf (nicht nur 7-9 Uhr Peak)
- 🔬 Marketing-Strategien für junge Zielgruppen (15-30 Jahre)

## 🌍 Kontext: Ridepooling in der Praxis (Hamburg-Studie)

### Zwei konzeptionell verschiedene Geschäftsmodelle

Empirische Studien aus Hamburg zeigen, dass **Ridepooling-Dienste je nach Geschäftsmodell völlig unterschiedliche Rollen** im Mobilitätssystem einnehmen können:

#### **hvv hop (ehemals ioki Hamburg) – Zubringerdienst zum ÖPNV**
- **Konzept:** Last-Mile-Lösung für ÖPNV-Anbindung
- **Finanzierung:** Öffentlich gefördert
- **Tarif:** 1 € Komfortzuschlag mit gültigem ÖV-Ticket
- **Betrieb:** 24/7 in kleineren Gebieten am Stadtrand (Osdorf/Lurup)
- **Nutzerverhalten:**
  - 39% Arbeitswege, starke Morgenspitze (7-9 Uhr)
  - **70% intermodale Nutzung** (Kombination mit S-Bahn)
  - 5.000-25.000 Fahrten zu den vier S-Bahn-Stationen
  - Samstag-Vormittag: 18% Einkaufswege

#### **MOIA – Direktverkehr als Pkw-Alternative**
- **Konzept:** Private Pkw-Alternative für Direktverbindungen
- **Finanzierung:** Eigenwirtschaftlich
- **Tarif:** Dynamische Preisgestaltung
- **Betrieb:** Großes innerstädtisches Gebiet (268 km²)
- **Nutzerverhalten:**
  - 60% Freizeitwege, Nachfragespitzen um 18 und 22 Uhr
  - **Nur 14% intermodale Nutzung**
  - Tagesunabhängig, nicht an klassische Verkehrsspitzen gebunden

### Sozialräumliche Effekte des Tarifwechsels

Nach dem Wechsel von ioki Hamburg zu MOIA (2023) im Gebiet Osdorf/Lurup:

**Nachfragerückgang:**
- Gesamt: -28% (123.560 → 88.788 Fahrten/Jahr)
- Gebiete mit sehr niedrigem/niedrigem Statusindex: **massiver Einbruch**
  - Osdorfer Born, nordwestliches Lurup besonders betroffen
- MOIA-Binnenfahrten: nur 4,9% (95,1% mit Start/Ziel außerhalb)

**Nachfrageverschiebung:**
- Gebiete mit höherem sozioökonomischen Status: Nutzung gestiegen
- Südliches Gebiet (Elbe-Einkaufszentrum-Umland): profitierte
- Gewerbegebiet: neue Nachfrage durch MOIA

**Vulnerable Gruppen besonders betroffen:**
- ioki Hamburg: 16% Nutzer mit Mobilitätseinschränkungen
- MOIA: nur 9% Nutzer mit Mobilitätseinschränkungen
- Günstiger Tarif war entscheidend für Zugang vulnerabler Gruppen

### Nutzerprofile: Überdurchschnittlich gebildet und multimodal

Beide Dienste bedienen ähnliche Demografien:
- **Bildung:** 47-61% mit universitärem Abschluss
- **Führerschein:** 88-90% besitzen einen
- **ÖPNV-Abo:** 46-58% haben ein Abo
- → Typische multimodale Mobilitätstypen mit hohem sozioökonomischen Status

### Strategische Erkenntnisse für Klagenfurt

**Zentrale Lehre aus Hamburg:**

✅ **Beide Modelle können parallel existieren** ohne gegenseitige Kannibalisierung:
- **Peripherie (wie Osdorf/Lurup):** Zubringerfunktion zum ÖPNV mit öffentlicher Förderung
- **Zentrum:** Direktverkehr als Pkw-Alternative, eigenwirtschaftlich

❌ **Ridepooling allein reicht nicht** für Mobilitätswende:
- Nötig ist **Gesamtkonzept** mit Push-Maßnahmen (attraktiver ÖPNV)
- Flexible On-Demand-Services als **strategische Ergänzung**, nicht Ersatz

⚠️ **Sozialräumliche Gerechtigkeit beachten:**
- Tarifgestaltung hat massive Auswirkung auf vulnerable Gruppen
- Öffentliche Förderung notwendig für inklusive Mobilität in der Peripherie
- Rein eigenwirtschaftliche Dienste bedienen eher privilegierte Nutzergruppen

**Übertragung auf Klagenfurt:**
- Ähnlicher Kontext wie Hamburg Osdorf/Lurup (120 km² Stadtgebiet, 105.000 Einwohner)
- **UC2 (Ältere 65+) und UC3 (Barrierefreiheit)** adressieren genau diese Inklusivitätsfragen
- 30% barrierefreie Fahrzeuge + Support-Maßnahmen = Lehre aus Hamburg-Erfahrung
- Öffentliche Förderung wahrscheinlich notwendig für 24-30 Fahrzeuge bei 95% Servicerate

**Quelle:** Empirische Studie Hamburg (hvv hop/ioki Hamburg vs. MOIA), Gebiet Osdorf/Lurup, 2023

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

## 📚 Weiterführende Dokumentation

- **[H1: Servicequalität-Optimierung](H1_service_quality.md)** - Detaillierte Ergebnisse für 20/30/40 Fahrzeuge
- **[H2: Minimale Flottengröße](H2_minimum_fleet.md)** - Kritische Schwellenwerte und Skalierungsverhalten
- **[UC2: Digitale Kompetenz](UC2_age_based.md)** - Altersgruppen-Vergleich und Support-Maßnahmen
- **[UC3: Barrierefreiheit](UC3_accessibility.md)** - Flottenzusammensetzung und Inklusivität
- **[📊 Vergleich 8-Sitzer vs. 4-Sitzer-Studie](comparison_previous_study.md)** - Validierung und neue Erkenntnisse

## Datenquellen
- **Netzwerkdaten:** OpenStreetMap Klagenfurt (2.099 Knoten, 5.658 Kanten)
- **Algorithmus:** Alonso-Mora et al. (2017) PNAS 114(3): 462-467 (1.620+ Zitationen)
- **Framework:** FleetPy (TUM München, 28+ wissenschaftliche Zitationen)
- **Vorherige Studie:** 4-Sitzer-Studie (Konsortium AIT Austrian Institute of Technology)

## Lizenz
Dieses Projekt verwendet das FleetPy-Framework unter dessen Lizenz.
© Technische Universität München, Lehrstuhl für Verkehrstechnik

---

**Erstellt:** November 2025
**Repository:** [github.com/Createdd/fleet_hypothesistests](https://github.com/Createdd/fleet_hypothesistests)
**Hinweis:** Diese Dokumentation wurde mithilfe von KI-Tools erstellt und unterstützt.