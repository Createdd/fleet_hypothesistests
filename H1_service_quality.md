# 🎯 Hypothese 1 (H1): Servicequalität-Optimierung# 🎯 Hypothesis 1 (H1): Service Quality Optimization



## Forschungsfrage## Research Question



**Ziel:** Bestimmung der optimalen Flottengröße für maximale Servicequalität bei akzeptabler Kosteneffizienz**Goal:** Determine optimal fleet size for maximum service quality with acceptable cost efficiency



**Testszenarien:****Test Scenarios:**

1. **Szenario 1 - Basisflotte:** 20 Fahrzeuge (minimal wirtschaftlich sinnvolle Flotte)1. **Scenario 1 - Base Fleet:** 20 vehicles (minimum economically viable fleet)

2. **Szenario 2 - Mittlere Flotte:** 30 Fahrzeuge (Balance Servicequalität/Kosten)2. **Scenario 2 - Medium Fleet:** 30 vehicles (balance service quality/cost)

3. **Szenario 3 - Große Flotte:** 40 Fahrzeuge (maximale Kapazität)3. **Scenario 3 - Large Fleet:** 40 vehicles (maximum capacity)



**Hypothese:** Größere Flotten führen zu höheren Serviceraten und kürzeren Wartezeiten, jedoch mit abnehmendem Grenznutzen.**Hypothesis:** Larger fleets lead to higher service rates and shorter wait times, but with diminishing returns.



## Zentrale Ergebnisse## Key Results



### Serviceraten nach Flottengröße### Service Rates by Fleet Size



| Szenario | Flottengröße | Bediente Anfragen | Servicerate | Ø Wartezeit | Gesamtzeit | Fahrzeugauslastung || Scenario | Fleet Size | Served Requests | Service Rate | Avg Wait Time | Total Time | Vehicle Utilization |

|----------|--------------|-------------------|-------------|-------------|-------------|-------------------||----------|------------|-----------------|--------------|---------------|-------------|-------------------|

| **Szenario 1** | 20 Fahrzeuge | 84/100 | **84,0%** | 5,0 min | ~18 min | 100% || **Scenario 1** | 20 vehicles | 84/100 | **84.0%** | 5.0 min | ~18 min | 100% |

| **Szenario 2** | 30 Fahrzeuge | 95/100 | **95,0%** | 4,2 min | ~17 min | 100% || **Scenario 2** | 30 vehicles | 95/100 | **95.0%** | 4.2 min | ~17 min | 100% |

| **Szenario 3** | 40 Fahrzeuge | 98/100 | **98,0%** | 3,6 min | ~16 min | 92,5% || **Scenario 3** | 40 vehicles | 98/100 | **98.0%** | 3.6 min | ~16 min | 92.5% |



**Datenquelle:** Direkte Simulationsergebnisse aus `studies/klagenfurt_h1_spitzenzeiten_case_study/results/`**Data Source:** Direct simulation results from `studies/klagenfurt_h1_spitzenzeiten_case_study/results/`

**Konfidenz:** Hoch (reproduzierbare Simulationsergebnisse)**Confidence:** High (reproducible simulation results)



### Wichtigste Erkenntnisse### Key Findings



- ✅ **Hohe Serviceraten**: 84-98% der Anfragen bedient- ✅ **High Service Rates**: 84-98% of requests served

- ⏱️ **Kurze Wartezeiten**: Durchschnittlich 3,6-5,0 Minuten- ⏱️ **Short Wait Times**: Average 3.6-5.0 minutes

- 🚗 **Hohe Auslastung**: 92-100% der Fahrzeuge aktiv genutzt- 🚗 **High Utilization**: 92-100% of vehicles actively used

- 📊 **Skalierungseffekt**: +50% Flotte (20→30) → +13% Servicerate- 📊 **Scaling Effect**: +50% fleet (20→30) → +13% service rate

- 💰 **Abnehmender Grenznutzen**: +33% Flotte (30→40) → nur +3% Servicerate- 💰 **Diminishing Returns**: +33% fleet (30→40) → only +3% service rate

- 🎯 **Optimum**: 30 Fahrzeuge bieten beste Kosten-Nutzen-Relation- 🎯 **Sweet Spot**: 30 vehicles offer best cost-benefit ratio



### Servicequalität nach Wartezeit### Service Quality by Wait Time



| Flottengröße | ≤3 min | ≤5 min | ≤8 min (Max) || Fleet Size | ≤3 min | ≤5 min | ≤8 min (Max) |

|--------------|--------|---------|--------------||------------|--------|---------|--------------|

| 20 Fahrzeuge | 35,7% | 51,2% | 100% || 20 vehicles | 35.7% | 51.2% | 100% |

| 30 Fahrzeuge | 51,6% | 67,4% | 100% || 30 vehicles | 51.6% | 67.4% | 100% |

| 40 Fahrzeuge | 60,2% | 74,5% | 100% || 40 vehicles | 60.2% | 74.5% | 100% |



## Strategische Empfehlungen## Strategic Recommendations



### 1. Kosteneffizienz priorisiert → 20 Fahrzeuge### 1. Cost-Efficiency Focus → 20 Vehicles

- ✅ 84% Servicerate (akzeptabel für Start-up)- ✅ 84% service rate (acceptable for startup)

- ✅ 100% Fahrzeugauslastung- ✅ 100% vehicle utilization

- ✅ 4,2 Anfragen pro Fahrzeug (höchste Effizienz)- ✅ 4.2 requests per vehicle (highest efficiency)

- ✅ Geringste CAPEX/OPEX- ✅ Lowest CAPEX/OPEX

- ⚠️ 16% unbediente Anfragen (Reputationsrisiko)- ⚠️ 16% unserved requests (reputation risk)



### 2. Balance Kosten/Service → 30 Fahrzeuge ⭐ EMPFOHLEN### 2. Cost/Service Balance → 30 Vehicles ⭐ RECOMMENDED

- ✅ 95% Servicerate (hervorragend)- ✅ 95% service rate (excellent)

- ✅ 100% Fahrzeugauslastung- ✅ 100% vehicle utilization

- ✅ 67% mit ≤5 min Wartezeit- ✅ 67% with ≤5 min wait time

- ✅ 3,2 Anfragen/Fahrzeug (gute Effizienz)- ✅ 3.2 requests/vehicle (good efficiency)

- ✅ Beste Kosten-Nutzen-Relation- ✅ Best cost-benefit ratio

- ✅ Nur 5% unbediente Anfragen (tolerierbar)- ✅ Only 5% unserved requests (tolerable risk)



### 3. Servicequalität priorisiert → 40 Fahrzeuge### 3. Service Quality Focus → 40 Vehicles

- ✅ 98% Servicerate (nahezu vollständig)- ✅ 98% service rate (nearly complete)

- ✅ 3,6 min durchschnittliche Wartezeit (kürzeste)- ✅ 3.6 min average wait time (shortest)

- ✅ 75% mit ≤5 min Wartezeit (Premium-Service)- ✅ 75% with ≤5 min wait time (premium service)

- ✅ Höchste Kundenzufriedenheit- ✅ Highest customer satisfaction

- ⚠️ 92,5% Auslastung (erste Überkapazität)- ⚠️ 92.5% utilization (first overcapacity)

- ⚠️ 2,6 Anfragen/Fahrzeug (geringere Effizienz)- ⚠️ 2.6 requests/vehicle (lower efficiency)

- ⚠️ Höhere Kosten bei minimalem Mehrwert (+3% Service vs. 30 Fzg)- ⚠️ Higher costs with minimal added value (+3% service vs. 30 vehicles)



## Kritische Erfolgsfaktoren## Critical Success Factors



✅ **Technische Machbarkeit bestätigt**✅ **Technical Feasibility Confirmed**

- Ridepooling in Klagenfurt funktioniert mit 84-98% Servicerate- Ridepooling in Klagenfurt works with 84-98% service rate

- Zonenbasierte Optimierung ist kritisch für Erfolg (12 Zonen essentiell)- Zone-based optimization critical for success (12 zones essential)

- Alonso-Mora-Algorithmus bewältigt Morgenspitze effektiv- Alonso-Mora algorithm effectively handles morning peak



💡 **Kritische Erkenntnisse**💡 **Critical Insights**

- **Zonensystem**: 12-Zonen-Struktur essentiell (vs. 1 Zone: 0% Service)- **Zone System**: 12-zone structure essential (vs. 1 zone: 0% service)

- **Zentroiden**: 103 strategische Ein-/Ausstiegspunkte reduzieren Leerfahrten- **Centroids**: 103 strategic pickup points reduce empty trips

- **Reoptimierung**: 30-Sekunden-Intervall ermöglicht dynamisches Matching- **Reoptimization**: 30-second interval enables dynamic matching

- **Abnehmender Grenznutzen**: Über 30 Fahrzeuge sinkt Grenznutzen erheblich- **Diminishing Returns**: Above 30 vehicles, marginal utility decreases significantly



⚠️ **Betriebliche Hinweise**⚠️ **Operational Notes**

- Morgenspitze (7-9 Uhr) ist dimensionierungs-kritisch für Tagesbetrieb- Morning peak (7-9 AM) is dimensioning-critical for daily operations

- Alle Szenarien erreichen 100% Service innerhalb 8 min Wartezeit- All scenarios achieve 100% service within 8 min wait time constraint

- Flotte ≥30 Fahrzeuge empfohlen für >95% Servicerate- Fleet ≥30 vehicles recommended for >95% service rate

- 20 Fahrzeuge nur für kostenoptimierte Start-up-Phase geeignet- 20 vehicles only suitable for cost-optimized startup phase



## Technische Details## Technical Details



### Simulationsparameter### Simulation Parameters

- **Zeitfenster**: 7:00-9:00 Uhr (Morgenspitze)- **Time Window**: 7:00-9:00 AM (morning peak)

- **Netzwerk**: 2.099 Knoten, 5.658 Kanten- **Network**: 2,099 nodes, 5,658 edges

- **Zonen**: 12 (K-Means-Clustering)- **Zones**: 12 (K-means clustering)

- **Algorithmus**: Alonso-Mora Batch Assignment- **Algorithm**: Alonso-Mora Batch Assignment

- **Reoptimierung**: Alle 30 Sekunden- **Reoptimization**: Every 30 seconds

- **Fahrzeugkapazität**: 4 Passagiere- **Vehicle Capacity**: 4 passengers

- **Max. Wartezeit**: 8 Minuten- **Max Wait Time**: 8 minutes



### Simulation ausführen### Running the Simulation



```bash```bash

# H1-Simulation starten# Start H1 simulation

python run_klagenfurt_h1_spitzenzeiten.pypython run_klagenfurt_h1_spitzenzeiten.py



# Analyse durchführen# Run analysis

python klagenfurt_h1_spitzenzeiten_analysis.pypython klagenfurt_h1_spitzenzeiten_analysis.py

``````



### Konfigurationsdatei### Configuration File



```yaml```yaml

sim_env: BatchOfferSimulationsim_env: BatchOfferSimulation

network_type: NetworkBasicnetwork_type: NetworkBasic

network_name: klagenfurt_h1_spitzenzeitennetwork_name: klagenfurt_h1_spitzenzeiten

demand_name: klagenfurt_h1_spitzenzeitendemand_name: klagenfurt_h1_spitzenzeiten

start_time: 25200  # 7:00 Uhrstart_time: 25200  # 7:00 AM

end_time: 32400    # 9:00 Uhrend_time: 32400    # 9:00 AM

time_step: 30time_step: 30

op_module: RidePoolingBatchAssignmentFleetcontrolop_module: RidePoolingBatchAssignmentFleetcontrol

op_rp_batch_optimizer: AlonsoMoraop_rp_batch_optimizer: AlonsoMora

op_max_wait_time: 480  # 8 Minutenop_max_wait_time: 480  # 8 minutes

op_max_detour_time_factor: 40op_max_detour_time_factor: 40

op_zone_system: klagenfurt_h1_spitzenzeitenop_zone_system: klagenfurt_h1_spitzenzeiten

``````



## Konfidenzlevel## Confidence Levels



### Hohe Konfidenz (>80%)### High Confidence (>80%)

- Serviceraten steigen mit Flottengröße- Service rates increase with fleet size

- Nicht-lineare Skalierung existiert- Non-linear scaling exists

- Abnehmender Grenznutzen über 30 Fahrzeuge- Diminishing returns above 30 vehicles

- Kritikalität des Zonensystems- Zone system criticality



### Mittlere Konfidenz (50-80%)### Medium Confidence (50-80%)

- Kosteneffizienz-Vergleiche- Cost efficiency comparisons

- Nutzerakzeptanz-Schwellenwerte- User acceptance thresholds

- Phasenmodell-Empfehlungen- Phase model recommendations



### Niedrige Konfidenz (<50%)### Low Confidence (<50%)

- Absolute Kostenschätzungen- Absolute cost estimates

- Reale Nutzerakzeptanz in Klagenfurt- Real user acceptance in Klagenfurt

- Langfristige betriebliche Auswirkungen- Long-term operational effects



## Referenzen## References



- Alonso-Mora et al. (2017) PNAS 114(3): 462-467- Alonso-Mora et al. (2017) PNAS 114(3): 462-467

- FleetPy Framework (TUM-VT)- FleetPy Framework (TUM-VT)

- OpenStreetMap Netzwerkdaten- OpenStreetMap Network Data