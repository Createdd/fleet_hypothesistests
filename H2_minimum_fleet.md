# 🔬 Hypothesis 2 (H2): Minimum Fleet Size

## Research Question

**Goal:** Determine the **minimum economically viable fleet size** for acceptable service quality (>85% service rate target)

**Test Scenarios:**
1. **Scenario 1 - Micro Fleet:** 8 vehicles (absolute minimum)
2. **Scenario 2 - Small Fleet:** 16 vehicles (double micro fleet)
3. **Scenario 3 - Base Fleet:** 24 vehicles (critical threshold)
4. **Scenario 4 - Standard Fleet:** 32 vehicles (comfort zone)

**Hypothesis:** There exists a critical threshold below which service rate drastically collapses (non-linear scaling)

## Key Results

### Service Rates by Fleet Size (Small Fleets)

| Scenario | Fleet Size | Served Requests | Service Rate | Avg Wait Time | Total Time | Vehicle Utilization |
|----------|------------|-----------------|--------------|---------------|------------|-------------------|
| **H2-Scenario 1** | 8 vehicles | 41/100 | **41.0%** | 5.34 min | 19.82 min | ~100% |
| **H2-Scenario 2** | 16 vehicles | 70/100 | **70.0%** | 5.05 min | 18.48 min | ~100% |
| **H2-Scenario 3** | 24 vehicles | 92/100 | **92.0%** | 4.67 min | 18.24 min | ~100% |
| **H2-Scenario 4** | 32 vehicles | 95/100 | **95.0%** | 4.09 min | 17.12 min | ~100% |

**Data Source:** Direct simulation results from `studies/klagenfurt_h2_spitzenzeiten_case_study/results/`
**Confidence:** High (reproducible simulation results)

### Scaling Behavior Analysis

**Critical Threshold Identified:**
- ❌ **8 vehicles**: Undersupply (41% service rate) - **not viable**
- ⚠️ **16 vehicles**: Critical range (70% service rate) - **marginally acceptable**
- ✅ **24 vehicles**: **Optimal minimum fleet** (92% service rate) - **meets acceptance threshold**
- ✅ **32 vehicles**: Comfort zone (95% service rate) - **high reliability**

**Scaling Jumps (Service Rate Improvement):**
- **8→16 vehicles** (+100% fleet): +29% service rate (+71% relative jump) → **Largest effect!**
- **16→24 vehicles** (+50% fleet): +22% service rate (+31% relative jump)
- **24→32 vehicles** (+33% fleet): +3% service rate (+3% relative jump) → **Diminishing Returns**

### Wait Time Comparison

| Fleet Size | Avg Wait Time | Total Time | Max Wait Time | Improvement vs Previous |
|------------|--------------|------------|---------------|------------------------|
| 8 vehicles | 5.34 min | 19.82 min | ~8 min | - (Baseline) |
| 16 vehicles | 5.05 min | 18.48 min | ~8 min | -5.4% wait time |
| 24 vehicles | 4.67 min | 18.24 min | ~8 min | -7.5% wait time |
| 32 vehicles | 4.09 min | 17.12 min | ~8 min | -12.4% wait time |

## Strategic Recommendations

### Cost-Optimized Operations

**Phase 1 - Startup/Pilot (3-6 months):**
- **Recommendation:** 24 vehicles
- **Service Rate:** 92% (above 85% minimum target)
- **Advantages:**
  - ✅ Low initial investment (60% vs. 40 vehicles)
  - ✅ Acceptable service quality for early adopters
  - ✅ Test phase for demand validation
  - ✅ 4.67 min average wait time
- **Risks:**
  - ⚠️ 8% unserved requests (reputation risk)
  - ⚠️ Limited buffer for demand spikes

**Phase 2 - Growth (6-12 months):**
- **Recommendation:** 32 vehicles
- **Service Rate:** 95% (excellent)
- **Advantages:**
  - ✅ High reliability (only 5% rejection)
  - ✅ 4.09 min wait time (premium level)
  - ✅ Buffer for demand fluctuations
  - ✅ Competitive with public transport

**Phase 3 - Maturity (>12 months):**
- **Recommendation:** H1 scenarios (30-40 vehicles)
- **Service Rate:** 95-98%
- **Goal:** Establishment as premium service

**Critical Boundary:**
⚠️ **NEVER operate below 16 vehicles** (70% service unacceptable for user acceptance)

## Service Quality Categories

| Category | Service Rate | Fleet Size | Rating | Use Case |
|----------|--------------|------------|---------|----------|
| **Undersupply** | <70% | <16 vehicles | ❌ Not viable | None |
| **Critical** | 70-85% | 16-20 vehicles | ⚠️ Marginal | Emergency only |
| **Acceptable** | 85-95% | 24-32 vehicles | ✅ Operable | **Minimum operation recommended** |
| **Optimal** | >95% | >30 vehicles | ✅ Excellent | Premium service |

## Technical Details

### Simulation Parameters
- **Time Window**: 7:00-9:00 AM (morning peak)
- **Demand**: 100 mobility requests
- **Algorithm**: Alonso-Mora Batch Assignment
- **Reoptimization**: Every 30 seconds
- **Vehicle Capacity**: 4 passengers
- **Max Wait Time**: 8 minutes

### Running the Simulation

```bash
# Start H2 simulation
python run_klagenfurt_h2_spitzenzeiten.py

# Run analysis
python klagenfurt_h2_spitzenzeiten_analysis.py
```

## Confidence Levels

### High Confidence (>80%)
- Critical threshold exists at 16 vehicles
- Non-linear scaling behavior
- Service collapse below 16 vehicles
- 24 vehicles as viable minimum

### Medium Confidence (50-80%)
- Phase model recommendations
- User acceptance thresholds
- Growth strategy timing

### Low Confidence (<50%)
- Real operational costs
- Long-term sustainability
- Actual market acceptance

## Known Limitations

1. **Synthetic Demand (no real data)**
   - **Impact:** Medium
   - **Mitigation:** Spatial distribution across zones, realistic temporal modeling

2. **No Cost Data (theoretical estimates)**
   - **Impact:** High
   - **Mitigation:** Focus on service quality and efficiency metrics

3. **Morning Peak Only (no daily variations)**
   - **Impact:** Medium
   - **Mitigation:** Morning peak is dimensioning-critical (conservative estimate)

## References

- Alonso-Mora et al. (2017) PNAS 114(3): 462-467
- FleetPy Framework (TUM-VT)
- OpenStreetMap Network Data