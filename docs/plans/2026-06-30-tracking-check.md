# tracking-check Skill — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Einen neuen Topic-Skill `tracking-check` im Plugin `honeyfield-marketing-mcp` bauen, der die Integrität des Conversion-/Event-Trackings (GA4 + GTM + Google Ads) datengetrieben auditiert, jeden Befund nach Beweiskraft stuft und Sicheres als Dry-Run-Operator behebt.

**Architecture:** Ein `SKILL.md` (schlank, ~Audit-Skill-Struktur) + drei on-demand-`references/` (Event-Soll-Library, DACH-Consent, Tool-Grenzen) + `evals/evals.json`. Der Skill liest echte MCP-Daten und hält sie gegen ein Soll; die Ehrlichkeit trägt eine 3-stufige Beleg-Logik (gemessen / nur konfiguriert / nicht prüfbar), die direkt aus der Tool-Reality abgeleitet ist.

**Tech Stack:** Markdown-Skill (Agent-Skill-Spec), YAML-Frontmatter, JSON-Evals, Python-Validierungs-Skripte. MCP-Tools: `ga4_*`, `gtm_*`, `ads_*conversion*`.

**Hinweis zur Plan-Form:** Dies ist ein **Skill-Authoring-Plan**, kein Code-TDD. Es gibt keine pytest-Unit-Tests. Das Äquivalent zum „Test pro Task" ist (a) die Validierungs-Pipeline (`check_skill_frontmatter.py`, `python3 -m json.tool`, `check_version_sync.py`, `claude plugin validate`) und (b) die `evals` als Verhaltens-Tests (Trigger/Defer/Tool-Reality). Jede Task endet mit einem konkreten, ausführbaren Verifikations-Befehl + erwartetem Ergebnis. Voller Datei-Volltext wird NICHT in den Plan dupliziert (DRY — der Plan würde sonst = die Datei); stattdessen liefert jede Task die **exakte Struktur + Inhalts-Anforderungen + Akzeptanzkriterien**, mit wörtlichen Bausteinen dort, wo sie load-bearing sind (description, Beleg-Stufen-Tabelle, Footgun-Liste). Detail-Quelle ist `docs/specs/2026-06-30-tracking-check-design.md` (referenziert pro Task).

## Global Constraints

- **Sprache/Stil:** Deutsch, imperativ, terse, daten-first, ehrlich über Grenzen, DACH-kalibriert (DE/AT/CH).
- **Frontmatter:** `name: tracking-check` (kebab-case, == Verzeichnisname). `description` mit Trigger-Phrasen **und** Abgrenzung zu Schwester-Skills. `metadata.version: 0.1.0`.
- **`description`-Limit: ≤1024 Zeichen, Ziel ~950.** Deutsche Anführungszeichen als Paar „…" mit **schließendem U+201D** (nicht ASCII `"`) — oder innere `"` als `\"` escapen. Bricht sonst den YAML-Parser still.
- **MCP-Tools** als Bare-Name in Backticks (`ga4_list_key_events`, `gtm_get_tag`, …).
- **Audit-Skill-Struktur** (CLAUDE.md): Beleg-Stufen → Schritt 0 (Projekt-Kontext-Absatz + `list_workspaces`/sources-Check + Markt-Kalibrierung) → Phasen (Blocker zuerst) → DACH-Layer → Footguns/Mythen → Output-Format → Operator (Dry-Run + Bestätigung) → Grenzen → Tools nach Phase → Verwandte Skills → Referenzen.
- **SKILL.md schlank halten (≤~500 Zeilen)**; Detail-Wissen in `references/*.md` (on-demand).
- **Projekt-Kontext-Absatz** (kanonisch, CLAUDE.md) in Schritt 0; `compliance`-Flags als harte Leitplanke. Keine `kunden-kontext`-Altreferenzen.
- **Version-Bump in allen drei Feldern** beim Hinzufügen des Skills: `plugin.json` `version`, marketplace-Plugin-Eintrag `version` (== plugin.json), `metadata.version`. Aktuell `1.3.1` → neu **`1.4.0`** (neuer Skill = MINOR).
- **Vor jedem Commit validieren:** `python3 .github/scripts/check_skill_frontmatter.py`, `python3 -m json.tool …/evals/evals.json`, `python3 .github/scripts/check_version_sync.py`, `claude plugin validate plugins/honeyfield-marketing-mcp/`.

## File Structure

| Datei | Verantwortung |
|---|---|
| `plugins/honeyfield-marketing-mcp/skills/tracking-check/SKILL.md` | Orchestrierung: Schritt 0, 6 Phasen, DACH-Consent-Layer, Footguns, Output, Operator, Grenzen, Tools, Verwandte Skills. Schlank. |
| `…/tracking-check/references/tracking-tool-grenzen.md` | Beleg-Stufen-Mapping + Footgun-Tabelle (was die MCP-Tools können/nicht). Rückgrat der Ehrlichkeit. |
| `…/tracking-check/references/event-soll-dach.md` | Event-Soll-Library nach Geschäftstyp (volle Corey-Library + DACH-Lead-Gen-Erweiterung) + Funnel-Sequenzen. Soll für Phase 5. |
| `…/tracking-check/references/dach-consent.md` | Consent Mode v2, §25 TTDSG, CMP-Landschaft, Server-Side; prüfbar vs. nicht. |
| `…/tracking-check/evals/evals.json` | 11 Verhaltens-Cases (Trigger/Defer/Tool-Reality/Operator/DACH). |
| `plugins/honeyfield-marketing-mcp/.claude-plugin/plugin.json` | Version-Bump 1.3.1 → 1.4.0. |
| `.claude-plugin/marketplace.json` | Plugin-Eintrag-`version` + `metadata.version` → 1.4.0. |

**Bau-Reihenfolge-Logik:** Die References sind das Fundament (SKILL.md verweist darauf), also zuerst — beginnend mit der Tool-Grenzen-Referenz, weil sie die Beleg-Stufen festlegt, die das ganze SKILL.md durchziehen. Dann SKILL.md, dann evals (testen SKILL.md-Verhalten), zuletzt Version-Bump + Gesamt-Validierung.

---

### Task 1: Skill-Gerüst + `tracking-tool-grenzen.md`

**Files:**
- Create: `plugins/honeyfield-marketing-mcp/skills/tracking-check/references/tracking-tool-grenzen.md`

**Interfaces:**
- Produces: Die kanonische Beleg-Stufen-Zuordnung + Footgun-Liste, auf die SKILL.md (Task 4) per „siehe `references/tracking-tool-grenzen.md`" verweist und deren Begriffe (gemessen / nur konfiguriert / nicht prüfbar) SKILL.md verbatim nutzt.

- [ ] **Step 1: Verzeichnis + Datei anlegen, Inhalt schreiben**

Inhalt = drei Blöcke, Quelle: Spec Abschnitt 4 + Anhang. Wörtlich load-bearing:

Block A — **Beleg-Stufen-Mapping** (Tabelle): Stufe | Bedeutung | Tools.
- *Gemessen (Daten fließen):* `ga4_list_key_events` (Per-Event-Counts), `ga4_conversions`, `ga4_report`, `ads_list_conversion_actions` (letztes Conversion-Datum), `ads_conversion_performance` (`last_gap_days`), `ga4_manage_google_ads_links` (list), `ga4_enhanced_measurement`/`ga4_data_retention` (get).
- *Nur konfiguriert (Firing unbewiesen):* `gtm_get_tag`, `gtm_list_tags`/`_triggers`/`_variables`, `gtm_get_version`, `ads_list_conversion_actions` (Inventar), `ga4_list_custom_dimensions`/`_metrics`.
- *Nicht prüfbar (beratend):* Consent-Mode-v2-Korrektheit, sGTM-Gesundheit, Attributionsmodell, Page-Snippet-Installation, echte Doppelzählung.

Block B — **Footgun-Liste** (jeweils: was ein naiver Skill behaupten würde → was die Tools wirklich hergeben → ehrliche Formulierung):
1. „Tag X feuert" — GTM zeigt nur Config, kein Browser-Firing → „konfiguriert + an Trigger verdrahtet" vs. separat „Daten kommen an (Counts>0)"; Config-ohne-Daten = **Verdacht**, nicht Befund.
2. „Consent Mode v2 korrekt" — nicht verifizierbar → höchstens Consent-Tag-Präsenz; Korrektheit als nicht prüfbar ausweisen.
3. „kein/aktives sGTM" — nur aus `transport_url`-Param ableitbar → „sGTM-Endpoint im GA4-Config-Tag hinterlegt: ja/nein", Live-Gesundheit nicht bestätigbar.
4. „Attributionsmodell ist X" — nirgends lesbar → weglassen / als Tool-Grenze nennen.
5. Zählung „jede/eine" & primär/sekundär aus `list` — Schema verspricht es nicht → erst Response prüfen, sonst „nicht ausgelesen".
6. `ga4_realtime_users` als Firing-Beweis — nur aggregierte User → für Event-Smoketest `ga4_list_key_events`/`ga4_report`.
7. Workspace-Draft ≠ Live — `gtm_list_tags` liest Draft, `gtm_container_info`/`gtm_get_version` Live → beide vergleichen, Quelle benennen (häufigster Bug).
8. „GA4-Snippet auf jeder Seite" — kein Tool liest Seiten-HTML → out of scope, nicht behaupten.
9. Enhanced Measurement = vollständiges Tracking — deckt nur GA4-Auto-Events → nicht als „Tracking vollständig" verkaufen.
10. Doppelzählung „wird erkannt" — Tools enumerieren nur → „potenzielle Dublette, manuell zu bestätigen".

Block C — **Operator-Dry-Run-Lage:** `validate_only` vorhanden bei allen Ads-Writes + `ga4_manage_audiences`; **kein** Dry-Run bei GA4-Writes + allen GTM-Writes (Skill simuliert selbst). GTM-Flow 4-stufig, `gtm_publish_version` einziger live-wirksamer Schritt.

- [ ] **Step 2: Verifikation**

Run: `test -f plugins/honeyfield-marketing-mcp/skills/tracking-check/references/tracking-tool-grenzen.md && grep -c "nicht prüfbar" plugins/honeyfield-marketing-mcp/skills/tracking-check/references/tracking-tool-grenzen.md`
Expected: Datei existiert, Treffer ≥1 (Beleg-Stufe vorhanden). Sichtprüfung: alle 10 Footguns + 3 Beleg-Stufen + Dry-Run-Lage enthalten.

- [ ] **Step 3: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/tracking-check/references/tracking-tool-grenzen.md
git commit -m "feat(tracking-check): Tool-Grenzen- und Beleg-Stufen-Referenz"
```

---

### Task 2: `event-soll-dach.md` (Event-Soll-Library)

**Files:**
- Create: `…/tracking-check/references/event-soll-dach.md`

**Interfaces:**
- Produces: Geschäftstyp-gegliederte Event-/Funnel-Soll-Listen, die Phase 5 in SKILL.md (Task 4) als Diff-Maßstab zieht.

**Empfohlener Research-Subagent (optional):** Ein Subagent kann Coreys `analytics/references/event-library.md` (`/Users/devbox/code-projects/other-repos/marketingskills/skills/analytics/references/event-library.md`) als Rohmaterial extrahieren und DACH-lokalisieren. Quelle ist bekannt; nur falls der volle Library-Text gebraucht wird.

- [ ] **Step 1: Datei schreiben — nach Geschäftstyp gegliedert**

Struktur (Quelle: Spec Abschnitt 8 + Corey-Event-Library):
- **Pro Geschäftstyp eine Sektion** mit (a) Kern-Events (Name `lowercase_underscore`, Object-Action, Beschreibung, Schlüssel-Properties) und (b) **Funnel-Sequenz** (nummerierte Event-Kette):
  - *Marketing-Site / Lead-Gen (DACH-Fokus, NEU):* `form_submit` (Anfrageformular), `phone_click` (`tel:`-Klick), `whatsapp_click`, `appointment_booked` (Terminbuchung), `directions_click` (Routenplaner), `email_click` (`mailto:`), `download` (Angebot/PDF). Funnel: `page_view` → `form_start` → `form_submit` → (offline) `lead_qualified`.
  - *E-Commerce:* `view_item`, `add_to_cart`, `begin_checkout`, `add_payment_info`, `purchase` (+ value/currency=EUR, transaction_id). Funnel: `view_item` → `add_to_cart` → `begin_checkout` → `add_payment_info` → `purchase`.
  - *SaaS/Product:* `sign_up`, `onboarding_completed`, `activation`, `subscribe`/`trial_start`. Funnel: `sign_up` → `onboarding_completed` → `activation` → `subscribe`.
  - *Lokaler Dienstleister (DACH, NEU):* wie Lead-Gen + `call_tracking`-Hinweis (statische Nummer vs. dynamic number insertion), GBP-Interaktionen out of scope (→ seo-audit).
- **Naming-Regeln** (Corey): Object-Action, lowercase_underscore, Kontext in Properties statt im Event-Namen.
- **DACH-Lokalisierung:** Währung EUR, deutsche Property-Beispiele; Lead-Gen/lokal priorisiert (Corey ist US-SaaS-lastig).
- Kopfzeile mit Nutzungshinweis: „Nur die geschäftstyp-relevante Sektion gegen den Kunden halten (aus `projekt-kontext`) — nicht die ganze Library."

- [ ] **Step 2: Verifikation**

Run: `grep -E "Lead-Gen|E-Commerce|SaaS|Lokaler" plugins/honeyfield-marketing-mcp/skills/tracking-check/references/event-soll-dach.md`
Expected: alle vier Geschäftstyp-Sektionen vorhanden. Sichtprüfung: jede Sektion hat Events + Funnel-Sequenz; DACH-Lead-Gen-Events (`phone_click`, `form_submit`, `whatsapp_click`, `appointment_booked`, `directions_click`) vorhanden.

- [ ] **Step 3: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/tracking-check/references/event-soll-dach.md
git commit -m "feat(tracking-check): Event-Soll-Library (Corey + DACH-Lead-Gen), nach Geschaeftstyp"
```

---

### Task 3: `dach-consent.md`

**Files:**
- Create: `…/tracking-check/references/dach-consent.md`

**Interfaces:**
- Produces: Den DACH-Consent-Detailkörper, auf den der Consent-Layer-Querschnitt in SKILL.md (Task 4) verweist.

**Empfohlener Research-Subagent (optional, empfohlen):** Consent-Recht ist aktualitätssensibel. Ein Subagent kann den aktuellen Stand zu Consent Mode v2 (`ad_user_data`/`ad_personalization`, basic vs. advanced), §25 TTDSG / DSGVO-Einwilligung, CMP-Landschaft (Usercentrics/Cookiebot/Consentmanager) und Server-Side-Tagging verifizieren, damit die Referenz nicht auf veraltetem Wissen beruht.

- [ ] **Step 1: Datei schreiben**

Pflichtinhalte (Quelle: Spec Abschnitt 5 „DACH-Consent-Layer"):
- **Was prüfbar (konfiguriert):** Consent-/CMP-Tag bzw. tag-level Consent-Settings im GTM via `gtm_list_tags`/`gtm_get_tag` — vorhanden/fehlt.
- **Was nicht prüfbar (beratend):** ob Consent Mode v2 korrekt greift (Default-denied → Update-on-grant; `ad_user_data`/`ad_personalization`), Tag-Firing vor Consent — Tool-Grenze, GTM-Preview/Tag-Assistant nötig.
- **Consent Mode v2:** die vier Signale, basic vs. advanced, was Google ab 2024 für Personalisierung/Remarketing verlangt.
- **DACH-Recht:** §25 TTDSG (DE) + DSGVO-Einwilligung, Cookie-Banner-Pflicht; AT/CH-Nuancen knapp. *Keine Rechtsberatung — nur Prüf-/Hinweischarakter.*
- **CMP-Landschaft:** Usercentrics, Cookiebot, Consentmanager — Integrationsmuster mit GTM/Consent Mode.
- **Server-Side-Tagging:** Zweck, woran erkennbar (`transport_url`/`server_container_url` im GA4-Config-Tag), warum Gesundheit nicht via API bestätigbar.
- **`compliance`-Flag-Verknüpfung:** gesetzte Flags aus `projekt-kontext` als harte Leitplanke.

- [ ] **Step 2: Verifikation**

Run: `grep -E "Consent Mode v2|TTDSG|ad_user_data|Server-Side" plugins/honeyfield-marketing-mcp/skills/tracking-check/references/dach-consent.md`
Expected: alle vier Begriffe vorhanden.

- [ ] **Step 3: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/tracking-check/references/dach-consent.md
git commit -m "feat(tracking-check): DACH-Consent-Referenz (Consent Mode v2, TTDSG, CMP, sGTM)"
```

---

### Task 4: `SKILL.md` (Haupt-Skill)

**Files:**
- Create: `…/tracking-check/SKILL.md`

**Interfaces:**
- Consumes: die drei References aus Task 1–3 (per „siehe `references/…`").
- Produces: den triggerbaren Skill; `evals` (Task 5) prüfen sein Verhalten.

- [ ] **Step 1: Frontmatter schreiben (description load-bearing)**

```yaml
---
name: tracking-check
description: "Datengetriebener Tracking- und Conversion-Audit für einen Kunden, kalibriert auf DACH (DE/AT/CH). Nutze diesen Skill, wenn geprüft werden soll, ob das Conversion- und Event-Tracking korrekt läuft: „stimmt mein Tracking“, „Conversions werden nicht gezählt“, „GA4 und Google Ads weichen ab“, „feuern meine Events / Tags“, „Conversion-Tracking prüfen“, „doppelte Conversions“, „Cookie-/Consent-Tracking DSGVO-konform“, „GTM-Setup prüfen“, „Tracking eingerichtet, aber nichts kommt an“. Zieht echte Daten aus GA4, Google Tag Manager und Google Ads über den Marketing-Ops-MCP, belegt jeden Befund nach Beweiskraft (gemessen / nur konfiguriert / nicht prüfbar) und behebt Sicheres nach Bestätigung. Für bezahlte Such-Performance nutze `google-ads-audit`; für organisches Ranking `seo-audit`; für KI-Sichtbarkeit `geo-audit`; fürs wöchentliche Reporting `wochenreport`."
metadata:
  version: 0.1.0
---
```
(Entwurf = 854 Zeichen Kerntext, mit Backticks ~862 — unter 1024. Achte beim Tippen darauf, dass jedes „ mit einem schließenden " U+201D endet.)

- [ ] **Step 2: Body schreiben — exakte Abschnittsfolge**

Quelle für jeden Abschnitt: Spec gleichnamiger Abschnitt. Reihenfolge (CLAUDE.md Audit-Struktur):
1. **Intro** (2–3 Sätze): Rolle als Fundament unter Ads-/SEO-Audit; datengetrieben, nicht checklisten-basiert; DACH.
2. **Drei Beleg-Stufen** — gemessen / nur konfiguriert / nicht prüfbar, je mit Ein-Satz-Definition; Verweis auf `references/tracking-tool-grenzen.md`.
3. **Schritt 0 — Vorbereitung:** kanonischer Projekt-Kontext-Absatz (CLAUDE.md, letzter Satz aufgabenspezifisch) + `compliance`-Flags; `list_workspaces` + sources-Check (`ga4`/`gtm`/`google_ads`); Markt-Kalibrierung.
4. **Phasen (Blocker zuerst)** — Phase 1 Gate (Tracking lebt?), 2 Key-Event-/Conversion-Config, 3 GA4↔Ads-Konsistenz, 4 GTM-Hygiene & Workspace-Drift, 5 Event-Coverage/Soll-Ist-Diff (Herzstück; geschäftstyp-relevante Sektion aus `event-soll-dach.md`), 6 Datenqualität. Pro Phase: konkrete Tools + die load-bearing Regel (z.B. Phase 4: Live vs. Draft vergleichen).
5. **DACH-Consent-Layer** (Querschnitt) — Präsenz prüfbar / Korrektheit beratend; Verweis `references/dach-consent.md`.
6. **Tool-Grenzen / Footguns** — Kurzliste + Verweis `references/tracking-tool-grenzen.md`; „Feuert"-nie-aus-Config-Regel, Workspace-Draft≠Live, realtime≠Firing-Beweis.
7. **Output-Format** — Kurz-Fazit + Befunde nach Phase (Problem/Wirkung/**Beleg+Stufe**/Fix/Priorität) + 4-Stufen-Maßnahmenplan + optionaler Tracking-Plan (Soll-Tabelle).
8. **Operator (Dry-Run + Bestätigung)** — Dry-Run-Lage (Ads `validate_only`; GA4/GTM kein Dry-Run → selbst simulieren); GTM-4-Schritt-Flow mit Bestätigung VOR `gtm_publish_version`, benannte Version + Change-Notes; Tabu-Liste (`gtm_publish_version` ungefragt, `ga4_delete_key_event`, `ga4_update_property`, Property/Stream anlegen = Setup out of scope).
9. **Grenzen** — die „nicht prüfbar"-Punkte ehrlich; kein Page-HTML; kein Setup-from-scratch.
10. **Tools nach Phase** — Tool-Liste je Phase (Anhang des Spec).
11. **Verwandte Skills** — `projekt-kontext` (zuerst) · `google-ads-audit` (Gate defert hierhin) · `seo-audit` · `geo-audit` · `wochenreport`.
12. **Referenzen** — die drei `references/`-Dateien mit Ein-Zeiler.

- [ ] **Step 3: Verifikation — Frontmatter-Parse + Länge + Schlankheit**

Run:
```bash
python3 .github/scripts/check_skill_frontmatter.py
python3 - <<'PY'
import re,sys
t=open('plugins/honeyfield-marketing-mcp/skills/tracking-check/SKILL.md',encoding='utf-8').read()
m=re.search(r'description:\s*"?(.*?)"?\nmetadata',t,re.S)
print("description Zeichen:", len(m.group(1)))
print("Zeilen gesamt:", t.count(chr(10))+1)
PY
```
Expected: `check_skill_frontmatter.py` meldet `OK: …/tracking-check/SKILL.md` (alle 5 Skills valide); description ≤1024; Zeilen ≤~500. Sichtprüfung: alle 12 Abschnitte vorhanden, Projekt-Kontext-Absatz drin, keine `kunden-kontext`-Reste.

- [ ] **Step 4: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/tracking-check/SKILL.md
git commit -m "feat(tracking-check): SKILL.md (6 Phasen, Beleg-Stufen, Dry-Run-Operator)"
```

---

### Task 5: `evals/evals.json`

**Files:**
- Create: `…/tracking-check/evals/evals.json`

**Interfaces:**
- Consumes: das Verhalten aus SKILL.md (Task 4) — `files`-Feld referenziert `SKILL.md` + die passende Referenz.

- [ ] **Step 1: 11 Cases schreiben** (Format wie `google-ads-audit/evals/evals.json`: `id`, `prompt`, `expected_output`, `assertions[]`, `files[]`). Cases (Quelle: Spec Abschnitt 9):

`trigger-basic-tracking-check`, `defer-to-google-ads-audit`, `defer-to-wochenreport`, `tool-reality-config-vs-firing`, `tool-reality-workspace-drift`, `tool-reality-consent-v2-not-verifiable`, `tool-reality-realtime-not-firing-proof`, `ga4-ads-consistency`, `event-coverage-funnel-gap`, `operator-confirmation-gtm-publish`, `dach-data-retention`.

Jede mit realistischem deutschem `prompt` + atomaren `assertions`. Load-bearing Assertions:
- `tool-reality-config-vs-firing`: „behauptet NICHT ‚Tag feuert' allein aus GTM-Config; verlangt Counts-Kreuzcheck".
- `tool-reality-workspace-drift`: „vergleicht Live-Version (`gtm_container_info`/`gtm_get_version`) mit Workspace-Draft (`gtm_list_tags`), benennt die Quelle".
- `tool-reality-consent-v2-not-verifiable`: „prüft Consent-Tag-Präsenz, deklariert Consent-v2-Korrektheit als nicht prüfbar".
- `operator-confirmation-gtm-publish`: „Bestätigung VOR `gtm_publish_version`, benannte Version mit Change-Notes".

- [ ] **Step 2: Verifikation**

Run: `python3 -m json.tool plugins/honeyfield-marketing-mcp/skills/tracking-check/evals/evals.json > /dev/null && python3 -c "import json;print(len(json.load(open('plugins/honeyfield-marketing-mcp/skills/tracking-check/evals/evals.json'))),'Cases')"`
Expected: valides JSON, `11 Cases`.

- [ ] **Step 3: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/tracking-check/evals/evals.json
git commit -m "feat(tracking-check): evals.json (11 Trigger-/Defer-/Tool-Reality-Cases)"
```

---

### Task 6: Version-Bump + Wiring + Gesamt-Validierung

**Files:**
- Modify: `plugins/honeyfield-marketing-mcp/.claude-plugin/plugin.json` (`version` 1.3.1 → 1.4.0)
- Modify: `.claude-plugin/marketplace.json` (Plugin-Eintrag `version` → 1.4.0; `metadata.version` → 1.4.0)
- Verify only: `google-ads-audit/SKILL.md`, `seo-audit/SKILL.md`, `projekt-kontext/SKILL.md` (die `tracking-check`-Verweise sind jetzt valide — kein Edit nötig, nur prüfen)

- [ ] **Step 1: Drei Versionsfelder auf 1.4.0 setzen**

`plugin.json` → `"version": "1.4.0"`. `marketplace.json` → im `plugins[]`-Eintrag von `honeyfield-marketing-mcp` `"version": "1.4.0"` UND `metadata.version` → `"1.4.0"`.

- [ ] **Step 2: Verweis-Konsistenz prüfen (kein Edit erwartet)**

Run: `grep -rl "tracking-check" plugins/honeyfield-marketing-mcp/skills/*/SKILL.md`
Expected: `google-ads-audit`, `seo-audit`, `projekt-kontext` listen `tracking-check` (Verweise jetzt valide). Falls ein Verweis fehlt/falsch → minimal korrigieren.

- [ ] **Step 3: Gesamt-Validierung (das Vollbild-„Testfenster")**

Run:
```bash
python3 .github/scripts/check_skill_frontmatter.py
python3 .github/scripts/check_version_sync.py
python3 -m json.tool plugins/honeyfield-marketing-mcp/skills/tracking-check/evals/evals.json > /dev/null && echo "evals OK"
claude plugin validate plugins/honeyfield-marketing-mcp/
```
Expected: 5 Skills frontmatter-valide; Versionen konsistent (`honeyfield-marketing-mcp @ 1.4.0`); evals OK; Manifest valide.

- [ ] **Step 4: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/.claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "feat(tracking-check): Plugin-Version 1.4.0 (neuer Measurement-Skill)"
```

---

## Self-Review (gegen den Spec)

**Spec-Coverage:**
- Spec §1 Zweck/Rolle → Task 4 Intro + Verwandte-Skills. ✓
- Spec §2 Scope (kein Setup) → Task 4 Operator-Tabu (Property/Stream anlegen). ✓
- Spec §3 Abgrenzung → Task 4 description + Task 5 defer-Cases. ✓
- Spec §4 Beleg-Stufen → Task 1 (Referenz) + Task 4 Abschnitt 2. ✓
- Spec §5 Phasen 0–6 + Consent + Footguns → Task 4 Abschnitte 3–6. ✓
- Spec §6 Output-Format → Task 4 Abschnitt 7. ✓
- Spec §7 Operator → Task 4 Abschnitt 8. ✓
- Spec §8 References → Tasks 1–3. ✓
- Spec §9 Evals → Task 5. ✓
- Spec §10 Version-Bump → Task 6. ✓
- Phase-5-Herzstück (Event-Coverage voll) → Task 2 Library + Task 4 Phase 5. ✓

**Placeholder-Scan:** keine „TBD"/„später"; Inhalts-Anforderungen pro Abschnitt konkret; load-bearing Bausteine (description, Beleg-Stufen, Footguns) wörtlich. References-Volltext bewusst nicht dupliziert (Skill-Authoring, DRY) — begründet im Header.

**Typ-/Namens-Konsistenz:** Tool-Namen über alle Tasks identisch (`ga4_list_key_events`, `gtm_get_tag`, `ads_conversion_performance`, …); Beleg-Stufen-Begriffe (gemessen / nur konfiguriert / nicht prüfbar) in Task 1 und Task 4 identisch; Version `1.4.0` konsistent über Task 6.

## Execution Handoff

Zwei Umsetzungs-Wege (siehe unten in der Konversation).
