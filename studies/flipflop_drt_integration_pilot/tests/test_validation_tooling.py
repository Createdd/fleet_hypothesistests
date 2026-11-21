"""Tests for the validation tooling (check_claims.py, key_figures.py) and the run_v2.py exit codes.

Run from the repository root:
    python -m unittest discover -s studies/flipflop_drt_integration_pilot/tests -v
"""
import contextlib
import io
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

STUDY_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDY_DIR))

import check_claims  # noqa: E402
import key_figures  # noqa: E402
import run_v2  # noqa: E402


class FormatTest(unittest.TestCase):
    def test_german_and_english_number_formats(self):
        f = check_claims.fmt_value
        self.assertEqual(f(0.867745, "de2"), "0,87")
        self.assertEqual(f(12.962654, "de1"), "13,0")
        self.assertEqual(f(471140, "de0"), "471.140")
        self.assertEqual(f(2601.2, "de0~100"), "2.600")
        self.assertEqual(f(104, "de0~10"), "100")
        self.assertEqual(f(15320, "en0"), "15,320")
        self.assertEqual(f(34.473644, "en1"), "34.5")
        self.assertEqual(f(1.21015, "en2"), "1.21")

    def test_invalid_format_and_missing_value_are_errors(self):
        with self.assertRaises(ValueError):
            check_claims.fmt_value(1.0, "xx1")
        with self.assertRaises(ValueError):
            check_claims.fmt_value(None, "de0")


class ClaimCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.figs = d / "kf.json"
        self.figs.write_text(json.dumps({"figures": {"zone_corr": 0.867745, "fleet": 150}}))
        # files must live under the repo root for the relative path in messages
        self.md = STUDY_DIR / "tests" / "_tmp_claims_test.md"

    def tearDown(self):
        self.md.unlink(missing_ok=True)
        self.tmp.cleanup()

    def _check(self, text, update=False):
        self.md.write_text(text)
        return check_claims.run(update=update, figures_file=self.figs, files=[self.md], docx=False)

    def test_matching_tag_passes(self):
        errors, counts = self._check("Korrelation <!--kf:zone_corr|de2-->0,87<!--/kf-->.")
        self.assertEqual(errors, [])
        self.assertEqual(list(counts.values()), [1])

    def test_stale_value_is_reported_and_update_rewrites_it(self):
        errors, _ = self._check("Korrelation <!--kf:zone_corr|de2-->0,86<!--/kf-->.")
        self.assertEqual(len(errors), 1)
        self.assertIn("shows '0,86', results say '0,87'", errors[0])
        self._check("Korrelation <!--kf:zone_corr|de2-->0,86<!--/kf-->.", update=True)
        self.assertEqual(self.md.read_text(), "Korrelation <!--kf:zone_corr|de2-->0,87<!--/kf-->.")

    def test_unknown_figure_and_tag_in_code_span_are_errors(self):
        errors, _ = self._check("<!--kf:nope|de0-->1<!--/kf--> and `x = <!--kf:fleet|de0-->150<!--/kf-->`")
        self.assertTrue(any("unknown figure 'nope'" in e for e in errors))
        self.assertTrue(any("tag inside code span" in e for e in errors))

    def test_docx_templates_render(self):
        self.assertEqual(check_claims.render("korreliert mit {zone_corr|de2}", {"zone_corr": 0.867745}), "korreliert mit 0,87")


class KeyFigureDiffTest(unittest.TestCase):
    def test_diff_reports_changed_missing_and_null_figures(self):
        problems = key_figures.diff({"a": 1.0, "b": 2.0, "c": None}, {"a": 1.0, "b": 2.5, "d": 3})
        self.assertEqual(len(problems), 3)
        self.assertTrue(any(p.startswith("b:") for p in problems))
        self.assertEqual(key_figures.diff({"a": 1.0000000001}, {"a": 1.0}), [])


class RunV2ExitCodeTest(unittest.TestCase):
    """Regression: run_v2.py exited 0 although scenarios failed, and accepted unknown --only names."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.results = d / "results"
        self.results.mkdir()
        self.scenarios = d / "scen.csv"
        self.scenarios.write_text("scenario_name,rq_file,op_fleet_composition\ngood,x.csv,default_vehtype:1\nbad,y.csv,default_vehtype:1\n")
        self.const = d / "const.yaml"
        self.const.write_text("x: 1\n")

    def tearDown(self):
        self.tmp.cleanup()

    def _main(self, *args, fake_run=None):
        argv = ["run_v2.py", str(self.scenarios), "--const-cfg", str(self.const), *args]
        fake_run = fake_run or (lambda *a, **k: None)
        with mock.patch.object(run_v2, "RESULTS_DIR", str(self.results)), mock.patch.object(sys, "argv", argv), \
                mock.patch.object(run_v2, "SCENARIO_DIR", self.tmp.name), \
                mock.patch.dict(sys.modules, {"run_examples": mock.Mock(run_scenarios=fake_run)}), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return run_v2.main()

    def _write_result(self, name, age_s=0):
        d = self.results / name
        d.mkdir(exist_ok=True)
        f = d / "standard_eval.csv"
        f.write_text("x\n")
        if age_s:
            t = time.time() - age_s
            os.utime(f, (t, t))

    def test_failed_scenario_gives_nonzero_exit(self):
        self.assertEqual(self._main(fake_run=lambda *a, **k: self._write_result("good")), 1)

    def test_all_scenarios_ok_gives_zero_exit(self):
        def ok(*a, **k):
            self._write_result("good")
            self._write_result("bad")
        self.assertEqual(self._main(fake_run=ok), 0)

    def test_stale_result_from_an_earlier_run_does_not_count(self):
        self._write_result("bad", age_s=3600)
        self.assertEqual(self._main(fake_run=lambda *a, **k: self._write_result("good")), 1)

    def test_unknown_only_name_is_rejected(self):
        self.assertEqual(self._main("--only", "goood"), 2)


if __name__ == "__main__":
    unittest.main()
