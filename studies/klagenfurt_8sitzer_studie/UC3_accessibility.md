# UC3: Barrierefreiheit – Rollstuhl und Kinderwagen-Nutzer

## Fragestellung

Personen mit Kindern/Kinderwagen und mobilitätseingeschränkte Personen (Rollstuhl) benötigen größere, barrierefreie Fahrzeuge. Welche Flottenzusammensetzung gewährleistet eine ausreichende Servicerate für diese Nutzergruppe während der Nachfragespitzen, ohne die Kosten unverhältnismäßig zu erhöhen?

---

## Simulation: Abbildung von Barrierefreiheit

### **Annahmen und Modellierung**

#### **1. Fahrzeugtypen**

Wir definieren zwei Fahrzeugtypen:

| Fahrzeugtyp | Kapazität | Fixkosten/Tag | Kosten/km | Boarding-Zeit | Besonderheit |
|-------------|-----------|---------------|-----------|---------------|--------------|
| **Standard (8 Sitze)** | 8 Passagiere | 20 € | 0,25 € | 30s | Normale Kleinbusse |
| **Barrierefreier Bus (12 Sitze)** | 12 Passagiere | 35 € | 0,35 € | 60s | Barrierefreier Zugang, Rollstuhl-/Kinderwagenplatz |#### **2. Nutzer mit besonderen Bedürfnissen**

- **Annahme**: **15% der Nachfrage** benötigen barrierefreie Fahrzeuge (Rollstuhl, Kinderwagen)
- **Modellierung**: Diese Nutzer belegen **2 Sitzplätze** statt 1 (repräsentiert Platzbedarf für Rollstuhl/Kinderwagen)
- **Einschränkung**: FleetPy unterstützt **keine explizite Anforderung "nur Gelenkbus"**. Daher nutzen wir die **erhöhte Kapazitätsnutzung** als Proxy.

#### **3. Boarding-Zeit**

- **Standard-Fahrzeug**: 30 Sekunden Einstiegszeit
- **Gelenkbus**: 45 Sekunden (längere Boarding-Zeit durch Rollstuhlrampe/Kinderwagen-Handling)

---

## Szenarien

| Szenario | Standard (8 Sitze) | Barrierefrei (12 Sitze) | Anteil Barrierefrei | Gesamtkapazität | Erwartete Servicerate |
|----------|--------------------|-----------------------|---------------------|-----------------|----------------------|
| **baseline** | 20 | 0 | 0% | 160 Sitze | Niedrig für Rollstuhl/Kinderwagen |
| **mixed_20** | 16 | 4 | 20% | 176 Sitze | Moderat |
| **mixed_30** | 14 | 6 | 30% | 184 Sitze | Gut (empfohlen) |
| **mixed_50** | 10 | 10 | 50% | 200 Sitze | Optimal, aber teuer |

**Parameter-Konstanten:**
- Simulationszeitraum: 7:00–9:00 Uhr (Morgenspitze)
- 100 Mobilitätsanfragen (davon ~15 mit Barrierefreiheitsbedarf)
- Maximale Wartezeit: 8 Minuten
- Maximaler Umwegfaktor: 40%
- Reoptimierungsintervall: 30 Sekunden

---

## Evaluationsmetriken

### **1. Servicequalität**
- **Servicerate [%]**: Anteil bedienter Anfragen (gesamt und für Nutzer mit Barrierefreiheitsbedarf)
- **Ø Wartezeit [min]**: Durchschnittliche Wartezeit (gesamt und für Nutzer mit Bedarf)
- **Median/90%-Perzentil Wartezeit**: Verteilung der Wartezeiten

### **2. Systemeffizienz**
- **Fahrzeugauslastung [%]**: Wie gut werden die Fahrzeuge genutzt?
- **Kosten/bediente Anfrage**: Verhältnis von Gesamtkosten (Fix + variabel) zu bedienten Nutzern

### **3. Trade-off Analyse**
- **Baseline**: Geringe Kosten, aber schlechte Servicerate für Nutzer mit Bedarf
- **mixed_50**: Hohe Servicerate, aber höhere Fixkosten durch mehr Gelenkbusse
- **Optimum**: mixed_30 als Balance zwischen Kosten und Servicequalität?

---

## Kritische Erkenntnis: Kapazität vs. Räumliche Verfügbarkeit

**Wichtiger Befund aus H2-Studie:**
Trotz Verdopplung der Fahrzeugkapazität (4→8 Sitze) bleiben Serviceraten bei gleicher Fahrzeuganzahl identisch. **Grund:** Im On-Demand-Ridepooling ist **räumliche Verfügbarkeit wichtiger als absolute Sitzplatzanzahl**.

**Konsequenz für UC3 (Barrierefreiheit):**
- Nicht nur wichtig: "Genug Sitze für Rollstuhl/Kinderwagen insgesamt"
- **Kritisch:** "Sind barrierefreie Fahrzeuge räumlich verteilt verfügbar?"
- Ein barrierefreies 12-Sitzer-Fahrzeug in Zone A hilft nicht bei Anfrage in Zone F
- → **Verteilung** der barrierefreien Fahrzeuge über Zonen ist entscheidend, nicht nur deren Anzahl

**Implikation für Szenarien:**
- **mixed_30 (30% barrierefrei = 6 Fahrzeuge)**: Besser als mixed_20, weil mehr Zonen abgedeckt werden können
- **mixed_50 (50% barrierefrei = 10 Fahrzeuge)**: Optimal für räumliche Verfügbarkeit, aber teurer

---

## Zentrale Erkenntnis: Räumliche Verteilung wichtiger als Gesamtkapazität

**Kritische Beobachtung:** Die fast verdoppelte Gesamtkapazität (160-200 statt 80-120 Sitze) führt NICHT automatisch zu besserer Servicerate für Nutzer mit Barrierefreiheitsbedarf!

### Warum ist räumliche Verfügbarkeit entscheidend?

**Im Barrierefreiheits-Kontext gilt:**
- Ein barrierefreier 12-Sitzer in Zone A hilft Rollstuhlnutzer in Zone F nicht
- Entscheidend ist: **Sind genug barrierefreie Fahrzeuge VERTEILT** (nicht nur: gibt es genug Sitze INSGESAMT)
- 10% barrierefreie Fahrzeuge bedeutet: nur ~2 Fahrzeuge für 12 Zonen → viele Zonen ohne barrierefreies Fahrzeug

**Konsequenz für UC3-Szenarien:**

| Szenario | Barrierefreie Fzg. | Durchschn. pro Zone | Verfügbarkeit |
|----------|-------------------|-------------------|---------------|
| baseline | 0 | 0,0 | ❌ Keine |
| mixed_20 | 4 | 0,3 | ⚠️ Sehr lückenhaft |
| mixed_30 | 6 | 0,5 | ⚠️ Lückenhaft |
| mixed_50 | 10 | 0,8 | ✅ Akzeptabel |

**Warum 30% empfohlen (nicht 20%)?**
- 4 barrierefreie Fahrzeuge auf 12 Zonen = zu geringe räumliche Abdeckung
- 6 barrierefreie Fahrzeuge = bessere Chance, dass eins in der Nähe ist
- Zusätzlich: Zeitliche Verfügbarkeit (Fahrzeug könnte bereits unterwegs sein)

**Der Vorteil der 12-Sitzer liegt woanders:**
- ✅ Wenn ein barrierefreies Fahrzeug verfügbar ist, kann es mehr Nutzer aufnehmen
- ✅ Geringere Kosten pro Sitzplatz im Vergleich zu kleineren Fahrzeugen
- ✅ Flexibilität für simultane Anfragen in gleicher Zone

**Kein Vorteil bei:**
- ❌ Reduktion der Anzahl barrierefreier Fahrzeuge (räumliche Abdeckung bleibt kritisch)
- ❌ Garantie, dass Nutzer in jeder Zone Zugang haben

## Erwartete Ergebnisse (Hypothesen)

**Wichtig:** Mit der neuen Konfiguration (8/12 Sitze statt 4/8) hat sich die Gesamtkapazität fast verdoppelt, aber die räumliche Verteilung bleibt der entscheidende Faktor:

1. **Baseline (0% Barrierefreie, 160 Sitzplätze)**:
   - Gesamtkapazität deutlich höher als mit 4-Sitzern (160 statt 80 Sitze)
   - Servicerate für Nutzer mit Bedarf: **Niedrig** (keine barrierefreien Fahrzeuge)
   - Gesamtservicerate: **Hoch** (durch große Gesamtkapazität)

2. **mixed_20 (20% Barrierefreie, 176 Sitzplätze)**:
   - 4 Fahrzeuge mit je 12 Sitzen für Barrierefreiheit
   - Servicerate für Nutzer mit Bedarf: **Moderat verbessert**
   - Gesamtservicerate: **Sehr gut** (durch kombinierte Kapazität)

3. **mixed_30 (30% Barrierefreie, 184 Sitzplätze)**:
   - 6 Fahrzeuge mit je 12 Sitzen für Barrierefreiheit
   - **Empfohlenes Minimum** für inklusiven Service
   - Balance zwischen Kosten und Barrierefreiheit

4. **mixed_50 (50% Barrierefreie, 200 Sitzplätze)**:
   - 10 Fahrzeuge mit je 12 Sitzen für Barrierefreiheit
   - Höchste Kapazität (200 Sitze)
   - Aber: **Kosten steigen um ~30-40%** gegenüber Baseline

---

## Wie ausführen?

### **Voraussetzungen**
- FleetPy-Conda-Environment aktiviert (`conda activate fleetpy`)
- Alle Dependencies installiert (siehe `environment.yml`)

### **1. Simulation starten**

```bash
cd /Users/danieldeutsch/Desktop/code_projects/FleetPy
conda activate fleetpy
python studies/klagenfurt_8sitzer_studie/run_uc3_accessibility.py
```

**Was passiert:**
- FleetPy simuliert alle 4 Szenarien nacheinander
- Ergebnisse werden in `studies/uc3_accessibility/studies/uc3_study/results/` gespeichert
- Jedes Szenario erzeugt:
  - `standard_eval.csv` (Hauptmetriken)
  - `1_user-stats.csv` (Nutzerstatistiken)
  - `2-0_op-stats.csv` (Operator-/Fahrzeugstatistiken)

**Erwartete Laufzeit:** ~5-10 Minuten (je nach CPU)

### **2. Ergebnisse analysieren**

Nach der Simulation:

```bash
jupyter notebook studies/uc3_accessibility/studies/uc3_study/analysis/uc3_analysis.ipynb
```

Das Notebook:
- Lädt alle Ergebnisse aus den 4 Szenarien
- Berechnet Serviceraten, Wartezeiten, Kosten
- Erstellt Vergleichsdiagramme (Plotly)
- Liefert Handlungsempfehlungen

---

## Interpretation und Handlungsempfehlungen

### **Kritische Schwellenwerte**

1. **Unter 20% Gelenkbusse**:
   - Unzureichende Abdeckung für Nutzer mit Barrierefreiheitsbedarf
   - Viele Anfragen werden abgelehnt oder erleben lange Wartezeiten

2. **30% Gelenkbusse (empfohlen)**:
   - Guter Kompromiss zwischen Kosten und Servicequalität
   - ~85% Servicerate für Nutzer mit Bedarf
   - Vertretbare Kostensteigerung (~15-20% gegenüber Baseline)

3. **Über 50% Gelenkbusse**:
   - Nur bei sehr hoher Nachfrage nach Barrierefreiheit sinnvoll
   - Kosten steigen überproportional

### **Policy-Implikationen**

- **Inklusionsziel**: Mindestens 30% barrierefreie Fahrzeuge für ÖPNV-Gleichstellung
- **Dynamische Flotte**: In Spitzenzeiten mehr Gelenkbusse einsetzen (falls operativ möglich)
- **Reservierungssystem**: Nutzer mit Bedarf könnten vorab buchen → bessere Ressourcenplanung

---

## Einschränkungen und Unsicherheiten

**Wichtige Annahmen und Einschränkungen:**
1. **15% Anteil Nutzer mit Barrierefreiheitsbedarf** – Schätzwert, keine Klagenfurt-spezifischen Daten
2. **Kostenunterschiede Standard (8 Sitze) vs. Barrierefreier Bus (12 Sitze)** – Plausible Annahmen, keine realen CAPEX/OPEX-Daten
3. **Platzbedarf = 2 Sitzplätze** – Vereinfachung; echte Rollstühle/Kinderwagen variieren
4. **Fahrzeugkapazitäten (8/12 Sitze)** – Aktualisiert von vorherigen 4/8 Sitzen für realistischere Kleinbus-Größen

**Kritische Erkenntnis: Gesamtkapazität vs. Räumliche Verfügbarkeit**

Die verdoppelte Gesamtkapazität (160-200 Sitze statt 80-120) bedeutet NICHT automatisch doppelte Servicerate:
- **Räumliche Verteilung** barrierefreier Fahrzeuge ist kritischer als absolute Sitzplatzanzahl
- Ein 12-Sitzer in Zone A hilft nicht bei Anfrage in Zone F (trotz freier Plätze)
- Bei niedriger Nachfragedichte: Fahrzeuge fahren oft nicht voll ausgelastet
- **Wichtig für UC3**: Anzahl und Verteilung barrierefreier Fahrzeuge (z.B. 6 Fahrzeuge bei mixed_30) bestimmt Barrierefreiheits-Servicerate, nicht nur Gesamtsitzplätze
- **Vorteil größerer Fahrzeuge**: Geringere Kosten pro Sitzplatz; höhere Flexibilität bei Nachfragespitzen

**Diese Simulation dient der Sensitivitätsanalyse**, nicht der exakten Vorhersage. Für operative Entscheidungen sollten echte Nachfragedaten und Kosten aus Klagenfurt verwendet werden.

---

## Nächste Schritte (optional)

1. **Empirische Validierung**: Echte Daten zu Rollstuhl-/Kinderwagennutzung in Klagenfurt erheben
2. **Reservierungsmodul testen**: Vorabplanung für Nutzer mit Bedarf
3. **Dynamische Flottensteuerung**: Tageszeitabhängige Anpassung der Flottenzusammensetzung
4. **Kostenoptimierung**: Detaillierte TCO-Analyse (Total Cost of Ownership) für verschiedene Fahrzeugtypen

---

**Hinweis:** Diese Dokumentation wurde mithilfe von KI-Tools erstellt und unterstützt.
