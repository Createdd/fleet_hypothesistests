# 🚌 FleetPy Klagenfurt H2 Spitzenzeiten Fallstudie

## Ridepooling-Simulation für Klagenfurt am Wörthersee - Hypothese 2

**Status:** ✅ Aktiv | **Framework:** FleetPy | **Version:** 2024

---

## 🎯 Studienziel

Diese Studie testet **Hypothese 2 (H2)**: Evaluation kleinerer Flottengrößen (8-32 Shuttles) zur Bestimmung der Mindestflottengröße für akzeptable Servicequalität während der morgendlichen Spitzenzeiten.

### Unterschied zu H1
- **H1**: Größere Flotten (20, 30, 40 Fahrzeuge) - Optimalitätstest
- **H2**: Kleinere Flotten (8, 16, 24, 32 Fahrzeuge) - Minimalitätstest

---

## 📊 Simulationsszenarien

| Szenario | Fahrzeuge | Erwartete Service-Rate | Ziel |
|----------|-----------|------------------------|------|
| **Szenario 1** | 8 Shuttles | ~50-60% | Baseline minimum |
| **Szenario 2** | 16 Shuttles | ~70-80% | Kritischer Bereich |
| **Szenario 3** | 24 Shuttles | ~85-90% | Akzeptanzgrenze |
| **Szenario 4** | 32 Shuttles | ~90-95% | Komfortzone |

---

## 🚀 Simulation ausführen

```bash
# H2 Simulation starten
python run_klagenfurt_h2_spitzenzeiten.py

# Analyse durchführen
python klagenfurt_h2_spitzenzeiten_analysis.py

# Analyse-Notebook öffnen
jupyter notebook studies/klagenfurt_h2_spitzenzeiten_case_study/analysis/klagenfurt_h2_spitzenzeiten_analysis.ipynb
```

---

## 📁 Projektstruktur

```
FleetPy/
├── studies/klagenfurt_h2_spitzenzeiten_case_study/
│   ├── scenarios/
│   │   ├── const_cfg_klagenfurt_h2_spitzenzeiten_case_study.yaml
│   │   └── scenario_cfg_klagenfurt_h2_spitzenzeiten_case_study.csv
│   ├── results/
│   │   ├── klagenfurt_h2_spitzenzeiten_scenario_1/   # 8 Shuttles
│   │   ├── klagenfurt_h2_spitzenzeiten_scenario_2/   # 16 Shuttles
│   │   ├── klagenfurt_h2_spitzenzeiten_scenario_3/   # 24 Shuttles
│   │   └── klagenfurt_h2_spitzenzeiten_scenario_4/   # 32 Shuttles
│   └── analysis/
│       └── klagenfurt_h2_spitzenzeiten_analysis.ipynb
├── run_klagenfurt_h2_spitzenzeiten.py
└── klagenfurt_h2_spitzenzeiten_analysis.py
```

---

## 📋 Konfiguration

### Szenario-Konfiguration

```csv
scenario_name,op_fleet_composition
klagenfurt_h2_spitzenzeiten_scenario_1,default_vehtype:8
klagenfurt_h2_spitzenzeiten_scenario_2,default_vehtype:16
klagenfurt_h2_spitzenzeiten_scenario_3,default_vehtype:24
klagenfurt_h2_spitzenzeiten_scenario_4,default_vehtype:32
```

### Kerneigenschaften
- **Zeitfenster**: 7:00-9:00 Uhr (Morgenspitze)
- **Netzwerk**: Gleich wie H1 (klagenfurt_h1_spitzenzeiten)
- **Nachfrage**: Gleich wie H1 (~100 Anfragen)
- **Max. Wartezeit**: 8 Minuten
- **Max. Umwegfaktor**: 40%

---

## 🔍 Forschungsfragen

1. **Minimale Flottengröße**: Ab wie vielen Fahrzeugen wird eine Service-Rate > 80% erreicht?
2. **Effizienzoptimum**: Bei welcher Flottengröße ist die Anzahl bedienter Anfragen pro Fahrzeug maximal?
3. **Kosteneffizienz**: Wo liegt der optimale Trade-off zwischen Servicequalität und Flottenkosten?
4. **Skalierbarkeit**: Wie verhält sich die Service-Rate bei Verdopplung der Flotte (8→16→32)?

---

## 📈 Erwartete Erkenntnisse

### Hypothesen
- Bei 8 Shuttles: Signifikante Unterversorgung (< 70% Service-Rate)
- Bei 16 Shuttles: Kritischer Bereich (70-85% Service-Rate)
- Bei 24 Shuttles: Akzeptable Versorgung (> 85% Service-Rate)
- Bei 32 Shuttles: Annäherung an H1-Ergebnisse

### Vergleich mit H1
Die H2-Studie ermöglicht die Identifikation der **minimalen wirtschaftlichen Flottengröße**, während H1 die **optimale Servicequalität** bei größeren Flotten untersucht.

---

## 👥 Projektinformationen

**Projekt:** Klagenfurt H2 Spitzenzeiten - Minimal Fleet Analysis
**Framework:** FleetPy (TUM-VT)
**Hypothese:** H2 - Minimalflotten-Test
**Datum:** Oktober 2025

---

<div align="center">
  <b>🚌 Ridepooling Research 🚌</b><br>
  <i>Simuliert mit FleetPy | Analysiert für Klagenfurt | Optimiert für Wirtschaftlichkeit</i>
</div>
