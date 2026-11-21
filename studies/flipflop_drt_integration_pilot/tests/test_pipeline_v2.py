"""Tests for the v2 consistency-test pipeline (prepare_demand_v2.py, evaluate_v2.py).

Standard library only (unittest), no extra dependency. Run from the repository root:

    python -m unittest discover -s studies/flipflop_drt_integration_pilot/tests -v

Unit tests use small synthetic inputs. The data-integrity tests read the locally generated
network/demand files (not in Git) and are skipped when those files are missing.
"""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import pandas as pd

STUDY_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = STUDY_DIR.parents[1]
sys.path.insert(0, str(STUDY_DIR))

import evaluate_v2  # noqa: E402
import prepare_demand_v2  # noqa: E402

NETWORK_DIR = ROOT_DIR / "data" / "networks" / "klagenfurt_gip" / "base"
DEMAND_DIR = ROOT_DIR / "data" / "demand" / "flipflop_v2" / "matched" / "klagenfurt_gip"
INIT_DIST_DIR = ROOT_DIR / "data" / "fleetctrl" / "initial_vehicle_distribution" / "klagenfurt_gip"


# --------------------------------------------------------------------------------------------
# prepare_demand_v2
# --------------------------------------------------------------------------------------------
def _nodes():
    # three nodes ~1 km apart along a line near Klagenfurt (lat 46.62)
    return pd.DataFrame({"node_index": [10, 11, 12], "pos_x": [14.30, 14.313, 14.326], "pos_y": [46.62, 46.62, 46.62]})


class SnapperTest(unittest.TestCase):
    def test_snaps_to_nearest_node_and_reports_metres(self):
        s = prepare_demand_v2.Snapper(_nodes())
        idx, d = s.snap([14.3001, 14.3255], [46.62, 46.6201])
        self.assertEqual(list(idx), [10, 12])
        # 0.0001 deg lon at 46.62 N ~ 7.6 m; 0.0005 lon + 0.0001 lat ~ 39 m
        self.assertAlmostEqual(d[0], 7.65, delta=0.2)
        self.assertTrue(30 < d[1] < 45)


class FinalizeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.patch = mock.patch.object(prepare_demand_v2, "OUT_DIR", Path(self.tmp.name))
        self.patch.start()
        self.snapper = prepare_demand_v2.Snapper(_nodes())

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def _run(self, df, max_snap_m=300.0):
        summary = []
        with contextlib.redirect_stdout(io.StringIO()):
            prepare_demand_v2.finalize(df, self.snapper, max_snap_m, "t", summary, {"source": "test"})
        return pd.read_csv(Path(self.tmp.name) / "t.csv"), summary[0]

    def test_filters_far_and_degenerate_trips_and_sorts_by_time(self):
        df = pd.DataFrame({
            "rq_time":   [500, 100, 300, 200],
            "lon_start": [14.300, 14.300, 14.300, 14.300],
            "lat_start": [46.620, 46.620, 46.620, 46.660],   # last one starts ~4.4 km away from every node
            "lon_end":   [14.326, 14.313, 14.3001, 14.313],  # third one snaps start and end to the same node
            "lat_end":   [46.620, 46.620, 46.620, 46.620],
        })
        out, summ = self._run(df)
        self.assertEqual(list(out.columns), ["request_id", "rq_time", "start", "end"])
        self.assertEqual(list(out["rq_time"]), [100, 500])          # sorted, filtered
        self.assertEqual(list(out["request_id"]), [0, 1])           # renumbered 0..n-1
        self.assertEqual(list(out["start"]), [10, 10])
        self.assertEqual(list(out["end"]), [11, 12])
        self.assertEqual((summ["rows_in"], summ["rows_out"]), (4, 2))

    def test_snap_limit_applies_to_both_endpoints(self):
        df = pd.DataFrame({"rq_time": [0], "lon_start": [14.300], "lat_start": [46.620],
                           "lon_end": [14.326], "lat_end": [46.6215]})   # end ~167 m off node 12
        self.assertEqual(len(self._run(df, max_snap_m=300)[0]), 1)
        self.assertEqual(len(self._run(df, max_snap_m=100)[0]), 0)

    def test_empty_input_writes_empty_file(self):
        df = pd.DataFrame({c: pd.Series(dtype=float) for c in ["rq_time", "lon_start", "lat_start", "lon_end", "lat_end"]})
        out, summ = self._run(df)
        self.assertEqual(len(out), 0)
        self.assertEqual(summ["rows_out"], 0)
        self.assertIsNone(summ["snap_p90_m"])


class MoiaFrameTest(unittest.TestCase):
    def test_frame_spans_origins_and_destinations(self):
        moia = pd.DataFrame({"origin_x": [1.0, 2.0], "destination_x": [0.5, 3.0],
                             "origin_y": [10.0, 11.0], "destination_y": [12.0, 9.0]})
        self.assertEqual(prepare_demand_v2.moia_frame(moia), (0.5, 3.0, 9.0, 12.0))


# --------------------------------------------------------------------------------------------
# evaluate_v2
# --------------------------------------------------------------------------------------------
STANDARD_EVAL = pd.DataFrame({"MoD_0": {
    "rides per veh rev hours": 5.0, "occupancy": 1.1, "% fleet utilization": 50.0,
    "% empty vkm": 20.0, "avg driving velocity [km/h]": 40.0, "total vkm": 1000.0}})


def _write_scenario(results_dir: Path, name: str, user_stats: pd.DataFrame):
    d = results_dir / name
    d.mkdir(parents=True)
    STANDARD_EVAL.to_csv(d / "standard_eval.csv")
    user_stats.to_csv(d / "1_user-stats.csv", index=False)
    return d


def _user_stats(rows):
    """rows: (served, wait_s, ivt_s, direct_s)"""
    return pd.DataFrame([{
        "request_id": i, "rq_time": 1000, "operator_id": 0 if served else np.nan,
        "pickup_time": 1000 + w if served else np.nan, "dropoff_time": 1000 + w + ivt if served else np.nan,
        "direct_route_travel_time": direct} for i, (served, w, ivt, direct) in enumerate(rows)])


class EvaluateScenarioTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.results = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_kpis_and_assumed_los_thresholds_are_inclusive(self):
        us = _user_stats([
            (True, 378, 600, 500),    # wait exactly 6.3 min, detour 1.2 -> within LOS
            (True, 379, 600, 500),    # wait 1 s too long -> served, not within LOS
            (True, 100, 700, 500),    # detour exactly 1.4 -> within LOS
            (True, 100, 701, 500),    # detour > 1.4 -> not within LOS
            (False, 0, 0, 500),       # not served
        ])
        d = _write_scenario(self.results, "v2w6_ff_draw1_f40", us)
        r = evaluate_v2.evaluate_scenario(d, wait_threshold_s=378, detour_threshold=1.4)
        self.assertEqual((r["variant"], r["source"], r["set"], r["fleet"]), ("w6", "ff", "draw1", 40))
        self.assertEqual(r["requests"], 5)
        self.assertAlmostEqual(r["served_pct"], 80.0)
        self.assertAlmostEqual(r["served_within_assumed_los_pct"], 40.0)
        self.assertAlmostEqual(r["rides_per_veh_h"], 5.0)

    def test_scenario_name_parsing(self):
        cases = {"v2_moia_day3_f15": ("", "moia", "day3", 15),
                 "v2_probe_moia_day0_f10": ("", "moia", "day0", 10),
                 "v2w6_ff_draw5_f150": ("w6", "ff", "draw5", 150)}
        for name, expected in cases.items():
            m = evaluate_v2.NAME_RE.match(name)
            self.assertIsNotNone(m, name)
            self.assertEqual((m["variant"] or "", m["source"], m["set"], int(m["fleet"])), expected)
        self.assertIsNone(evaluate_v2.NAME_RE.match("audit_v2_moia_day0_f10"))

    def test_fleet_aggregate_keeps_operating_variants_apart(self):
        """Regression: the per-fleet console summary must not average the standard (8 min) and
        the assumed-quality (w6) configuration into one row (main() docstring: aggregate across
        days / draws only)."""
        all_served = _user_stats([(True, 60, 500, 500)] * 4)
        half_served = _user_stats([(True, 60, 500, 500)] * 2 + [(False, 0, 0, 500)] * 2)
        _write_scenario(self.results, "v2_ff_draw1_f40", all_served)     # standard: 100 %
        _write_scenario(self.results, "v2w6_ff_draw1_f40", half_served)  # assumed quality: 50 %
        out = io.StringIO()
        argv = ["evaluate_v2.py", "--pattern", "v2*", "--out", str(self.results / "eval.csv")]
        with mock.patch.object(evaluate_v2, "RESULTS_DIR", self.results), mock.patch.object(sys, "argv", argv), \
                contextlib.redirect_stdout(out):
            evaluate_v2.main()
        summary = out.getvalue().split("per fleet size")[1]
        self.assertNotIn("75.0", summary, "standard and w6 runs were averaged together:\n" + summary)
        self.assertIn("100.0", summary)
        self.assertIn("50.0", summary)


# --------------------------------------------------------------------------------------------
# data integrity of the locally generated pipeline outputs (skipped if not generated)
# --------------------------------------------------------------------------------------------
@unittest.skipUnless((NETWORK_DIR / "nodes.csv").exists() and DEMAND_DIR.exists(), "v2 network/demand not generated locally")
class GeneratedDataIntegrityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = pd.read_csv(NETWORK_DIR / "nodes.csv")
        cls.edges = pd.read_csv(NETWORK_DIR / "edges.csv")

    def test_network_is_one_strongly_connected_component(self):
        from scipy.sparse import coo_matrix
        from scipy.sparse.csgraph import connected_components
        n = len(self.nodes)
        self.assertEqual(list(self.nodes["node_index"]), list(range(n)))
        g = coo_matrix((np.ones(len(self.edges)), (self.edges["from_node"], self.edges["to_node"])), shape=(n, n))
        n_comp, _ = connected_components(g, directed=True, connection="strong")
        self.assertEqual(n_comp, 1)

    def test_edges_have_positive_length_and_travel_time(self):
        self.assertTrue((self.edges["distance"] > 0).all())
        self.assertTrue((self.edges["travel_time"] > 0).all())
        self.assertFalse(self.edges.duplicated(["from_node", "to_node"]).any())

    def test_demand_files_reference_valid_nodes_within_one_day(self):
        files = sorted(DEMAND_DIR.glob("*.csv"))
        self.assertGreater(len(files), 0)
        valid = set(self.nodes["node_index"])
        for f in files:
            with self.subTest(file=f.name):
                d = pd.read_csv(f)
                self.assertTrue(d["start"].isin(valid).all() and d["end"].isin(valid).all())
                self.assertFalse((d["start"] == d["end"]).any())
                self.assertTrue(d["rq_time"].between(0, 86399).all())
                self.assertTrue(d["rq_time"].is_monotonic_increasing)
                self.assertEqual(list(d["request_id"]), list(range(len(d))))

    def test_vehicle_start_distributions_are_probability_vectors(self):
        for name in ["uniform.csv", "moia_origin_density.csv"]:
            with self.subTest(file=name):
                p = pd.read_csv(INIT_DIST_DIR / name)
                self.assertEqual(len(p), len(self.nodes))
                self.assertTrue((p["probability"] > 0).all())
                self.assertAlmostEqual(p["probability"].sum(), 1.0, places=9)


if __name__ == "__main__":
    unittest.main()
