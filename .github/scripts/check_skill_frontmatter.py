#!/usr/bin/env python3
"""Validiert das YAML-Frontmatter aller Skills (echter Parse, nicht nur grep).

Faengt z.B. eine unquotierte `description:` mit `: ` darin, die den strengen
YAML-Parser bricht und zur Laufzeit dazu fuehrt, dass Claude Code die Metadata
still verwirft (Skill triggert dann nicht). Prueft zusaetzlich das harte
1024-Zeichen-Limit der `description`: laenger -> Claude Web verwirft den Skill
still beim Einlesen (Claude Code ist toleranter und laedt ihn trotzdem, daher
faellt es lokal nicht auf). Default-Glob: plugins/*/skills/*/SKILL.md;
optional koennen Glob-Pattern als Argumente uebergeben werden.
"""
import glob
import sys

import yaml

patterns = sys.argv[1:] or ["plugins/*/skills/*/SKILL.md"]
files = sorted(f for p in patterns for f in glob.glob(p))
all_errors = []
for f in files:
    errs = []
    txt = open(f, encoding="utf-8").read()
    if not (txt.startswith("---\n") or txt.startswith("---\r\n")):
        errs.append("kein Frontmatter (startet nicht mit ---)")
    else:
        parts = txt.split("---", 2)
        if len(parts) < 3:
            errs.append("Frontmatter nicht geschlossen (kein zweites ---)")
        else:
            try:
                fm = yaml.safe_load(parts[1])
                if not isinstance(fm, dict):
                    errs.append("Frontmatter ist kein Mapping")
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
            except yaml.YAMLError as e:
                errs.append("YAML-Frontmatter parst nicht: " + str(e).replace("\n", " "))
    if errs:
        all_errors += [f"{f}: {e}" for e in errs]
    else:
        print(f"OK: {f}")

if all_errors:
    print("\nFEHLER:")
    for e in all_errors:
        print(" -", e)
    sys.exit(1)
print(f"\n{len(files)} Skill(s) geprueft - Frontmatter valide")
