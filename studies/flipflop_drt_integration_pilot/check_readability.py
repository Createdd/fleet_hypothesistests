"""Can the repository be read? Checks every tracked Markdown file and notebook the way a reader sees it.

For each tracked *.md and *.ipynb (notebook: its markdown cells):
  * rendered like GitHub (pandoc, GFM): no raw HTML/comment fragments visible as text
  * every relative link and image resolves to a file or folder that exists AND is tracked in git
    (a file that only exists locally is missing on GitHub)
  * notebooks are valid nbformat and carry no stored error output
Without pandoc the check fails ("not verified" is not a pass).

Usage (from repo root):
  python studies/flipflop_drt_integration_pilot/check_readability.py
"""
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

STUDY_DIR = Path(__file__).resolve().parent
ROOT_DIR = STUDY_DIR.parents[1]
sys.path.insert(0, str(STUDY_DIR))
from check_claims import find_pandoc  # noqa: E402

LINK_RE = re.compile(r"(!?)\[[^\]]*\]\(<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\)")
IMG_TAG_RE = re.compile(r"<img[^>]+src=\"([^\"]+)\"")
VISIBLE_RAW_RE = re.compile(r".{0,30}(?:&lt;!--|--&gt;|&lt;/?(?:div|img|br|details|summary|p|a|table|tr|td)\b).{0,30}")


def tracked_files():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT_DIR, capture_output=True, text=True, check=True).stdout
    return {l for l in out.splitlines() if l}


def markdown_of(path: Path):
    if path.suffix == ".ipynb":
        import nbformat
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        return "\n\n".join(c.source for c in nb.cells if c.cell_type == "markdown"), nb
    return path.read_text(errors="replace"), None


def problems_in(path: Path, pandoc, tracked):
    rel = str(path.relative_to(ROOT_DIR))
    try:
        text, nb = markdown_of(path)
    except Exception as e:  # noqa: BLE001  (an unreadable notebook is a finding)
        return [f"{rel}: notebook invalid ({type(e).__name__}: {str(e)[:80]})"]
    out = []
    html = subprocess.run([pandoc, "-f", "gfm", "-t", "html"], input=text, capture_output=True, text=True, check=True).stdout
    visible = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    out += [f"{rel}: visible raw markup …{m}…" for m in sorted(set(VISIBLE_RAW_RE.findall(visible)))]
    targets = [(k, t) for k, t in LINK_RE.findall(text)] + [("!", t) for t in IMG_TAG_RE.findall(text)]
    tracked_dirs = {str(Path(f).parent) for f in tracked} | {str(p) for f in tracked for p in Path(f).parents}
    for kind, target in targets:
        t = unquote(target.split("#")[0].split("?")[0])
        if not t or re.match(r"[a-z][a-z0-9+.-]*:", t):
            continue
        p = (ROOT_DIR / t.lstrip("/")) if t.startswith("/") else (path.parent / t)
        what = "image" if kind == "!" else "link"
        if not p.exists():
            out.append(f"{rel}: broken {what} {target}")
            continue
        r = Path(p.resolve()).relative_to(ROOT_DIR.resolve()) if str(p.resolve()).startswith(str(ROOT_DIR.resolve())) else None
        if r is not None and str(r) not in tracked and str(r) not in tracked_dirs:
            out.append(f"{rel}: {what} target exists only locally, not in git (missing on GitHub): {target}")
    if nb is not None:
        n_err = sum(1 for c in nb.cells if c.cell_type == "code" and any(o.get("output_type") == "error" for o in c.get("outputs", [])))
        if n_err:
            out.append(f"{rel}: {n_err} code cell(s) with stored error output")
    return out


def run():
    pandoc = find_pandoc()
    tracked = tracked_files()
    docs = sorted(ROOT_DIR / f for f in tracked if f.endswith((".md", ".ipynb")) and (ROOT_DIR / f).exists())
    if pandoc is None:
        return [f"rendering of {len(docs)} documents NOT verified — pandoc not found (install it or set PANDOC)"], len(docs)
    errors = []
    for d in docs:
        errors += problems_in(d, pandoc, tracked)
    return errors, len(docs)


def main():
    errors, n = run()
    if errors:
        print(f"{len(errors)} readability problem(s) in {n} documents:\n  " + "\n  ".join(errors), file=sys.stderr)
        return 1
    print(f"all {n} tracked documents render cleanly; all links and images resolve to tracked files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
