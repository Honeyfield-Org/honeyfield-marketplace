#!/usr/bin/env python3
"""Validiert das YAML-Frontmatter aller Skills (echter Parse, nicht nur grep).

Faengt z.B. eine unquotierte `description:` mit `: ` darin, die den strengen
YAML-Parser bricht und zur Laufzeit dazu fuehrt, dass Claude Code die Metadata
still verwirft (Skill triggert dann nicht). Prueft zusaetzlich das harte
1024-Zeichen-Limit der `description`: laenger -> Claude Web verwirft den Skill
still beim Einlesen (Claude Code ist toleranter und laedt ihn trotzdem, daher
faellt es lokal nicht auf). Default-Glob: plugins/*/skills/*/SKILL.md;
optional koennen Glob-Pattern als Argumente uebergeben werden.

Zusaetzlich: **Skill-Version-Drift-Guard** (git-diff-aware). Eine geaenderte
`SKILL.md` MUSS ihre skill-eigene `metadata.version` mit-erhoehen (zusaetzlich
zu den 3 Marketplace-Feldern, die `check_version_sync.py` prueft). Sonst
driftet die Skill-Version still. Der Guard vergleicht jede SKILL.md gegen eine
Base-Ref:
  - Base kommt aus `SKILL_VERSION_BASE` (in CI aus dem Event gesetzt) oder,
    lokal, aus `merge-base origin/main HEAD`.
  - Ist keine Base aufloesbar (Shallow-Clone ohne origin/main, kein git, ...),
    wird der Guard STILL uebersprungen (nie ein False-Positive-CI-Fehler).
  - Neue Skills (in der Base nicht vorhanden) werden nicht geflaggt.
"""
import glob
import os
import subprocess
import sys

import yaml


def parse_frontmatter(txt):
    """Return (fm_dict, error_str); fm_dict is None on error."""
    if not (txt.startswith("---\n") or txt.startswith("---\r\n")):
        return None, "kein Frontmatter (startet nicht mit ---)"
    parts = txt.split("---", 2)
    if len(parts) < 3:
        return None, "Frontmatter nicht geschlossen (kein zweites ---)"
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return None, "YAML-Frontmatter parst nicht: " + str(e).replace("\n", " ")
    if not isinstance(fm, dict):
        return None, "Frontmatter ist kein Mapping"
    return fm, None


def skill_version(fm):
    """metadata.version als str, oder None wenn nicht vorhanden."""
    if isinstance(fm, dict):
        meta = fm.get("metadata")
        if isinstance(meta, dict) and meta.get("version") is not None:
            return str(meta["version"])
    return None


def git(*args):
    """(returncode, stdout). returncode 127 wenn kein git."""
    try:
        r = subprocess.run(["git", *args], capture_output=True, text=True)
        return r.returncode, r.stdout
    except FileNotFoundError:
        return 127, ""


def resolve_base():
    """Base-Ref fuer den Drift-Vergleich, oder None (Guard skippen)."""
    env = os.environ.get("SKILL_VERSION_BASE", "").strip()
    if env:
        rc, _ = git("cat-file", "-e", env + "^{commit}")
        return env if rc == 0 else None
    rc, _ = git("rev-parse", "--verify", "--quiet", "origin/main")
    if rc != 0:
        return None
    rc, out = git("merge-base", "origin/main", "HEAD")
    return out.strip() or None


def changed_vs_base(base, path):
    """True wenn path zwischen base und Working Tree abweicht."""
    # git diff --quiet: rc 0 = keine Aenderung, 1 = Aenderung.
    rc, _ = git("diff", "--quiet", base, "--", path)
    return rc == 1


def version_at_base(base, path):
    """metadata.version des Files in der Base, oder None (neu / nicht lesbar)."""
    rc, out = git("show", f"{base}:{path}")
    if rc != 0:
        return None
    fm, err = parse_frontmatter(out)
    return None if err else skill_version(fm)


patterns = sys.argv[1:] or ["plugins/*/skills/*/SKILL.md"]
files = sorted(f for p in patterns for f in glob.glob(p))
all_errors = []

base = resolve_base()
drift_note = None
if base is None:
    drift_note = (
        "Version-Drift-Guard uebersprungen (keine aufloesbare Base; "
        "SKILL_VERSION_BASE oder origin/main noetig)."
    )

for f in files:
    errs = []
    txt = open(f, encoding="utf-8").read()
    fm, ferr = parse_frontmatter(txt)
    if ferr:
        errs.append(ferr)
    else:
        for key in ("name", "description"):
            val = fm.get(key)
            if not isinstance(val, str) or not val.strip():
                errs.append(f"'{key}' fehlt oder ist leer")
        desc = fm.get("description")
        if isinstance(desc, str) and len(desc) > 1024:
            errs.append(
                f"'description' zu lang: {len(desc)} Zeichen (max 1024) "
                "- Claude Web verwirft den Skill sonst still, "
                "Claude Code laedt ihn trotzdem"
            )
        if base is not None and changed_vs_base(base, f):
            cur_v = skill_version(fm)
            base_v = version_at_base(base, f)
            if base_v is not None and cur_v is not None and cur_v == base_v:
                errs.append(
                    f"SKILL.md geaendert, aber metadata.version nicht erhoeht "
                    f"(weiterhin {cur_v}) - bei Inhaltsaenderung die Skill-Version "
                    f"mitziehen [Base: {base}]"
                )
    if errs:
        all_errors += [f"{f}: {e}" for e in errs]
    else:
        print(f"OK: {f}")

if drift_note:
    print("\nHinweis:", drift_note)

if all_errors:
    print("\nFEHLER:")
    for e in all_errors:
        print(" -", e)
    sys.exit(1)
print(f"\n{len(files)} Skill(s) geprueft - Frontmatter valide")
