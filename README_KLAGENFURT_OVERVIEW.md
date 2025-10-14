# 🚌 Klagenfurt Ridepooling Studien - Übersicht

## Studienvergleich: H1 vs H2

### 📊 **Hypothese 1 (H1): Optimal Fleet Analysis**
**Ziel:** Bestimmung der optimalen Flottengröße für maximale Servicequalität

| Szenario | Fahrzeuge | Erwartung |
|----------|-----------|-----------|
| H1-Scenario 1 | 20 Shuttles | Baseline |
| H1-Scenario 2 | 30 Shuttles | Optimum |
| H1-Scenario 3 | 40 Shuttles | Maximum |

**Forschungsfrage:** Welche Flottengröße bietet die beste Balance zwischen Servicequalität und Ressourceneinsatz bei bereits guter Basisversorgung?

**Ausführen:**
```bash
python run_klagenfurt_h1_spitzenzeiten.py
python klagenfurt_h1_spitzenzeiten_analysis.py
```

---

### 📊 **Hypothese 2 (H2): Minimal Fleet Analysis**
**Ziel:** Bestimmung der minimalen Flottengröße für akzeptable Servicequalität

| Szenario | Fahrzeuge | Erwartung |
|----------|-----------|-----------|
| H2-Scenario 1 | 8 Shuttles | Unterversorgung |
| H2-Scenario 2 | 16 Shuttles | Kritisch |
| H2-Scenario 3 | 24 Shuttles | Akzeptabel |
| H2-Scenario 4 | 32 Shuttles | Gut |

**Forschungsfrage:** Was ist die minimal notwendige Flottengröße für wirtschaftlich vertretbare Servicequalität (>80% Service-Rate)?

**Ausführen:**
```bash
python run_klagenfurt_h2_spitzenzeiten.py
python klagenfurt_h2_spitzenzeiten_analysis.py
```

---

## 🎯 Kombinierte Analyse

### Flottengrößen-Spektrum
```
H2 ←─────────────────────────────────→ H1
8 ─── 16 ─── 24 ─── 32 ─── 20 ─── 30 ─── 40

Minimal     Kritisch    Akzeptabel    Optimal    Maximum
```

### Erwartete Service-Raten
```
Fleet Size:  8    16    24    32    20    30    40
H2:        [50%] [75%] [85%] [92%]  -     -     -
H1:         -     -     -     -   [84%] [92%] [98%]
```

### Kernmetriken für Vergleich

| Metrik | H2 (8-32) | H1 (20-40) |
|--------|-----------|------------|
| **Fokus** | Minimalversorgung | Optimalversorgung |
| **Service-Rate** | 50-92% | 84-98% |
| **Wartezeit** | 5-10 min | 3.6-5.0 min |
| **Kosteneffizienz** | Hoch | Mittel |
| **Servicequalität** | Variable | Konstant hoch |

---

## 📁 Projektstruktur

```
FleetPy/
├── README_KLAGENFURT_H1.md  # H1 Dokumentation
├── README_KLAGENFURT_H2.md  # H2 Dokumentation
├── README_KLAGENFURT_OVERVIEW.md  # Diese Datei
│
├── run_klagenfurt_h1_spitzenzeiten.py
├── run_klagenfurt_h2_spitzenzeiten.py
├── klagenfurt_h1_spitzenzeiten_analysis.py
├── klagenfurt_h2_spitzenzeiten_analysis.py
│
└── studies/
    ├── klagenfurt_h1_spitzenzeiten_case_study/
    │   ├── scenarios/
    │   ├── results/
    │   │   ├── klagenfurt_h1_spitzenzeiten_scenario_1/  (20)
    │   │   ├── klagenfurt_h1_spitzenzeiten_scenario_2/  (30)
    │   │   └── klagenfurt_h1_spitzenzeiten_scenario_3/  (40)
    │   └── analysis/
    │
    └── klagenfurt_h2_spitzenzeiten_case_study/
        ├── scenarios/
        ├── results/
        │   ├── klagenfurt_h2_spitzenzeiten_scenario_1/  (8)
        │   ├── klagenfurt_h2_spitzenzeiten_scenario_2/  (16)
        │   ├── klagenfurt_h2_spitzenzeiten_scenario_3/  (24)
        │   └── klagenfurt_h2_spitzenzeiten_scenario_4/  (32)
        └── analysis/
```

---

## 🔬 Gemeinsame Parameter

Beide Studien verwenden:
- **Netzwerk:** klagenfurt_h1_spitzenzeiten (2.099 Knoten)
- **Nachfrage:** klagenfurt_h1_spitzenzeiten (~100 Anfragen)
- **Zeitfenster:** 7:00-9:00 Uhr (Morgenspitze)
- **Max. Wartezeit:** 8 Minuten (480s)
- **Max. Umweg:** 40%
- **Zonensystem:** 12 Zonen
- **Algorithmus:** Alonso-Mora Ridepooling

---

## 📈 Analyseablauf

### 1. Alle Szenarien simulieren
```bash
# H1 (20, 30, 40 Fahrzeuge)
python run_klagenfurt_h1_spitzenzeiten.py

# H2 (8, 16, 24, 32 Fahrzeuge)
python run_klagenfurt_h2_spitzenzeiten.py
```

### 2. Einzelanalysen durchführen
```bash
python klagenfurt_h1_spitzenzeiten_analysis.py
python klagenfurt_h2_spitzenzeiten_analysis.py
```

### 3. Vergleichsanalyse erstellen
```python
import pandas as pd

h1_results = pd.read_csv('studies/klagenfurt_h1_spitzenzeiten_case_study/results/klagenfurt_h1_spitzenzeiten_scenarios_comparison.csv')
h2_results = pd.read_csv('studies/klagenfurt_h2_spitzenzeiten_case_study/results/klagenfurt_h2_spitzenzeiten_scenarios_comparison.csv')

combined = pd.concat([h2_results, h1_results]).sort_values('Fleet Size')
print(combined)
```

---

## 🎓 Forschungsbeitrag

### H2 beantwortet:
- ✅ Minimale wirtschaftliche Flottengröße
- ✅ Skalierungsverhalten bei kleinen Flotten
- ✅ Kritische Schwellenwerte der Servicequalität
- ✅ Kosten-Nutzen-Verhältnis bei Minimalversorgung

### H1 beantwortet:
- ✅ Optimale Flottengröße für maximale Service-Rate
- ✅ Diminishing Returns bei größeren Flotten
- ✅ Maximal erreichbare Servicequalität
- ✅ Performanz bei Überkapazität

### Kombiniert:
- ✅ Vollständiges Spektrum: 8-40 Fahrzeuge
- ✅ Wirtschaftliche vs. qualitative Optima
- ✅ Skalierungseffekte über gesamten Bereich
- ✅ Evidenzbasierte Flottengrößen-Empfehlungen

---

## 👥 Projektinformationen

**Projekt:** Klagenfurt Ridepooling Feasibility Studies
**Framework:** FleetPy (TUM-VT)
**Hypothesen:** H1 (Optimal) + H2 (Minimal)
**Datum:** Oktober 2025
**Repository:** https://github.com/Createdd/fleet_hypothesistests

---

<div align="center">
  <b>🚌 Comprehensive Ridepooling Analysis 🚌</b><br>
  <i>Von minimaler Versorgung bis zu optimaler Servicequalität</i>
</div>
