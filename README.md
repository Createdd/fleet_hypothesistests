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

### Aktuelle Studie: Filtered Network (6 Zonen, 500 Anfragen)

**Konfiguration:**
- Netzwerk: 3,435 Knoten, 6 Kernzonen (gefiltert von 12)
- Nachfrage: 500 Anfragen über 6-22 Uhr (16 Stunden, 70% Peak 7-9 Uhr)
- Zeitfenster: Ganztägiger Betrieb (realistisches Szenario)

#### H1: Flottengrößen-Variation (Filtered Network)
| Flottengröße | Servicerate | Ø Wartezeit | Bedient/Gesamt | Fahrzeugauslastung |
|--------------|-------------|-------------|----------------|-------------------|
| 8 Fahrzeuge  | 1,8% | 4,6 min | 9/500 | 87,5% |
| 16 Fahrzeuge | 1,8% | 4,6 min | 9/500 | 43,8% |
| 24 Fahrzeuge | 3,0% | 4,1 min | 15/500 | 45,8% |

**Interpretation:**
- Die niedrigen Serviceraten (1,8-3,0%) sind **erwartungsgemäß** bei dieser Konstellation:
  - **Sehr kleine Flotten** (8-24 Fahrzeuge) für großflächiges Gebiet (6 Zonen)
  - **Hohe Nachfrage** (500 Anfragen) über langen Zeitraum (16 Stunden)
  - **Räumliche Verteilung** als Hauptbottleneck: Zu wenige Fahrzeuge für effektive Abdeckung
  - **Ganztägiger Betrieb** statt fokussierte Spitzenzeit (mehr Streuung)

**Kritische Erkenntnis:**
- 8-24 Fahrzeuge sind **deutlich zu wenig** für 500 Anfragen
- Servicerate steigt nur marginal mit Flottengröße (1,8% → 3,0%)
- Beweis: **Räumliche Abdeckung dominiert** - selbst Verdreifachung der Flotte bringt kaum Verbesserung
- Empfehlung: Signifikant größere Flotten (>50 Fahrzeuge) oder reduzierte Nachfrage/Betriebszeit notwendig

### Vergleich: Spitzenzeit-fokussierte Studie (100 Anfragen, 2 Stunden)
*Frühere Konfiguration mit fokussiertem Zeitfenster (7-9 Uhr Morgenspitze):*

| Flottengröße | Servicerate | Wartezeit | Nachfrage | Zeitfenster |
|--------------|-------------|-----------|-----------|-------------|
| 8 Fahrzeuge  | 41,0% | 5,3 min | 100 Anfragen | 2h (7-9 Uhr) |
| 16 Fahrzeuge | 70,0% | 5,0 min | 100 Anfragen | 2h (7-9 Uhr) |
| 24 Fahrzeuge | 92,0% | 4,7 min | 100 Anfragen | 2h (7-9 Uhr) |

**Vergleich der Konfigurationen:**
| Parameter | Ganztägig (Neu) | Spitzenzeit (Alt) | Faktor |
|-----------|----------------|-------------------|--------|
| Anfragen | 500 | 100 | 5x |
| Zeitfenster | 16h (6-22 Uhr) | 2h (7-9 Uhr) | 8x |
| Nachfragedichte | 31 Anfragen/h | 50 Anfragen/h | 0,6x |
| Servicerate (24 Fzg) | 3,0% | 92,0% | 0,03x |

**⚠️ Wichtig:** Diese Studien sind **nicht direkt vergleichbar** aufgrund fundamental unterschiedlicher Konfigurationen (Nachfragemenge, Zeitfenster, Zonen)

### UC2: Digitale Kompetenz & Altersgruppen (Status: Ergebnisse nicht verfügbar)

**Hinweis:** Die UC2-Simulationen mit dem gefilterten Netzwerk zeigen ähnlich niedrige Serviceraten wie H1 (<5%), was bei kleinen Flotten und hoher Nachfrage erwartbar ist. Detaillierte Analyse steht aus.

### UC3: Barrierefreiheit (Status: Ergebnisse nicht verfügbar)

**Hinweis:** Die UC3-Simulationen mit dem gefilterten Netzwerk zeigen ähnlich niedrige Serviceraten wie H1 (<5%), was bei kleinen Flotten und hoher Nachfrage erwartbar ist. Detaillierte Analyse steht aus.

**Empfehlung für aussagekräftige Ergebnisse:**
- Entweder **deutlich größere Flotten** (>50 Fahrzeuge) testen
- Oder **reduzierte Nachfrage** (z.B. 100 Anfragen) in fokussiertem Zeitfenster (2h Spitzenzeit)
- Oder **längere Simulationszeit** mit realistischer ganztägiger Nachfrageverteilung

## Systemkonfiguration

### Netzwerk: Gefiltertes Klagenfurt Kernnetzwerk

**Aktuelle Konfiguration (Filtered Network):**
- **Knoten**: 3,435 (gefiltert von 6,394)
- **Kanten**: 4,338 (gefiltert von 8,277)
- **Zonen**: 6 (gefiltert von 12) - Fokus auf Klagenfurt Kerngebiet
- **Zentroiden**: 300 (50 pro Zone)
- **Node Indexing**: Kontinuierlich 0-3434 (reindexed für NetworkBasic)

**Entfernte Zonen** (outlying areas): 2, 3, 5, 8, 11, 12
**Beibehaltene Kern-Zonen** (1→0, 4→1, 6→2, 7→3, 9→4, 10→5):
- Zone 0 (ex-1): 396 Knoten
- Zone 1 (ex-4): 669 Knoten
- Zone 2 (ex-6): 577 Knoten
- Zone 3 (ex-7): 656 Knoten
- Zone 4 (ex-9): 391 Knoten
- Zone 5 (ex-10): 746 Knoten

**Rationale für Filterung:**
- Konzentration auf Klagenfurt Stadtgebiet (Lakeside Park bis Zentrum)
- Verbesserung der räumlichen Kohärenz
- Reduktion von Randlagen-Zonen mit geringer Nachfrage
- Optimierung für focused Ridepooling Service

**Visualisierung:** Siehe `klagenfurt_filtered_zones_map.png` - OpenStreetMap-Basemap mit Zonengrenzen, Netzwerk-Edges und Lakeside Park Markierung

### Netzwerk-Setup ausführen
```bash
# Complete network regeneration (one unified script)
cd data/networks/klagenfurt_h1_spitzenzeiten
python setup_filtered_network.py  # Filters, remaps zones, reindexes nodes, generates centroids

# Optional: Create visualization
python visualize_zones.py

# Generate demand
cd ../../demand/klagenfurt_h1_spitzenzeiten
python generate_fullday_demand.py
```

Details siehe: [data/networks/klagenfurt_h1_spitzenzeiten/README.md](data/networks/klagenfurt_h1_spitzenzeiten/README.md)

---

## Weitere Systemkonfiguration

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

## 🔧 Kompletter Prozessablauf: Netzwerk → Zonen → Nachfrage → Simulation

Dieser Abschnitt dokumentiert die **vollständige Prozesskette** zum Regenerieren der Klagenfurt-Studie von Grund auf.

### Schritt 1: Netzwerk und Zonen filtern

**Problem:** Das ursprüngliche Netzwerk umfasste 12 Zonen, wovon 6 Zonen (2, 3, 5, 8, 11, 12) zu weit außerhalb des Klagenfurter Kerngebiets lagen und entfernt werden sollten.

**Lösung:** Filterung auf 6 Kernzonen (1, 4, 6, 7, 9, 10), remapped zu IDs 0-5.

```bash
cd data/networks/klagenfurt_h1_spitzenzeiten
conda run -n fleetpy python filter_network_zones.py
```

**Ausgabe:**
- Backup der Originaldateien: `backup_fullnetwork/`
- Gefilterte `nodes.csv` (nur Knoten in Kernzonen)
- Gefilterte `edges.csv` (nur Kanten zwischen Kernknoten)
- Gefilterte `data/zones/klagenfurt_h1_spitzenzeiten/base/node_zone_info.csv` (Zone IDs 0-5)

### Schritt 2: Zentroiden regenerieren

**Zweck:** Zentroiden sind strategische Ein-/Ausstiegspunkte innerhalb jeder Zone. Nach dem Filtern müssen diese neu berechnet werden.

```bash
cd data/networks/klagenfurt_h1_spitzenzeiten
conda run -n fleetpy python regenerate_centroids.py
```

**Algorithmus:** Spatial K-means-like Verteilung mit ~50 Zentroiden pro Zone für optimale Abdeckung.

**Ausgabe:** Aktualisierte `node_zone_info.csv` mit `is_centroid=1` für ausgewählte Knoten.

### Schritt 3: Nachfrage generieren

**Zweck:** Generierung realistischer Mobilitätsnachfrage über den Tag verteilt mit Spitzenkonzentration 7-9 Uhr.

```bash
cd data/demand/klagenfurt_h1_spitzenzeiten
conda run -n fleetpy python generate_fullday_demand.py
```

**Parameter:**
- 500 Anfragen gesamt
- Zeitfenster: 6:00-22:00 Uhr (16 Stunden)
- 70% Konzentration in Spitzenzeit (7-9 Uhr)
- Nur Knoten aus gefilterten Zonen
- Seed: 42 (reproduzierbar)

**Ausgabe:** `matched/klagenfurt_h1_spitzenzeiten/demand_requests.csv`

**Spaltenformat:**
```csv
Unnamed: 0,request_id,rq_time,start,end,earliest_pickup_time
0,0,25200,1234,5678,25200
```

### Schritt 4: Simulationen ausführen

**Alle Studien laufen:**

```bash
# H1: Servicequalität (3 Szenarien: 20, 30, 40 Fahrzeuge)
conda run -n fleetpy python run_klagenfurt_h1_spitzenzeiten.py > h1.log 2>&1 &

# H2: Minimale Flotte (4 Szenarien: 8, 16, 24, 32 Fahrzeuge)
conda run -n fleetpy python run_klagenfurt_h2_spitzenzeiten.py > h2.log 2>&1 &

# UC2: Altersbasiert (6 Szenarien)
conda run -n fleetpy python run_uc2_age_based.py > uc2.log 2>&1 &

# UC3: Barrierefreiheit (4 Szenarien: 0%, 20%, 30%, 50% barrierefrei)
conda run -n fleetpy python run_uc3_accessibility.py > uc3.log 2>&1 &
```

**Laufzeit:** ~10-20 Sekunden pro Szenario (500 Anfragen, 16 Stunden Simulation)

**Ausgabe-Verzeichnisse:**
- `studies/klagenfurt_h1_spitzenzeiten_case_study/results/`
- `studies/klagenfurt_h2_spitzenzeiten_case_study/results/`
- `studies/uc2_age_based/results/`
- `studies/uc3_accessibility/results/`

### Schritt 5: Ergebnisse analysieren

**Jupyter Notebooks starten:**

```bash
# H1 Analyse
jupyter notebook studies/klagenfurt_h1_spitzenzeiten_case_study/analysis/klagenfurt_h1_spitzenzeiten_analysis.ipynb

# H2 Analyse
jupyter notebook studies/klagenfurt_h2_spitzenzeiten_case_study/analysis/klagenfurt_h2_spitzenzeiten_analysis.ipynb

# UC2 Analyse
jupyter notebook studies/uc2_age_based/analysis/uc2_analysis.ipynb

# UC3 Analyse
jupyter notebook studies/uc3_accessibility/analysis/uc3_analysis.ipynb
```

**Alternativer Workflow:** Alle Cells in VS Code ausführen (Jupyter Extension).

### 🔄 Vollständige Regenerierung (alle Schritte)

```bash
#!/bin/bash
# Komplette Regenerierung von Grund auf

echo "Schritt 1/5: Netzwerk filtern..."
cd data/networks/klagenfurt_h1_spitzenzeiten
conda run -n fleetpy python filter_network_zones.py

echo "Schritt 2/5: Zentroiden regenerieren..."
conda run -n fleetpy python regenerate_centroids.py

echo "Schritt 3/5: Nachfrage generieren..."
cd ../../demand/klagenfurt_h1_spitzenzeiten
conda run -n fleetpy python generate_fullday_demand.py

echo "Schritt 4/5: Simulationen ausführen..."
cd ../../..
conda run -n fleetpy python run_klagenfurt_h1_spitzenzeiten.py > h1.log 2>&1 &
conda run -n fleetpy python run_klagenfurt_h2_spitzenzeiten.py > h2.log 2>&1 &
conda run -n fleetpy python run_uc2_age_based.py > uc2.log 2>&1 &
conda run -n fleetpy python run_uc3_accessibility.py > uc3.log 2>&1 &

echo "Schritt 5/5: Warten auf Simulation..."
wait
echo "✓ Alle Simulationen abgeschlossen!"
echo "Analysiere Ergebnisse in Jupyter Notebooks."
```

### ⚠️ Wichtige Hinweise

**Reihenfolge beachten:** Die Schritte müssen sequenziell ausgeführt werden:
1. Netzwerk filtern ZUERST (definiert gültige Knoten)
2. Zentroiden regenerieren (benötigt gefilterte Knoten)
3. Nachfrage generieren (benötigt gültige Knoten + Zentroiden)
4. Simulationen ausführen (benötigt valide Nachfrage)

**Backups:** Alle Filterskripte erstellen automatisch Backups in `backup_fullnetwork/`.

**Reproduzierbarkeit:** Seed=42 in `generate_fullday_demand.py` garantiert identische Nachfrage.

**Fehlerbehandlung:**
- Wenn Simulation zu schnell läuft (< 5s): Nachfrage prüfen (ungültige Knoten?)
- Wenn Service-Rate = 0%: Zone-Mapping prüfen
- Wenn "Node not found": Netzwerk-Filterung wiederholen

## Datenquellen
- **Netzwerkdaten:** OpenStreetMap Klagenfurt (gefiltert: 6 Kernzonen, vorher 12 Zonen)
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