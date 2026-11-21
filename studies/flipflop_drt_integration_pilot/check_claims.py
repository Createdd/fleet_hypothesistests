"""Check that every result figure quoted in the documentation matches results/key_figures.json.

Markdown files and notebook markdown cells mark each quoted result with an invisible tag:

    Korrelation <!--kf:zone_corr:de2-->0,87<!--/kf-->

`key` is a figure name from key_figures.json, `fmt` how it is written (":" as separator, never "|",
which would split a markdown table cell):
    de<N>   German number, N decimals, "." as thousands separator        (2.601 / 11,6 / 0,87)
    en<N>   English number, N decimals, "," as thousands separator       (15,320 / 34.5 / 0.87)
    ...~<K> round to the nearest multiple of K first                     (de0~100 -> 2.600)

Each tagged document is also rendered like GitHub does (pandoc, GFM): every tag must end up as a hidden
comment, no tag fragment may be visible, relative links must resolve. Without pandoc this check fails.

The Word report cannot carry tags; its quoted figures are listed as sentence templates in
DOCX_CLAIMS below and must appear verbatim in the document text.

Usage (from repo root):
  python studies/flipflop_drt_integration_pilot/check_claims.py            # check, exit 1 on any mismatch
  python studies/flipflop_drt_integration_pilot/check_claims.py --update   # rewrite tagged values in .md/.ipynb
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
STUDY_DIR = ROOT_DIR / "studies" / "flipflop_drt_integration_pilot"
KEY_FIGURES_FILE = STUDY_DIR / "results" / "key_figures.json"

TAGGED_FILES = [
    ROOT_DIR / "README.md",
    STUDY_DIR / "README.md",
    STUDY_DIR / "analysis" / "flipflop_consistency_test.ipynb",
    STUDY_DIR / "analysis" / "consortium_presentation_flipflop_validation.ipynb",
    STUDY_DIR / "analysis" / "flipflop_demand_model_validity.ipynb",
]
# minimum number of tags per file, so that silently deleting the tags is caught as well
MIN_TAGS = {"README.md": 15, "studies/flipflop_drt_integration_pilot/README.md": 25}

DOCX_FILE = STUDY_DIR / "FlipFlop_FleetPy_Kurzbericht_2026-11-14.docx"
DOCX_CLAIMS = [
    "Zugangszeit von {drt_access_share_pct|de0} % der ÖV-Zugangszeit",
    "Straßengraph aus der Graphenintegrations-Plattform (GIP) mit {network_nodes|de0~100} Knoten",
    "eine Fahrt über 5 km Luftlinie benötigt rund {network_5km_beeline_min|de0} Minuten",
    "an sieben Kalendertagen ({moia_requests_per_day_min|de0}–{moia_requests_per_day_max|de0} Fahrten je Tag)",
    "aus allen fünf stochastischen Ziehungen",
    "rund {ff_switchers_per_day_mean|de0~100} Wege je Tag innerhalb des Bediengebiets",
    "Umfang: {sweep_runs_defined|de0} Simulationsläufe mit Flottengrößen von {moia_fleet_min|de0} bis {moia_fleet_max|de0} Fahrzeugen",
    "bzw. {ff_fleet_min|de0} bis {ff_fleet_max|de0} Fahrzeugen (prognostizierte Nachfrage)",
    "maximal {assumed_wait_min|de1} Minuten Wartezeit",
    "korreliert mit {zone_corr|de2} mit jener der realen Fahrten",
    "erreichen {moia_implied_fleet_min|de0} bis {moia_implied_fleet_max|de0} Fahrzeuge einen Bedienungsgrad von mindestens 90 %",
    "Echte MOIA-Fahrten ({moia_requests_per_day_min|de0}–{moia_requests_per_day_max|de0})",
    "8 Fzg: {moia_w6_f8_served_pct|de0} %", "10 Fzg: {moia_w6_f10_served_pct|de0} %",
    "15 Fzg: {moia_w6_f15_served_pct|de0} %", "20 Fzg: {moia_w6_f20_served_pct|de0} %",
    "{moia_w6_largest_fleet_below_90|de0}–{moia_w6_fleet_reaching_90|de0} Fzg",
    "FlipFlop-Umsteiger (ca. {ff_switchers_per_day_mean|de0~100})",
    "40 Fzg: {ff_w6_f40_served_pct|de0} %", "60 Fzg: {ff_w6_f60_served_pct|de0} %",
    "100 Fzg: {ff_w6_f100_served_pct|de0} %", "150 Fzg: {ff_w6_f150_served_pct|de0} %",
    "ca. {ff_w6_fleet_max|de0} Fzg",
    "erst mit rund {ff_w6_fleet_max|de0} Fahrzeugen erreicht",
    "mit {equal_load_ff_served_pct|de0} % zu einem höheren Anteil bedient als die reale ({equal_load_moia_served_pct|de0} %)",
    "Wartezeit ≤ {assumed_wait_min|de1} Minuten und Fahrzeit ≤ {assumed_detour|de1}-fache Direktfahrzeit",
]

TAG_RE = re.compile(r"<!--kf:(?P<key>[a-z0-9_]+):(?P<fmt>[a-z]+\d(?:~\d+)?)-->(?P<text>.*?)<!--/kf-->", re.S)
FMT_RE = re.compile(r"^(?P<lang>de|en)(?P<dec>\d)(?:~(?P<step>\d+))?$")
PLACEHOLDER_RE = re.compile(r"\{(?P<key>[a-z0-9_]+)\|(?P<fmt>[a-z]+\d(?:~\d+)?)\}")


def fmt_value(value, fmt: str) -> str:
    m = FMT_RE.match(fmt)
    if not m:
        raise ValueError(f"unknown format {fmt!r}")
    if value is None:
        raise ValueError("figure is null")
    v = float(value)
    if m["step"]:
        step = int(m["step"])
        v = round(v / step) * step
    dec = int(m["dec"])
    s = f"{v:,.{dec}f}"  # 12,345.67
    if m["lang"] == "de":
        s = s.replace(",", "\0").replace(".", ",").replace("\0", ".")
    return s


def render(template: str, figs: dict) -> str:
    return PLACEHOLDER_RE.sub(lambda m: fmt_value(figs[m["key"]], m["fmt"]), template)


def text_units(path: Path):
    """(label, text) pairs that can carry tags: the whole file for markdown, each markdown cell for notebooks."""
    if path.suffix == ".ipynb":
        nb = json.loads(path.read_text())
        return [(f"cell {i}", "".join(c["source"])) for i, c in enumerate(nb["cells"]) if c["cell_type"] == "markdown"]
    return [("", path.read_text())]


def check_tags(path: Path, figs: dict, update: bool):
    errors, n_tags = [], 0
    units = text_units(path)
    new_units = []
    for label, text in units:
        def repl(m):
            nonlocal n_tags
            n_tags += 1
            key, fmt, shown = m["key"], m["fmt"], m["text"]
            where = f"{path.relative_to(ROOT_DIR)}{' ' + label if label else ''}"
            if key not in figs:
                errors.append(f"{where}: unknown figure '{key}'")
                return m.group(0)
            expected = fmt_value(figs[key], fmt)
            if shown != expected:
                errors.append(f"{where}: {key} shows '{shown}', results say '{expected}'")
                if update:
                    return f"<!--kf:{key}:{fmt}-->{expected}<!--/kf-->"
            return m.group(0)
        new_units.append(TAG_RE.sub(repl, text))
        # "|" inside a tag splits a markdown table cell and makes the tag visible
        for bad in re.findall(r"<!--kf:[^>]*\|[^>]*-->", text):
            errors.append(f"{path.relative_to(ROOT_DIR)}{' ' + label if label else ''}: '|' in tag {bad} (use ':')")
        # an HTML comment inside a `code span` is rendered literally, so a tag there would be visible
        for span in re.findall(r"`[^`\n]*`", text):
            if "<!--kf:" in span:
                errors.append(f"{path.relative_to(ROOT_DIR)}{' ' + label if label else ''}: tag inside code span {span}")
    if update and errors:
        if path.suffix == ".ipynb":
            nb = json.loads(path.read_text())
            md = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
            for cell, (_, old), new in zip(md, units, new_units):
                if old != new:
                    cell["source"] = new.splitlines(keepends=True)
            path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
        else:
            path.write_text(new_units[0])
    rel = str(path.relative_to(ROOT_DIR))
    if n_tags < MIN_TAGS.get(rel, 1):
        errors.append(f"{rel}: only {n_tags} tagged figures (expected at least {MIN_TAGS.get(rel, 1)})")
    return errors, n_tags


def docx_text(path: Path) -> str:
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    xml = re.sub(r"</w:p>", "\n", xml)
    return re.sub(r"<[^>]+>", "", xml)


def check_docx(figs: dict):
    text = docx_text(DOCX_FILE)
    errors = []
    for t in DOCX_CLAIMS:
        expected = render(t, figs)
        if expected not in text:
            errors.append(f"{DOCX_FILE.name}: expected text not found: '{expected}'")
    return errors, len(DOCX_CLAIMS)


def find_pandoc():
    for c in (os.environ.get("PANDOC"), shutil.which("pandoc"), str(Path.home() / "opt" / "anaconda3" / "bin" / "pandoc")):
        if c and Path(c).is_file():
            return c
    return None


def check_rendering(path: Path, pandoc):
    """What the reader sees: render like GitHub (GFM) and require that every tag ends up as a hidden
    comment, that no tag fragment is visible text, and that relative links resolve."""
    rel = str(path.relative_to(ROOT_DIR))
    if pandoc is None:
        return [f"{rel}: rendering NOT verified — pandoc not found (install it or set PANDOC)"]
    source = "\n\n".join(t for _, t in text_units(path))
    html = subprocess.run([pandoc, "-f", "gfm", "-t", "html"], input=source, capture_output=True, text=True, check=True).stdout
    errors = []
    n_src = len(TAG_RE.findall(source))
    n_open, n_close = html.count("<!--kf:"), html.count("<!--/kf-->")
    if n_open != n_src or n_close != n_src:
        errors.append(f"{rel}: {n_src} tags in the source but only {min(n_open, n_close)} render as hidden comments")
    visible = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    for frag in sorted(set(re.findall(r".{0,30}(?:kf:|&lt;!--|--&gt;).{0,30}", visible))):
        errors.append(f"{rel}: visible tag fragment in rendered output: …{frag}…")
    for target in re.findall(r"\]\(([^)\s]+)\)", source):
        t = target.split("#")[0]
        if t and not re.match(r"[a-z]+:", t) and not (path.parent / t).exists():
            errors.append(f"{rel}: broken link {target}")
    return errors


def run(update=False, figures_file=KEY_FIGURES_FILE, files=None, docx=True, rendering=True):
    figs = json.loads(Path(figures_file).read_text())["figures"]
    errors, counts = [], {}
    pandoc = find_pandoc() if rendering else None
    for f in files or TAGGED_FILES:
        e, n = check_tags(Path(f), figs, update)
        errors += e
        if rendering:
            errors += check_rendering(Path(f), pandoc)
        counts[str(Path(f).relative_to(ROOT_DIR))] = n
    if docx:
        e, n = check_docx(figs)
        errors += e
        counts[DOCX_FILE.name] = n
    return errors, counts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--update", action="store_true", help="rewrite tagged values in .md/.ipynb to the computed figures")
    args = ap.parse_args()
    errors, counts = run(update=args.update)
    for f, n in counts.items():
        print(f"  {n:3d} figures  {f}")
    if errors:
        verb = "updated" if args.update else "MISMATCH"
        print(f"\n{len(errors)} claim(s) {verb}:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 0 if args.update and all("shows" in e for e in errors) else 1
    print(f"all {sum(counts.values())} quoted figures match key_figures.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
