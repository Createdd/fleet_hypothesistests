import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def load_data(result_dir):
    # Load user and operations CSVs with actual filenames
    users = pd.read_csv(os.path.join(result_dir, '1_user-stats.csv'))
    ops   = pd.read_csv(os.path.join(result_dir, '2-0_op-stats.csv'))
    return users, ops

def aggregate_temporal(users, ops, interval_minutes=15):
    # Compute waiting time (pickup_time - rq_time)
    users['waiting_time'] = users['pickup_time'] - users['rq_time']

    # Convert request_time and op start_time to timedelta for resampling
    users['time'] = pd.to_timedelta(users['rq_time'], unit='s')
    ops['time']   = pd.to_timedelta(ops['start_time'], unit='s')

    # Aggregate user metrics per interval
    user_ts = users.set_index('time').resample(f'{interval_minutes}T').agg({
        'request_id': 'count',
        'waiting_time': 'mean'
    }).rename(columns={'request_id':'requests','waiting_time':'avg_wait_s'})

    # Fleet utilization: % of vehicles with occupancy>0 per interval
    ops['occupied'] = ops['occupancy'] > 0
    util = ops.groupby(pd.Grouper(key='time', freq=f'{interval_minutes}T')).occupied.mean() * 100
    util_ts = util.rename('util_pct')

    # Combine into one DataFrame
    df = pd.concat([user_ts, util_ts], axis=1).fillna(0)
    return df

def plot_temporal(df, scenario_name):
    fig, ax1 = plt.subplots(figsize=(10, 4))

    # Bar: requests per interval
    width = df.index.freq.delta.total_seconds() / 3600 * 0.8
    ax1.bar(df.index.total_seconds()/3600, df.requests,
            width=width, color='C0', alpha=0.6, label='Requests')
    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('Requests per Interval', color='C0')
    ax1.tick_params(axis='y', labelcolor='C0')

    # Line: avg waiting time and utilization
    ax2 = ax1.twinx()
    ax2.plot(df.index.total_seconds()/3600, df.avg_wait_s/60,
             'C1-o', label='Avg Wait (min)')
    ax2.plot(df.index.total_seconds()/3600, df.util_pct,
             'C2-s', label='Utilization (%)')
    ax2.set_ylabel('Avg Wait (min) & Util (%)', color='C1')
    ax2.tick_params(axis='y', labelcolor='C1')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1+lines2, labels1+labels2, loc='upper left')

    plt.title(f'Temporal Metrics for {scenario_name}')
    plt.tight_layout()
    plt.savefig(f'temporal_{scenario_name}.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python plot_munich_temporal.py <result_directory>")
        sys.exit(1)

    result_dir = sys.argv[1]
    scenario = os.path.basename(result_dir.rstrip('/'))
    users, ops = load_data(result_dir)
    df = aggregate_temporal(users, ops, interval_minutes=15)
    plot_temporal(df, scenario)
