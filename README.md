# 🚌 FLIP-FLOP × FleetPy — Validierung der KI-Nachfrageprognose für Klagenfurt

[![FleetPy](https://img.shields.io/badge/Framework-FleetPy-blue)](https://github.com/TUM-VT/FleetPy)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-green.svg)](https://www.python.org/downloads/)

**Konsortium:** AIT Austrian Institute of Technology, DatenVorsprung, KMG Klagenfurt Mobil, pdcp/SURAAA, Stadt Klagenfurt, Tech Meets Legal (FFG-gefördert).

**Die Frage:** FlipFlop (AIT) sagt per KI-Modell voraus, welche Personen bei einem On-Demand-Angebot (DRT, bedarfsgesteuerter Ridepooling-Verkehr) vom Auto/ÖV/Rad/Fuß umsteigen würden. Ist diese prognostizierte Nachfrage realistisch — und lässt sie sich mit einer Fahrzeugflotte überhaupt sinnvoll bedienen?

**Die Methode:** Das [FleetPy](https://github.com/TUM-VT/FleetPy)-Simulationsframework (TUM) dient als **unabhängiges Validierungswerkzeug**: Die FlipFlop-Prognose wird gegen echte KMG/MOIA-Betriebsdaten aus Klagenfurt benchmarkt — räumlich, mengenmäßig und operativ (simulierte Servicerate bei identischem Netz, Betriebstag und Flottengrößen).

## Ergebnisse (Kurzfassung)

| Check | Ergebnis |
|---|---|
| **Räumlich** — Entsteht die Nachfrage in denselben Stadtteilen wie echte Fahrten? | **0,86 Korrelation** zwischen FlipFlop-Prognose und echten KMG/MOIA-Fahrten über 8 Zonen |
| **Mengenmäßig** — Ist die Nachfragemenge plausibel? | FlipFlop sagt 3,3–23x mehr Nachfrage voraus als MOIA real realisiert — eine Untergrenze, kein Alarmsignal (echtes Warnsignal wäre *weniger* gewesen) |
| **Operativ (Konsistenz-Test, v2)** — Liefert eine plausible Flotte die Bedienqualität, die FlipFlop bei der Prognose *angenommen* hat? | Erst mit **~150 Fahrzeugen** erhalten 90 % der prognostizierten Umsteiger die angenommene Qualität (≤ 6,3 min Wartezeit); mit 40 Fahrzeugen sind es 54 %. Die echte MOIA-Nachfrage braucht dafür 15–20 Fahrzeuge. **Die Prognose ist eine Obergrenze** — mit einer realistischen Flotte liegt die Gleichgewichts-Nachfrage niedriger. Bei gleicher Last pro Fahrzeug ist die FlipFlop-Nachfrage aber mindestens so gut bedienbar wie echte Nachfrage. |

> **Zurückgezogen (Nov 2026):** Die frühere operative Aussage „Servicerate-Kurven nahezu identisch" beruhte auf einem Simulationsnetz mit fehlerhaften Fahrzeiten (effektiv 3–4 km/h). Netz, Nachfrage und Fragestellung wurden in v2 neu aufgesetzt; Details und Annahmen im [v2-Notebook](studies/flipflop_drt_integration_pilot/analysis/flipflop_v2_consistency_test.ipynb). Die räumliche und die mengenmäßige Prüfung nutzen keine Simulation und sind davon nicht betroffen.

Die 8 Vergleichszonen wurden per Clustering direkt aus den echten MOIA-Fahrten gebildet (keine Verwaltungsgrenzen). Zone 4 ist das Stadtzentrum — dort weicht die Prognose am stärksten ab (39 % vs. 24 % der Fahrtstarts):

![FlipFlop vs. MOIA: Anteil der Fahrtstarts je Zone](studies/flipflop_drt_integration_pilot/results/flipflop_vs_moia_zone_map.png)

Ein unabhängiger Fund bestätigt zudem eine bereits von AIT beobachtete Modell-Eigenschaft: hohe Kostensensitivität, geringe Zeitsensitivität im Choice-Modell — zwei getrennte Methoden, ein übereinstimmendes Ergebnis.

## 📌 Einstieg

1. **Konsistenz-Test (aktuell, v2):** [`flipflop_v2_consistency_test.ipynb`](studies/flipflop_drt_integration_pilot/analysis/flipflop_v2_consistency_test.ipynb) — implizite MOIA-Flotte, Flottenbedarf der FlipFlop-Nachfrage, Verhalten bei gleicher Last
2. **Präsentationsfassung (kurz; Abschnitt 3 dort durch v2 ersetzt):** [`consortium_presentation_flipflop_validation.ipynb`](studies/flipflop_drt_integration_pilot/analysis/consortium_presentation_flipflop_validation.ipynb)
3. **Räumliche und mengenmäßige Prüfung im Detail:** [`flipflop_demand_model_validity.ipynb`](studies/flipflop_drt_integration_pilot/analysis/flipflop_demand_model_validity.ipynb)
4. **Methodik, Skripte, Reproduktion, offene Punkte:** [`studies/flipflop_drt_integration_pilot/README.md`](studies/flipflop_drt_integration_pilot/README.md)

## Setup

```bash
git clone https://github.com/Createdd/fleet_hypothesistests.git
cd fleet_hypothesistests
conda env create -f environment.yml
conda activate fleetpy
```

Die FlipFlop-Eingangsdaten (`data/SampleFiles_recovered/`, Modell-Draws von AIT) und die MOIA-Fahrtdaten (`data/demand/trips_klagenfurt.csv`) sind nicht Teil des Repos und müssen separat abgelegt werden. Alle Befehle zum Netzbau, zur Nachfrageaufbereitung und zu den Simulationsläufen stehen im [Studien-README](studies/flipflop_drt_integration_pilot/README.md).

## Weitere Inhalte

- **Frühere 8-Sitzer-Fallstudie (2025, H1/H2/UC2/UC3):** Machbarkeitsstudie mit 8-/12-Sitzer-Fahrzeugen, abgeschlossen; Ergebnisse wegen eines Netzwerkfehlers derzeit **unter Vorbehalt** → [studies/klagenfurt_8sitzer_studie/README.md](studies/klagenfurt_8sitzer_studie/README.md)
- **Framework:** `src/`, `run_examples.py` und die Beispielstudien in `studies/` (example_study, munich, manhattan, chicago, module_tests) stammen aus dem TUM-FleetPy-Upstream; Parameterreferenz in [Input_Parameters.md](Input_Parameters.md). Einzige lokale Änderung am Framework: CLI-Fix in `run_examples.py` (`sys.argv[1:]`).
- **Archiv:** abgelöste Skripte, Notebooks und README-Versionen in [archive/](archive/).

## Glossar

- **DRT:** Demand-Responsive Transport — bedarfsgesteuerter On-Demand-Verkehr ohne festen Fahrplan, hier als Ridepooling
- **Umsteiger (H-A):** Weg, der laut FlipFlop im Ist-Zustand nicht mit ÖV, bei DRT-Angebot zum ÖV-Tarif aber mit DRT zurückgelegt würde
- **Servicerate:** Anteil bedienter Anfragen an allen Anfragen
- **Wartezeit:** Zeit zwischen Anfrage und Abholung (Ø über bediente Anfragen)

## Datenquellen

- **Nachfrageprognose:** FlipFlop Mixed-Logit-Choice-Modell (AIT), 471.140 kalibrierte Wege, 5 stochastische Draws je Szenario
- **Betriebsdaten:** MOIA-Fahrten Klagenfurt (7 Kalendertage), bereitgestellt über das Konsortium
- **Netzwerkdaten:** OpenStreetMap Klagenfurt
- **Algorithmus:** Alonso-Mora et al. (2017), PNAS 114(3): 462-467
- **Framework:** [FleetPy](https://github.com/TUM-VT/FleetPy) (TUM München)

## Lizenz
Dieses Projekt verwendet das FleetPy-Framework unter dessen Lizenz.
© Technische Universität München, Lehrstuhl für Verkehrstechnik

---

**Repository:** [github.com/Createdd/fleet_hypothesistests](https://github.com/Createdd/fleet_hypothesistests)
**Hinweis:** Diese Dokumentation wurde mithilfe von KI-Tools erstellt und unterstützt.
