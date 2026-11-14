# 🚌 FLIP-FLOP × FleetPy — Plausibilitäts- und Konsistenzprüfung der KI-Nachfrageprognose für Klagenfurt

[![FleetPy](https://img.shields.io/badge/Framework-FleetPy-blue)](https://github.com/TUM-VT/FleetPy)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-green.svg)](https://www.python.org/downloads/)

**Konsortium:** AIT Austrian Institute of Technology, DatenVorsprung, KMG Klagenfurt Mobil, pdcp/SURAAA, Stadt Klagenfurt, Tech Meets Legal (FFG-gefördert).

**Die Frage:** FlipFlop (AIT) sagt per KI-Modell voraus, welche Personen bei einem On-Demand-Angebot (DRT, bedarfsgesteuerter Ridepooling-Verkehr) vom Auto/ÖV/Rad/Fuß umsteigen würden. Ist diese prognostizierte Nachfrage realistisch — und lässt sie sich mit einer Fahrzeugflotte überhaupt sinnvoll bedienen?

**Die Methode:** Das [FleetPy](https://github.com/TUM-VT/FleetPy)-Simulationsframework (TUM) dient als **unabhängiges Prüfinstrument** in drei Dimensionen: räumliche und mengenmäßige Plausibilität der Prognose gegenüber echten KMG/MOIA-Fahrten, betriebliche Umsetzbarkeit (Flottenbedarf) und innere Konsistenz — liefert eine realistische Flotte die Bedienqualität, die FlipFlop bei der Prognose vorausgesetzt hat? Ob die prognostizierten Personen tatsächlich umsteigen, kann nur der reale Betrieb zeigen; die Simulation prüft die Voraussetzungen dafür.

## Ergebnisse (Kurzfassung)

| Prüfung | Befund | Was sich daraus ableiten lässt |
|---|---|---|
| **Räumlich** — Entsteht die prognostizierte Nachfrage dort, wo heute echte Fahrten stattfinden? | Die Verteilung der prognostizierten Fahrtstarts über 8 Zonen stimmt mit den echten KMG/MOIA-Fahrten weitgehend überein (Korrelation 0,86). Größte Abweichung im Stadtzentrum (Zone 4: 39 % vs. 24 %). | Das Modell bildet die räumliche Struktur der Nachfrage richtig ab. Die Zentrumsabweichung ist der eine Punkt, der mit AIT zu klären ist. |
| **Mengenmäßig** — Ist die prognostizierte Menge plausibel? | FlipFlop prognostiziert rund **2.600 DRT-Wege pro Tag** im Bediengebiet; der heutige MOIA-Betrieb realisiert **100–260 Fahrten pro Tag**. | Die Prognose beschreibt das Potenzial eines flächendeckenden Angebots zum ÖV-Tarif, nicht den heutigen Betrieb. Dass sie deutlich über der heute realisierten Nachfrage liegt, ist bei einem kleinen bestehenden Angebot zu erwarten; läge sie darunter, wäre das Modell unplausibel. |
| **Operativ** — Welche Flotte setzt die Prognose voraus? | Die heutige echte Nachfrage wird mit **15–20 Fahrzeugen** zu über 90 % bedient. Die prognostizierte Nachfrage erreicht bei der vom Modell unterstellten Bedienqualität (Wartezeit ≤ ca. 6 min) 90 % erst mit **rund 150 Fahrzeugen**; mit 40 Fahrzeugen werden 54 % bedient. Bei gleicher Auslastung je Fahrzeug ist die prognostizierte Nachfrage besser bündelbar als die heutige. | Die Prognose gilt nur zusammen mit einer entsprechend großen Flotte. Mit einer realistischen Flotte bekommt ein Teil der prognostizierten Umsteiger nicht die unterstellte Qualität und steigt im Modell nicht um — die tatsächlich erreichbare Nachfrage liegt also unter der Prognose. Wie weit darunter, ergibt eine Rückkopplung der erreichbaren Bedienqualität in das FlipFlop-Modell (nächster Schritt mit AIT). |

**Kurz:** Die Prognose ist räumlich richtig, mengenmäßig als Potenzial zu lesen und betrieblich gut bündelbar. Für die Dimensionierung eines realen Angebots sind Flottengröße und Nachfrage gemeinsam zu bestimmen; die simulierten Kennzahlen (Flotte, Bedienungsgrad, Wartezeiten je Szenario) liefern dafür die Grundlage. Annahmen: Bedienqualität aus der AIT-Modelldokumentation abgeleitet (Zugang = 30 % der ÖV-Zugangszeit), Bediengebiet = Gebiet der echten Fahrten, Flotte und Betriebszeitraum des MOIA-Betriebs lagen nicht vor.

Die 8 Vergleichszonen wurden per Clustering direkt aus den echten MOIA-Fahrten gebildet (keine Verwaltungsgrenzen). Zone 4 ist das Stadtzentrum — dort weicht die Prognose am stärksten ab (39 % vs. 24 % der Fahrtstarts):

![FlipFlop vs. MOIA: Anteil der Fahrtstarts je Zone](studies/flipflop_drt_integration_pilot/results/flipflop_vs_moia_zone_map.png)

Die geringe Umsteigequote (ÖV-Anteil im Bediengebiet 11,6 % → 12,9 % im DRT-Szenario zum ÖV-Tarif) deckt sich mit der von AIT selbst beobachteten hohen Kosten- und geringen Zeitsensitivität des Wahlmodells.

## 📌 Einstieg

0. **Einseiter für den Endbericht:** [FlipFlop_FleetPy_Kurzbericht_2026-11-14.docx](studies/flipflop_drt_integration_pilot/FlipFlop_FleetPy_Kurzbericht_2026-11-14.docx)
1. **Konsistenzprüfung (operativ):** [`flipflop_consistency_test.ipynb`](studies/flipflop_drt_integration_pilot/analysis/flipflop_consistency_test.ipynb) — implizite MOIA-Flotte, Flottenbedarf der FlipFlop-Nachfrage, Verhalten bei gleicher Last
2. **Präsentationsfassung (kurz, alle drei Prüfungen):** [`consortium_presentation_flipflop_validation.ipynb`](studies/flipflop_drt_integration_pilot/analysis/consortium_presentation_flipflop_validation.ipynb)
3. **Räumliche und mengenmäßige Prüfung im Detail:** [`flipflop_demand_model_validity.ipynb`](studies/flipflop_drt_integration_pilot/analysis/flipflop_demand_model_validity.ipynb)
4. **Methodik, Skripte, Reproduktion, offene Punkte:** [`studies/flipflop_drt_integration_pilot/README.md`](studies/flipflop_drt_integration_pilot/README.md)

## Setup

```bash
git clone https://github.com/Createdd/fleet_hypothesistests.git
cd fleet_hypothesistests
conda env create -f environment.yml
conda activate fleetpy
(cd src/routing/cpp_router && python setup.py build_ext --inplace)   # C++-Router, einmalig; von den Simulationen benötigt
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
- **Netzwerkdaten:** Graphenintegrations-Plattform (GIP, `data/gip_network_ogd.gpkg`) für die Konsistenzprüfung; OpenStreetMap für Karten und die frühere 8-Sitzer-Studie
- **Algorithmus:** Alonso-Mora et al. (2017), PNAS 114(3): 462-467
- **Framework:** [FleetPy](https://github.com/TUM-VT/FleetPy) (TUM München)

## Lizenz
Dieses Projekt verwendet das FleetPy-Framework unter dessen Lizenz.
© Technische Universität München, Lehrstuhl für Verkehrstechnik

---

**Repository:** [github.com/Createdd/fleet_hypothesistests](https://github.com/Createdd/fleet_hypothesistests)
**Hinweis:** Diese Dokumentation wurde mithilfe von KI-Tools erstellt und unterstützt.
