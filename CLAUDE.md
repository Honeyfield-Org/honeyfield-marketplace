# CLAUDE.md — honeyfield-marketplace

Marketplace-Repo. Plugins unter `plugins/<plugin>/`; Skills unter `plugins/<plugin>/skills/<skill>/SKILL.md` (+ optional `references/`, `evals/`), auto-discovered. **Die Konventionen unten gelten für das Plugin `honeyfield-marketing-mcp`** — weitere Plugins können eigene definieren.

## `honeyfield-marketing-mcp` — Pflicht für jeden Skill: Projekt-Kontext zuerst
Jeder Kontext-konsumierende Skill **im Plugin `honeyfield-marketing-mcp`** (alle außer `projekt-kontext` selbst) **muss** früh — in Schritt 0 / „Vorbereitung" — diesen Absatz enthalten (Kernstruktur und `compliance`-Satz wörtlich; aufgabenspezifische Einschübe — welche Kontext-Felder für die Aufgabe zählen, knappe Fallback-Fragen — und ein angepasster letzter Satz sind erlaubt):

> **Projekt-Kontext zuerst.** Liegt für dieses Projekt ein Projekt-Kontext vor — als **Projektwissen** in diesem Claude-Projekt oder als `projekt-kontext.md` im Arbeitsverzeichnis —, nutze ihn, bevor du fragst, und frage nur nach, was dort fehlt oder für diese Aufgabe spezifisch ist. Beachte gesetzte `compliance`-Flags als harte Leitplanke. Fehlt der Kontext, biete an, ihn per `projekt-kontext` anzulegen.

Der `projekt-kontext`-Skill erzeugt/pflegt dieses Fundament-Dokument (Frontmatter mit Stable Keys + Prosa). So muss kein Skill Markt/Marke/Ziele/Recht erneut abfragen. Speicherung ist plattformabhängig: **Claude.ai** → Projektwissen (manuell ablegen), **Claude Code** → `projekt-kontext.md` im Repo. Ausnahme: `projekt-kontext` selbst (Foundation) — dort ersetzt Schritt 1 (Existenz prüfen, updaten statt neu) den Absatz; der wörtliche Absatz wäre zirkulär.

## Skill-Konventionen (`honeyfield-marketing-mcp`)
- **Sprache:** Deutsch, imperativ, terse, daten-first, ehrlich über Grenzen. DACH-kalibriert (DE/AT/CH). **Persona-Ausnahme:** Die Eröffnung eines Skills (Rollen-/Zielabsätze vor der ersten Sektion) darf die Rolle in zweiter Person setzen („Du bist ein …-Spezialist”) — etabliertes Muster über alle Skills des Plugins; ab der ersten Sektion gilt Imperativ/Infinitiv.
- **Frontmatter:** `name` (kebab-case), `description` (mit Trigger-Phrasen **und** Abgrenzung zu Schwester-Skills), `metadata.version`.
- **YAML-Footgun:** deutsche Anführungszeichen in der `description` immer als Paar „…" (öffnend U+201E, **schließend U+201D**) — **niemals** ASCII-`"` als Schließzeichen (bricht den YAML-Parser; der Skill triggert dann still nicht). Alternativ als `\"` escapen.
- **`description`-Länge: hartes Limit 1024 Zeichen.** Länger → **Claude Web verwirft den Skill still beim Einlesen** (Claude Code ist toleranter und lädt ihn trotzdem, also fällt es lokal nicht auf — der Skill kommt beim Kunden nie an). Ziel ~950 Zeichen mit Marge. `check_skill_frontmatter.py` erzwingt das Limit (CI). Genau dieser Fall ließ `google-ads-audit` in Claude Web verschwinden, obwohl auf `main` + valide.
- **MCP-Tools** mit Bare-Name in Backticks nennen (u.a. `ads_*`, `ga4_*`, `sc_*`, `dfs_*`, `gbp_*`, `gtm_*`, `clarity_*`, `list_workspaces` — nur Beispiele, nicht vollständig). Einzige vollständige Quelle — Tool-Inventar nach Domäne mit R/W-Markierung: `plugins/honeyfield-marketing-mcp/references/tool-map.md`. Muster für Schreib-Aktionen (read→preview→confirm, Hochrisiko-/irreversibel-Liste): `references/write-guardrails.md`.
- **Skill-Struktur nach Typ.** Gemeinsam für alle: Beleg-Stufen, Schritt 0 (Projekt-Kontext-Absatz + `list_workspaces`/`sources`-Check + Markt-Kalibrierung), DACH-Layer, `evals/`, „Verwandte Skills". Der Aufbau danach hängt vom Typ ab:
  - **Audit-Skills** (`google-ads-audit`, `seo-audit`, `geo-audit`, `tracking-check`): → Phasen (Blocker zuerst) → DACH-Layer → Mythen → Output-Format → **Operator** (Schreib-Aktionen nur mit Dry-Run + Bestätigung) → Grenzen → Tools nach Phase → Verwandte Skills → Referenzen.
  - **Creation-Skills** (`ad-creative`): **Modi** statt Blocker-Phasen (z.B. neu generieren / aus Performance iterieren) → Ehrlichkeits-Modell aus der Tool-Reality → Output → **Operator** (schreibt nur nach Bestätigung, z.B. Anzeigen als `PAUSED`) → Grenzen.
  - **Report-Hubs** (`wochenreport`): **read-only — kein Operator**. Orchestrieren statt duplizieren: Kern-KPIs je Kanal ziehen, bei Auffälligkeiten auf den passenden Audit-Skill **verweisen**, nicht selbst tief diagnostizieren.
- **References/Evals:** Detail-Wissen in `references/*.md` (on-demand laden, hält SKILL.md schlank); `evals/evals.json` mit Trigger-/Defer-/Tool-Reality-Cases. **Jeder Skill braucht `evals/`** — fehlt es, ist nie geprüft, ob der Skill korrekt triggert und gegen die Schwester-Skills defert.

## Skill-Schnitt — ein Topic pro Skill, kein Funktions-Suffix
Wie ein neuer Skill geschnitten wird (Entscheidung 2026-06-30, abgeleitet vom Referenz-Marketplace `marketingskills`, der Funktions-Suffixe in v2 aktiv zurückbaute: `paid-ads`→`ads`, `analytics-tracking`→`analytics`, `page-cro`+`form-cro`→`cro`):

- **Topic-Skills bündeln Diagnose + Fix.** Ein Skill pro Kanal/Thema (`google-ads-audit`, `seo-audit`, `geo-audit`), der diagnostiziert **und** die behebbaren Punkte als Operator (Dry-Run + Bestätigung) umsetzt. Audit und Umsetzung **nicht** auf zwei Skills aufteilen — sie teilen Tools, Metriken und Kontext.
- **Foundation:** `projekt-kontext` liefert den geteilten Markt-/Marke-/Ziele-/Recht-Kontext, den jeder Skill zuerst liest.
- **Reports nur als Cross-Topic-Hub.** Ein Report rechtfertigt einen eigenen Skill **nur**, wenn er kanalübergreifend aggregiert (`wochenreport` über Ads + SEO + GEO). Ein Single-Topic-Report (nur Ads) gehört als Abschnitt in den Topic-Skill, **nicht** als `<topic>-report` daneben.
- **Kein Funktions-Suffix-Wildwuchs.** Niemals `<topic>-audit` + `<topic>-report` + `<topic>-build` nebeneinander. Funktion (audit/report/build) lebt **im** Topic-Skill, nicht im Namen.
- **Splitten nur nach Deliverable, nicht nach Funktion.** Ein Topic erst aufteilen, wenn ein klar **anderes Artefakt** entsteht (z.B. Massen-Anzeigen-Generierung neben dem Ads-Audit) — dann nach dem Output benennen (`ad-creative`), nicht `ads-build`. Auslöser: anderes Deliverable **oder** SKILL.md wird zu groß (~>500 Zeilen). Bei starker Überlappung **mergen** statt nebeneinanderstellen.
- **Unser Vorteil ggü. reinen Wissens-/Checklisten-Skills** (wie `marketingskills`): echte MCP-Daten + sichere Write-Operatoren + Beleg-Stufen + DACH-Kalibrierung. Das ist der Qualitätsmaßstab pro Skill — nicht die Skill-Anzahl. Tiefe schlägt Breite.

## Vor jedem Commit validieren
- `python3 .github/scripts/check_skill_frontmatter.py` — echter YAML-Parse aller Skills (läuft auch in CI `validate.yml`).
- `python3 .github/scripts/check_version_sync.py` — `plugin.json`-Version == marketplace-Plugin-Eintrag für jedes Plugin (läuft auch in CI). Der Guard gegen den Sync-Drift.
- `python3 -m json.tool plugins/honeyfield-marketing-mcp/skills/<skill>/evals/evals.json` — Evals valides JSON.
- `python3 -m json.tool plugins/<plugin>/.mcp.json` — MCP-Config valides JSON (CI prüft alle `plugins/*/.mcp.json`; `honeyfield-eurlex-mcp`/`honeyfield-ris-mcp` bestehen nur aus `.mcp.json` + `plugin.json`).
- `claude plugin validate plugins/<plugin>/` — Manifest, für **jedes** geänderte Plugin (CI loopt über alle `plugins/*/`).
- Beim Anlegen eines Skills, der Kontext konsumiert: prüfen, dass der Projekt-Kontext-Absatz drin ist und keine alten `kunden-kontext`-Referenzen übrig sind.
- **Inhaltliche Plugin-Änderung** (neuer/geänderter Skill, References, MCP-Config)? → Version in **allen drei Feldern** erhöht (siehe „Release & Org-Marketplace-Sync") — sonst synct der Org-Marketplace nicht.

## Release & Org-Marketplace-Sync
Der Org-Marketplace in Claude.ai synct **von `main`** und erkennt ein Update **nur an erhöhten Versionsnummern**. Drei Dinge gehen sonst immer wieder schief:

1. **Inhalt geändert, Version nicht erhöht → kein Sync.** Jede inhaltliche Änderung an einem Plugin (neuer Skill, geänderte `SKILL.md`/References, MCP-Config) **muss** mit einem Version-Bump einhergehen. Ohne Bump sieht der Sync keine Änderung — auch manuelles „Update" in den Org-Settings bringt dann nichts.
2. **Drei Versionsfelder, die zusammen steigen** (laufen sonst auseinander — `marketplace.json` wird am häufigsten vergessen, weil die Quelle der Wahrheit in `plugin.json` liegt):
   - `plugins/<plugin>/.claude-plugin/plugin.json` → `version` — Quelle der Wahrheit fürs Plugin.
   - `.claude-plugin/marketplace.json` → der `version` des Plugin-Eintrags in `plugins[]` — **muss exakt = `plugin.json` sein.**
   - `.claude-plugin/marketplace.json` → `metadata.version` — Katalog-Version, bei jeder Katalog-Änderung erhöhen.
3. **Sync zieht von `main`, nicht vom Feature-Branch.** Ein Skill, der nur auf einem Feature-Branch / in einem offenen PR liegt, taucht in Claude Web **nie** auf — egal wie oft man „Update" drückt. Erst nach `main` mergen, dann syncen.

Verifikation vor „fertig":
- `python3 .github/scripts/check_version_sync.py` → erzwingt `plugin.json` `version` == marketplace-Plugin-Eintrag für **jedes** Plugin (und schlägt fehl, wenn `metadata.version` hinterherhinkt). Läuft auch in CI `validate.yml`. Dieser Check fängt genau den Drift, der dazu führte, dass `google-ads-audit` beim Client nie ankam.
- `git ls-tree -r main --name-only -- plugins/<plugin>/skills/` → was liegt wirklich auf `main`?
