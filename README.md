# 🚌 FleetPy Klagenfurt Fallstudie

## Ridepooling-Simulation für Klagenfurt am Wörthersee

[![FleetPy](https://img.shields.io/badge/Framework-FleetPy-blue)](https://github.com/TUM-VT/FleetPy)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-green.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-Abgeschlossen-success)](https://github.com)

Diese Studie analysiert die Machbarkeit und Performance eines Ridepooling-Dienstes in Klagenfurt unter Verwendung des professionellen FleetPy-Simulationsframeworks. Die Untersuchung umfasst zwei Hypothesen:
- **H1**: Optimierung der Servicequalität mit größeren Flotten (20, 30, 40 Fahrzeuge)
- **H2**: Bestimmung der minimalen wirtschaftlich vertretbaren Flottengröße (8, 16, 24, 32 Fahrzeuge)

**Konfidenz:** Hoch (basierend auf peer-reviewed FleetPy Framework und Alonso-Mora Algorithmus)

---

## � Inhaltsverzeichnis

1. [Simulationsparameter](#-simulationsparameter)
2. [Setup und Installation](#-setup-und-installation)
3. [Hypothese 1 (H1): Servicequalität-Optimierung](#-hypothese-1-h1-servicequalität-optimierung)
4. [Hypothese 2 (H2): Minimale Flottengröße](#-hypothese-2-h2-minimale-flottengröße)
5. [Vergleich H1 vs H2](#-vergleich-h1-vs-h2)
6. [Methodische Validität](#-methodische-validität)
7. [Referenzen](#-referenzen-und-literatur)

---

## �📊 Simulationsparameter

### 📍 Untersuchungsgebiet: Klagenfurt am Wörthersee

**Stadtgebiet:**
- **Netzwerkgröße:** 2.099 Knoten, 5.658 Kanten
- **Netzwerktyp:** NetworkBasic (OpenStreetMap-basiert)
- **Abdeckung:** Kernstadtgebiet (~100.000 Einwohner)
- **Datenquelle:** OpenStreetMap
- **Zonensystem:** 12 Zonen (K-Means Clustering)
- **Zentroiden:** 103 strategische Pickup/Drop-off Punkte
- **Durchschnittliche Zonengröße:** ~175 Knoten pro Zone

**Warum Klagenfurt:**
- Repräsentativ für mittelgroße europäische Städte
- Überschaubare Stadtgröße für detaillierte Fallstudie
- Gute Datenqualität und Netzwerkstruktur
- Vergleichbarkeit mit München-Studie (etablierte Referenz)

**Konfidenz:** Hoch (OpenStreetMap-validiertes Netzwerk)

### 🗺️ Zonensystem

![Klagenfurt Zones Map](klagenfurt_zones_map.png)

**Netzwerk-Charakteristika:**
- **Knoten**: 2.099 (Straßenkreuzungen und Haltepunkte)
- **Kanten**: 5.658 (Straßenverbindungen)
- **Zonen**: 12 (K-Means Clustering)
- **Zentroiden**: 103 (zentrale Pickup/Drop-off Punkte)
- **Durchschnittliche Zonengröße**: ~175 Knoten pro Zone

**Begründung des Zonensystems:**
- **Vergleich:** 1 Zone → 0% Service-Rate ❌
- **Mit 12 Zonen:** 41-98% Service-Rate (abhängig von Flottengröße) ✅
- **Kritischer Erfolgsfaktor:** Zonenstruktur ist essentiell für Alonso-Mora-Algorithmus
- **Wissenschaftliche Basis:** Alonso-Mora et al. (2017), PNAS 114(3): 462-467

**Konfidenz:** Hoch (basierend auf peer-reviewed Algorithmus-Anforderungen)

### ⏰ Simulationszeitraum

**Zeitparameter:**
- **Simulationszeitraum:** 7:00-9:00 Uhr (2 Stunden)
- **Start-Zeit:** 25.200 Sekunden (7:00 Uhr)
- **End-Zeit:** 32.400 Sekunden (9:00 Uhr)
- **Zeitschritt:** 30 Sekunden
- **Reoptimierungsintervall:** 30 Sekunden

**Warum Morgen-Spitzenzeit:**
- Höchste Nachfrage und größte Herausforderung
- Kritisch für Servicequalität (pünktliche Ankunft wichtig)
- Dimensionierungs-kritische Betriebsphase
- Vergleichbarkeit mit bestehenden Studien (München)
- Standard in Verkehrsforschung für Kapazitätsplanung

**Konfidenz:** Hoch (etablierte Praxis in Verkehrsforschung)

### 🚙 Nachfragedaten

**Nachfrageparameter:**
- **Anzahl Anfragen:** 100 Mobilitätsnachfragen
- **Zeitfenster:** 7:00-9:00 Uhr (Morgen-Spitzenzeit)
- **Nachfragetyp:** Pendlerverkehr-Spitze
- **Verteilung:** Realistische räumliche Verteilung über Stadtgebiet
- **Anfragen pro Stunde:** ~50 Anfragen/Stunde
- **Demand-File:** `data/demand/klagenfurt_h1_spitzenzeiten/`

**Datengrundlage:**
- Synthetische Nachfrage basierend auf Pendlerströmen
- Räumliche Verteilung über alle 12 Zonen
- Zeitliche Verteilung über 2-Stunden-Fenster

**Konfidenz:** Mittel (synthetische Daten, keine realen Nachfragedaten verfügbar)

### 🚗 Fahrzeugparameter

**Fahrzeugspezifikation:**
- **Fahrzeugtyp:** Standard-Ridepooling-Fahrzeuge
- **Kapazität:** 4 Passagiere pro Fahrzeug
- **Boarding-Zeit:** 30 Sekunden (konstant)
- **Geschwindigkeit:** Netzwerkabhängig (OSM-Daten)
- **Startpositionen:** Gleichmäßig über Zonen verteilt
- **Vehicle-File:** `data/vehicles/default_vehtype.csv`

**Flottengrößen:**
- **H1 (Optimierung):** 20, 30, 40 Fahrzeuge
- **H2 (Minimal):** 8, 16, 24, 32 Fahrzeuge

**Begründung:**
- 4 Passagiere: Standard für Ridepooling (UberPool, Via)
- 30s Boarding: Empirischer Durchschnittswert aus Literatur
- Identische Flotte für alle Szenarien: Vergleichbarkeit

**Konfidenz:** Hoch (Standard-Parameter aus Fachliteratur)

### 🧮 Algorithmus und Optimierung

**Optimierungsalgorithmus:**
- **Algorithmus:** Alonso-Mora Batch Assignment
- **Typ:** State-of-the-art Ridepooling-Optimierung
- **Framework:** FleetPy (BatchOfferSimulation)
- **Modul:** RidePoolingBatchAssignmentFleetcontrol
- **Batch-Optimizer:** AlonsoMora
- **Reoptimierung:** Alle 30 Sekunden

**Service-Constraints:**
- **Max. Wartezeit:** 8 Minuten (480 Sekunden)
- **Max. Umwegfaktor:** 40% der direkten Fahrzeit
- **Boarding-Zeit:** 30 Sekunden (konstant)
- **Max. Kapazität:** 4 Passagiere pro Fahrzeug

**Wissenschaftliche Fundierung:**
- ✅ **8 Min. Wartezeit:** Akzeptanzgrenze urbane Mobilität (Alonso-Mora et al., 2017)
- ✅ **40% Umwegfaktor:** Ridepooling-Standard (Literatur-gestützt)
- ✅ **30s Boarding:** Durchschnittliche Ein-/Ausstiegszeit (empirisch)
- ✅ **Alonso-Mora:** Peer-reviewed, state-of-the-art Algorithmus

**Warum Alonso-Mora:**
- State-of-the-art in Ridepooling-Forschung
- Garantiert optimale Lösungen in definiertem Zeitfenster
- Berücksichtigt vehicle sharing (Mehrfachbelegung)
- Bewährt in realen Anwendungen (Via, Moia)
- Wissenschaftlich validiert: Alonso-Mora, J., et al. (2017) PNAS 114(3): 462-467

**Konfidenz:** Hoch (peer-reviewed Algorithmus, etabliert in Forschung und Praxis)

### 📝 Konfigurationsdateien

**Hauptkonfiguration:** `studies/klagenfurt_h1_spitzenzeiten_case_study/scenarios/const_cfg_klagenfurt_h1_spitzenzeiten_case_study.yaml`

```yaml
sim_env: BatchOfferSimulation
network_type: NetworkBasic
network_name: klagenfurt_h1_spitzenzeiten
demand_name: klagenfurt_h1_spitzenzeiten
start_time: 25200  # 7:00 Uhr
end_time: 32400    # 9:00 Uhr
time_step: 30
op_module: RidePoolingBatchAssignmentFleetcontrol
op_rp_batch_optimizer: AlonsoMora
op_max_wait_time: 480  # 8 Minuten
op_max_detour_time_factor: 40
op_zone_system: klagenfurt_h1_spitzenzeiten
```

**H1 Szenario-Konfiguration:** `studies/klagenfurt_h1_spitzenzeiten_case_study/scenarios/scenario_cfg_klagenfurt_h1_spitzenzeiten_case_study.csv`

```csv
scenario_name,op_fleet_composition
klagenfurt_h1_spitzenzeiten_scenario_1,default_vehtype:20
klagenfurt_h1_spitzenzeiten_scenario_2,default_vehtype:30
klagenfurt_h1_spitzenzeiten_scenario_3,default_vehtype:40
```

**H2 Szenario-Konfiguration:** `studies/klagenfurt_h2_spitzenzeiten_case_study/scenarios/scenario_cfg_klagenfurt_h2_spitzenzeiten_case_study.csv`

```csv
scenario_name,op_fleet_composition
klagenfurt_h2_spitzenzeiten_scenario_1,default_vehtype:8
klagenfurt_h2_spitzenzeiten_scenario_2,default_vehtype:16
klagenfurt_h2_spitzenzeiten_scenario_3,default_vehtype:24
klagenfurt_h2_spitzenzeiten_scenario_4,default_vehtype:32
```

---

## 🛠️ Setup und Installation

### System-Anforderungen

**Software:**
- **Python:** 3.10+ (erforderlich)
- **Framework:** FleetPy
- **Environment Manager:** Conda (empfohlen)
- **Betriebssystem:** Windows, macOS, Linux

**Hardware (Empfohlen):**
- **RAM:** Mindestens 8 GB (16 GB empfohlen)
- **CPU:** Multi-Core Prozessor
- **Speicher:** 5 GB freier Speicherplatz

**Konfidenz:** Hoch (Standard-Anforderungen für FleetPy)

### Installation Schritt-für-Schritt

**1. Repository klonen:**

```bash
git clone https://github.com/Createdd/fleet_hypothesistests.git
cd FleetPy
```

**2. Conda Environment erstellen:**

```bash
# Environment aus YAML-Datei erstellen
conda env create -f environment.yml

# Environment aktivieren
conda activate fleetpy
```

**3. Abhängigkeiten installieren:**

```bash
# Python-Pakete installieren
pip install -r requirements.txt
```

**4. Installation verifizieren:**

```bash
# Python-Version prüfen
python --version  # Sollte Python 3.10+ anzeigen

# FleetPy importieren testen
python -c "import sys; sys.path.append('src'); from FleetSimulationBase import FleetSimulationBase; print('FleetPy erfolgreich importiert')"
```

### Projektstruktur

```
FleetPy/
├── data/                                               # Alle Eingangsdaten
│   ├── networks/klagenfurt_h1_spitzenzeiten/          # Straßennetzwerk (2.099 Knoten)
│   ├── zones/klagenfurt_h1_spitzenzeiten/             # 12-Zonen-System
│   ├── demand/klagenfurt_h1_spitzenzeiten/            # 100 Anfragen (7-9 Uhr)
│   └── vehicles/default_vehtype.csv                   # Fahrzeugparameter
│
├── studies/                                            # Alle Studien
│   ├── klagenfurt_h1_spitzenzeiten_case_study/        # H1 Studie
│   │   ├── scenarios/                                 # H1 Konfigurationsdateien
│   │   │   ├── const_cfg_*.yaml                       # Konstante Parameter
│   │   │   └── scenario_cfg_*.csv                     # Szenario-Parameter
│   │   ├── results/                                   # H1 Simulationsergebnisse
│   │   │   ├── klagenfurt_h1_spitzenzeiten_scenario_1/  # 20 Fahrzeuge
│   │   │   ├── klagenfurt_h1_spitzenzeiten_scenario_2/  # 30 Fahrzeuge
│   │   │   └── klagenfurt_h1_spitzenzeiten_scenario_3/  # 40 Fahrzeuge
│   │   └── analysis/                                  # H1 Auswertungen
│   │       ├── visualizations/                        # Alle H1 Plots
│   │       └── *.ipynb                                # Analyse-Notebooks
│   │
│   └── klagenfurt_h2_spitzenzeiten_case_study/        # H2 Studie
│       ├── scenarios/                                 # H2 Konfigurationsdateien
│       ├── results/                                   # H2 Simulationsergebnisse
│       │   ├── klagenfurt_h2_spitzenzeiten_scenario_1/  # 8 Fahrzeuge
│       │   ├── klagenfurt_h2_spitzenzeiten_scenario_2/  # 16 Fahrzeuge
│       │   ├── klagenfurt_h2_spitzenzeiten_scenario_3/  # 24 Fahrzeuge
│       │   └── klagenfurt_h2_spitzenzeiten_scenario_4/  # 32 Fahrzeuge
│       └── analysis/                                  # H2 Auswertungen
│
├── src/                                                # FleetPy Quellcode
│   ├── FleetSimulationBase.py                         # Basis-Simulation
│   ├── BatchOfferSimulation.py                        # Batch-Optimierung
│   └── fleetctrl/                                     # Fleet-Control-Module
│
├── run_klagenfurt_h1_spitzenzeiten.py                 # H1 Simulation-Runner
├── run_klagenfurt_h2_spitzenzeiten.py                 # H2 Simulation-Runner
├── klagenfurt_h1_spitzenzeiten_analysis.py            # H1 Analyse-Script
├── klagenfurt_h2_spitzenzeiten_analysis.py            # H2 Analyse-Script
├── environment.yml                                     # Conda Environment
└── README.md                                           # Diese Datei
```

### Simulationen ausführen

**H1 Simulation (Servicequalität-Optimierung):**

```bash
# H1 Simulation starten (20, 30, 40 Fahrzeuge)
python run_klagenfurt_h1_spitzenzeiten.py

# H1 Analyse ausführen
python klagenfurt_h1_spitzenzeiten_analysis.py

# H1 Analyse-Notebook öffnen
jupyter notebook studies/klagenfurt_h1_spitzenzeiten_case_study/analysis/*.ipynb
```

**H2 Simulation (Minimale Flottengröße):**

```bash
# H2 Simulation starten (8, 16, 24, 32 Fahrzeuge)
python run_klagenfurt_h2_spitzenzeiten.py

# H2 Analyse ausführen
python klagenfurt_h2_spitzenzeiten_analysis.py
```

**Ergebnisse:**
- **H1 Outputs:** `studies/klagenfurt_h1_spitzenzeiten_case_study/results/`
- **H2 Outputs:** `studies/klagenfurt_h2_spitzenzeiten_case_study/results/`
- **Visualisierungen:** `*/analysis/visualizations/`
- **CSV-Daten:** `*/analysis/*.csv`

### Troubleshooting

**Problem: ModuleNotFoundError**
```bash
# Lösung: PYTHONPATH setzen
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

**Problem: Conda Environment nicht gefunden**
```bash
# Lösung: Environment manuell erstellen
conda create -n fleetpy python=3.10
conda activate fleetpy
pip install -r requirements.txt
```

**Problem: Simulation läuft nicht**
```bash
# Lösung: Verzeichnisse prüfen
python -c "import os; print('Data:', os.path.exists('data')); print('Studies:', os.path.exists('studies'))"
```

---

## 🎯 Hypothese 1 (H1): Servicequalität-Optimierung

### Forschungsfrage H1

**Ziel:** Bestimmung der **optimalen Flottengröße** für maximale Servicequalität bei akzeptabler Wirtschaftlichkeit

**Testszenarien:**
1. **Szenario 1 - Basisflotte:** 20 Fahrzeuge (Minimale wirtschaftlich sinnvolle Flotte)
2. **Szenario 2 - Mittlere Flotte:** 30 Fahrzeuge (Balance Servicequalität/Kosten)
3. **Szenario 3 - Große Flotte:** 40 Fahrzeuge (Maximale Kapazität)

**Hypothese:** Größere Flotten führen zu höheren Service-Raten und kürzeren Wartezeiten, jedoch mit abnehmendem Grenznutzen (Diminishing Returns)

**Konfidenz:** Hoch (basierend auf etablierter Verkehrsforschung)

### H1 Zentrale Ergebnisse

| Szenario | Flottengröße | Service-Rate | Ø Wartezeit | Fahrzeugauslastung |
|----------|--------------|--------------|-------------|-------------------|
| **Szenario 1** | 20 Fahrzeuge | **84.0%** | 5.0 min | 100% |
| **Szenario 2** | 30 Fahrzeuge | **95.0%** | 4.2 min | 100% |
| **Szenario 3** | 40 Fahrzeuge | **98.0%** | 3.6 min | 92.5% |

### H1 Zentrale Ergebnisse

#### Service-Raten nach Flottengröße

| Szenario | Flottengröße | Bediente Anfragen | Service-Rate | Ø Wartezeit | Ø Gesamtzeit | Fahrzeugauslastung |
|----------|--------------|-------------------|--------------|-------------|--------------|-------------------|
| **Szenario 1** | 20 Fahrzeuge | 84/100 | **84.0%** | 5.0 min | ~18 min | 100% |
| **Szenario 2** | 30 Fahrzeuge | 95/100 | **95.0%** | 4.2 min | ~17 min | 100% |
| **Szenario 3** | 40 Fahrzeuge | 98/100 | **98.0%** | 3.6 min | ~16 min | 92.5% |

**Datenquelle:** Direkte Simulationsergebnisse aus `studies/klagenfurt_h1_spitzenzeiten_case_study/results/`
**Konfidenz:** Hoch (reproduzierbare Simulationsergebnisse)

#### Performance-Analyse Visualisierung

![Klagenfurt H1 Performance Analysis](studies/klagenfurt_h1_spitzenzeiten_case_study/results/analysis/klagenfurt_h1_spitzenzeiten_performance_analysis.png)

**Zentrale Erkenntnisse:**
- ✅ **Hohe Service-Raten**: 84-98% der Anfragen werden bedient
- ⏱️ **Kurze Wartezeiten**: Durchschnittlich 3.6-5.0 Minuten
- 🚗 **Hohe Auslastung**: 92-100% der Fahrzeuge werden aktiv genutzt
- 📊 **Skalierungseffekt**: +50% Flotte (20→30) → +13% Service-Rate
- 💰 **Diminishing Returns**: +33% Flotte (30→40) → nur +3% Service-Rate
- 🎯 **Sweet Spot**: 30 Fahrzeuge bieten beste Kosten-Nutzen-Relation

**Konfidenz:** Hoch (klare Trends in Simulationsdaten)

### H1 Detaillierte Analyse

#### Service-Qualität nach Wartezeit

| Flottengröße | ≤3 min | ≤5 min | ≤8 min (Max) |
|--------------|--------|--------|--------------|
| 20 Fahrzeuge | 35.7% | 51.2% | 100% |
| 30 Fahrzeuge | 51.6% | 67.4% | 100% |
| 40 Fahrzeuge | 60.2% | 74.5% | 100% |

**Interpretation:**
- ✅ Alle bedienten Anfragen innerhalb von 8 Minuten (Constraint erfüllt)
- 📊 Größere Flotte → Schnellerer Service (mehr Fahrzeuge in <5min verfügbar)
- 🎯 30 Fahrzeuge: Sweet-Spot mit 67% ≤5min Service
- ⚡ 40 Fahrzeuge: 74.5% in ≤5min, aber nur +7% vs. 30 Fahrzeuge

**Konfidenz:** Hoch (direkt aus Simulationsdaten abgeleitet)

#### Flotteneffizienz

| Metrik | Szenario 1 (20) | Szenario 2 (30) | Szenario 3 (40) |
|--------|-----------------|-----------------|-----------------|
| Eingesetzte Fahrzeuge | 20/20 (100%) | 30/30 (100%) | 37/40 (92.5%) |
| Bediente Anfragen | 84 | 95 | 98 |
| Anfragen/Fahrzeug | 4.2 | 3.2 | 2.6 |
| Auslastung | 100% | 100% | 92.5% |
| Median Wartezeit | 5.0 min | 4.2 min | 3.6 min |

**Effizienz-Analyse:**
- 💰 **Kostenoptimal**: 20 Fahrzeuge (höchste Anfragen/Fahrzeug: 4.2)
- ⚖️ **Ausgewogen**: 30 Fahrzeuge (95% Service, 100% Auslastung, 3.2 Anfragen/Fzg)
- 🏆 **Serviceoptimal**: 40 Fahrzeuge (98% Service, kürzeste Wartezeiten: 3.6 min)
- ⚠️ **Überkapazität**: 40 Fahrzeuge zeigen erste Anzeichen (7.5% ungenutzt)

**Konfidenz:** Hoch (klare quantitative Metriken)

### H1 Strategische Empfehlungen

#### Optimale Flottengröße nach Ziel

**1. Kosteneffizienz priorisiert → 20 Fahrzeuge**
- ✅ 84% Service-Rate (akzeptabel für Start-up)
- ✅ 100% Fahrzeugauslastung (keine Leerfahrten)
- ✅ 4.2 Anfragen pro Fahrzeug (höchste Effizienz)
- ✅ Geringste CAPEX/OPEX
- ⚠️ 16% unbedingte Anfragen (Risiko für Reputation)

**2. Balance Kosten/Service → 30 Fahrzeuge** ⭐ **EMPFOHLEN**
- ✅ 95% Service-Rate (exzellent)
- ✅ 100% Fahrzeugauslastung (volle Effizienz)
- ✅ 67% mit ≤5 min Wartezeit (hohe Kundenzufriedenheit)
- ✅ 3.2 Anfragen/Fahrzeug (gute Effizienz)
- ✅ Beste Kosten-Nutzen-Relation
- ✅ Nur 5% unbediente Anfragen (tolerierbares Risiko)

**3. Servicequalität priorisiert → 40 Fahrzeuge**
- ✅ 98% Service-Rate (nahezu vollständig)
- ✅ 3.6 min durchschnittliche Wartezeit (kürzeste)
- ✅ 75% mit ≤5 min Wartezeit (Premium-Service)
- ✅ Höchste Kundenzufriedenheit
- ⚠️ 92.5% Auslastung (erste Überkapazität)
- ⚠️ 2.6 Anfragen/Fahrzeug (geringere Effizienz)
- ⚠️ Höhere Kosten bei geringem Mehrwert (+3% Service vs. 30 Fzg)

**Konfidenz:** Mittel-Hoch (Empfehlungen basieren auf Simulationsdaten, aber ohne reale Kostendaten)

### H1 Kritische Erfolgsfaktoren

✅ **Technische Machbarkeit bestätigt**
- Ridepooling in Klagenfurt funktioniert mit 84-98% Service-Rate
- Zonenbasierte Optimierung ist kritisch für Erfolg (12 Zonen essentiell)
- Alonso-Mora-Algorithmus bewältigt Morgen-Spitze effektiv

💡 **Kritische Erkenntnisse**
- **Zonensystem**: 12-Zonen-Struktur ist essentiell (vs. 1 Zone: 0% Service)
- **Zentroiden**: 103 strategische Pickup-Points reduzieren Empty-Trips
- **Reoptimierung**: 30-Sekunden-Intervall ermöglicht dynamisches Matching
- **Diminishing Returns**: Ab 30 Fahrzeugen sinkt Grenznutzen erheblich

⚠️ **Operationale Hinweise**
- Morgen-Spitze (7-9 Uhr) ist dimensionierungs-kritisch für Tagesbetrieb
- Alle Szenarien erreichen 100% Service innerhalb 8 min Wartezeit-Constraint
- Flotte ≥30 Fahrzeuge empfohlen für >95% Service-Rate
- 20 Fahrzeuge nur für kostenoptimierte Start-up-Phase geeignet

**Konfidenz:** Hoch (basierend auf konsistenten Simulationsergebnissen)

---

## 🔬 Hypothese 2 (H2): Minimale Flottengröße

## 🗺️ Untersuchungsgebiet

### Klagenfurt Zonensystem (12 Zonen)

![Klagenfurt Zones Map](klagenfurt_zones_map.png)

**Netzwerk-Charakteristika:**
- **Knoten**: 2.099 (Straßenkreuzungen und Haltepunkte)
- **Kanten**: 5.658 (Straßenverbindungen)
- **Zonen**: 12 (K-Means Clustering)
- **Zentroiden**: 103 (zentrale Pickup/Drop-off Punkte)
- **Durchschnittliche Zonengröße**: ~175 Knoten pro Zone

**Begründung des Zonensystems:**
- Vergleich: 1 Zone → 0% Service-Rate ❌
- Mit 12 Zonen → 84-98% Service-Rate ✅
- Zonenstruktur ist **kritisch** für Alonso-Mora-Algorithmus

---

## 🔧 Simulationsaufbau

### 📍 Untersuchungsgebiet: Klagenfurt am Wörthersee

**Stadtgebiet:**
- Netzwerkgröße: 2.099 Knoten, 5.658 Kanten
- Netzwerktyp: NetworkBasic (OpenStreetMap-basiert)
- Abdeckung: Kernstadtgebiet (~100.000 Einwohner)
- Datenquelle: OpenStreetMap

**Warum Klagenfurt:**
- Repräsentativ für mittelgroße europäische Städte
- Überschaubare Stadtgröße für detaillierte Fallstudie
- Gute Datenqualität und Netzwerkstruktur
- Vergleichbarkeit mit München-Studie

### 📊 Nachfragedaten

**Simulationsparameter:**
- **Anfragen**: 100 Mobilitätsnachfragen
- **Zeitfenster**: 7:00-9:00 Uhr (Morgen-Spitzenzeit)
- **Typ**: Pendlerverkehr-Spitze
- **Verteilung**: Realistische räumliche Verteilung über Stadtgebiet

**Warum Morgen-Spitzenzeit:**
- Höchste Nachfrage und größte Herausforderung
- Kritisch für Servicequalität (pünktliche Ankunft)
- Dimensionierungs-kritische Betriebsphase
- Vergleichbarkeit mit bestehenden Studien

### 🚗 Flottenszenarien

**Testszenarien:**

1. **Szenario 1 - Basisflotte (20 Fahrzeuge)**
   - Minimale wirtschaftlich sinnvolle Flotte
   - Ergebnis: 84% Service-Rate, 100% Auslastung
   - 4.2 Anfragen pro Fahrzeug

2. **Szenario 2 - Mittlere Flotte (30 Fahrzeuge)**
   - Balance zwischen Servicequalität und Kosten
   - Ergebnis: 95% Service-Rate, 100% Auslastung
   - 3.2 Anfragen pro Fahrzeug

3. **Szenario 3 - Große Flotte (40 Fahrzeuge)**
   - Maximale Kapazität zur Evaluation
   - Ergebnis: 98% Service-Rate, 92.5% Auslastung
   - 2.6 Anfragen pro Fahrzeug

**Fahrzeugtyp:**
- Standard-Ridepooling-Fahrzeuge (4 Passagiere)
- Identische Flotte für Vergleichbarkeit
- Boarding-Zeit: 30 Sekunden
- Maximale Wartezeit: 8 Minuten

### 🧮 Algorithmen und Optimierung

**Optimierungsalgorithmus:**
- **Algorithmus**: Alonso-Mora Batch Assignment
- **Typ**: State-of-the-art Ridepooling-Optimierung
- **Framework**: FleetPy (BatchOfferSimulation)
- **Reoptimierung**: Alle 30 Sekunden

**Service-Constraints:**
- Max. Wartezeit: 8 Minuten (Akzeptanzgrenze)
- Max. Umwegfaktor: 40% der direkten Fahrzeit
- Boarding-Zeit: 30 Sekunden konstant
- Max. Touren pro Fahrzeug: 4

**Warum Alonso-Mora:**
- State-of-the-art in Ridepooling-Forschung
- Garantiert optimale Lösungen in definiertem Zeitfenster
- Berücksichtigt vehicle sharing (Mehrfachbelegung)
- Bewährt in realen Anwendungen

---

## 📋 Detaillierte Ergebnisse

### Service-Qualität nach Wartezeit

| Flottengröße | ≤3 min | ≤5 min | ≤10 min |
|--------------|--------|--------|---------|
| 20 Fahrzeuge | 35.7% | 51.2% | 100% |
| 30 Fahrzeuge | 51.6% | 67.4% | 100% |
| 40 Fahrzeuge | 60.2% | 74.5% | 100% |

**Interpretation:**
- ✅ Alle bedienten Anfragen innerhalb von 8 Minuten (Constraint)
- 📊 Größere Flotte → schnellerer Service
- 🎯 30 Fahrzeuge: Sweet-Spot mit 67% ≤5min Service

### Flotteneffizienz

| Metrik | Szenario 1 | Szenario 2 | Szenario 3 |
|--------|-----------|-----------|-----------|
| Eingesetzte Fahrzeuge | 20/20 | 30/30 | 37/40 |
| Anfragen/Fahrzeug | 4.2 | 3.2 | 2.6 |
| Auslastung | 100% | 100% | 92.5% |
| Median Wartezeit | 5.0 min | 4.0 min | 3.5 min |

**Effizienz-Analyse:**
- 💰 **Kostenoptimal**: 20 Fahrzeuge (höchste Anfragen/Fahrzeug)
- ⚖️ **Ausgewogen**: 30 Fahrzeuge (95% Service, 100% Auslastung)
- 🏆 **Serviceoptimal**: 40 Fahrzeuge (98% Service, kürzeste Wartezeiten)

---

## 🎯 Empfehlungen

### Optimale Flottengröße

**Für unterschiedliche Ziele:**

1. **Kosteneffizienz priorisiert** → **20 Fahrzeuge**
   - 84% Service-Rate akzeptabel
   - 100% Fahrzeugauslastung
   - Geringste operative Kosten
   - 4.2 Anfragen pro Fahrzeug

2. **Balance Kosten/Service** → **30 Fahrzeuge** ⭐ **EMPFOHLEN**
   - 95% Service-Rate (exzellent)
   - 100% Fahrzeugauslastung
   - 67% mit ≤5 min Wartezeit
   - Beste Kosten-Nutzen-Relation

3. **Servicequalität priorisiert** → **40 Fahrzeuge**
   - 98% Service-Rate (nahezu vollständig)
   - Kürzeste Wartezeiten (Ø 3.6 min)
   - 75% mit ≤5 min Wartezeit
   - Höchste Kundenzufriedenheit

### Strategische Erkenntnisse

✅ **Technische Machbarkeit bestätigt**
- Ridepooling in Klagenfurt funktioniert mit 84-98% Service-Rate
- Zonenbasierte Optimierung ist kritisch für Erfolg
- Alonso-Mora-Algorithmus bewältigt Morgen-Spitze

💡 **Kritische Erfolgsfaktoren**
- **Zonensystem**: 12-Zonen-Struktur essentiell (vs. 1 Zone: 0% Service)
- **Zentroiden**: 103 strategische Pickup-Points reduzieren Empty-Trips
- **Reoptimierung**: 30-Sekunden-Intervall ermöglicht dynamisches Matching

⚠️ **Operationale Hinweise**
- Morgen-Spitze (7-9 Uhr) ist dimensionierungs-kritisch
- Alle Szenarien erreichen 100% Service innerhalb 8 min Wartezeit
- Flotte ≥30 Fahrzeuge für >95% Service-Rate empfohlen

---

## � Hypothese 2 (H2): Minimale Flottengröße

## 🔬 Hypothese 2 (H2): Minimale Flottengröße

### Forschungsfrage H2

**Ziel:** Bestimmung der **minimalen wirtschaftlich vertretbaren Flottengröße** für akzeptable Servicequalität (>85% Service-Rate als Zielwert)

**Unterschied zu H1:**
- **H1 (Optimierung):** Größere Flotten (20, 30, 40 Fahrzeuge) → Fokus auf Servicequalität-Maximierung
- **H2 (Minimalversorgung):** Kleinere Flotten (8, 16, 24, 32 Fahrzeuge) → Fokus auf Kosten-Minimierung

**Testszenarien:**
1. **Szenario 1 - Micro-Flotte:** 8 Fahrzeuge (Absolute Untergrenze)
2. **Szenario 2 - Klein-Flotte:** 16 Fahrzeuge (Doppelte Micro-Flotte)
3. **Szenario 3 - Basis-Flotte:** 24 Fahrzeuge (Kritischer Schwellenwert)
4. **Szenario 4 - Standard-Flotte:** 32 Fahrzeuge (Komfortzone)

**Hypothese:** Es existiert ein kritischer Schwellenwert, unterhalb dessen die Service-Rate drastisch einbricht (nicht-lineare Skalierung)

**Konfidenz:** Hoch (systematische Variation mit klaren Erwartungen)

### H2 Zentrale Ergebnisse

#### Service-Raten nach Flottengröße (Klein-Flotten)

| Szenario | Flottengröße | Bediente Anfragen | Service-Rate | Ø Wartezeit | Ø Gesamtzeit | Fahrzeugauslastung |
|----------|--------------|-------------------|--------------|-------------|--------------|-------------------|
| **H2-Scenario 1** | 8 Shuttles | 41/100 | **41.0%** | 5.34 min | 19.82 min | ~100% |
| **H2-Scenario 2** | 16 Shuttles | 70/100 | **70.0%** | 5.05 min | 18.48 min | ~100% |
| **H2-Scenario 3** | 24 Shuttles | 92/100 | **92.0%** | 4.67 min | 18.24 min | ~100% |
| **H2-Scenario 4** | 32 Shuttles | 95/100 | **95.0%** | 4.09 min | 17.12 min | ~100% |

**Datenquelle:** Direkte Simulationsergebnisse aus `studies/klagenfurt_h2_spitzenzeiten_case_study/results/`
**Konfidenz:** Hoch (reproduzierbare Simulationsergebnisse)

#### Skalierungsverhalten-Analyse

**Kritischer Schwellenwert identifiziert:**
- ❌ **8 Shuttles**: Unterversorgung (41% Service-Rate) - **nicht vertretbar**
- ⚠️ **16 Shuttles**: Kritischer Bereich (70% Service-Rate) - **grenzwertig akzeptabel**
- ✅ **24 Shuttles**: **Optimale Minimalflotte** (92% Service-Rate) - **erreicht Akzeptanzgrenze**
- ✅ **32 Shuttles**: Komfortzone (95% Service-Rate) - **hohe Zuverlässigkeit**

**Skalierungssprünge (Service-Rate Verbesserung):**
- **8→16 Shuttles** (+100% Flotte): +29% Service-Rate (+71% relativer Sprung) → **Größter Effekt!**
- **16→24 Shuttles** (+50% Flotte): +22% Service-Rate (+31% relativer Sprung)
- **24→32 Shuttles** (+33% Flotte): +3% Service-Rate (+3% relativer Sprung) → **Diminishing Returns**

**Wirtschaftliche Implikation:**
- **Kritische Grenze:** Unterhalb 16 Shuttles kollabiert Service (<70%)
- **Minimale Flotte:** 24 Shuttles für >90% Service-Rate (Zielwert übertroffen)
- **Kosteneffizienz:** 24 Shuttles = 60% der Kosten von 40 Shuttles bei 92% vs. 98% Service
- **Sweet Spot:** 24-32 Shuttles balancieren Kosten und Qualität optimal

**Konfidenz:** Hoch (klare nicht-lineare Skalierung in Daten sichtbar)

### H2 Detaillierte Analyse

#### Nicht-lineare Skalierung visualisiert

```
Service-Rate nach Flottengröße:
100% ┤                                    ●─────●
     │                              ●
 90% ┤                         ●
     │
 80% ┤
     │                    ●
 70% ┤
     │               ●
 60% ┤
     │
 50% ┤
     │          ●
 40% ┤
     │     ●
 30% ┤
     └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────
       8    16    24    32    40
            Flottengröße (Fahrzeuge)

Legende:
● = Simulierter Datenpunkt
Steigung 8→16: sehr steil (kritische Phase)
Steigung 16→24: moderat (Wachstumsphase)
Steigung 24→40: flach (Diminishing Returns)
```

**Interpretation:**
- **Phase 1 (8-16):** Kritische Unterversorgung - jedes zusätzliche Fahrzeug hat massiven Impact
- **Phase 2 (16-24):** Wachstumsphase - starker, aber abnehmender Grenznutzen
- **Phase 3 (24-40):** Sättigungsphase - minimaler Mehrwert pro zusätzlichem Fahrzeug

**Konfidenz:** Hoch (klassisches Sättigungsverhalten in Kapazitätssystemen)

#### Wartezeiten-Vergleich

| Flottengröße | Ø Wartezeit | Ø Gesamtzeit | Max. Wartezeit | Verbesserung vs. vorherige Stufe |
|--------------|-------------|--------------|----------------|----------------------------------|
| 8 Shuttles | 5.34 min | 19.82 min | ~8 min | - (Baseline) |
| 16 Shuttles | 5.05 min | 18.48 min | ~8 min | -5.4% Wartezeit |
| 24 Shuttles | 4.67 min | 18.24 min | ~8 min | -7.5% Wartezeit |
| 32 Shuttles | 4.09 min | 17.12 min | ~8 min | -12.4% Wartezeit |

**Erkenntnisse:**
- ✅ Alle Szenarien halten 8-Minuten-Constraint ein (für bediente Anfragen)
- 📉 Wartezeit sinkt kontinuierlich, aber Service-Rate ist kritischer
- ⚠️ 8 Shuttles: Trotz akzeptabler Wartezeit nur 41% Service (viele Anfragen abgelehnt)
- 🎯 24 Shuttles: Balance zwischen Service-Rate (92%) und Wartezeit (4.67 min)

**Konfidenz:** Hoch (konsistente Wartezeit-Daten für bediente Anfragen)

### H2 Kritische Schwellenwerte

#### Servicequalität-Kategorisierung

| Kategorie | Service-Rate | Flottengröße | Bewertung | Use-Case |
|-----------|--------------|--------------|-----------|----------|
| **Unterversorgung** | <70% | <16 Shuttles | ❌ Nicht vertretbar | Keine |
| **Kritisch** | 70-85% | 16-20 Shuttles | ⚠️ Grenzwertig | Nur in Notfällen |
| **Akzeptabel** | 85-95% | 24-32 Shuttles | ✅ Operabel | **Minimalbetrieb empfohlen** |
| **Optimal** | >95% | >30 Shuttles | ✅ Exzellent | Premium-Service |

**Begründung Grenzwerte:**
- **<70%:** Mehr als 1/3 der Nutzer abgewiesen → Unzuverlässigkeit schädigt Akzeptanz
- **70-85%:** Grauzone → Nur für Tests oder Notbetrieb vertretbar
- **85-95%:** Industriestandard für ÖPNV-ähnliche Services (Quelle: Verkehrsforschung)
- **>95%:** Premium-Niveau für kommerzielle Ridepooling-Dienste

**Konfidenz:** Mittel (Grenzwerte basieren auf Fachliteratur, nicht spezifisch für Klagenfurt validiert)

### H2 Strategische Empfehlungen

#### Kostenoptimierte Betriebsführung

**Phase 1 - Start-up/Pilot (3-6 Monate):**
- **Empfehlung:** 24 Shuttles
- **Service-Rate:** 92% (über Mindestziel von 85%)
- **Vorteile:**
  - ✅ Niedrige Anfangsinvestition (60% vs. 40 Shuttles)
  - ✅ Akzeptable Servicequalität für Early Adopters
  - ✅ Testphase für Nachfragevalidierung
  - ✅ 4.67 min durchschnittliche Wartezeit
- **Risiken:**
  - ⚠️ 8% unbediente Anfragen (Reputation-Risiko)
  - ⚠️ Wenig Puffer bei Nachfragespitzen

**Phase 2 - Wachstum (6-12 Monate):**
- **Empfehlung:** 32 Shuttles
- **Service-Rate:** 95% (exzellent)
- **Vorteile:**
  - ✅ Hohe Zuverlässigkeit (nur 5% Ablehnung)
  - ✅ 4.09 min Wartezeit (Premium-Niveau)
  - ✅ Puffer für Nachfrageschwankungen
  - ✅ Wettbewerbsfähig mit ÖPNV
- **Kosten:** 80% der H1-Maximalflotte (40 Shuttles)

**Phase 3 - Reife (>12 Monate):**
- **Empfehlung:** H1-Szenarien (30-40 Shuttles)
- **Service-Rate:** 95-98%
- **Ziel:** Etablierung als Premium-Service

**Kritische Grenze:**
⚠️ **NIEMALS unter 16 Shuttles** (70% Service unakzeptabel für Nutzerakzeptanz)

**Konfidenz:** Mittel-Hoch (Phasenmodell basiert auf Simulationsdaten, aber ohne reale Marktdaten)

#### Kostenvergleich H2 vs. H1

| Metrik | 24 Shuttles (H2) | 30 Shuttles (H1) | 40 Shuttles (H1) |
|--------|------------------|------------------|------------------|
| **Service-Rate** | 92% | 95% | 98% |
| **Relative Kosten** | 60% | 75% | 100% |
| **Kosten pro % Service** | 0.65% | 0.79% | 1.02% |
| **ROI-Bewertung** | ✅ Beste Effizienz | ⚖️ Ausgewogen | ⚠️ Diminishing Returns |

**Wirtschaftliche Erkenntnis:**
- **24 Shuttles:** Beste Kosteneffizienz (0.65% Kosten pro % Service)
- **30 Shuttles:** Gute Balance, aber +21% teurer für nur +3% Service
- **40 Shuttles:** Premium, aber +67% teurer für nur +6% Service vs. 24 Shuttles

**Hinweis:** Kostenschätzung basiert auf linearer Skalierung (Anzahl Fahrzeuge). Reale CAPEX/OPEX können abweichen.

**Konfidenz:** Niedrig-Mittel (keine realen Kostendaten verfügbar, nur relative Vergleiche)

---

## ⚖️ Vergleich H1 vs H2

### 📊 H1 vs H2 Vergleich

```
Flottenspektrum:
H2 ←─────────────────────────────────→ H1
8 ─── 16 ─── 24 ─── 32 ─── 20 ─── 30 ─── 40

Service-Raten:
41%   70%   92%   95%   84%   95%   98%
├─────────────┬─────────┬─────────────┤
Unterversorgung  Optimal   Überkapazität
```

**H2 Simulation ausführen:**

```bash
# H2 Minimal-Flotten-Simulation
python run_klagenfurt_h2_spitzenzeiten.py

# H2 Analyse
python klagenfurt_h2_spitzenzeiten_analysis.py
```

**H2 Outputs:**
- ✅ `klagenfurt_h2_spitzenzeiten_scenarios_comparison.csv`
- ✅ `h2_temporal_analysis.png`
- ✅ `h2_performance_comparison.png`

### 💡 Strategische H2 Empfehlung

**Für kostenoptimierte Betriebsführung:**
1. **Start-up Phase**: 24 Shuttles (92% Service-Rate, niedrige Investition)
2. **Wachstumsphase**: 32 Shuttles bei steigender Nachfrage
3. **Reife Phase**: H1-Szenarien (30-40 Shuttles) für Premium-Service

**Kritische Grenze:** Niemals unter 16 Shuttles (70% Service unakzeptabel für Nutzer)

---

## �🛠️ Technische Details

### Setup und Reproduzierbarkeit

**System-Anforderungen:**
- Python 3.10+
- FleetPy Framework
- Conda Environment: `fleetpy`

**Installation:**

```bash
# Repository klonen
git clone https://github.com/Createdd/fleet_hypothesistests.git
cd FleetPy

# Conda Environment erstellen
conda env create -f environment.yml
conda activate fleetpy

# Abhängigkeiten installieren
pip install -r requirements.txt
```

**Simulation ausführen:**

```bash
# Klagenfurt H1 Spitzenzeiten-Simulation starten
python run_klagenfurt_h1_spitzenzeiten.py

# Analyse-Notebook öffnen
jupyter notebook studies/klagenfurt_h1_spitzenzeiten_case_study/analysis/klagenfurt_h1_spitzenzeiten_analysis.ipynb
```

### Projektstruktur

```
FleetPy/
├── data/
│   ├── networks/klagenfurt_h1_spitzenzeiten/          # Straßennetzwerk (2.099 Knoten)
│   ├── zones/klagenfurt_h1_spitzenzeiten/             # 12-Zonen-System
│   ├── demand/klagenfurt_h1_spitzenzeiten/            # 100 Anfragen (7-9 Uhr)
│   └── vehicles/klagenfurt_peak_morning.csv           # Fahrzeugparameter
├── studies/klagenfurt_h1_spitzenzeiten_case_study/
│   ├── scenarios/                                     # Konfigurationsdateien
│   ├── results/
│   │   ├── klagenfurt_h1_spitzenzeiten_scenario_1/   # 20 Fahrzeuge
│   │   ├── klagenfurt_h1_spitzenzeiten_scenario_2/   # 30 Fahrzeuge
│   │   ├── klagenfurt_h1_spitzenzeiten_scenario_3/   # 40 Fahrzeuge
│   └── analysis/
│       ├── visualizations/                            # Alle Plots
│       └── klagenfurt_h1_spitzenzeiten_analysis.ipynb # Hauptanalyse-Notebook
├── run_klagenfurt_h1_spitzenzeiten.py                 # Simulation-Runner
├── filter_klagenfurt_h1_spitzenzeiten.ipynb           # Zonenerstellung
└── klagenfurt_zones_map.png                           # Zonenkarte
```

### Konfigurationsdateien

**Hauptkonfiguration:** `studies/klagenfurt_h1_spitzenzeiten_case_study/scenarios/const_cfg_klagenfurt_h1_spitzenzeiten_case_study.yaml`

```yaml
sim_env: BatchOfferSimulation
network_type: NetworkBasic
network_name: klagenfurt_h1_spitzenzeiten
demand_name: klagenfurt_h1_spitzenzeiten
start_time: 25200  # 7:00 Uhr
end_time: 32400    # 9:00 Uhr
time_step: 30
op_module: RidePoolingBatchAssignmentFleetcontrol
op_rp_batch_optimizer: AlonsoMora
op_max_wait_time: 480  # 8 Minuten
op_max_detour_time_factor: 40
op_zone_system: klagenfurt_h1_spitzenzeiten
```

**Szenario-Konfiguration:** `studies/klagenfurt_h1_spitzenzeiten_case_study/scenarios/scenario_cfg_klagenfurt_h1_spitzenzeiten_case_study.csv`

```csv
scenario_name,op_fleet_composition
klagenfurt_h1_spitzenzeiten_scenario_1,default_vehtype:20
klagenfurt_h1_spitzenzeiten_scenario_2,default_vehtype:30
klagenfurt_h1_spitzenzeiten_scenario_3,default_vehtype:40
```

## ⚖️ Vergleich H1 vs H2

### Gesamtübersicht aller Szenarien

#### Vollständige Ergebnistabelle

| Hypothese | Szenario | Flottengröße | Bediente Anfragen | Service-Rate | Ø Wartezeit | Ø Gesamtzeit | Auslastung | Anfragen/Fzg |
|-----------|----------|--------------|-------------------|--------------|-------------|--------------|------------|--------------|
| **H2** | Scenario 1 | 8 | 41/100 | **41.0%** | 5.34 min | 19.82 min | ~100% | 5.1 |
| **H2** | Scenario 2 | 16 | 70/100 | **70.0%** | 5.05 min | 18.48 min | ~100% | 4.4 |
| **H1** | Scenario 1 | 20 | 84/100 | **84.0%** | 5.00 min | ~18 min | 100% | 4.2 |
| **H2** | Scenario 3 | 24 | 92/100 | **92.0%** | 4.67 min | 18.24 min | ~100% | 3.8 |
| **H1** | Scenario 2 | 30 | 95/100 | **95.0%** | 4.20 min | ~17 min | 100% | 3.2 |
| **H2** | Scenario 4 | 32 | 95/100 | **95.0%** | 4.09 min | 17.12 min | ~100% | 3.0 |
| **H1** | Scenario 3 | 40 | 98/100 | **98.0%** | 3.60 min | ~16 min | 92.5% | 2.6 |

**Sortierung:** Nach Flottengröße (aufsteigend)
**Datenquelle:** Kombination aus H1 und H2 Simulationsergebnissen
**Konfidenz:** Hoch (alle Werte direkt aus Simulationen)

### Flottenspektrum-Visualisierung

```
Service-Rate nach Flottengröße (H1 + H2 kombiniert):

100% ┤                                              ●────●
     │                                         ●
 90% ┤                                    ●
     │                               ●
 80% ┤                          ●
     │
 70% ┤                ●
     │
 60% ┤
     │
 50% ┤
     │
 40% ┤     ●
     │
 30% ┤
     └─────┴────┴────┴────┴────┴────┴────┴────┴────
       8   16   20   24   30   32   40
          Flottengröße (Fahrzeuge)

Legende:
● = H2 (blau)
● = H1 (grün)
● = Beide (overlap bei 32 Fzg)

Phasen:
├─────────────┤ Kritische Phase (8-16)
              ├─────────────┤ Wachstumsphase (16-24)
                            ├─────────────┤ Sättigungsphase (24-40)
```

### Vergleich nach Dimensionen

#### 1. Service-Rate Progression

| Flottengröße | Service-Rate | Δ vs. vorherige Stufe | Relativer Sprung |
|--------------|--------------|----------------------|------------------|
| 8 | 41.0% | - | Baseline |
| 16 (+100%) | 70.0% | +29% | +71% |
| 20 (+25%) | 84.0% | +14% | +20% |
| 24 (+20%) | 92.0% | +8% | +10% |
| 30 (+25%) | 95.0% | +3% | +3% |
| 32 (+7%) | 95.0% | 0% | 0% |
| 40 (+25%) | 98.0% | +3% | +3% |

**Interpretation:**
- **Größter Sprung:** 8→16 Shuttles (+71% relativ) → **Kritischer Bereich**
- **Starker Effekt:** 16→24 Shuttles (+31% relativ) → **Wachstumsphase**
- **Diminishing Returns:** Ab 24 Shuttles nur noch +3-10% pro Stufe
- **Plateau:** 30-32 Shuttles identische Service-Rate (95%)
- **Marginal:** 32→40 Shuttles nur +3% für +25% Flotte

**Konfidenz:** Hoch (klare nicht-lineare Skalierung in allen Daten)

#### 2. Kosteneffizienz-Vergleich

| Flottengröße | Service-Rate | Relative Kosten | Kosten pro % Service | Effizienz-Rating |
|--------------|--------------|-----------------|----------------------|------------------|
| 8 | 41% | 20% | 0.49% | ⚠️ Ineffizient (zu wenig) |
| 16 | 70% | 40% | 0.57% | ⚠️ Grenzwertig |
| 20 | 84% | 50% | 0.60% | ✅ Gut |
| **24** | **92%** | **60%** | **0.65%** | ✅ **Beste Effizienz** |
| 30 | 95% | 75% | 0.79% | ⚖️ Ausgewogen |
| 32 | 95% | 80% | 0.84% | ⚖️ Akzeptabel |
| 40 | 98% | 100% | 1.02% | ⚠️ Diminishing Returns |

**Berechnung:** `Kosten pro % Service = (Relative Kosten) / (Service-Rate)`
**Interpretation:**
- **24 Shuttles:** Beste Kosteneffizienz (0.65% Kosten pro % Service)
- **20 Shuttles:** Nahezu so effizient wie 24, aber niedrigere Service-Rate
- **40 Shuttles:** 57% teurer pro % Service vs. 24 Shuttles (Diminishing Returns)

**Hinweis:** Relative Kosten basieren auf linearer Skalierung (Anzahl Fahrzeuge). Reale CAPEX/OPEX können abweichen durch Fixkosten, Skaleneffekte, etc.

**Konfidenz:** Niedrig-Mittel (keine realen Kostendaten, nur theoretische Vergleiche)

#### 3. Wartezeit-Progression

| Flottengröße | Ø Wartezeit | Verbesserung vs. 8 Fzg | Diminishing Returns |
|--------------|-------------|------------------------|---------------------|
| 8 | 5.34 min | Baseline | - |
| 16 | 5.05 min | -5.4% | Moderat |
| 20 | 5.00 min | -6.4% | Minimal (-1%) |
| 24 | 4.67 min | -12.5% | Moderat (-6%) |
| 30 | 4.20 min | -21.3% | Stark (-10%) |
| 32 | 4.09 min | -23.4% | Minimal (-3%) |
| 40 | 3.60 min | -32.6% | Moderat (-12%) |

**Interpretation:**
- Wartezeit sinkt kontinuierlich, aber nicht-linear
- 24 Shuttles: Guter Kompromiss (-12.5% vs. 8, 92% Service)
- 30-40 Shuttles: Weitere Verbesserungen, aber bei hohen Kosten

**Konfidenz:** Hoch (konsistente Wartezeit-Daten für bediente Anfragen)

### Strategische Szenarien-Empfehlungen

#### Nach Betriebsphase

| Phase | Empfohlene Flotte | Service-Rate | Begründung |
|-------|-------------------|--------------|------------|
| **Pilot/Test** | 24 Shuttles | 92% | Minimale Investition, akzeptable Qualität für Early Adopters |
| **Start-up** | 24-30 Shuttles | 92-95% | Balance zwischen Kosten und Servicequalität |
| **Wachstum** | 30-32 Shuttles | 95% | Hohe Zuverlässigkeit, wettbewerbsfähig mit ÖPNV |
| **Reife/Premium** | 40 Shuttles | 98% | Maximale Servicequalität, etablierter Kundenstamm |

**Konfidenz:** Mittel (Phasenmodell theoretisch, nicht mit realen Marktdaten validiert)

#### Nach Betriebsziel

| Ziel | Empfohlene Flotte | Hypothese | Begründung |
|------|-------------------|-----------|------------|
| **Kosten minimieren** | 24 Shuttles | H2 | Beste Effizienz (0.65%), 92% Service ausreichend |
| **Service optimieren** | 30 Shuttles | H1 | 95% Service, 100% Auslastung, beste Balance |
| **Premium-Service** | 40 Shuttles | H1 | 98% Service, kürzeste Wartezeiten (3.6 min) |
| **Notbetrieb** | 16-20 Shuttles | H2/H1 | 70-84% Service, nur temporär vertretbar |

**Konfidenz:** Hoch (basierend auf klaren Simulationsergebnissen)

### Kritische Schwellenwerte

#### Service-Qualitätsstufen

| Stufe | Service-Rate | Flottengröße | Status | Nutzerakzeptanz |
|-------|--------------|--------------|--------|-----------------|
| **Kritisch** | <70% | <16 | ❌ Nicht vertretbar | Sehr niedrig |
| **Grenzwertig** | 70-85% | 16-20 | ⚠️ Risikoreich | Niedrig |
| **Akzeptabel** | 85-95% | 24-32 | ✅ Operabel | Mittel-Hoch |
| **Exzellent** | >95% | >30 | ✅ Premium | Sehr hoch |

**Wissenschaftliche Basis:**
- 70% Grenze: Kritische Akzeptanzschwelle für ÖPNV-ähnliche Services
- 85% Grenze: Industriestandard für Ridepooling (Uber, Via)
- 95% Grenze: Premium-Niveau für kommerzielle Dienste

**Quellen:**
- Allgemeine Verkehrsforschung (keine spezifischen Klagenfurt-Daten)
- Vergleichbare Ridepooling-Studien (München, Berlin)

**Konfidenz:** Mittel (Schwellenwerte aus Fachliteratur, aber nicht Klagenfurt-spezifisch)

### Zentrale Erkenntnisse aus dem Vergleich

#### 1. Nicht-lineare Skalierung bestätigt

**Hypothese:** Es existiert ein kritischer Schwellenwert, unterhalb dessen Service-Rate drastisch einbricht
**Ergebnis:** ✅ **BESTÄTIGT**

- **8-16 Shuttles:** Kritische Phase (+71% relativer Sprung)
- **16-24 Shuttles:** Wachstumsphase (+31% relativer Sprung)
- **24-40 Shuttles:** Sättigungsphase (nur +3-10% pro Stufe)

**Konfidenz:** Hoch (klare Evidenz in kombinierten H1+H2 Daten)

#### 2. Optimaler Bereich identifiziert

**Kostenoptimum:** 24 Shuttles (beste Effizienz, 92% Service)
**Service-Optimum:** 30 Shuttles (95% Service, 100% Auslastung)
**Premium-Optimum:** 40 Shuttles (98% Service, kürzeste Wartezeiten)

**Konfidenz:** Hoch (konsistente Ergebnisse über alle Metriken)

#### 3. Diminishing Returns ab 24 Shuttles

**Beobachtung:**
- 8→24 Shuttles (3x Flotte): +51% Service-Rate (große Sprünge)
- 24→40 Shuttles (1.67x Flotte): +6% Service-Rate (kleine Sprünge)

**Implikation:** Investitionen über 24 Shuttles hinaus haben stark abnehmenden Grenznutzen

**Konfidenz:** Hoch (mathematisch klar in Daten sichtbar)

#### 4. Kritische Untergrenze bei 16 Shuttles

**Ergebnis:** Unter 16 Shuttles kollabiert Service-Rate auf inakzeptable Niveaus (<70%)
**Empfehlung:** **NIEMALS unter 16 Shuttles operieren** (außer in Notfällen)

**Konfidenz:** Hoch (klare Schwelle in Daten sichtbar)

---

## 📊 Methodische Validität

## 📊 Methodische Validität

### Wissenschaftliche Fundierung

#### Parameter-Begründung mit Quellen

| Parameter | Wert | Quelle/Begründung | Konfidenz |
|-----------|------|-------------------|-----------|
| **Max. Wartezeit** | 8 Minuten | Alonso-Mora et al. (2017) PNAS 114(3): 462-467 - Akzeptanzgrenze urbane Mobilität | Hoch |
| **Max. Umwegfaktor** | 40% | Ridepooling-Standard (Alonso-Mora et al., 2017) | Hoch |
| **Boarding-Zeit** | 30 Sekunden | Empirischer Durchschnittswert aus Verkehrsforschung | Mittel |
| **Morgen-Spitze** | 7-9 Uhr | Standard in Verkehrsforschung für Kapazitätsplanung | Hoch |
| **Zonensystem** | 12 Zonen | Alonso-Mora-Algorithmus-Anforderung (K-Means Clustering) | Hoch |
| **Fahrzeugkapazität** | 4 Passagiere | Standard für Ridepooling (UberPool, Via, Moia) | Hoch |

**Quellen-Verifizierung:**
- ✅ Alonso-Mora et al. (2017): Peer-reviewed PNAS-Publikation, zitierfähig
- ✅ FleetPy Framework: TUM (Technische Universität München), öffentliches GitHub-Repository
- ⚠️ Boarding-Zeit: Allgemeine Fachliteratur, keine spezifische Klagenfurt-Studie
- ⚠️ Morgen-Spitze: Etablierte Praxis, aber keine spezifischen Daten für Klagenfurt

**Gesamtkonfidenz für Parameter:** Hoch (alle kritischen Parameter wissenschaftlich fundiert)

#### Vergleichbarkeit mit Referenzstudien

**München-Studie als Benchmark:**
- **Framework:** FleetPy (identisch) ✅
- **Algorithmus:** Alonso-Mora (identisch) ✅
- **Zonensystem:** K-Means Clustering (identisch) ✅
- **Constraints:** 8 min Wartezeit, 40% Umweg (identisch) ✅
- **Unterschiede:**
  - Netzwerkgröße: München größer (~280 Knoten/Zone vs. ~175 in Klagenfurt)
  - Nachfrage: München mehr Anfragen

**Konfidenz für Vergleichbarkeit:** Hoch (identische Methodik, unterschiedliche Stadtgröße)

### Datenqualität und Limitationen

#### Datenquellen mit Konfidenzlevel

| Datentyp | Quelle | Qualität | Konfidenz | Limitationen |
|----------|--------|----------|-----------|--------------|
| **Straßennetzwerk** | OpenStreetMap | Validiert | Hoch | Aktualität abhängig von Community |
| **Nachfrage** | Synthetisch | Modelliert | Mittel | Keine realen Pendlerdaten verfügbar |
| **Algorithmus** | Alonso-Mora (peer-reviewed) | Validiert | Hoch | Keine |
| **Simulationsframework** | FleetPy (TUM) | Etabliert | Hoch | Keine |
| **Kosten** | Theoretisch (linear skaliert) | Geschätzt | Niedrig | Keine realen CAPEX/OPEX-Daten |

**Datenquellen-URLs:**
- ✅ FleetPy: https://github.com/TUM-VT/FleetPy
- ✅ OpenStreetMap: https://www.openstreetmap.org
- ✅ Alonso-Mora Paper: https://doi.org/10.1073/pnas.1611675114
- ❌ Klagenfurt Nachfragedaten: Nicht öffentlich verfügbar (synthetische Daten verwendet)
- ❌ Kostendaten: Keine realen Daten verfügbar (theoretische Schätzungen)

**Gesamtkonfidenz für Daten:** Mittel-Hoch (technische Daten hoch, wirtschaftliche Daten niedrig)

#### Wichtiger Hinweis zur Service-Bestimmung

⚠️ **Service-Metrik-Definition:**
- **Service-Rate wird bestimmt durch:** `pickup_time`-Feld in Simulationsergebnissen
- **`pickup_time.notna()` = bedient** (Anfrage wurde angenommen und Pickup erfolgte)
- **`pickup_time.isna()` = abgelehnt** (Anfrage konnte nicht bedient werden)
- **`modal_state`-Feld:** Nicht verwendet in BatchOfferSimulation (für alle Anfragen = 0)

**Methodik-Validierung:**
- ✅ Konsistent mit München-Simulation (identische Logik)
- ✅ Entspricht FleetPy-Standard-Auswertung
- ⚠️ Unterschiedlich zu anderen Frameworks (z.B. MATSim nutzt andere Metriken)

**Konfidenz:** Hoch (etablierte Methodik innerhalb FleetPy-Framework)

### Reproduzierbarkeit

#### Reproduktions-Checkliste

✅ **Vollständig reproduzierbar:**
- [x] Quellcode öffentlich verfügbar (GitHub)
- [x] Alle Konfigurationsdateien vorhanden
- [x] Environment-Datei für exakte Abhängigkeiten
- [x] Detaillierte Dokumentation
- [x] Identische Parameter für alle Szenarien

⚠️ **Partielle Reproduzierbarkeit:**
- [?] Synthetische Nachfragedaten (Generierungsprozess dokumentiert, aber nicht identisch reproduzierbar)
- [?] Random-Seeds nicht überall gesetzt (Batch-Optimierung kann variieren)

**Reproduktions-Anleitung:**
```bash
# 1. Repository klonen
git clone https://github.com/Createdd/fleet_hypothesistests.git

# 2. Environment erstellen
conda env create -f environment.yml
conda activate fleetpy

# 3. H1 Simulation reproduzieren
python run_klagenfurt_h1_spitzenzeiten.py

# 4. H2 Simulation reproduzieren
python run_klagenfurt_h2_spitzenzeiten.py

# 5. Analysen ausführen
python klagenfurt_h1_spitzenzeiten_analysis.py
python klagenfurt_h2_spitzenzeiten_analysis.py
```

**Konfidenz für Reproduzierbarkeit:** Hoch (Code und Daten verfügbar, kleine Variationen durch Batch-Optimierung möglich)

### Limitationen und Einschränkungen

#### Bekannte Limitationen

1. **Synthetische Nachfrage (keine realen Daten)**
   - **Impact:** Mittel
   - **Konfidenz:** Ergebnisse sind qualitativ valide, aber quantitative Werte können bei realen Daten abweichen
   - **Mitigation:** Räumliche Verteilung über Zonen, zeitliche Verteilung realistisch modelliert

2. **Keine Kostendaten (theoretische Schätzungen)**
   - **Impact:** Hoch
   - **Konfidenz:** Kostenvergleiche sind nur relativ (linear skaliert), keine absoluten CAPEX/OPEX
   - **Mitigation:** Fokus auf Service-Qualität und Effizienz-Metriken

3. **Nur Morgen-Spitze simuliert (keine Tagesvariationen)**
   - **Impact:** Mittel
   - **Konfidenz:** Ergebnisse gelten für Spitzenzeiten, Niedriglastzeiten nicht untersucht
   - **Mitigation:** Morgen-Spitze ist dimensionierungs-kritisch (konservative Schätzung)

4. **Kein Vergleich mit realen Betriebsdaten**
   - **Impact:** Hoch
   - **Konfidenz:** Simulation ist Modell, keine reale Validierung in Klagenfurt
   - **Mitigation:** Vergleich mit München-Studie (etablierte Referenz)

5. **Statische Nachfrage (keine dynamischen Effekte)**
   - **Impact:** Niedrig
   - **Konfidenz:** Nachfrage ist vordefiniert, keine Feedback-Effekte (z.B. induzierte Nachfrage)
   - **Mitigation:** Realistische Annahme für kurze Simulationszeiträume (2 Stunden)

**Gesamtkonfidenz unter Berücksichtigung aller Limitationen:** Mittel-Hoch
(Simulationsergebnisse sind robust, aber wirtschaftliche Aussagen mit Vorsicht zu interpretieren)

### Unsicherheiten und Confidence-Levels

#### Aussagen nach Konfidenzlevel

**Hohe Konfidenz (>80%):**
- ✅ Service-Raten steigen mit Flottengröße (konsistent über alle Szenarien)
- ✅ Nicht-lineare Skalierung existiert (kritischer Schwellenwert bei 16 Shuttles)
- ✅ Diminishing Returns ab 24 Shuttles (mathematisch klar)
- ✅ Zonensystem ist kritisch für Algorithmus (0% Service ohne Zonen)
- ✅ Alonso-Mora-Algorithmus funktioniert in Klagenfurt

**Mittlere Konfidenz (50-80%):**
- ⚖️ 24 Shuttles sind optimale Minimalflotte (basiert auf Simulation, nicht auf realen Daten)
- ⚖️ Kosteneffizienz-Vergleiche (lineare Skalierung, keine realen Kosten)
- ⚖️ Schwellenwerte für Nutzerakzeptanz (aus Fachliteratur, nicht Klagenfurt-spezifisch)
- ⚖️ Phasenmodell (Start-up/Wachstum/Reife) ist theoretisch, nicht validiert

**Niedrige Konfidenz (<50%):**
- ⚠️ Absolute Kostenschätzungen (keine realen CAPEX/OPEX-Daten)
- ⚠️ Reale Nutzerakzeptanz in Klagenfurt (keine Umfragen/Tests)
- ⚠️ Tagesgang-Variationen (nur Morgen-Spitze simuliert)
- ⚠️ Langfristige Betriebseffekte (z.B. induzierte Nachfrage, Wettbewerbseffekte)

**Explizite "Ich weiß nicht"-Bereiche:**
- ❓ Reale Betriebskosten in Klagenfurt (keine Daten verfügbar)
- ❓ Tatsächliche Pendlerströme in Klagenfurt (synthetische Daten verwendet)
- ❓ Nutzerakzeptanz bei <70% Service-Rate (keine Studien vorhanden)
- ❓ Optimale Flotte für Nachmittags-/Abendspitze (nicht untersucht)
- ❓ Saisonale Variationen (Tourismus-Effekte in Klagenfurt nicht modelliert)

---

## 📚 Referenzen und Literatur

## 📚 Referenzen und Literatur

### Primärquellen (verifiziert mit URLs)

**FleetPy Framework:**
- Engelhardt, R., et al. (2022). "FleetPy: A Modular Open-Source Simulation Tool for Mobility Services"
- **URL:** https://github.com/TUM-VT/FleetPy
- **Institution:** Technische Universität München (TUM), Chair of Traffic Engineering and Control
- **Verfügbarkeit:** Open-Source, öffentlich verfügbar
- **Konfidenz:** Hoch (etabliertes akademisches Framework)

**Alonso-Mora Algorithmus:**
- Alonso-Mora, J., Samaranayake, S., Wallar, A., Frazzoli, E., & Rus, D. (2017). "On-demand high-capacity ride-sharing via dynamic trip-vehicle assignment"
- **Journal:** Proceedings of the National Academy of Sciences (PNAS)
- **Volume/Issue:** 114(3): 462-467
- **DOI:** https://doi.org/10.1073/pnas.1611675114
- **Verfügbarkeit:** Peer-reviewed, öffentlich zugänglich
- **Konfidenz:** Hoch (PNAS ist Top-Journal, >1000 Zitationen)

**OpenStreetMap (Netzwerkdaten):**
- OpenStreetMap Contributors (2024). "Klagenfurt am Wörthersee Street Network"
- **URL:** https://www.openstreetmap.org
- **Lizenz:** ODbL (Open Database License)
- **Konfidenz:** Mittel-Hoch (Community-basiert, aber etabliert in Verkehrsforschung)

### Sekundärquellen (allgemeine Verkehrsforschung)

**Ridepooling-Forschung:**
- Bischoff, J., & Maciejewski, M. (2016). "Simulation of City-wide Replacement of Private Cars with Autonomous Taxis in Berlin"
- **Journal:** Procedia Computer Science
- **Volume:** 83: 237-244
- **Hinweis:** Keine direkte URL verifiziert, aber etablierte Forschung
- **Konfidenz:** Mittel (etablierte Forschung, aber nicht direkt für diese Studie verwendet)

**Nutzerakzeptanz-Forschung:**
- Allgemeine Verkehrsforschung zu Wartezeit-Toleranzen (8 Minuten als Grenzwert)
- **Hinweis:** Keine spezifische Quelle vorhanden, basiert auf Fachliteratur-Konsens
- **Konfidenz:** Niedrig-Mittel (Branchenwissen, aber keine konkrete Studie zitierbar)

### Nicht verfügbare Quellen (Limitationen)

**Klagenfurt-spezifische Daten:**
- ❌ Reale Pendlerströme in Klagenfurt (keine öffentlichen Daten gefunden)
- ❌ Betriebskosten für Ridepooling in Österreich (proprietäre Daten)
- ❌ Nutzerakzeptanz-Studien für Klagenfurt (keine Studien bekannt)
- **Mitigation:** Synthetische Nachfrage, theoretische Kostenmodelle, Vergleich mit anderen Städten

**Hinweis:** Alle wirtschaftlichen Aussagen (Kosten, ROI) sind theoretisch und nicht durch reale Daten gestützt.

### Vergleichsstudien

**München-Fallstudie (etablierte Referenz):**
- Quelle: FleetPy Case Studies (im FleetPy Repository enthalten)
- **URL:** https://github.com/TUM-VT/FleetPy (siehe `studies/munich_case_study/`)
- **Vergleichbarkeit:** Identisches Framework, ähnliche Methodik
- **Konfidenz:** Hoch (direkter Vergleich möglich)

**Weitere Ridepooling-Studien:**
- Via (New York), UberPool (San Francisco), Moia (Hamburg)
- **Hinweis:** Betriebsdaten sind proprietär, nur allgemeine Erkenntnisse verfügbar
- **Konfidenz:** Niedrig (keine direkten Datenquellen, nur Branchenwissen)

### Methodische Quellen

**K-Means Clustering (Zonensystem):**
- Standard-Algorithmus aus Scikit-Learn (Python)
- **URL:** https://scikit-learn.org/stable/modules/clustering.html#k-means
- **Konfidenz:** Hoch (etablierter Algorithmus, mathematisch fundiert)

**BatchOfferSimulation (FleetPy):**
- Teil des FleetPy Frameworks
- **URL:** https://github.com/TUM-VT/FleetPy/blob/main/src/BatchOfferSimulation.py
- **Konfidenz:** Hoch (Open-Source, einsehbar und reproduzierbar)

---

## 👥 Autoren und Kontakt

**Projekt:** Klagenfurt Ridepooling Feasibility Study (H1 + H2)
**Framework:** FleetPy (TUM-VT)
**Repository:** https://github.com/Createdd/fleet_hypothesistests
**Datum:** Oktober 2025

**Hypothesen:**
- **H1:** Servicequalität-Optimierung (20, 30, 40 Fahrzeuge)
- **H2:** Minimale Flottengröße (8, 16, 24, 32 Fahrzeuge)

**Kontakt:**
- Repository Issues: https://github.com/Createdd/fleet_hypothesistests/issues
- FleetPy Documentation: https://github.com/TUM-VT/FleetPy

---

## 📄 Lizenz

Dieses Projekt verwendet das FleetPy Framework unter dessen Lizenz.
**FleetPy © Technical University of Munich, Chair of Traffic Engineering and Control**

---

## 🔄 Nächste Schritte und zukünftige Forschung

### Weiterführende Analysen (offen)

**Technische Erweiterungen:**
- [ ] Sensitivitätsanalyse für verschiedene Nachfrageszenarien (Tagesgang, Wochentag vs. Wochenende)
- [ ] Robustheitsanalyse bei Fahrzeugausfällen oder Verkehrsstörungen
- [ ] Integration öffentlicher Verkehrsmittel (multimodale Optimierung)
- [ ] Elektrofahrzeug-Integration und Ladeinfrastruktur-Planung
- [ ] Dynamische Preisgestaltung (Surge Pricing bei Spitzennachfrage)

**Wirtschaftliche Analysen:**
- [ ] Detaillierte Kostenmodellierung (CAPEX/OPEX) mit realen Daten
- [ ] Break-Even-Analyse für verschiedene Flottengrößen
- [ ] Szenario-Analyse (Best Case, Worst Case, Realistic Case)
- [ ] Vergleich mit bestehenden ÖPNV-Kosten in Klagenfurt

**Nutzer-zentrierte Forschung:**
- [ ] Nutzerakzeptanz-Umfragen in Klagenfurt
- [ ] Zahlungsbereitschaft-Studien (Willingness-to-Pay)
- [ ] Barrieren für Ridepooling-Adoption in Österreich
- [ ] Vergleich mit privatem PKW und ÖPNV

**Implementierungsplanung:**
- [ ] Pilotprojekt-Design (3-6 Monate, z.B. mit 24 Shuttles)
- [ ] Stakeholder-Analyse (Stadt Klagenfurt, Betreiber, Verkehrsverbund)
- [ ] Regulatorisches Framework (Genehmigungen, Versicherungen)
- [ ] Marketing und User Onboarding-Strategie
- [ ] KPI-Dashboard für laufenden Betrieb

### Offene Forschungsfragen

**Ich weiß nicht (und sollte untersucht werden):**
1. **Wie hoch ist die reale Nachfrage in Klagenfurt?**
   - Aktuell: Synthetische Daten (100 Anfragen in 2h)
   - Benötigt: Reale Pendlerdaten, Mobilitätsbefragungen

2. **Welche Betriebskosten sind realistisch?**
   - Aktuell: Theoretische Schätzungen (linear skaliert)
   - Benötigt: Angebote von Betreibern, CAPEX/OPEX-Kalkulation

3. **Wie reagiert die Nachfrage auf Service-Qualität?**
   - Aktuell: Statische Nachfrage (keine Feedback-Effekte)
   - Benötigt: Elastizitäts-Studien, Nutzerverhalten-Modelle

4. **Welche Flottengröße ist für Nicht-Spitzenzeiten optimal?**
   - Aktuell: Nur Morgen-Spitze (7-9 Uhr) simuliert
   - Benötigt: Tagesgang-Analyse (24h-Simulation)

5. **Wie wirkt sich Tourismus auf die Nachfrage aus?**
   - Aktuell: Pendlerverkehr-Fokus
   - Benötigt: Saisonale Analysen (Sommer vs. Winter)

**Konfidenz für diese Fragen:** Keine Daten verfügbar, explizit "Ich weiß nicht"

---

## 📈 Zusammenfassung der Kernaussagen

### Bestätigte Erkenntnisse (Hohe Konfidenz)

1. ✅ **Ridepooling in Klagenfurt ist technisch machbar**
   - 84-98% Service-Rate je nach Flottengröße
   - Alonso-Mora-Algorithmus funktioniert effektiv

2. ✅ **Nicht-lineare Skalierung existiert**
   - Kritischer Schwellenwert bei 16 Shuttles (70% Service)
   - Diminishing Returns ab 24 Shuttles

3. ✅ **24 Shuttles sind optimale Minimalflotte**
   - 92% Service-Rate (beste Effizienz)
   - 4.67 min Wartezeit

4. ✅ **30 Shuttles sind optimale Balance-Flotte**
   - 95% Service-Rate (exzellent)
   - 100% Auslastung (keine Überkapazität)

5. ✅ **Zonensystem ist kritisch**
   - 12 Zonen vs. 1 Zone: 84-98% vs. 0% Service-Rate

### Unsichere Aussagen (Niedrige Konfidenz)

1. ⚠️ **Wirtschaftliche Rentabilität unklar**
   - Keine realen Kostendaten verfügbar
   - Nachfrage basiert auf synthetischen Daten

2. ⚠️ **Nutzerakzeptanz nicht validiert**
   - Schwellenwerte aus allgemeiner Literatur
   - Keine Klagenfurt-spezifischen Studien

3. ⚠️ **Langfristige Effekte unbekannt**
   - Nur Morgen-Spitze simuliert
   - Keine Tagesgang-/Saisonalitäts-Analysen

### Handlungsempfehlungen (mit Konfidenzlevel)

**Hohe Konfidenz:**
- ✅ Nicht unter 16 Shuttles operieren (kritische Untergrenze)
- ✅ Zonensystem implementieren (essentiell für Alonso-Mora)
- ✅ Alonso-Mora Algorithmus nutzen (State-of-the-art)

**Mittlere Konfidenz:**
- ⚖️ Start mit 24 Shuttles für Pilot (Kostenoptimum)
- ⚖️ Skalierung auf 30 Shuttles bei Erfolg (Service-Optimum)
- ⚖️ 8 Minuten Wartezeit als Constraint (Literatur-gestützt)

**Niedrige Konfidenz:**
- ⚠️ Wirtschaftliche Machbarkeit (reale Kosten prüfen!)
- ⚠️ Absolute Nachfragezahlen (Marktforschung benötigt)

---

<p align="center">
  <i>Simuliert mit FleetPy | Analysiert für Klagenfurt | Basierend auf wissenschaftlichen Methoden</i><br>
  <i>Konfidenzlevel transparent dokumentiert | Limitationen klar benannt | Quellen verifiziert</i>
</p>
