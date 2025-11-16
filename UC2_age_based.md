## UC2: Altersbasierte digitale Kompetenz und Begleitmaßnahmen

Fragestellung: Ältere Personen haben geringere digitale Kompetenz. Welche Begleitmaßnahmen helfen, damit sie von einem On-Demand-Algorithmus profitieren?

## Simulation: Abbildung der digitalen Kompetenz

Digitale Kompetenz wird als Interaktion mit Angeboten und Bedienbarkeit modelliert. Wir nutzen vorhandene Parameter und Traveller-Modelle:

- Entscheidungsfenster: user_max_decision_time (G_AR_MAX_DEC_T)
  - Kürzeres Fenster → höhere Wahrscheinlichkeit für „keine Antwort“ (Auto-Decline)

- Angebotsakzeptanz vs. Wartezeit: WaitingTimeSensitiveLinearDeclineRequest
  - user_max_wait_time (G_AR_MAX_WT)
  - user_max_wait_time_2 (G_AR_MAX_WT_2)
  - Akzeptanz nimmt linear zwischen beiden Grenzen ab

- Mobilität am Bordstein: walking_speed (G_WALKING_SPEED), max_walking_dist (G_MAX_WALKING_DIST)
  - Niedrigere Gehgeschwindigkeit/geringere Distanz → realistischere Erreichbarkeit

- Boarding-/Assistenzzeit: op_const_boarding_time (G_OP_CONST_BT)
  - Längere konstante Boarding-Zeit repräsentiert Unterstützungsbedarf

Optional erweiterbar:
- Preis-/Nutzensensitivität (G_AR_PRICE_F, G_MC_VOT) für realistischere Wahlverhalten
- Reservierungen/Telefonvermittlung (ReservationModule / BrokerDecisionRequest) für assistierte Buchung

## Unterstützungsmaßnahmen → Parametrisierung

1) Keine Unterstützung (Baseline)
- Kürzeres Entscheidungsfenster (z. B. 30–60 s)
- Enge Wartezeit-Toleranz (z. B. G_AR_MAX_WT=180 s, G_AR_MAX_WT_2=300 s)
- Längere Boarding-Zeit (z. B. 45–60 s)
- Reduzierte walking_speed (z. B. 0.9–1.1 m/s) und geringe max_walking_dist

2) Telefon-Support
- user_max_decision_time deutlich erhöhen (z. B. 180–300 s)
- Optional: Boarding-Zeit leicht reduzieren (Assistenz am Telefon koordiniert)

3) Vereinfachte App (UX)
- Erhöhtes Akzeptanzfenster: G_AR_MAX_WT↑, G_AR_MAX_WT_2↑ (klare Kommunikation steigert Toleranz)
- Optionale Tooltips/Hinweise simuliert durch geringere Abbruchwahrscheinlichkeit (implizit über Akzeptanzkurve)

4) Vollständige Unterstützung
- Kombination aus 2) + 3) + reduzierte Boarding-Zeit (z. B. 30 s) durch Vor-Ort-Hilfe
- Optional: BrokerDecisionRequest (Operator/Broker wählt bestes Angebot)

## Szenariodesign (Beispielwerte)

| Szenario | rq_type | user_max_decision_time | user_max_wait_time | user_max_wait_time_2 | walking_speed | max_walking_dist | op_const_boarding_time |
|---|---|---:|---:|---:|---:|---:|---:|
| baseline | WaitingTimeSensitiveLinearDeclineRequest | 60 | 180 | 300 | 1.0 | 200 | 60 |
| phone_support | WaitingTimeSensitiveLinearDeclineRequest | 240 | 180 | 300 | 1.0 | 200 | 50 |
| simple_ui | WaitingTimeSensitiveLinearDeclineRequest | 120 | 240 | 420 | 1.0 | 200 | 50 |
| full_support | WaitingTimeSensitiveLinearDeclineRequest | 300 | 300 | 480 | 1.0 | 250 | 30 |

**Flottenkonfiguration:** 20 Fahrzeuge mit je **8 Sitzplätzen** (Gesamtkapazität: 160 Sitzplätze)

**Wichtiger Hinweis zur Fahrzeugkapazität:** Die 8-Sitzer (statt 4-Sitzer in älteren Studien) bedeuten NICHT automatisch, dass man mit weniger Fahrzeugen auskommt. Im On-Demand-Ridepooling ist die **räumliche Abdeckung** wichtiger als die absolute Sitzplatzanzahl. 20 Fahrzeuge sind nötig, um alle 12 Zonen gut abzudecken - unabhängig ob 4 oder 8 Sitze pro Fahrzeug. Der Vorteil liegt in den geringeren Kosten pro Sitzplatz und der Flexibilität für gelegentliches Pooling.

Hinweis: Die exakt sinnvollen Werte hängen vom Kontext (Stadt, Demografie, Hardware) ab. Obige Werte sind konservative Defaults für Sensitivitätsanalysen.

## Evaluationsmetriken (Ältere Zielgruppe)

- Servicerate [%] (Anteil bedienter Anfragen)
- Ø Wartezeit [min] und Median; 90. Perzentil
- Anteil mit ≤5 min Wartezeit
- Fahrzeugauslastung [%] (Systemperspektive)
- Abbruch-/Nicht-Antwort-Quote (implizit über latest_decision_time, falls verfügbar)
- Erreichbarkeit: Anteil, der die max_walking_dist überschreitet (falls Fußweg modelliert)

## Wie ausführen?

1) Setze in der Konstantkonfiguration rq_type = WaitingTimeSensitiveLinearDeclineRequest und aktiviere die oben genannten Parameter (G_AR_MAX_WT, G_AR_MAX_WT_2, G_AR_MAX_DEC_T, G_WALKING_SPEED, G_MAX_WALKING_DIST, G_OP_CONST_BT).

2) Erzeuge ein Szenario-CSV (z. B. `uc2_scenarios.csv`) mit Zeilen für baseline/phone_support/simple_ui/full_support und den jeweiligen Werten.

3) Starte die Simulationen mit `run_scenarios(constant_config, uc2_scenarios.csv, ...)` oder einem kleinen Runner (analog zu H1/H2).

Falls dein existierendes Studien-Setup YAML nutzt (wie H1/H2), kannst du die Parameter als Szenariovariablen in die CSV legen und die Konstanten in der YAML belassen. Wichtig ist, dass `rq_type` auf `WaitingTimeSensitiveLinearDeclineRequest` gestellt wird.

## Erklärung/Interpretation

- Baseline zeigt typischerweise niedrigere Serviceraten und höhere Abbrüche (kurzes Entscheidungsfenster, geringe Akzeptanz)
- Telefon-Support adressiert „digitale Hürde“ primär über mehr Entscheidungszeit → weniger Auto-Declines
- Vereinfachte App verschiebt Akzeptanzkurve → höhere Toleranz für moderate Wartezeiten, steigert effektive Servicerate
- Vollständige Unterstützung kombiniert Effekte und senkt zusätzlich Boarding-Reibung → beste Nutzbarkeit für die Zielgruppe

## Nächste Schritte (optional)

- Metrik „Fairness": Gap zwischen älteren vs. gesamten Nutzern (Servicerate, Wartezeit)
- Reservierungslogik testen: Vorbestellungen/Hotline als Alternative zur Sofortbuchung
- Preis-/Tarifkommunikation: Preis-Sensitivität der Zielgruppe variieren

---

**Hinweis:** Diese Dokumentation wurde mithilfe von KI-Tools erstellt und unterstützt.