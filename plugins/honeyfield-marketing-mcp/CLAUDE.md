# CLAUDE.md — honeyfield-marketing-mcp

Dieses Plugin: Marketing-Ops-MCP (über `mcp.ads.honeyfield.at`) + DACH-Skills. Skills liegen unter `skills/<skill>/SKILL.md` (+ optional `references/`, `evals/`) und werden auto-discovered. **Diese Regeln gelten nur für Skills in diesem Plugin.**

## Pflicht für jeden Skill in diesem Plugin: Projekt-Kontext zuerst
Jeder Skill in `honeyfield-marketing-mcp` (Audit wie Creation) **muss** früh — in Schritt 0 / „Vorbereitung" — diesen Absatz enthalten (letzter Satz an die Aufgabe anpassbar):

> **Projekt-Kontext zuerst.** Liegt für dieses Projekt ein Projekt-Kontext vor — als **Projektwissen** in diesem Claude-Projekt oder als `projekt-kontext.md` im Arbeitsverzeichnis —, nutze ihn, bevor du fragst, und frage nur nach, was dort fehlt oder für diese Aufgabe spezifisch ist. Beachte gesetzte `compliance`-Flags als harte Leitplanke. Fehlt der Kontext, biete an, ihn per `projekt-kontext` anzulegen.

Der `projekt-kontext`-Skill erzeugt/pflegt dieses Fundament-Dokument (Frontmatter mit Stable Keys + Prosa). So muss kein Skill Markt/Marke/Ziele/Recht erneut abfragen. Speicherung ist plattformabhängig: **Claude.ai** → Projektwissen (manuell ablegen), **Claude Code** → `projekt-kontext.md` im Repo.

## Skill-Konventionen
- **Sprache:** Deutsch, imperativ, terse, daten-first, ehrlich über Grenzen. DACH-kalibriert (DE/AT/CH).
- **Frontmatter:** `name` (kebab-case), `description` (mit Trigger-Phrasen **und** Abgrenzung zu Schwester-Skills), `metadata.version`.
- **YAML-Footgun:** deutsche Anführungszeichen in der `description` immer als Paar „…" (öffnend U+201E, **schließend U+201D**) — **niemals** ASCII-`"` als Schließzeichen (bricht den YAML-Parser; der Skill triggert dann still nicht). Alternativ als `\"` escapen.
- **MCP-Tools** mit Bare-Name in Backticks nennen (`ads_*`, `ga4_*`, `sc_*`, `dfs_*`, `gbp_*`, `gtm_*`, `clarity_*`, `list_workspaces`).
- **Audit-Skill-Struktur:** Beleg-Stufen → Schritt 0 (inkl. Projekt-Kontext-Absatz + `list_workspaces`/`sources`-Check + Markt-Kalibrierung) → Phasen (Blocker zuerst) → DACH-Layer → Mythen → Output-Format → Operator (Schreib-Aktionen nur mit Dry-Run + Bestätigung) → Grenzen → Tools nach Phase → Verwandte Skills → Referenzen.
- **References/Evals:** Detail-Wissen in `references/*.md` (on-demand laden, hält SKILL.md schlank); `evals/evals.json` mit Trigger-/Defer-/Tool-Reality-Cases.

## Vor jedem Commit validieren (aus dem Repo-Root)
- `python3 .github/scripts/check_skill_frontmatter.py` — echter YAML-Parse aller Skills (läuft auch in CI `validate.yml`).
- `python3 -m json.tool plugins/honeyfield-marketing-mcp/skills/<skill>/evals/evals.json` — Evals valides JSON.
- `claude plugin validate plugins/honeyfield-marketing-mcp/` — Manifest.
- Beim Anlegen eines Skills, der Kontext konsumiert: prüfen, dass der Projekt-Kontext-Absatz drin ist und keine alten `kunden-kontext`-Referenzen übrig sind.
