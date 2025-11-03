# UC3: Barrierefreiheit – Rollstuhl und Kinderwagen-Nutzer

## Fragestellung

Personen mit Kindern/Kinderwagen und mobilitätseingeschränkte Personen (Rollstuhl) benötigen größere, barrierefreie Fahrzeuge. Welche Flottenzusammensetzung gewährleistet eine ausreichende Servicerate für diese Nutzergruppe während der Nachfragespitzen, ohne die Kosten unverhältnismäßig zu erhöhen?

---

## Simulation: Abbildung von Barrierefreiheit

### **Annahmen und Modellierung**

#### **1. Fahrzeugtypen**

Wir definieren zwei Fahrzeugtypen:

| Fahrzeugtyp | Kapazität | Fixkosten/Tag | Kosten/km | Besonderheit |
|-------------|-----------|---------------|-----------|--------------|
| **Standard (4 Sitze)** | 4 Passagiere | 20 € | 0,25 € | Normale PKW/Kleinbusse |
| **Gelenkbus (8 Sitze)** | 8 Passagiere | 35 € | 0,35 € | Barrierefreier Zugang, Rollstuhl-/Kinderwagenplatz |

#### **2. Nutzer mit besonderen Bedürfnissen**

- **Annahme**: **15% der Nachfrage** benötigen barrierefreie Fahrzeuge (Rollstuhl, Kinderwagen)
- **Modellierung**: Diese Nutzer belegen **2 Sitzplätze** statt 1 (repräsentiert Platzbedarf für Rollstuhl/Kinderwagen)
- **Einschränkung**: FleetPy unterstützt **keine explizite Anforderung "nur Gelenkbus"**. Daher nutzen wir die **erhöhte Kapazitätsnutzung** als Proxy.

#### **3. Boarding-Zeit**

- **Standard-Fahrzeug**: 30 Sekunden Einstiegszeit
- **Gelenkbus**: 45 Sekunden (längere Boarding-Zeit durch Rollstuhlrampe/Kinderwagen-Handling)

---

## Szenarien

| Szenario | Flottenzusammensetzung | Standard-Fzg. | Gelenkbusse | Anteil Gelenkbusse | Erwartete Servicerate |
|----------|------------------------|---------------|-------------|--------------------|-----------------------|
| **baseline** | Nur Standard | 20 | 0 | 0% | Niedrig für Rollstuhl/Kinderwagen |
| **mixed_20** | Gemischte Flotte | 16 | 4 | 20% | Moderat |
| **mixed_30** | Gemischte Flotte | 14 | 6 | 30% | Gut |
| **mixed_50** | Gemischte Flotte | 10 | 10 | 50% | Optimal, aber teuer |

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

## Erwartete Ergebnisse (Hypothesen)

1. **Baseline (0% Gelenkbusse)**:
   - Servicerate für Nutzer mit Bedarf: **<50%** (viele Anfragen können nicht bedient werden, da Fahrzeuge voll sind)
   - Gesamtservicerate: **~70%** (Standard-Nutzer werden priorisiert)

2. **mixed_20 (20% Gelenkbusse)**:
   - Servicerate für Nutzer mit Bedarf: **~65-75%**
   - Gesamtservicerate: **~75-80%**

3. **mixed_30 (30% Gelenkbusse)**:
   - Servicerate für Nutzer mit Bedarf: **~80-85%**
   - Gesamtservicerate: **~85-90%**
   - **Empfohlenes Minimum** für inklusiven Service

4. **mixed_50 (50% Gelenkbusse)**:
   - Servicerate für Nutzer mit Bedarf: **>90%**
   - Gesamtservicerate: **~95%**
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
python run_uc3_accessibility.py
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

**Ich kann KEINE echten Quellen für folgende Annahmen liefern:**
1. **15% Anteil Nutzer mit Barrierefreiheitsbedarf** – Schätzwert, keine Klagenfurt-spezifischen Daten
2. **Kostenunterschiede Standard vs. Gelenkbus** – Plausible Annahmen, keine realen CAPEX/OPEX-Daten
3. **Platzbedarf = 2 Sitzplätze** – Vereinfachung; echte Rollstühle/Kinderwagen variieren

**Diese Simulation dient der Sensitivitätsanalyse**, nicht der exakten Vorhersage. Für operative Entscheidungen sollten echte Nachfragedaten und Kosten aus Klagenfurt verwendet werden.

---

## Nächste Schritte (optional)

1. **Empirische Validierung**: Echte Daten zu Rollstuhl-/Kinderwagennutzung in Klagenfurt erheben
2. **Reservierungsmodul testen**: Vorabplanung für Nutzer mit Bedarf
3. **Dynamische Flottensteuerung**: Tageszeitabhängige Anpassung der Flottenzusammensetzung
4. **Kostenoptimierung**: Detaillierte TCO-Analyse (Total Cost of Ownership) für verschiedene Fahrzeugtypen

---

**Hinweis:** Diese Dokumentation wurde mithilfe von KI-Tools erstellt und unterstützt.
