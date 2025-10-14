import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

class KlagenfurtH1SpitzenzeitenAnalysis:
    def __init__(self, results_dir):
        """Initialize with the path to results directory"""
        self.results_dir = results_dir
        self.scenarios = {}
        self._load_results()

    def _load_results(self):
        """Load results from all scenario directories."""
        scenario_dirs = [d for d in os.listdir(self.results_dir)
                        if os.path.isdir(os.path.join(self.results_dir, d))]

        for scenario in scenario_dirs:
            scenario_path = os.path.join(self.results_dir, scenario)
            # Load user data
            users_file = os.path.join(scenario_path, "users.csv")
            if os.path.exists(users_file):
                users_df = pd.read_csv(users_file)
                users_df['time'] = pd.to_datetime(users_df['time'], unit='s')
            else:
                users_df = pd.DataFrame()

            # Load vehicle data
            vehicles_file = os.path.join(scenario_path, "vehicles.csv")
            if os.path.exists(vehicles_file):
                vehicles_df = pd.read_csv(vehicles_file)
                vehicles_df['time'] = pd.to_datetime(vehicles_df['time'], unit='s')
            else:
                vehicles_df = pd.DataFrame()

            self.scenarios[scenario] = {
                'users': users_df,
                'vehicles': vehicles_df
            }

    def calculate_metrics(self) -> pd.DataFrame:
        """Calculate key metrics for all scenarios."""
        metrics = []

        for scenario, data in self.scenarios.items():
            users_df = data['users']
            vehicles_df = data['vehicles']

            if not users_df.empty:
                # Calculate metrics
                total_trips = len(users_df)
                avg_wait_time = users_df['waiting_time'].mean() / 60  # Convert to minutes
                max_wait_time = users_df['waiting_time'].max() / 60
                service_rate_10min = (users_df['waiting_time'] <= 600).mean() * 100  # <= 10 minutes
                unique_vehicles = vehicles_df['vid'].nunique() if not vehicles_df.empty else 0

                # Calculate peak hour demand (rolling 1-hour window)
                users_df['hour'] = users_df['time'].dt.hour
                peak_demand = users_df.groupby('hour').size().max()

                metrics.append({
                    'Scenario': scenario,
                    'Total Trips': total_trips,
                    'Avg Wait Time (min)': round(avg_wait_time, 1),
                    'Max Wait Time (min)': round(max_wait_time, 1),
                    'Service Rate ≤10min (%)': round(service_rate_10min, 1),
                    'Unique Vehicles': unique_vehicles,
                    'Peak Hour Demand': peak_demand
                })

        return pd.DataFrame(metrics)

    def plot_temporal_analysis(self, interval_minutes: int = 15) -> plt.Figure:
        """Create temporal analysis plots."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Temporal Analysis - Klagenfurt H1 Spitzenzeiten Study')

        for scenario, data in self.scenarios.items():
            users_df = data['users']
            if users_df.empty:
                continue

            # Resample data to specified interval
            users_ts = users_df.set_index('time').resample(f'{interval_minutes}min').agg({
                'rid': 'count',
                'waiting_time': 'mean',
                'driving_time': 'mean'
            })

            # Plot request count
            axes[0, 0].plot(users_ts.index.hour + users_ts.index.minute/60,
                          users_ts['rid'], label=scenario)
            axes[0, 0].set_title('Request Count Over Time')
            axes[0, 0].set_xlabel('Hour of Day')
            axes[0, 0].set_ylabel('Number of Requests')

            # Plot average waiting time
            axes[0, 1].plot(users_ts.index.hour + users_ts.index.minute/60,
                          users_ts['waiting_time']/60, label=scenario)
            axes[0, 1].set_title('Average Waiting Time')
            axes[0, 1].set_xlabel('Hour of Day')
            axes[0, 1].set_ylabel('Minutes')

            # Plot average driving time
            axes[1, 0].plot(users_ts.index.hour + users_ts.index.minute/60,
                          users_ts['driving_time']/60, label=scenario)
            axes[1, 0].set_title('Average Driving Time')
            axes[1, 0].set_xlabel('Hour of Day')
            axes[1, 0].set_ylabel('Minutes')

        for ax in axes.flat:
            ax.legend()
            ax.grid(True)

        plt.tight_layout()
        return fig

    def plot_fleet_utilization(self) -> plt.Figure:
        """Plot fleet utilization over time."""
        fig, ax = plt.subplots(figsize=(12, 6))

        for scenario, data in self.scenarios.items():
            vehicles_df = data['vehicles']
            if vehicles_df.empty:
                continue

            # Calculate utilization (vehicles with passengers / total vehicles)
            util_ts = vehicles_df.set_index('time').resample('15min').agg({
                'vid': 'count',
                'occupancy': lambda x: (x > 0).sum()
            })
            utilization = (util_ts['occupancy'] / util_ts['vid']) * 100

            ax.plot(util_ts.index.hour + util_ts.index.minute/60,
                   utilization, label=scenario)

        ax.set_title('Fleet Utilization Over Time')
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Utilization (%)')
        ax.legend()
        ax.grid(True)

        plt.tight_layout()
        return fig

def main():
    """Main analysis function."""
        # Set up paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, "studies", "klagenfurt_h1_spitzenzeiten_case_study", "results")

    # Create analysis instance
    analysis = KlagenfurtH1SpitzenzeitenAnalysis(results_dir)

    # Calculate and save metrics
    metrics_df = analysis.calculate_metrics()
    metrics_df.to_csv(os.path.join(results_dir, "klagenfurt_h1_spitzenzeiten_scenarios_comparison.csv"), index=False)
    print("\n=== KLAGENFURT H1 SPITZENZEITEN SCENARIOS COMPARISON ===")
    print(metrics_df.to_string(index=False))

    # Create and save plots
    temporal_fig = analysis.plot_temporal_analysis()
    temporal_fig.savefig(os.path.join(results_dir, "temporal_analysis.png"))

    utilization_fig = analysis.plot_fleet_utilization()
    utilization_fig.savefig(os.path.join(results_dir, "fleet_utilization.png"))

    print("\nAnalysis complete. Results saved to:", results_dir)

if __name__ == "__main__":
    main()
# ## Import Libraries

# %%
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import glob
from IPython.display import display, HTML

def find_result_dir(scenario_name, base_dirs=None):
    """Find the correct result directory"""
    if base_dirs is None:
        base_dirs = ['studies/klagenfurt_h1_spitzenzeiten/results', 'results', 'studies/studies/results']

    for base in base_dirs:
        path = os.path.join(base, scenario_name)
        if os.path.exists(path):
            return path
    return None

def load_data(result_dir):
    """Load user and operations data from FleetPy results directory"""
    users = pd.read_csv(os.path.join(result_dir, '1_user-stats.csv'))
    ops = pd.read_csv(os.path.join(result_dir, '2-0_op-stats.csv'))

    # Process time columns
    users['waiting_time'] = users['pickup_time'] - users['rq_time']
    users['time'] = pd.to_timedelta(users['rq_time'], unit='s')
    users['hour'] = users['time'].dt.hour
    ops['time'] = pd.to_timedelta(ops['start_time'], unit='s')

    return users, ops

def aggregate_temporal(users, ops, interval_minutes=15):
    """Aggregate metrics by time intervals"""
    user_ts = users.set_index('time').resample(f'{interval_minutes}T').agg({
        'request_id': 'count',
        'waiting_time': ['mean', 'std', 'max']
    })

    # Flatten column names
    user_ts.columns = ['requests', 'wait_mean', 'wait_std', 'wait_max']

    # Convert to minutes
    for col in ['wait_mean', 'wait_std', 'wait_max']:
        user_ts[col] = user_ts[col] / 60

    # Calculate utilization
    ops['occupied'] = ops['occupancy'] > 0
    util = ops.groupby(pd.Grouper(key='time', freq=f'{interval_minutes}T')).occupied.mean() * 100
    user_ts['utilization'] = util

    return user_ts.fillna(0)

def plot_temporal(df, title):
    """Create temporal plot of waiting times and utilization"""
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot mean waiting time
    line1 = ax1.plot(df.index.hour + df.index.minute/60,
                     df['wait_mean'], 'b-', label='Mean Wait Time')
    ax1.fill_between(df.index.hour + df.index.minute/60,
                     df['wait_mean'] - df['wait_std'],
                     df['wait_mean'] + df['wait_std'],
                     alpha=0.2)
    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('Wait Time (minutes)')

    # Plot request volume on secondary axis
    ax2 = ax1.twinx()
    line2 = ax2.plot(df.index.hour + df.index.minute/60,
                     df['requests'], 'r--', label='Requests')
    line3 = ax2.plot(df.index.hour + df.index.minute/60,
                     df['utilization'], 'g:', label='Utilization %')
    ax2.set_ylabel('Requests / Utilization %')

    # Add legend
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')

    plt.title(title)
    plt.grid(True, alpha=0.3)
    return fig

def create_comparison_plots(users1, users2):
    """Create comparison plots between morning and afternoon scenarios"""
    # Waiting time distributions
    plt.figure(figsize=(10, 6))
    plt.hist(users1['waiting_time']/60, bins=50, alpha=0.5, label='Morning Peak')
    plt.hist(users2['waiting_time']/60, bins=50, alpha=0.5, label='Afternoon Peak')
    plt.xlabel('Waiting Time (minutes)')
    plt.ylabel('Count')
    plt.title('Distribution of Waiting Times')
    plt.legend()
    plt.show()

    # Request patterns
    plt.figure(figsize=(10, 6))
    hourly1 = users1.groupby('hour').size()
    hourly2 = users2.groupby('hour').size()
    plt.plot(hourly1.index, hourly1.values, 'b-', label='Morning Peak')
    plt.plot(hourly2.index, hourly2.values, 'r-', label='Afternoon Peak')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Requests')
    plt.title('Hourly Request Patterns')
    plt.legend()
    plt.show()

def create_summary_table(users1, users2, ops1, ops2):
    """Create summary table comparing both scenarios"""
    metrics = {
        'Total Requests': [len(users1), len(users2)],
        'Mean Wait (min)': [users1['waiting_time'].mean()/60, users2['waiting_time'].mean()/60],
        'Max Wait (min)': [users1['waiting_time'].max()/60, users2['waiting_time'].max()/60],
        'Service Rate (≤10min)': [(users1['waiting_time'] <= 600).mean()*100,
                                 (users2['waiting_time'] <= 600).mean()*100],
        'Active Vehicles': [ops1['vehicle_id'].nunique(), ops2['vehicle_id'].nunique()]
    }

    summary = pd.DataFrame(metrics, index=['Morning Peak', 'Afternoon Peak'])
    print("\nSummary Comparison:")
    print(summary.round(2))

def load_data(result_dir):
    """Load user requests and operator data from result directory"""
    users = pd.read_csv(os.path.join(result_dir, 'user_request_results.csv'))
    ops = pd.read_csv(os.path.join(result_dir, 'op_metrics.csv'))

    # Convert time columns
    users['rq_time'] = pd.to_datetime(users['rq_time'])
    users['hour'] = users['rq_time'].dt.hour

    return users, ops

def aggregate_temporal(users, ops, interval_minutes=15):
    """Aggregate data into temporal bins"""
    df = users.copy()
    df['time_bin'] = df['rq_time'].dt.floor(f'{interval_minutes}min')

    # Compute metrics per time bin
    grouped = df.groupby('time_bin').agg({
        'waiting_time': ['count', 'mean', 'std', 'max'],
        'id': 'count'
    }).reset_index()

    # Flatten column names
    grouped.columns = ['time_bin', 'requests', 'wait_mean', 'wait_std', 'wait_max', 'total_requests']

    # Convert to minutes
    grouped['wait_mean'] = grouped['wait_mean'] / 60
    grouped['wait_std'] = grouped['wait_std'] / 60
    grouped['wait_max'] = grouped['wait_max'] / 60

    return grouped

def plot_temporal(df, title):
    """Create temporal plot of waiting times"""
    plt.figure(figsize=(12, 6))

    # Plot mean waiting time
    plt.plot(df['time_bin'], df['wait_mean'], 'b-', label='Mean Wait Time')

    # Add shaded area for standard deviation
    plt.fill_between(df['time_bin'],
                    df['wait_mean'] - df['wait_std'],
                    df['wait_mean'] + df['wait_std'],
                    alpha=0.2)

    # Plot request volume
    ax2 = plt.twinx()
    ax2.plot(df['time_bin'], df['requests'], 'r--', label='Requests')
    ax2.set_ylabel('Number of Requests', color='r')

    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Wait Time (minutes)')

    # Add legend
    lines1, labels1 = plt.gca().get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    return plt.gcf()

def create_comparison_plots(users1, users2, df1, df2):
    """Create comparison plots between morning and afternoon scenarios"""
    # Waiting time distributions
    plt.figure(figsize=(10, 6))
    plt.hist(users1['waiting_time']/60, bins=50, alpha=0.5, label='Morning Peak')
    plt.hist(users2['waiting_time']/60, bins=50, alpha=0.5, label='Afternoon Peak')
    plt.xlabel('Waiting Time (minutes)')
    plt.ylabel('Count')
    plt.title('Distribution of Waiting Times')
    plt.legend()
    plt.show()

    # Request patterns
    plt.figure(figsize=(10, 6))
    hourly1 = users1.groupby('hour').size()
    hourly2 = users2.groupby('hour').size()
    plt.plot(hourly1.index, hourly1.values, 'b-', label='Morning Peak')
    plt.plot(hourly2.index, hourly2.values, 'r-', label='Afternoon Peak')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Requests')
    plt.title('Hourly Request Patterns')
    plt.legend()
    plt.show()

def create_summary_table(users1, users2, ops1, ops2):
    """Create summary table comparing both scenarios"""
    metrics = {
        'Total Requests': [len(users1), len(users2)],
        'Mean Wait (min)': [users1['waiting_time'].mean()/60, users2['waiting_time'].mean()/60],
        'Max Wait (min)': [users1['waiting_time'].max()/60, users2['waiting_time'].max()/60],
        'Service Rate (≤10min)': [(users1['waiting_time'] <= 600).mean()*100,
                                 (users2['waiting_time'] <= 600).mean()*100],
        'Active Vehicles': [ops1['vehicle_id'].nunique(), ops2['vehicle_id'].nunique()]
    }

    summary = pd.DataFrame(metrics, index=['Morning Peak', 'Afternoon Peak'])
    print("\nSummary Comparison:")
    print(summary.round(2))

# Set plotting style
plt.style.use('seaborn-v0_8')  # Use a specific seaborn style version
sns.set_palette("husl")

# Configure pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

def main():
    """Main analysis function"""
    # Set plotting style
    plt.style.use('seaborn-v0_8')

    # Find result directories
    scenario1_dir = find_result_dir('klagenfurt_h1_spitzenzeiten_peak_morning')
    scenario2_dir = find_result_dir('klagenfurt_h1_spitzenzeiten_peak_afternoon')

    if not scenario1_dir or not scenario2_dir:
        print("Could not find result directories. Please verify the simulation completed successfully.")
        print("Checked directories: studies/klagenfurt_h1_spitzenzeiten/results, results, studies/studies/results")
        return

    try:
        # Load and process data
        users1, ops1 = load_data(scenario1_dir)
        df1 = aggregate_temporal(users1, ops1, interval_minutes=15)

        users2, ops2 = load_data(scenario2_dir)
        df2 = aggregate_temporal(users2, ops2, interval_minutes=15)

        print("Data loaded successfully!")
        print(f"Morning peak requests: {len(users1):,}")
        print(f"Afternoon peak requests: {len(users2):,}")

        # Display temporal analysis
        print("\n=== TEMPORAL ANALYSIS ===")
        plot_temporal(df1, 'Klagenfurt H1 Spitzenzeiten Morning Peak')
        plt.show()
        plot_temporal(df2, 'Klagenfurt H1 Spitzenzeiten Afternoon Peak')
        plt.show()

        # Create comparison plots
        print("\n=== COMPARISON ANALYSIS ===")
        create_comparison_plots(users1, users2)

        # Print summary statistics
        print("\n=== SCENARIO SUMMARIES ===")
        create_summary_table(users1, users2, ops1, ops2)

    except FileNotFoundError as e:
        print(f"Error: Could not load result files: {e}")
        return
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return

if __name__ == "__main__":
    main()

# %% [markdown]
# ## Data Loading Functions
#
# Define helper functions to load and process the simulation results.

# %%
def load_data(result_dir):
    """Load user and operations data from FleetPy results directory"""
    users = pd.read_csv(os.path.join(result_dir, '1_user-stats.csv'))
    ops = pd.read_csv(os.path.join(result_dir, '2-0_op-stats.csv'))
    return users, ops

def aggregate_temporal(users, ops, interval_minutes=15):
    """Aggregate metrics by time intervals"""
    users['waiting_time'] = users['pickup_time'] - users['rq_time']
    users['time'] = pd.to_timedelta(users['rq_time'], unit='s')
    ops['time'] = pd.to_timedelta(ops['start_time'], unit='s')

    user_ts = users.set_index('time').resample(f'{interval_minutes}T').agg({
        'request_id': 'count',
        'waiting_time': 'mean'
    }).rename(columns={'request_id': 'requests', 'waiting_time': 'avg_wait_s'})

    ops['occupied'] = ops['occupancy'] > 0
    util = ops.groupby(pd.Grouper(key='time', freq=f'{interval_minutes}T')).occupied.mean() * 100
    util_ts = util.rename('util_pct')

    return pd.concat([user_ts, util_ts], axis=1).fillna(0)

def plot_temporal(df, scenario_name):
    """Create temporal analysis plot"""
    fig, ax1 = plt.subplots(figsize=(12, 6))

    width = df.index.freq.delta.total_seconds() / 3600 * 0.8
    ax1.bar(df.index.total_seconds()/3600, df.requests,
            width=width, color='C0', alpha=0.6, label='Requests')
    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('Requests per Interval', color='C0')
    ax1.tick_params(axis='y', labelcolor='C0')

    ax2 = ax1.twinx()
    ax2.plot(df.index.total_seconds()/3600, df.avg_wait_s/60,
             'C1-o', label='Avg Wait (min)', linewidth=2)
    ax2.plot(df.index.total_seconds()/3600, df.util_pct,
             'C2-s', label='Utilization (%)', linewidth=2)
    ax2.set_ylabel('Avg Wait (min) & Util (%)', color='C1')
    ax2.tick_params(axis='y', labelcolor='C1')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1+lines2, labels1+labels2, loc='upper left')

    plt.title(f'Temporal Metrics for {scenario_name}', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

# %% [markdown]
# ## Load Klagenfurt Simulation Results
#
# Load results from morning and afternoon peak scenarios.

# %%
def main():
    # Define result directories - check both possible locations
    base_dirs = ['studies/klagenfurt_h1_spitzenzeiten/results', 'results', 'studies/studies/results']

    def find_result_dir(scenario_name):
        """Find the correct result directory"""
        for base in base_dirs:
            path = os.path.join(base, scenario_name)
            if os.path.exists(path):
                return path
        return None

    scenario1_dir = find_result_dir('klagenfurt_h1_spitzenzeiten_peak_morning')
    scenario2_dir = find_result_dir('klagenfurt_h1_spitzenzeiten_peak_afternoon')

    if not scenario1_dir or not scenario2_dir:
        print("Could not find result directories. Please verify the simulation completed successfully.")
        return

    # Load and process data
    try:
        users1, ops1 = load_data(scenario1_dir)
        df1 = aggregate_temporal(users1, ops1, interval_minutes=15)

        users2, ops2 = load_data(scenario2_dir)
        df2 = aggregate_temporal(users2, ops2, interval_minutes=15)
    except FileNotFoundError as e:
        print(f"Error: Could not load result files: {e}")
        return

    print("Data loaded successfully!")
    print(f"Morning peak requests: {len(users1):,}")
    print(f"Afternoon peak requests: {len(users2):,}")

    # Display temporal analysis
    print("=== TEMPORAL ANALYSIS ===")
    plot_temporal(df1, 'Klagenfurt H1 Spitzenzeiten Morning Peak')
    plt.show()
    plot_temporal(df2, 'Klagenfurt H1 Spitzenzeiten Afternoon Peak')
    plt.show()

if __name__ == "__main__":
    main()

