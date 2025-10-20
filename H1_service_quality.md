# 🎯 Hypothesis 1 (H1): Service Quality Optimization

## Research Question

**Goal:** Determine optimal fleet size for maximum service quality with acceptable cost efficiency

**Test Scenarios:**
1. **Scenario 1 - Base Fleet:** 20 vehicles (minimum economically viable fleet)
2. **Scenario 2 - Medium Fleet:** 30 vehicles (balance service quality/cost)
3. **Scenario 3 - Large Fleet:** 40 vehicles (maximum capacity)

**Hypothesis:** Larger fleets lead to higher service rates and shorter wait times, but with diminishing returns.

## Key Results

### Service Rates by Fleet Size

| Scenario | Fleet Size | Served Requests | Service Rate | Avg Wait Time | Total Time | Vehicle Utilization |
|----------|------------|-----------------|--------------|---------------|-------------|-------------------|
| **Scenario 1** | 20 vehicles | 84/100 | **84.0%** | 5.0 min | ~18 min | 100% |
| **Scenario 2** | 30 vehicles | 95/100 | **95.0%** | 4.2 min | ~17 min | 100% |
| **Scenario 3** | 40 vehicles | 98/100 | **98.0%** | 3.6 min | ~16 min | 92.5% |

**Data Source:** Direct simulation results from `studies/klagenfurt_h1_spitzenzeiten_case_study/results/`
**Confidence:** High (reproducible simulation results)

### Key Findings

- ✅ **High Service Rates**: 84-98% of requests served
- ⏱️ **Short Wait Times**: Average 3.6-5.0 minutes
- 🚗 **High Utilization**: 92-100% of vehicles actively used
- 📊 **Scaling Effect**: +50% fleet (20→30) → +13% service rate
- 💰 **Diminishing Returns**: +33% fleet (30→40) → only +3% service rate
- 🎯 **Sweet Spot**: 30 vehicles offer best cost-benefit ratio

### Service Quality by Wait Time

| Fleet Size | ≤3 min | ≤5 min | ≤8 min (Max) |
|------------|--------|---------|--------------|
| 20 vehicles | 35.7% | 51.2% | 100% |
| 30 vehicles | 51.6% | 67.4% | 100% |
| 40 vehicles | 60.2% | 74.5% | 100% |

## Strategic Recommendations

### 1. Cost-Efficiency Focus → 20 Vehicles
- ✅ 84% service rate (acceptable for startup)
- ✅ 100% vehicle utilization
- ✅ 4.2 requests per vehicle (highest efficiency)
- ✅ Lowest CAPEX/OPEX
- ⚠️ 16% unserved requests (reputation risk)

### 2. Cost/Service Balance → 30 Vehicles ⭐ RECOMMENDED
- ✅ 95% service rate (excellent)
- ✅ 100% vehicle utilization
- ✅ 67% with ≤5 min wait time
- ✅ 3.2 requests/vehicle (good efficiency)
- ✅ Best cost-benefit ratio
- ✅ Only 5% unserved requests (tolerable risk)

### 3. Service Quality Focus → 40 Vehicles
- ✅ 98% service rate (nearly complete)
- ✅ 3.6 min average wait time (shortest)
- ✅ 75% with ≤5 min wait time (premium service)
- ✅ Highest customer satisfaction
- ⚠️ 92.5% utilization (first overcapacity)
- ⚠️ 2.6 requests/vehicle (lower efficiency)
- ⚠️ Higher costs with minimal added value (+3% service vs. 30 vehicles)

## Critical Success Factors

✅ **Technical Feasibility Confirmed**
- Ridepooling in Klagenfurt works with 84-98% service rate
- Zone-based optimization critical for success (12 zones essential)
- Alonso-Mora algorithm effectively handles morning peak

💡 **Critical Insights**
- **Zone System**: 12-zone structure essential (vs. 1 zone: 0% service)
- **Centroids**: 103 strategic pickup points reduce empty trips
- **Reoptimization**: 30-second interval enables dynamic matching
- **Diminishing Returns**: Above 30 vehicles, marginal utility decreases significantly

⚠️ **Operational Notes**
- Morning peak (7-9 AM) is dimensioning-critical for daily operations
- All scenarios achieve 100% service within 8 min wait time constraint
- Fleet ≥30 vehicles recommended for >95% service rate
- 20 vehicles only suitable for cost-optimized startup phase

## Technical Details

### Simulation Parameters
- **Time Window**: 7:00-9:00 AM (morning peak)
- **Network**: 2,099 nodes, 5,658 edges
- **Zones**: 12 (K-means clustering)
- **Algorithm**: Alonso-Mora Batch Assignment
- **Reoptimization**: Every 30 seconds
- **Vehicle Capacity**: 4 passengers
- **Max Wait Time**: 8 minutes

### Running the Simulation

```bash
# Start H1 simulation
python run_klagenfurt_h1_spitzenzeiten.py

# Run analysis
python klagenfurt_h1_spitzenzeiten_analysis.py
```

### Configuration File

```yaml
sim_env: BatchOfferSimulation
network_type: NetworkBasic
network_name: klagenfurt_h1_spitzenzeiten
demand_name: klagenfurt_h1_spitzenzeiten
start_time: 25200  # 7:00 AM
end_time: 32400    # 9:00 AM
time_step: 30
op_module: RidePoolingBatchAssignmentFleetcontrol
op_rp_batch_optimizer: AlonsoMora
op_max_wait_time: 480  # 8 minutes
op_max_detour_time_factor: 40
op_zone_system: klagenfurt_h1_spitzenzeiten
```

## Confidence Levels

### High Confidence (>80%)
- Service rates increase with fleet size
- Non-linear scaling exists
- Diminishing returns above 30 vehicles
- Zone system criticality

### Medium Confidence (50-80%)
- Cost efficiency comparisons
- User acceptance thresholds
- Phase model recommendations

### Low Confidence (<50%)
- Absolute cost estimates
- Real user acceptance in Klagenfurt
- Long-term operational effects

## References

- Alonso-Mora et al. (2017) PNAS 114(3): 462-467
- FleetPy Framework (TUM-VT)
- OpenStreetMap Network Data