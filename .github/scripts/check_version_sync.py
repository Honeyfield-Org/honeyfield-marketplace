#!/usr/bin/env python3
"""Erzwingt die Versions-Konsistenz, an der der Org-Marketplace-Sync haengt.

Hintergrund (realer Incident): Der Org-Marketplace synct von `main` und erkennt
ein Plugin-Update **nur an der Version im marketplace.json-Plugin-Eintrag**. Laeuft
diese Zahl gegenueber der Quelle der Wahrheit (`<source>/.claude-plugin/plugin.json`)
auseinander, sieht der Katalog kein Update — neue Skills (z.B. google-ads-audit)
kommen beim Client nie an, obwohl sie auf `main` liegen.

Harte Invarianten, die dieser Check erzwingt:
  fuer jedes Plugin in marketplace.json:
    marketplace.json plugins[].version  ==  <source>/.claude-plugin/plugin.json version
    <source>/.codex-plugin/plugin.json version == <source>/.claude-plugin/plugin.json version

Zusaetzlicher harter Check (fuehrt ebenfalls zu exit 1): metadata.version
(Katalog-Version) muss mindestens so hoch sein wie die hoechste Plugin-Version —
sonst hinkt der Katalog hinterher.
"""
import json
import os
import sys


def parse_semver(v):
    """'1.3.0' -> (1, 3, 0); nicht-numerische Teile -> Vergleich faellt auf String zurueck."""
    try:
        return tuple(int(x) for x in str(v).split("."))
    except (ValueError, AttributeError):
        return None


def main():
    mp_path = ".claude-plugin/marketplace.json"
    if not os.path.isfile(mp_path):
        print(f"FEHLER: {mp_path} nicht gefunden", file=sys.stderr)
        return 1

    with open(mp_path, encoding="utf-8") as f:
        mp = json.load(f)

    errors = []
    plugin_versions = []

    for entry in mp.get("plugins", []):
        name = entry.get("name", "<ohne name>")
        mp_version = entry.get("version")
        source = entry.get("source", "")
        pj_path = os.path.join(source, ".claude-plugin", "plugin.json")

        if not os.path.isfile(pj_path):
            errors.append(f"{name}: plugin.json nicht gefunden unter {pj_path}")
            continue

        with open(pj_path, encoding="utf-8") as f:
            pj_version = json.load(f).get("version")

        codex_pj_path = os.path.join(source, ".codex-plugin", "plugin.json")
        if not os.path.isfile(codex_pj_path):
            errors.append(f"{name}: Codex plugin.json nicht gefunden unter {codex_pj_path}")
            continue
        with open(codex_pj_path, encoding="utf-8") as f:
            codex_pj_version = json.load(f).get("version")

        if mp_version != pj_version:
            errors.append(
                f"{name}: Versions-DRIFT — marketplace.json={mp_version!r} "
                f"!= plugin.json={pj_version!r}. "
                f"Der Org-Sync liest marketplace.json; ohne Angleich bleibt das "
                f"Update beim Client unsichtbar."
            )
        else:
            print(f"OK: {name} @ {pj_version} (plugin.json == marketplace.json)")

        if codex_pj_version != pj_version:
            errors.append(
                f"{name}: Versions-DRIFT — .codex-plugin={codex_pj_version!r} "
                f"!= .claude-plugin={pj_version!r}."
            )
        else:
            print(f"OK: {name} @ {pj_version} (Codex == Claude)")

        pv = parse_semver(pj_version)
        if pv is not None:
            plugin_versions.append((pv, pj_version))

    # Harter Check: Katalog-Version darf nicht hinter der hoechsten Plugin-Version liegen.
    meta_version = mp.get("metadata", {}).get("version")
    meta_sv = parse_semver(meta_version)
    if meta_sv is not None and plugin_versions:
        highest_sv, highest_str = max(plugin_versions)
        if meta_sv < highest_sv:
            errors.append(
                f"metadata.version={meta_version!r} liegt unter der hoechsten "
                f"Plugin-Version={highest_str!r}. Katalog-Version mitziehen, "
                f"damit der Marketplace-Eintrag die Aktualitaet widerspiegelt."
            )

    if errors:
        print("\nFEHLER:")
        for e in errors:
            print(" -", e)
        print(
            "\nFix: alle vier Felder zusammen erhoehen — "
            "plugin.json.version, marketplace.json plugins[].version (== plugin.json), "
            ".codex-plugin/plugin.json.version und metadata.version (Katalog).",
        )
        return 1

    print(f"\n{len(mp.get('plugins', []))} Plugin(s) geprueft - Versionen konsistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
