import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple
import numpy as np

class KlagenfurtH2SpitzenzeitenAnalysis:
    def __init__(self, results_dir):
        """Initialize with the path to results directory"""
        self.results_dir = results_dir
        self.scenarios = {}
        self.fleet_sizes = [8, 16, 24, 32]
        self.scenario_names = [
            'klagenfurt_h2_spitzenzeiten_scenario_1',
            'klagenfurt_h2_spitzenzeiten_scenario_2',
            'klagenfurt_h2_spitzenzeiten_scenario_3',
            'klagenfurt_h2_spitzenzeiten_scenario_4'
        ]

    def load_all_scenarios(self):
        """Load data from all scenario result directories"""
        for scenario_name, fleet_size in zip(self.scenario_names, self.fleet_sizes):
            scenario_path = os.path.join(self.results_dir, scenario_name)

            if not os.path.exists(scenario_path):
                print(f"Warning: {scenario_name} not found at {scenario_path}")
                continue

            try:
                users_df = pd.read_csv(os.path.join(scenario_path, '1_user-stats.csv'))
                ops_df = pd.read_csv(os.path.join(scenario_path, '2-0_op-stats.csv'))

                self.scenarios[fleet_size] = {
                    'users': users_df,
                    'ops': ops_df,
                    'name': scenario_name
                }
                print(f"✓ Loaded {scenario_name}: {len(users_df)} requests, Fleet: {fleet_size}")
            except Exception as e:
                print(f"✗ Error loading {scenario_name}: {e}")

        return len(self.scenarios) > 0

    def calculate_metrics(self) -> pd.DataFrame:
        """Calculate key performance metrics for all scenarios"""
        metrics = []

        for fleet_size in self.fleet_sizes:
            if fleet_size not in self.scenarios:
                continue

            data = self.scenarios[fleet_size]
            users_df = data['users']
            ops_df = data['ops']

            # Calculate metrics
            total_requests = len(users_df)
            # Served requests have non-null operator_id
            served = len(users_df[users_df['operator_id'].notna()])
            service_rate = (served / total_requests * 100) if total_requests > 0 else 0

            served_users = users_df[users_df['operator_id'].notna()]
            # Calculate wait time, in-vehicle time from timestamps
            avg_wait_time = (served_users['pickup_time'] - served_users['rq_time']).mean() if len(served_users) > 0 else 0
            avg_in_vehicle_time = (served_users['dropoff_time'] - served_users['pickup_time']).mean() if len(served_users) > 0 else 0
            avg_total_time = (served_users['dropoff_time'] - served_users['rq_time']).mean() if len(served_users) > 0 else 0

            # Vehicle utilization from ops data
            avg_occupancy = ops_df['op_mean_occupation'].mean() if 'op_mean_occupation' in ops_df.columns else 0

            metrics.append({
                'Fleet Size': fleet_size,
                'Total Requests': total_requests,
                'Served': served,
                'Service Rate (%)': round(service_rate, 2),
                'Avg Wait Time (min)': round(avg_wait_time / 60, 2),
                'Avg In-Vehicle Time (min)': round(avg_in_vehicle_time / 60, 2),
                'Avg Total Time (min)': round(avg_total_time / 60, 2),
                'Avg Occupancy': round(avg_occupancy, 2)
            })

        return pd.DataFrame(metrics)

    def plot_comparison(self) -> plt.Figure:
        """Create comprehensive comparison plots"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Klagenfurt H2 Spitzenzeiten - Performance Comparison (8-32 Shuttles)',
                     fontsize=16, fontweight='bold')

        metrics_df = self.calculate_metrics()

        # 1. Service Rate
        ax = axes[0, 0]
        ax.bar(metrics_df['Fleet Size'], metrics_df['Service Rate (%)'],
               color=['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4'])
        ax.set_xlabel('Fleet Size', fontsize=11)
        ax.set_ylabel('Service Rate (%)', fontsize=11)
        ax.set_title('Service Rate by Fleet Size', fontweight='bold')
        ax.set_ylim([0, 100])
        ax.grid(axis='y', alpha=0.3)
        for i, v in enumerate(metrics_df['Service Rate (%)']):
            ax.text(metrics_df['Fleet Size'].iloc[i], v + 2, f'{v:.1f}%',
                   ha='center', fontweight='bold')

        # 2. Average Wait Time
        ax = axes[0, 1]
        ax.plot(metrics_df['Fleet Size'], metrics_df['Avg Wait Time (min)'],
                marker='o', linewidth=2, markersize=8, color='#d62728')
        ax.set_xlabel('Fleet Size', fontsize=11)
        ax.set_ylabel('Wait Time (minutes)', fontsize=11)
        ax.set_title('Average Wait Time', fontweight='bold')
        ax.grid(True, alpha=0.3)

        # 3. Average Total Time
        ax = axes[0, 2]
        ax.plot(metrics_df['Fleet Size'], metrics_df['Avg Total Time (min)'],
                marker='s', linewidth=2, markersize=8, color='#2ca02c')
        ax.set_xlabel('Fleet Size', fontsize=11)
        ax.set_ylabel('Total Time (minutes)', fontsize=11)
        ax.set_title('Average Total Journey Time', fontweight='bold')
        ax.grid(True, alpha=0.3)

        # 4. Served vs Rejected
        ax = axes[1, 0]
        served = metrics_df['Served']
        rejected = metrics_df['Total Requests'] - metrics_df['Served']
        x = np.arange(len(metrics_df))
        width = 0.35
        ax.bar(x, served, width, label='Served', color='#2ca02c')
        ax.bar(x, rejected, width, bottom=served, label='Rejected', color='#d62728')
        ax.set_xlabel('Fleet Size', fontsize=11)
        ax.set_ylabel('Number of Requests', fontsize=11)
        ax.set_title('Request Distribution', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics_df['Fleet Size'])
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        # 5. Vehicle Occupancy
        ax = axes[1, 1]
        ax.bar(metrics_df['Fleet Size'], metrics_df['Avg Occupancy'],
               color=['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4'])
        ax.set_xlabel('Fleet Size', fontsize=11)
        ax.set_ylabel('Average Occupancy', fontsize=11)
        ax.set_title('Average Vehicle Occupancy', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)

        # 6. Efficiency Metric (Served per Vehicle)
        ax = axes[1, 2]
        efficiency = metrics_df['Served'] / metrics_df['Fleet Size']
        ax.plot(metrics_df['Fleet Size'], efficiency,
                marker='D', linewidth=2, markersize=8, color='#9467bd')
        ax.set_xlabel('Fleet Size', fontsize=11)
        ax.set_ylabel('Requests Served per Vehicle', fontsize=11)
        ax.set_title('Fleet Efficiency', fontweight='bold')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_temporal_analysis(self, interval_minutes: int = 15) -> plt.Figure:
        """Create temporal analysis plots."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Temporal Analysis - Klagenfurt H2 Spitzenzeiten Study (8-32 Shuttles)')

        for fleet_size, data in self.scenarios.items():
            users_df = data['users']

            # Group by time intervals
            users_df['time_bin'] = (users_df['rq_time'] // (interval_minutes * 60)) * (interval_minutes * 60)
            temporal = users_df.groupby('time_bin').agg({
                'rq_time': 'count',
                'operator_id': lambda x: x.notna().sum()
            }).reset_index()
            temporal.columns = ['time_bin', 'rq', 'served']
            temporal['service_rate'] = (temporal['served'] / temporal['rq'] * 100)
            temporal['time_label'] = pd.to_datetime(temporal['time_bin'], unit='s').dt.strftime('%H:%M')

            # Plot requests over time
            axes[0, 0].plot(temporal['time_label'], temporal['rq'],
                          marker='o', label=f'{fleet_size} shuttles')
            axes[0, 0].set_xlabel('Time')
            axes[0, 0].set_ylabel('Number of Requests')
            axes[0, 0].set_title('Requests Over Time')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)
            plt.setp(axes[0, 0].xaxis.get_majorticklabels(), rotation=45)

            # Plot service rate over time
            axes[0, 1].plot(temporal['time_label'], temporal['service_rate'],
                          marker='s', label=f'{fleet_size} shuttles')
            axes[0, 1].set_xlabel('Time')
            axes[0, 1].set_ylabel('Service Rate (%)')
            axes[0, 1].set_title('Service Rate Over Time')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
            plt.setp(axes[0, 1].xaxis.get_majorticklabels(), rotation=45)

        # Wait time distribution
        ax = axes[1, 0]
        for fleet_size, data in self.scenarios.items():
            served = data['users'][data['users']['operator_id'].notna()]
            if len(served) > 0:
                wait_times = (served['pickup_time'] - served['rq_time']) / 60
                ax.hist(wait_times, bins=30, alpha=0.5,
                       label=f'{fleet_size} shuttles')
        ax.set_xlabel('Wait Time (minutes)')
        ax.set_ylabel('Frequency')
        ax.set_title('Wait Time Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Travel time distribution
        ax = axes[1, 1]
        for fleet_size, data in self.scenarios.items():
            served = data['users'][data['users']['operator_id'].notna()]
            if len(served) > 0:
                total_times = (served['dropoff_time'] - served['rq_time']) / 60
                ax.hist(total_times, bins=30, alpha=0.5,
                       label=f'{fleet_size} shuttles')
        ax.set_xlabel('Total Travel Time (minutes)')
        ax.set_ylabel('Frequency')
        ax.set_title('Total Travel Time Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig


if __name__ == "__main__":
    # Set up paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, "studies", "klagenfurt_h2_spitzenzeiten_case_study", "results")

    # Create analysis instance
    analysis = KlagenfurtH2SpitzenzeitenAnalysis(results_dir)

    # Load scenarios
    print("Loading H2 scenarios...")
    if not analysis.load_all_scenarios():
        print("Error: Could not load any scenarios")
        exit(1)

    # Calculate and save metrics
    metrics_df = analysis.calculate_metrics()
    metrics_df.to_csv(os.path.join(results_dir, "klagenfurt_h2_spitzenzeiten_scenarios_comparison.csv"), index=False)
    print("\n=== KLAGENFURT H2 SPITZENZEITEN SCENARIOS COMPARISON ===")
    print(metrics_df.to_string(index=False))

    # Create and save plots
    temporal_fig = analysis.plot_temporal_analysis()
    temporal_fig.savefig(os.path.join(results_dir, "h2_temporal_analysis.png"))

    comparison_fig = analysis.plot_comparison()
    comparison_fig.savefig(os.path.join(results_dir, "h2_performance_comparison.png"))

    print(f"\n✓ Analysis complete!")
    print(f"✓ Results saved to: {results_dir}")
    print(f"✓ Comparison CSV: klagenfurt_h2_spitzenzeiten_scenarios_comparison.csv")
    print(f"✓ Charts: h2_temporal_analysis.png, h2_performance_comparison.png")
