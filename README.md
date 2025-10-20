# 🚌 FleetPy Klagenfurt Case Study

[![FleetPy](https://img.shields.io/badge/Framework-FleetPy-blue)](https://github.com/TUM-VT/FleetPy)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-green.svg)](https://www.python.org/downloads/)

## Overview

This study analyzes the feasibility and performance of a ridepooling service in Klagenfurt using the FleetPy simulation framework. The analysis is split into two main hypothesis tests:

### [Hypothesis 1 (H1): Service Quality Optimization](H1_service_quality.md)
- Focus on optimizing service quality with larger fleets
- Testing fleets of 20, 30, and 40 vehicles
- Emphasis on maximizing service rate and minimizing wait times

### [Hypothesis 2 (H2): Minimum Fleet Size](H2_minimum_fleet.md)
- Focus on determining minimum economically viable fleet size
- Testing fleets of 8, 16, 24, and 32 vehicles
- Emphasis on finding critical thresholds and cost efficiency

## Key Findings

### Service Rate Comparison
| Fleet Size | Service Rate | Wait Time | Vehicle Utilization |
|------------|--------------|-----------|-------------------|
| 8 vehicles | 41.0% | 5.34 min | ~100% |
| 16 vehicles | 70.0% | 5.05 min | ~100% |
| 20 vehicles | 84.0% | 5.00 min | 100% |
| 24 vehicles | 92.0% | 4.67 min | ~100% |
| 30 vehicles | 95.0% | 4.20 min | 100% |
| 32 vehicles | 95.0% | 4.09 min | ~100% |
| 40 vehicles | 98.0% | 3.60 min | 92.5% |

**Critical Thresholds:**
- Below 16 vehicles: Service collapses (<70% service rate)
- 24 vehicles: Optimal minimum fleet (92% service rate)
- 30-32 vehicles: Sweet spot for service quality (95% service rate)
- Above 40 vehicles: Diminishing returns (minimal gain for higher cost)

## System Configuration

### Network Parameters
- **Nodes:** 2,099 (street intersections and stops)
- **Edges:** 5,658 (street connections)
- **Zones:** 12 (K-means clustering)
- **Centroids:** 103 (strategic pickup/drop-off points)

### Service Constraints
- **Maximum wait time:** 8 minutes
- **Maximum detour factor:** 40% of direct travel time
- **Boarding time:** 30 seconds (constant)
- **Vehicle capacity:** 4 passengers

### Time Parameters
- **Simulation period:** 7:00-9:00 (morning peak)
- **Reoptimization interval:** 30 seconds
- **Demand:** 100 mobility requests

## Project Setup

### Requirements
- Python 3.10+
- FleetPy Framework
- Conda Environment

### Installation

1. Clone repository:
\`\`\`bash
git clone https://github.com/Createdd/fleet_hypothesistests.git
cd FleetPy
\`\`\`

2. Create environment:
\`\`\`bash
conda env create -f environment.yml
conda activate fleetpy
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Running Simulations

For H1 (Service Quality):
\`\`\`bash
python run_klagenfurt_h1_spitzenzeiten.py
python klagenfurt_h1_spitzenzeiten_analysis.py
\`\`\`

For H2 (Minimum Fleet):
\`\`\`bash
python run_klagenfurt_h2_spitzenzeiten.py
python klagenfurt_h2_spitzenzeiten_analysis.py
\`\`\`

## Confidence Levels

### High Confidence (>80%)
- Service rates increase with fleet size
- Non-linear scaling exists (critical threshold at 16 vehicles)
- Diminishing returns above 24 vehicles
- Zone system is critical for algorithm success

### Medium Confidence (50-80%)
- 24 vehicles as optimal minimum fleet
- Cost efficiency comparisons
- User acceptance thresholds

### Low Confidence (<50%)
- Absolute cost estimates (no real CAPEX/OPEX data)
- Real user acceptance in Klagenfurt
- Long-term operational effects

## Data Sources
- Network data: OpenStreetMap (verified)
- Algorithm: Alonso-Mora et al. (2017) PNAS 114(3): 462-467
- Framework: FleetPy (TUM-VT)

## License
This project uses the FleetPy framework under its license.
© Technical University of Munich, Chair of Traffic Engineering and Control