## UC2: Altersbasierte digitale Kompetenz und Nutzungsverhalten

**Erweiterte Fragestellung:**
1. **Ältere Nutzer (65+)**: Welche Begleitmaßnahmen helfen bei geringer digitaler Kompetenz?
2. **Schüler (15-20 Jahre)**: Welche Anreize steigern die Nutzung trotz hoher digitaler Kompetenz?
3. **Studenten (21-30 Jahre)**: Wie unterscheidet sich das Nutzungsverhalten von Schülern?

---

## Teil A: Ältere Zielgruppe (65+ Jahre)

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

---

## Teil B: Junge Zielgruppen (15-20 und 21-30 Jahre)

### Forschungsfrage

**Zentrale Beobachtung:** Junge Menschen (15-30 Jahre) haben **hohe digitale Kompetenz**, nutzen On-Demand-Ridepooling aber **unterproportional**.

**Fragen:**
1. **Schüler (15-20 Jahre)**: Wie unterscheidet sich das Nutzungsverhalten von älteren Nutzern?
2. **Studenten (21-30 Jahre)**: Unterscheidet sich das Nutzungsverhalten von Schülern?

### Hypothesen

**H1 - Unterrepräsentation junger Nutzer:**
- Digital-affine Gruppen brauchen **keine** technische Unterstützung
- **Frage**: Wie unterscheidet sich das Nutzungsverhalten von jungen vs. älteren Nutzern?

**H2 - Unterschiede Schüler (15-20) vs. Studenten (21-30):**
- **Schüler**: Geringere Mobilität (1.4 m/s, 400m Laufdistanz)
- **Studenten**: Höhere Mobilität (1.5 m/s, 500m Laufdistanz)
- **Erwartung**: Studenten nutzen Service flexibler als Schüler

**H3 - 24/7-Betrieb für Universitätsviertel:**
- **Zielgruppe**: Studenten am Lakeside Park Klagenfurt (~2.500 Studierende)
- **Nachfrageprofil**: Morgen-Peak (7-9 Uhr), Mittag (12-14 Uhr), Abend (17-19 Uhr)
- **Frage**: Unterscheidet sich das Nutzungsverhalten junger Nutzer vom Gesamtdurchschnitt?

### Simulation: Abbildung junger Nutzer

**Parameter-Philosophie:**
- **Hohe digitale Kompetenz** → Sehr kurze Entscheidungszeit (15-30s statt 60-300s bei Älteren)
- **Schnelle Mobilität** → Höhere Gehgeschwindigkeit (1.4-1.5 m/s), größere Laufdistanz (400-600m)
- **Schnelles Boarding** → Kurze Einstiegszeit (12-20s statt 30-60s)
- **Flexible Wartezeit-Toleranz** → Je nach Anreizen: 300-600s (5-10 min)

**Unterschied zu älteren Nutzern:**
| Parameter | Ältere (65+) | Schüler (15-20) | Studenten (21-30) |
|-----------|--------------|-----------------|-------------------|
| Entscheidungszeit | 60-300s | 15-25s | 20-30s |
| Wartezeit-Toleranz | 180-480s | 300-480s | 360-600s |
| Gehgeschwindigkeit | 0.9-1.1 m/s | 1.4 m/s | 1.5 m/s |
| Max. Laufdistanz | 200-250m | 400m | 500m |
| Boarding-Zeit | 30-60s | 15s | 12s |

### Szenarien für junge Nutzer

#### Schüler (15-20 Jahre)

**Szenario: students_15_20**
- Hohe digitale Kompetenz (sehr kurze Entscheidungszeit: 20s)
- Schnelle Mobilität (1.4 m/s, 400m Laufdistanz)
- Schnelles Boarding (15s)
- Moderate Wartezeit-Toleranz (300-420s)

**Parameter:**
| Szenario | user_max_decision_time | user_max_wait_time | user_max_wait_time_2 | walking_speed | max_walking_dist | op_const_boarding_time |
|----------|------------------------|---------------------|----------------------|---------------|------------------|------------------------|
| students_15_20 | 20 | 300 | 420 | 1.4 | 400 | 15 |

#### Studenten (21-30 Jahre)

**Szenario: students_21_30**
- Sehr hohe digitale Kompetenz (kurze Entscheidungszeit: 25s)
- Sehr schnelle Mobilität (1.5 m/s, 500m Laufdistanz)
- Sehr schnelles Boarding (12s)
- Höhere Wartezeit-Toleranz (360-480s)

**Parameter:**
| Szenario | user_max_decision_time | user_max_wait_time | user_max_wait_time_2 | walking_speed | max_walking_dist | op_const_boarding_time |
|----------|------------------------|---------------------|----------------------|---------------|------------------|------------------------|
| students_21_30 | 25 | 360 | 480 | 1.5 | 500 | 12 |

### 24/7-Betriebsprofil (Studenten/Schüler kombiniert)

**Nachfrageprofil über den Tag:**
| Zeitfenster | Uhrzeit | Zielgruppe | Erwartete Nachfrage |
|-------------|---------|------------|---------------------|
| **Morning Peak** | 7-9 Uhr | Schüler + Studenten | 150 Anfragen |
| **Midday** | 12-14 Uhr | Schüler (Mensa) | 80 Anfragen |
| **Evening Peak** | 17-19 Uhr | Studenten Heimfahrt | 120 Anfragen |

**Fokus dieser Studie:** Morgen-Peak (7-9 Uhr) - Vergleich mit H1

### Evaluationsmetriken (junge Zielgruppen)

**Vergleich der Altersgruppen:**
- Servicerate [%] (nach Altersgruppe)
- Ø Wartezeit [min] und Median; 90. Perzentil
- Fahrzeugauslastung [%]
- Digitale Kompetenz-Indikatoren (Entscheidungszeit, Boarding-Zeit)

### Erwartete Ergebnisse

**Schüler (15-20 Jahre):**
- Hohe digitale Kompetenz (schnelle Entscheidung, schnelles Boarding)
- Schnelle Mobilität (höhere Gehgeschwindigkeit, größere Laufdistanz)
- Vergleich mit älteren Nutzern zeigt Unterschiede in Nutzungsverhalten

**Studenten (21-30 Jahre):**
- Sehr hohe digitale Kompetenz (noch schneller als Schüler)
- Sehr hohe Mobilität (längste Laufdistanzen)
- Höchste Wartezeit-Toleranz unter allen Altersgruppen

**Unterschied 15-20 vs. 21-30:**
- **Schüler**: Etwas langsamer, kürzere Laufdistanzen
- **Studenten**: Mobilste Gruppe, höchste Flexibilität

### Interpretation und Handlungsempfehlungen

**Vergleich der Altersgruppen:**
- **Ältere (65+)**: Niedrige digitale Kompetenz → Unterstützungsmaßnahmen nötig
- **Schüler (15-20)**: Hohe digitale Kompetenz, moderate Mobilität
- **Studenten (21-30)**: Höchste digitale Kompetenz, höchste Mobilität

---

## Teil C: Nächste Schritte (optional)

**Erweiterte Analysen:**
- Metrik „Fairness": Gap zwischen älteren (65+) vs. Schülern (15-20) vs. Studenten (21-30)
- Vergleich der drei Altersgruppen in Bezug auf Servicerate und Wartezeiten
- Empirische Validierung der Parameter-Annahmen

---

**Hinweis:** Diese Dokumentation wurde mithilfe von KI-Tools erstellt und unterstützt.