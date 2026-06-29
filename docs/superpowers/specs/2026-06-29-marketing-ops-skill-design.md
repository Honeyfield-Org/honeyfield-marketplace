# Design: `marketing-ops` — Orchestrator-Skill für das Honeyfield Marketing-Ops MCP

**Datum:** 2026-06-29
**Branch:** `feat/marketing-ops-skill`
**Repo:** `honeyfield-marketplace`
**Plugin:** `honeyfield-marketing-mcp`

## Problem

Das Plugin `honeyfield-marketing-mcp` exponiert ein großes MCP (`mcp.ads.honeyfield.at`):
~100 Tools über Google Ads (~70, viele schreibend), GA4, Search Console, Google
Business Profile, GTM, Microsoft Clarity, DataForSEO, Strapi, dazu Meta/LinkedIn,
`budget_pacing`, `anomaly_check` — und ein Multi-Tenant-Workspace-Modell
(`list_workspaces`, pro Workspace verbundene `sources`).

Aktuell existieren nur zwei tiefe, datengetriebene Spoke-Skills (`seo-audit`,
`geo-audit`). Beide setzen einen Hub voraus, der fehlt: einen Einstiegspunkt, der
den Workspace-Kontext klärt, die Tool-Landschaft kennt, die Nutzer-Absicht an den
richtigen Ort routet und Konventionen erzwingt. Beide Skills referenzieren zudem
vier noch nicht existente „Verwandte Skills" (`kunden-kontext`, `wochenreport`,
`suchbegriff-hygiene`, `tracking-check`).

Ohne Hub muss das Modell die ~100 Tools jedes Mal selbst sortieren — ohne
garantiertes Workspace-Setup, ohne DACH-Kalibrierung, ohne Schreib-Disziplin.

## Ziel

Ein **aktiver Orchestrator** ("Front-Door") für das Marketing-MCP. Er führt die
Session: klärt zuerst Workspace + Quellen, klassifiziert die (oft vage) Absicht,
routet an einen Spezial-Skill oder fährt die richtige Tool-Gruppe selbst — und
erzwingt durchgängige Konventionen (DACH-Kalibrierung, Belege statt Raten,
*read before write*, Schreib-Bestätigung).

### Festgelegte Entscheidungen

- **Rolle:** Aktiver Orchestrator (kein passives Cheatsheet — die Tool-Map ist
  Teil davon, dient aber dem Routen/Erzwingen).
- **Reichweite:** Ganzes MCP **inklusive schreibender Aktionen** (Kampagnen,
  Budgets, Keywords, Bids, GTM-Tags, GBP-Antworten) — mit harten Guardrails.
- **Trigger:** Default-Front-Door — feuert breit bei Marketing-MCP-Absichten;
  die tiefen Spokes (`seo-audit`, `geo-audit`) feuern weiter auf ihre spezifischen
  Begriffe und haben **Vorrang** (Yield-Regel).
- **Mechanik:** Nur Description-Triggering (#1), durch **evals** gehärtet. **Kein**
  PreToolUse-Hook — Skill-Aktivierung ist modell-getrieben, nicht hart an einen
  Tool-Call koppelbar; der Hook wäre ein Guardrail-Netz, ist aber Claude-Code-only,
  feuert zu spät zum Routen und erzeugt Rauschen. Später nachrüstbar, falls #1
  in der Praxis nicht reicht.
- **Architektur:** Ansatz A — ein `SKILL.md` + `references/`, konsistent mit den
  bestehenden Skills.

## Architektur

```
plugins/honeyfield-marketing-mcp/skills/marketing-ops/
  SKILL.md
  references/
    tool-map.md          # alle ~100 Tools nach Domäne: was / wann / welche source nötig
    ads-playbooks.md     # Ads sicher bedienen: Kampagne/Budget/Keyword/Bid/Anzeige-Flows
    write-guardrails.md  # Bestätigungs-Protokoll, irreversible-Aktionen-Liste, Preview-Format
  evals/                 # Eval-Harness via skill-creator (Format dort gepinnt)
```

Progressive Disclosure: `SKILL.md` bleibt schlank (Schritt 0, Routing, Konventionen,
Guardrail-Kern); Gewicht (vollständige Tool-Map, Ads-Playbooks, Guardrail-Details)
liegt in `references/` und wird nur bei Bedarf geladen.

### SKILL.md — Inhalt

1. **Identität:** Front-Door / Lotse für das Honeyfield Marketing-Ops MCP.
2. **Schritt 0 — Workspace & Quellen (immer zuerst):** `list_workspaces` →
   Ziel-Workspace bestätigen → dessen `sources` lesen. `kunden-kontext` lesen,
   *falls vorhanden* (weiche Referenz, keine Abhängigkeit). Keine Daten raten —
   fehlende Quelle wird als Lücke benannt.
3. **Intent-Klassifikation → Routing-Tabelle** (s.u.).
4. **Konventionen (quer):** DACH `location`/`language` auf jedem `dfs_*`
   (AT default; DE→Germany/de, AT→Austria/de, CH→Switzerland/de); Source-Gating
   (nur Pfade fahren, deren Quelle verbunden ist); Belege statt Vermutung;
   *read before write*.
5. **Schreib-Guardrails** (s.u.).
6. **Handoff-Verhalten:** bei Spoke → ankündigen + übergeben; bei Direkt-Steuerung
   → Plan zeigen, dann handeln.
7. **Grenzen** ehrlich benennen + **Verwandte Skills** + References-Pointer.

### Routing-Tabelle (Herzstück)

| Absicht | Ziel |
|---|---|
| SEO/Ranking, „warum ranke ich nicht", Traffic-Einbruch, technisches SEO | **→ `seo-audit`** (Vorrang) |
| KI-Sichtbarkeit, ChatGPT/Perplexity, GEO/AEO | **→ `geo-audit`** (Vorrang) |
| Google Ads: Kampagnen/Budget/Keywords/Bids/Anzeigen/Performance/Suchbegriffe/Recommendations | → `references/ads-playbooks.md` (direkt) |
| Conversions/Tracking/GTM | → `gtm_*`, GA4 key-events, `conversion_actions`-Tools |
| Analytics/Reporting (GA4, Search Console) | → Tool-Gruppe (später `wochenreport`) |
| Local / Google Business Profile | → `gbp_*` |
| Standalone Keyword/SERP/Backlink | → `dfs_*` |
| Vage („schau dir Kunde X an / läuft das?") | → Schritt 0 + Default-Übersicht (`list_campaigns` + `budget_pacing` + `anomaly_check` + GA4/SC-Top) → dann gezielt nachfragen |

**Yield-Regel:** Feuern `seo-audit`/`geo-audit` auf ihre spezifischen Begriffe,
haben sie Vorrang; der Orchestrator drängt sich nicht dazwischen.

### Schreib-Guardrails

- **Keine Mutation ohne explizite Bestätigung** — vorher exakten Diff zeigen:
  *Entität · Feld · alt → neu*.
- **Hochrisiko/irreversibel einzeln bestätigen:** `remove_campaign`,
  `remove_ad_group`, `remove_ad`, `remove_keyword`, `update_campaign_budget`,
  `update_campaign_status` (pause/enable), Bidding-Strategie-Wechsel,
  `upload_conversions`, Customer-Match-Upload/-Remove, `gtm_publish_version`,
  alle `delete_*`.
- Wo möglich erst `PAUSED`/Draft statt destruktiv.
- Nie Bulk-Mutation ohne aufgezählten Preview.
- Fehlt Schreib-Scope/Permission → sagen, nicht versuchen.

## Evals (Deliverable)

Härten das Description-Triggering und das Routing. Drei Klassen:

- **Trigger-evals:** positiv (Marketing-MCP-Absichten → `marketing-ops` feuert)
  vs. negativ (reine `seo-audit`/`geo-audit`-Begriffe werden *nicht* gekapert;
  Nicht-Marketing-Prompts feuern nicht).
- **Routing-evals:** feuert → landet beim richtigen Ziel (richtiger Spoke /
  richtige Tool-Gruppe).
- **Verhaltens-evals:** Schritt 0 zuerst? Mutation nur nach Bestätigung?

Harness über `skill-creator`; das genaue Eval-Format wird bei der Implementierung
dort gepinnt.

## Bewusst außerhalb des Scopes (YAGNI)

- `kunden-kontext`, `wochenreport`, `suchbegriff-hygiene`, `tracking-check` werden
  **nicht** gebaut — nur weich referenziert. Spätere eigene Branches.
- **Kein** PreToolUse-Hook / kein `hooks/`-Zusatz am Plugin.
- **Keine** neuen Spoke-Skills pro uncovered Domäne (der Orchestrator fährt diese
  Tool-Gruppen direkt).

## Risiken & offene Punkte

- **Trigger-Kollision** mit `seo-audit`/`geo-audit`: Hauptrisiko des Default-
  Front-Door. Mitigation: scharfe Yield-Regel in der `description` + negative
  Trigger-evals. Ist die description zu gierig, kapert der Orchestrator Audit-
  Anfragen; ist sie zu zaghaft, feuert er nicht.
- **Schreib-Reichweite**: voller Mutations-Scope erhöht die Wichtigkeit der
  Guardrails — Verhaltens-evals müssen „keine Mutation ohne Bestätigung" absichern.
- **Eval-Format** noch nicht final (hängt am `skill-creator`-Harness).
- **Deployment-Kontext**: Skills triggern in Claude Code und im claude.ai-Connector;
  ein Hook würde nur in Claude Code greifen — daher bewusst draußen.
