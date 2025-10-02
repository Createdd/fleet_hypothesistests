# %% [markdown]
# Klagenfurt Zone & Data Preparation Notebook
# This notebook creates a multi-zone system for Klagenfurt, generates network nodes/edges, demand requests, and computes fleet distribution.

# %%
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import MultiLineString
from sklearn.cluster import KMeans
import networkx as nx

# %%
# 1. Load Klagenfurt network geometry
network = gpd.read_file("klagenfurt_network.gpkg")

# %%
# 2. Build nodes and edges from network
nodes_list = []
edges_list = []
node_id = 0
node_lookup = {}

def process_line(line):
    global node_id
    coords = list(line.coords)
    start, end = coords[0], coords[-1]
    for coord in (start, end):
        if coord not in node_lookup:
            node_lookup[coord] = node_id
            nodes_list.append({
                'node_index': node_id,
                'is_stop_only': 0,
                'pos_x': coord[0],
                'pos_y': coord[1]
            })
            node_id += 1
    o = node_lookup[start]
    d = node_lookup[end]
    length = line.length
    return o, d, length

for _, row in network.iterrows():
    geom = row.geometry
    parts = geom.geoms if isinstance(geom, MultiLineString) else [geom]
    for part in parts:
        o, d, length = process_line(part)
        dist_m = length * 111000
        tt_s = max(30, dist_m / (50_000/3600))
        edges_list.append({
            'from_node': o,
            'to_node': d,
            'distance': dist_m,
            'travel_time': tt_s,
            'source_edge_id': np.nan
        })

nodes_df = pd.DataFrame(nodes_list)
edges_df = pd.DataFrame(edges_list, columns=[
    'from_node','to_node','distance','travel_time','source_edge_id'
])

nodes_df.to_csv('data/networks/klagenfurt/base/nodes.csv', index=False)
edges_df.to_csv('data/networks/klagenfurt/base/edges.csv', index=False)

print(f"Nodes: {len(nodes_df)}, Edges: {len(edges_df)}")

# %%
# 3. Create multi-zone mapping via K-Means (5 zones)
coords = nodes_df[['pos_x','pos_y']].values
kmeans = KMeans(n_clusters=5, random_state=0).fit(coords)
nodes_df['zone_id'] = kmeans.labels_ + 1
nodes_df['is_centroid'] = 0
nodes_df['is_boarding_node'] = 1

zone_mapping = nodes_df[['node_index','zone_id','is_centroid','is_boarding_node']]
zone_mapping.to_csv('data/zones/klagenfurt/base/node_zone_info.csv', index=False)
print(f"Created zone mapping with {zone_mapping.zone_id.nunique()} zones")

# %%
# 4. Create demand requests sample (100 requests)
np.random.seed(42)
demand_data = []
for i in range(100):
    origin = np.random.choice(nodes_df['node_index'])
    destination = np.random.choice(nodes_df['node_index'])
    trip_time = np.random.randint(25200, 32400)
    demand_data.append({
        'Unnamed: 0': float(i),
        'request_id': float(i),
        'rq_time': float(trip_time),
        'start': float(origin),
        'end': float(destination),
        'earliest_pickup_time': float(trip_time)
    })

demand_df = pd.DataFrame(demand_data)
demand_df.to_csv(
    'data/demand/klagenfurt/matched/klagenfurt/demand_requests.csv',
    index=False
)
print(f"Created {len(demand_df)} demand requests")

# %%
# 5. Verify connectivity and drop unreachable zones
edges = pd.read_csv('data/networks/klagenfurt/base/edges.csv')
zones  = pd.read_csv('data/zones/klagenfurt/base/node_zone_info.csv')

G = nx.DiGraph()
for _, r in edges.iterrows():
    G.add_edge(int(r.from_node), int(r.to_node), weight=r.travel_time)

lengths = nx.single_source_dijkstra_path_length(G, source=0, weight='weight')
unreachable = set(zones.node_index) - set(lengths.keys())
if unreachable:
    print("Dropping unreachable zones:", unreachable)
    zones = zones[~zones.node_index.isin(unreachable)]
    zones.to_csv('data/zones/klagenfurt/base/node_zone_info.csv', index=False)
else:
    print("All zones reachable.")

# %%
# 6. Compute and print vehicle distribution per zone (200 vehicles)
zones_ids = pd.read_csv('data/zones/klagenfurt/base/node_zone_info.csv')['zone_id'].unique()
n_zones = len(zones_ids)
vehicles_per_zone = 200 // n_zones
extra = 200 % n_zones

comp = {
    str(z): vehicles_per_zone + (1 if i < extra else 0)
    for i, z in enumerate(zones_ids)
}
print("Vehicle distribution per zone:", comp)

# %% 7. Write veh_200.csv in Munich style
import os
import numpy as np
import pandas as pd

# Load node–zone info and your custom fleet composition
zones = pd.read_csv('data/zones/klagenfurt/base/node_zone_info.csv')
fleet_comp = {'1': 40, '2': 40, '3': 40, '4': 40, '5': 40}

# Build vehicle records
records = []
veh_id = 0
for zone_str, count in fleet_comp.items():
    zone_id = int(zone_str)
    nodes = zones.loc[zones['zone_id'] == zone_id, 'node_index'].values
    starts = np.random.choice(nodes, size=count, replace=True)
    for init_node in starts:
        records.append((veh_id, int(init_node)))
        veh_id += 1

veh_df = pd.DataFrame(records)

# Ensure output directory exists
out_dir = 'data/vehicles'
os.makedirs(out_dir, exist_ok=True)

# Write headerless CSV named 'veh_200.csv'
file_path = os.path.join(out_dir, 'veh_200.csv')
veh_df.to_csv(file_path, index=False, header=False)

print(f"Wrote {len(records)} vehicles to {file_path}")
