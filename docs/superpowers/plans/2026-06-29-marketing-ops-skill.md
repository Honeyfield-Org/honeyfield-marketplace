# marketing-ops Orchestrator-Skill — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Einen aktiven Orchestrator-Skill `marketing-ops` bauen, der als Front-Door für das Honeyfield Marketing-Ops MCP dient — Workspace/Quellen klärt, Absicht klassifiziert, an Spokes routet oder Tool-Gruppen direkt fährt, mit DACH-Kalibrierung und Schreib-Guardrails — und sein Triggering durch evals härtet.

**Architecture:** Ein `SKILL.md` + drei `references/`-Dateien (Ansatz A, konsistent mit `seo-audit`/`geo-audit`). Die Tool-Map wird aus der *einzigen autoritativen Quelle* abgeleitet: `mcp-server/server.py` im Schwester-Repo `ads-mcp-platform` (139 `@mcp.tool()`-Registrierungen, Tool-Name = Funktionsname, jeder mit `workspace`-Param). Evals über den `skill-creator`-Harness: Trigger-evals (`run_loop.py`) härten die `description` ohne MCP; Verhaltens-eval-Fälle werden autoriert und auf Transkript-Ebene gegradet.

**Tech Stack:** Markdown (Skill-Content), YAML-Frontmatter, JSON (Evals). Validierung: `python3 .github/scripts/check_skill_frontmatter.py`, `claude plugin validate`. Eval-Harness: `skill-creator` (`scripts/run_loop.py`, `assets/eval_review.html`).

## Global Constraints

- **Skill-Ort:** `plugins/honeyfield-marketing-mcp/skills/marketing-ops/` — Auto-Discovery über `plugins/*/skills/*/SKILL.md`, **keine** Manifest-Änderung nötig, damit der Skill erscheint.
- **Frontmatter muss valide YAML sein.** `name` + `description` sind Pflicht-Strings. Die `description` enthält `: ` und Anführungszeichen → den ganzen Wert in **doppelte Anführungszeichen** wrappen UND für die zitierten Begriffe **typografische** Anführungszeichen `„…"` verwenden (nicht ASCII `"`), exakt wie `seo-audit`/`geo-audit` — sonst bricht der strenge YAML-Parser und der Skill triggert still nicht. Nach jeder Frontmatter-Änderung `check_skill_frontmatter.py` laufen lassen.
- **Tool-Namen unpräfixiert** schreiben (`list_workspaces`, `ads_create_campaign`, `dfs_serp_google_organic`), exakt wie die bestehenden Skills — nicht das `mcp__claude_ai_marketing__`-Präfix.
- **Jeder genannte Tool-Name muss in `server.py` existieren.** Keine erfundenen Tools. Quelle: `/Users/devbox/code-projects/honeyfield/ads-mcp-platform/mcp-server/server.py`.
- **DACH-Kalibrierung:** auf jedem `dfs_*`-Call `location`+`language` (AT default; DE→`Germany`/`de`, AT→`Austria`/`de`, CH→`Switzerland`/`de`). Jeder Tool-Call nutzt den `workspace`-Param.
- **Stil:** Deutsch, terse, datengetrieben, *read before write* — wie die bestehenden Skills. `metadata: { version: 0.1.0 }`.
- **Eval-Run-Outputs** (Workspaces, Iterationen) gehören in den Scratchpad, **nicht** ins Repo. Committet werden nur die Eval-*Definitionen* (`evals/*.json`).

---

### Task 1: Tool-Map (`references/tool-map.md`)

**Files:**
- Create: `plugins/honeyfield-marketing-mcp/skills/marketing-ops/references/tool-map.md`
- Source (read-only): `/Users/devbox/code-projects/honeyfield/ads-mcp-platform/mcp-server/server.py`

**Interfaces:**
- Produces: Die kanonische Domänen-Gruppierung + Tool-Inventar, auf das `SKILL.md`, `ads-playbooks.md`, `write-guardrails.md` per Pointer verweisen.

- [ ] **Step 1: Tool-Inventar extrahieren**

```bash
cd /Users/devbox/code-projects/honeyfield/ads-mcp-platform/mcp-server
# Tool-Namen + Signatur-Zeile + erste Docstring-Zeile je @mcp.tool():
grep -nE '@mcp\.tool|^(async )?def [a-z]' server.py | grep -A1 '@mcp.tool'
```

Erwartung: 139 Funktions-Namen mit Signatur (z.B. `ads_create_campaign(...)`, jeweils mit `workspace: str | None = None`).

- [ ] **Step 2: `tool-map.md` schreiben — nach Domäne gruppiert**

Struktur (eine Tabelle pro Domäne). Spalten: **Tool · was · Quelle nötig · R/W**. „R/W" = `R` (liest), `W` (mutiert). Domänen + Source-Mapping:

```markdown
# Tool-Map — Honeyfield Marketing-Ops MCP

Alle Tools nehmen `workspace`. Quelle = welche Workspace-`source` verbunden sein muss.
Lege Schreib-Tools (W) nie ohne `write-guardrails.md` an.

## Foundation
| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `list_workspaces` | Workspaces + verbundene `sources` | — | R |
| `ping` | Health-Check | — | R |

## Google Ads — Lesen/Reporting (source: google_ads)
| `ads_campaign_performance` | Kampagnen-KPIs (days) | google_ads | R |
| `ads_search_terms` | Suchbegriffs-Report | google_ads | R |
| … (alle ads_*-Reporting-Tools aus server.py) |

## Google Ads — Mutation (source: google_ads)  ⚠ Guardrails
| `ads_create_campaign` | Kampagne anlegen | google_ads | W |
| `ads_update_campaign_budget` | Budget ändern | google_ads | W |
| … (alle ads_create_/update_/remove_/add_/set_/move_/replace_/apply_/upload_) |

## GA4 (source: ga4) · Search Console (source: search_console) ·
## Google Business Profile (source: business_profile) · GTM (source: gtm) ·
## Clarity (source: clarity) · DataForSEO (source: dataforseo) ·
## Strapi (source: strapi) · Social (meta_/linkedin_) · Diagnostics (budget_pacing, anomaly_check)
( je eine Tabelle, gleiche Spalten )
```

Jede Domäne vollständig aus `server.py` füllen — kein Tool auslassen, keins erfinden.

- [ ] **Step 3: Vollständigkeit + Echtheit verifizieren**

```bash
cd /Users/devbox/code-projects/honeyfield/honeyfield-marketplace
SK=plugins/honeyfield-marketing-mcp/skills/marketing-ops
SRV=/Users/devbox/code-projects/honeyfield/ads-mcp-platform/mcp-server/server.py
# Alle in tool-map referenzierten Tools existieren in server.py?
grep -oE '`[a-z][a-z0-9_]+`' $SK/references/tool-map.md | tr -d '`' | sort -u > /tmp/map_tools.txt
grep -oE 'def ([a-z][a-z0-9_]+)\(' $SRV | sed -E 's/def //; s/\(//' | sort -u > /tmp/srv_tools.txt
echo "In Map, aber NICHT in server.py (muss leer sein):"; comm -23 /tmp/map_tools.txt /tmp/srv_tools.txt
```

Erwartung: die zweite Liste ist leer (jeder gemappte Name existiert). Tools, die in `server.py` sind, aber bewusst nicht gemappt werden, sind ok.

- [ ] **Step 4: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/marketing-ops/references/tool-map.md
git commit -m "feat(marketing-ops): Tool-Map aus server.py (139 Tools nach Domäne)"
```

---

### Task 2: Schreib-Guardrails (`references/write-guardrails.md`)

**Files:**
- Create: `plugins/honeyfield-marketing-mcp/skills/marketing-ops/references/write-guardrails.md`

**Interfaces:**
- Consumes: die W-Tools aus `tool-map.md`.
- Produces: das Bestätigungs-Protokoll + Preview-Format, auf das `SKILL.md` und `ads-playbooks.md` verweisen.

- [ ] **Step 1: Mutations-Tools aus server.py auflisten**

```bash
SRV=/Users/devbox/code-projects/honeyfield/ads-mcp-platform/mcp-server/server.py
grep -oE 'def ([a-z][a-z0-9_]+)\(' $SRV | sed -E 's/def //; s/\(//' \
  | grep -E '_(create|update|remove|delete|add|set|move|replace|apply|upload|submit|reply|publish)' | sort -u
```

Erwartung: die Liste der schreibenden Tools (Basis für die Hochrisiko-Liste).

- [ ] **Step 2: `write-guardrails.md` schreiben**

Konkreter Inhalt:

```markdown
# Schreib-Guardrails

Grundregel: **read before write.** Erst den Ist-Zustand lesen (passendes R-Tool),
dann den exakten Diff zeigen, dann erst — nach expliziter Bestätigung — mutieren.

## Preview-Format (vor JEDER Mutation zeigen)
> Aktion: `<tool>` · Workspace: `<ws>`
> Entität: <name/id> · Feld: <feld> · **alt → neu**
> Wirkung/Reichweite: <1 Satz> · Reversibel: ja/nein

## Hochrisiko / irreversibel — EINZELN bestätigen (nie gebündelt)
- `ads_remove_campaign`, `ads_remove_ad_group`, `ads_remove_ad`, `ads_remove_keyword`
- `ads_update_campaign_budget`, `ads_update_campaign_status` (pause/enable)
- `ads_update_campaign_bidding_strategy`
- `ads_upload_conversions`, `ads_upload_customer_match_members`, `ads_remove_customer_match_members`
- `gtm_publish_version`, `sc_submit_sitemap`, `sc_delete_sitemap`
- alle weiteren `*_delete_*` / `*_remove_*` aus tool-map.md
( Liste 1:1 gegen Step-1-Ausgabe abgleichen — nur real existierende Tools )

## Defaults
- Wo möglich erst `PAUSED`/Draft statt destruktiv.
- Nie Bulk-Mutation (`ads_bulk_*`) ohne aufgezählten Preview je Element.
- Fehlt Schreib-Scope/`source` → sagen, nicht versuchen.
```

- [ ] **Step 3: Echtheit verifizieren**

```bash
SK=plugins/honeyfield-marketing-mcp/skills/marketing-ops
SRV=/Users/devbox/code-projects/honeyfield/ads-mcp-platform/mcp-server/server.py
grep -oE '`[a-z][a-z0-9_]+`' $SK/references/write-guardrails.md | tr -d '`' | sort -u > /tmp/g.txt
grep -oE 'def ([a-z][a-z0-9_]+)\(' $SRV | sed -E 's/def //; s/\(//' | sort -u > /tmp/srv_tools.txt
echo "In Guardrails, aber NICHT in server.py (muss leer sein):"; comm -23 /tmp/g.txt /tmp/srv_tools.txt
```

Erwartung: leer.

- [ ] **Step 4: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/marketing-ops/references/write-guardrails.md
git commit -m "feat(marketing-ops): Schreib-Guardrails + Preview-Format"
```

---

### Task 3: Ads-Playbooks (`references/ads-playbooks.md`)

**Files:**
- Create: `plugins/honeyfield-marketing-mcp/skills/marketing-ops/references/ads-playbooks.md`

**Interfaces:**
- Consumes: Tool-Namen aus `tool-map.md`, Protokoll aus `write-guardrails.md`.
- Produces: Schritt-für-Schritt-Flows für die Ads-Domäne, auf die das Routing in `SKILL.md` verweist.

- [ ] **Step 1: `ads-playbooks.md` schreiben — je Flow: read → preview → confirm → write**

Mindestens diese Flows, jeweils mit konkreter Tool-Sequenz:

```markdown
# Ads-Playbooks

Jeder mutierende Flow folgt write-guardrails.md: erst lesen, Diff zeigen, bestätigen lassen.

## Budget anpassen
1. `ads_list_campaigns` + `ads_budget_status` → Ist-Budget + Pacing lesen.
2. `budget_pacing` (Diagnostics) → über/unter Plan?
3. Preview (alt → neu) zeigen → bestätigen → `ads_update_campaign_budget`.

## Neue Kampagne
1. `ads_list_campaigns` → Namens-/Struktur-Kontext.
2. Preview der Eckdaten → bestätigen → `ads_create_campaign` (Status PAUSED).
3. `ads_create_ad_group` → `ads_add_keyword`/`ads_bulk_add_keywords` → `ads_create_ad`.
4. Erst nach Review `ads_update_campaign_status` auf ENABLED (Hochrisiko, einzeln).

## Suchbegriff-Hygiene
1. `ads_search_terms` → verschwendete Terms.
2. Vorschlagsliste zeigen → bestätigen → `ads_add_negative_keyword`/`ads_bulk_add_negative_keywords`.

## Gebote / Keyword-Status / Anzeigen / Recommendations
( je ein Flow: ads_update_keyword_bid · ads_update_ad_group_bid ·
  ads_update_keyword_status · ads_update_ad/ads_replace_ad ·
  ads_list_recommendations → ads_apply_recommendation/ads_dismiss_recommendation )
```

- [ ] **Step 2: Echtheit verifizieren** (gleicher `comm -23`-Check wie Task 1/2 gegen `server.py`) — Erwartung leer.

- [ ] **Step 3: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/marketing-ops/references/ads-playbooks.md
git commit -m "feat(marketing-ops): Ads-Playbooks (read→preview→confirm→write Flows)"
```

---

### Task 4: SKILL.md (Orchestrator-Kern)

**Files:**
- Create: `plugins/honeyfield-marketing-mcp/skills/marketing-ops/SKILL.md`
- Validate: `.github/scripts/check_skill_frontmatter.py`

**Interfaces:**
- Consumes: alle drei `references/`-Dateien (per Pointer).
- Produces: das triggernde + routende Verhalten; die `description` ist Eingang für Task 5.

- [ ] **Step 1: SKILL.md schreiben — exaktes Frontmatter + Body**

````markdown
---
name: marketing-ops
description: "Front-Door / Orchestrator für das Honeyfield Marketing-Ops MCP. Nutze diesen Skill als Einstieg für die Bedienung des Marketing-MCP: Google Ads (Kampagnen, Budgets, Keywords, Gebote, Anzeigen, Suchbegriffe, Recommendations), GA4, Search Console, Google Business Profile, GTM, Microsoft Clarity, DataForSEO sowie Meta/LinkedIn. Auch bei: „schau dir Kunde/Workspace X an", „wie läuft die Kampagne", „was kann ich hier tun", „Budget anpassen", „neue Kampagne/Anzeige erstellen", „Performance prüfen", „welche Daten/Workspaces habe ich", oder vagen bzw. übergreifenden Marketing-Anliegen. Klärt zuerst Workspace + verbundene Quellen, klassifiziert die Absicht, routet an den richtigen Spezial-Skill oder fährt die Tool-Gruppe direkt — mit DACH-Kalibrierung und Schreib-Bestätigung. Für einen tiefen klassischen SEO-/Ranking-Audit nutze stattdessen `seo-audit`; für KI-/Antwortmaschinen-Sichtbarkeit (ChatGPT/Perplexity/GEO/AEO) `geo-audit`."
metadata:
  version: 0.1.0
---

# Marketing-Ops (Front-Door)

Du bist der Lotse für das Honeyfield Marketing-Ops MCP. Du führst die Session:
Workspace klären, Absicht einordnen, an den richtigen Ort routen, Konventionen
erzwingen. Du rätst keine Daten zusammen und mutierst nie ungefragt.

## Schritt 0 — Workspace & Quellen (IMMER zuerst)
1. `list_workspaces` → Ziel-Workspace bestätigen (bei mehreren: kurz fragen).
2. Dessen `sources` lesen → nur Pfade fahren, deren Quelle verbunden ist;
   fehlt eine, als Lücke benennen, nicht raten.
3. Falls ein `kunden-kontext` für den Workspace existiert: lesen (weiche Referenz).
4. Jeden folgenden Tool-Call mit `workspace=<ws>`.

## Intent-Klassifikation → Routing
| Absicht | Ziel |
|---|---|
| SEO/Ranking, „warum ranke ich nicht", Traffic-Einbruch, technisches SEO | **→ Skill `seo-audit`** (Vorrang) |
| KI-Sichtbarkeit, ChatGPT/Perplexity, GEO/AEO | **→ Skill `geo-audit`** (Vorrang) |
| Google Ads (Kampagnen/Budget/Keywords/Bids/Anzeigen/Suchbegriffe/Recos) | → `references/ads-playbooks.md` |
| Conversions/Tracking/GTM | → `gtm_*`, GA4 key-events, `ads_*conversion*` (tool-map) |
| Analytics/Reporting (GA4, Search Console) | → GA4-/SC-Tools (tool-map) |
| Local / Google Business Profile | → `gbp_*` (tool-map) |
| Keyword/SERP/Backlink standalone | → `dfs_*` (tool-map, DACH-Kalibrierung!) |
| Vage („läuft das?") | → Schritt 0 + Default-Übersicht: `ads_list_campaigns` + `budget_pacing` + `anomaly_check` + GA4/SC-Top → dann gezielt nachfragen |

**Yield-Regel:** Adressiert die Anfrage klar einen tiefen Audit (klassisches
Ranking → `seo-audit`; KI-Sichtbarkeit → `geo-audit`), übergib dorthin und dräng
dich nicht dazwischen. Tool-Inventar nach Domäne: `references/tool-map.md`.

## Konventionen (quer)
- **DACH:** auf jedem `dfs_*` `location`+`language` setzen (AT default;
  DE→`Germany`/`de`, AT→`Austria`/`de`, CH→`Switzerland`/`de`).
- **Source-Gating** + Belege statt Vermutung.
- **read before write** — Mutation immer nach Preview + Bestätigung.

## Schreiben
Bevor du irgendetwas mutierst, folge `references/write-guardrails.md`
(Preview-Format, Hochrisiko-Liste, einzeln bestätigen). Nie ungefragt.

## Handoff
- An Spoke: kurz ankündigen („Das ist ein klassischer SEO-Audit → ich übergebe an `seo-audit`."), dann den Skill nutzen.
- Direkt: Plan in 1–2 Sätzen zeigen, dann handeln.

## Grenzen
Kein seitenweiter Crawler; Daten nur aus verbundenen Quellen; Momentaufnahme.

## Verwandte Skills
`seo-audit` · `geo-audit` · (geplant: `kunden-kontext`, `wochenreport`, `suchbegriff-hygiene`, `tracking-check`)

## Referenzen
- `references/tool-map.md` — alle Tools nach Domäne + Quelle + R/W.
- `references/ads-playbooks.md` — Ads-Flows (read→preview→confirm→write).
- `references/write-guardrails.md` — Bestätigungs-Protokoll + Hochrisiko-Liste.
````

- [ ] **Step 2: Frontmatter validieren**

```bash
cd /Users/devbox/code-projects/honeyfield/honeyfield-marketplace
python3 -c "import yaml" 2>/dev/null || python3 -m pip install --quiet --break-system-packages pyyaml
python3 .github/scripts/check_skill_frontmatter.py "plugins/honeyfield-marketing-mcp/skills/marketing-ops/SKILL.md"
```

Erwartung: `OK: plugins/.../marketing-ops/SKILL.md` und Exit 0. Bei Fehler: Anführungszeichen prüfen (typografische `„…"` im Body der description, ganzer Wert in `"…"`).

- [ ] **Step 3: Tool-Namen im SKILL.md gegen server.py prüfen** (gleicher `comm -23`-Check) — Erwartung leer.

- [ ] **Step 4: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/marketing-ops/SKILL.md
git commit -m "feat(marketing-ops): SKILL.md — Schritt 0, Routing, Konventionen, Guardrail-Pointer"
```

---

### Task 5: Trigger-Evals + Description-Optimierung

**Files:**
- Create: `plugins/honeyfield-marketing-mcp/skills/marketing-ops/evals/trigger-evals.json`
- Run-Outputs (NICHT committen): Scratchpad-Workspace.

**Interfaces:**
- Consumes: die `description` aus Task 4.
- Produces: optimierte `description` (zurück in SKILL.md).

- [ ] **Step 1: 20 Trigger-Queries schreiben** (`trigger-evals.json`)

Format (`run_loop.py`-kompatibel): Array aus `{query, should_trigger}`. 8–10 positiv, 8–10 negative Near-Misses.

```json
[
  {"query": "schau dir mal den workspace von zahnarzt meier an, läuft das budget gut oder verbrennen wir geld?", "should_trigger": true},
  {"query": "ich will für den kunden eine neue google ads kampagne aufsetzen, erstmal pausiert", "should_trigger": true},
  {"query": "was kann ich mit dem marketing mcp hier eigentlich alles machen?", "should_trigger": true},
  {"query": "negative keywords ergänzen, wir zahlen für total irrelevante suchbegriffe", "should_trigger": true},
  {"query": "welche workspaces hab ich verbunden und welche datenquellen hängen dran?", "should_trigger": true},
  {"query": "gtm conversion tracking für den kontaktformular-submit einrichten", "should_trigger": true},
  {"query": "wie performt die meta kampagne vs google diesen monat?", "should_trigger": true},
  {"query": "gbp reviews vom letzten monat anschauen und antworten", "should_trigger": true},

  {"query": "warum ranken wir bei „zahnarzt salzburg\" nicht auf seite 1, mach mal einen technischen seo-audit", "should_trigger": false},
  {"query": "werde ich in chatgpt und perplexity überhaupt erwähnt? bitte geo/aeo audit", "should_trigger": false},
  {"query": "schreib mir einen blogartikel über zahnzusatzversicherung", "should_trigger": false},
  {"query": "kannst du diese xlsx mit den ad-kosten in ein chart umwandeln?", "should_trigger": false},
  {"query": "erklär mir wie der google ads auktionsmechanismus funktioniert", "should_trigger": false},
  {"query": "core web vitals und ladezeit der startseite prüfen", "should_trigger": false},
  {"query": "formuliere eine linkedin-anzeige als text, noch nichts schalten", "should_trigger": false},
  {"query": "was kostet das dataforseo abo nochmal?", "should_trigger": false}
]
```

(Inhaltlich an reale Agentur-Prompts anlehnen; negative gezielt Near-Miss zu `seo-audit`/`geo-audit`/Content.)

- [ ] **Step 2: Eval-Set mit dem User reviewen** (HTML-Template)

```bash
SC=/Users/devbox/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator
# assets/eval_review.html lesen, Platzhalter ersetzen (__EVAL_DATA_PLACEHOLDER__ = JSON-Array,
# __SKILL_NAME_PLACEHOLDER__ = marketing-ops, __SKILL_DESCRIPTION_PLACEHOLDER__ = aktuelle description),
# nach /tmp/eval_review_marketing-ops.html schreiben und öffnen:
open /tmp/eval_review_marketing-ops.html
```

User editiert/togglet, exportiert nach `~/Downloads/eval_set.json`. Diese Version übernehmen.

- [ ] **Step 3: Optimierungs-Loop laufen lassen** (Hintergrund)

```bash
SC=/Users/devbox/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator
WS=/private/tmp/claude-501/.../scratchpad/marketing-ops-workspace   # Scratchpad
cp ~/Downloads/eval_set.json "$WS/trigger-eval.json"
cd "$SC" && python -m scripts.run_loop \
  --eval-set "$WS/trigger-eval.json" \
  --skill-path /Users/devbox/code-projects/honeyfield/honeyfield-marketplace/plugins/honeyfield-marketing-mcp/skills/marketing-ops \
  --model claude-opus-4-8 \
  --max-iterations 5 --verbose
```

Erwartung: Loop läuft 5 Iterationen, splittet train/test, gibt JSON mit `best_description` (nach Test-Score gewählt) + HTML-Report.

- [ ] **Step 4: Beste Description übernehmen + re-validieren**

`best_description` ins SKILL.md-Frontmatter übernehmen (typografische Quotes beibehalten), Before/After + Scores dem User zeigen, dann:

```bash
cd /Users/devbox/code-projects/honeyfield/honeyfield-marketplace
python3 .github/scripts/check_skill_frontmatter.py "plugins/honeyfield-marketing-mcp/skills/marketing-ops/SKILL.md"
```

Erwartung: OK / Exit 0.

- [ ] **Step 5: Commit** (nur Eval-Definition + ggf. SKILL.md, keine Run-Outputs)

```bash
git add plugins/honeyfield-marketing-mcp/skills/marketing-ops/evals/trigger-evals.json \
        plugins/honeyfield-marketing-mcp/skills/marketing-ops/SKILL.md
git commit -m "feat(marketing-ops): Trigger-Evals + per run_loop optimierte Description"
```

---

### Task 6: Verhaltens-Evals (Routing + Guardrails)

**Files:**
- Create: `plugins/honeyfield-marketing-mcp/skills/marketing-ops/evals/evals.json`

**Interfaces:**
- Consumes: das fertige SKILL.md + references.
- Produces: gradierbare Verhaltens-Checks (Transkript-Ebene; Live-MCP-Run gated auf verbundenen Workspace).

- [ ] **Step 1: `evals.json` schreiben** (skill-creator-Schema: prompts + assertions)

Assertions objektiv aus dem Agenten-Transkript prüfbar — **ohne** echten MCP-Call (das Modell beschreibt, welche Tools es in welcher Reihenfolge nutzen würde; Guardrail = es fragt vor der Mutation):

```json
{
  "skill_name": "marketing-ops",
  "evals": [
    {
      "id": 1,
      "prompt": "schau dir den workspace 'zahnarzt-meier' an, läuft die google ads kampagne gut?",
      "expected_output": "Ruft zuerst list_workspaces / klärt Quellen (Schritt 0), dann Default-Übersicht; keine Mutation.",
      "assertions": [
        {"text": "konsultiert/erwähnt list_workspaces vor anderen MCP-Tools", "type": "qualitative"},
        {"text": "schlägt keine schreibende Aktion ohne Rückfrage vor", "type": "qualitative"}
      ]
    },
    {
      "id": 2,
      "prompt": "warum ranke ich bei 'zahnarzt salzburg' nicht? mach einen technischen seo-audit",
      "expected_output": "Routet/übergibt an seo-audit (Yield-Regel), kapert nicht selbst.",
      "assertions": [{"text": "verweist auf bzw. übergibt an seo-audit", "type": "qualitative"}]
    },
    {
      "id": 3,
      "prompt": "setz das tagesbudget von kampagne 'Brand' auf 50 euro",
      "expected_output": "Liest Ist-Budget, zeigt Preview alt→neu, fragt vor ads_update_campaign_budget.",
      "assertions": [
        {"text": "zeigt Preview (alt → neu) vor der Mutation", "type": "qualitative"},
        {"text": "fragt explizit um Bestätigung vor ads_update_campaign_budget", "type": "qualitative"}
      ]
    }
  ]
}
```

- [ ] **Step 2: Grading-Pass** (with-skill vs baseline, Transkript-Grade)

```bash
SC=/Users/devbox/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator
# Pro Eval zwei Runs (with-skill / baseline) im Scratchpad-Workspace spawnen,
# dann gegen agents/grader.md graden (grading.json: text/passed/evidence),
# aggregieren:
cd "$SC" && python scripts/aggregate_benchmark.py <workspace>/iteration-1
```

Erwartung: with-skill schlägt baseline bei Routing (Eval 2) und Guardrail (Eval 3); benchmark.json erzeugt.

- [ ] **Step 3: Live-MCP-Hinweis dokumentieren**

In `evals.json` oben einen Kommentar/`_note`-Eintrag: echte Tool-Ausführung braucht einen verbundenen Workspace; die hiesigen Assertions graden das *Vorgehen* (Reihenfolge/Bestätigung), nicht echte API-Resultate.

- [ ] **Step 4: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/marketing-ops/evals/evals.json
git commit -m "feat(marketing-ops): Verhaltens-Evals (Schritt-0, Routing-Yield, Schreib-Bestätigung)"
```

---

### Task 7: Marketplace-Integration + finale Validierung

**Files:**
- Modify: `plugins/honeyfield-marketing-mcp/.claude-plugin/plugin.json` (Version-Bump + Beschreibung)
- Modify: `.claude-plugin/marketplace.json` (Version + Beschreibung des Marketing-Plugins)

**Interfaces:**
- Consumes: den fertigen Skill.

- [ ] **Step 1: Versionen + Beschreibungen anheben**

`plugin.json` und der Marketing-Eintrag in `marketplace.json`: `version` `1.1.0` → `1.2.0`; Beschreibung um den Front-Door ergänzen (z.B. „… mit DACH-Audit-Skills und `marketing-ops` als Front-Door"). JSON valide halten.

- [ ] **Step 2: Vollständige CI lokal nachstellen**

```bash
cd /Users/devbox/code-projects/honeyfield/honeyfield-marketplace
for f in .claude-plugin/marketplace.json plugins/*/.claude-plugin/plugin.json plugins/*/.mcp.json; do
  [ -f "$f" ] && python3 -m json.tool "$f" >/dev/null && echo "OK: $f"; done
python3 .github/scripts/check_skill_frontmatter.py
claude plugin validate plugins/honeyfield-marketing-mcp/
```

Erwartung: alle JSON OK; Frontmatter-Check meldet jetzt **3** Skills valide (seo-audit, geo-audit, marketing-ops); `claude plugin validate` OK.

- [ ] **Step 3: Skill-Discovery sanity-checken**

```bash
ls plugins/honeyfield-marketing-mcp/skills/marketing-ops/
# erwartet: SKILL.md  references/  evals/
test -f plugins/honeyfield-marketing-mcp/skills/marketing-ops/SKILL.md && echo "SKILL.md vorhanden"
```

- [ ] **Step 4: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/.claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "feat(marketing-ops): Plugin/Marketplace v1.2.0 — Front-Door integriert"
```

---

## Self-Review (gegen das Spec)

**Spec-Coverage:**
- Aktiver Orchestrator → Task 4 (SKILL.md: Schritt 0, Routing, Handoff). ✓
- Ganzes MCP inkl. schreiben → Task 1 (W-Tools gemappt), Task 2 (Guardrails), Task 3 (Ads-Write-Flows). ✓
- Default-Front-Door + Yield-Regel → Task 4 (description + Routing-Tabelle + Yield), Task 5 (negative Trigger-evals zu seo-/geo-audit). ✓
- Nur Description-Triggering + evals, kein Hook → Task 5 (Trigger), Task 6 (Verhalten); kein `hooks/`. ✓
- Ansatz A (SKILL.md + references/) → Tasks 1–4. ✓
- DACH-Kalibrierung, read-before-write, Source-Gating → Global Constraints + Task 4 Konventionen. ✓
- Eval-Format über skill-creator → Task 5/6 mit echten Schemata + Befehlen. ✓
- YAGNI (keine neuen Spokes/Foundation/Hook) → nirgends gebaut, nur referenziert. ✓

**Platzhalter-Scan:** Keine „TBD/TODO" in Steps; alle Befehle konkret; Eval-JSON mit echten Beispiel-Einträgen; SKILL.md-Volltext enthalten. Die `references/`-Dokumente zeigen Struktur + repräsentative Zeilen statt aller 139 Tools (bewusst — der Vollständigkeits-Check in jedem Task erzwingt die echte Befüllung gegen `server.py`).

**Typ-/Namens-Konsistenz:** Tool-Namen durchgängig unpräfixiert; jeder Task hat denselben `comm -23`-Echtheits-Check gegen `server.py`; `best_description` aus Task 5 fließt in dieselbe SKILL.md-Frontmatter zurück.
