# ad-creative Skill — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Einen neuen Creation-Skill `ad-creative` im Plugin `honeyfield-marketing-mcp` bauen, der daten-fundierte, DACH-rechtssichere Google-Ads-Textassets (RSA + Sitelinks) generiert/iteriert und nach Bestätigung als pausierte Assets ins Konto schreibt.

**Architecture:** Ein `SKILL.md` (Creation-Struktur: Schritt 0 + zwei Modi + Werberecht-Check + Operator) + zwei on-demand-`references/` (RSA-Mechanik, DACH-Ad-Copy/Werberecht) + `evals/evals.json`. Der Skill zieht echte Konto-Daten für Angles und validiert Zeichen/Recht selbst, weil die Tools das nicht erzwingen.

**Tech Stack:** Markdown-Skill (Agent-Skill-Spec), YAML-Frontmatter, JSON-Evals. MCP-Tools: `ads_*` (Create/Replace/Read).

**Hinweis zur Plan-Form:** Skill-Authoring, kein Code-TDD. „Test pro Task" = Validierungs-Pipeline (`check_skill_frontmatter.py`, `json.tool`, `check_version_sync.py`, `claude plugin validate`) + `evals`. Volltext nicht dupliziert (DRY); jede Task liefert exakte Struktur + Inhalts-Anforderungen + Akzeptanzkriterien, mit wörtlichen Bausteinen wo load-bearing (description, Ehrlichkeits-Regeln, Output-Format). Detailquelle: `docs/specs/2026-07-01-ad-creative-design.md`.

## Global Constraints

- **Sprache/Stil:** Deutsch, imperativ, terse, daten-first, ehrlich über Grenzen, DACH-kalibriert (DE/AT/CH).
- **Frontmatter:** `name: ad-creative` (== Verzeichnis). `metadata.version: 0.1.0`. `description` mit Trigger + Abgrenzung.
- **`description`-Limit ≤1024, Ziel ~950.** Deutsche Quotes „…" mit schließendem **U+201D** — NICHT U+201C, nicht ASCII `"`. **Verifikation zwingend:** Anzahl U+201E (öffnend) == Anzahl U+201D (schließend), Anzahl U+201C == 0, Anzahl ASCII-`"` in der description == 0. (Der Plan-Entwurf unten wurde mit falschem U+201C getippt — beim Übernehmen auf U+201D normalisieren und per grep prüfen.)
- **MCP-Tools** als Bare-Name in Backticks (`ads_create_ad`, `ads_search_terms`, …).
- **Creation-Skill-Struktur (bewusste Abweichung von der Audit-Konvention):** KEINE „Blocker zuerst"-Phasen. Stattdessen: Schritt 0 → zwei Modi (Neu / Iterieren) → DACH-Werberecht-Querschnitt → Output → Operator → Grenzen → Tools → Verwandte → Referenzen. Der kanonische Projekt-Kontext-Absatz bleibt Pflicht in Schritt 0.
- **SKILL.md ≤~500 Zeilen**; Tiefe in `references/` (per Verweis, nicht dupliziert).
- **`compliance`-Flags** aus `projekt-kontext` als harte Leitplanke; keine `kunden-kontext`-Altreferenzen.
- **Load-bearing Ehrlichkeits-Regeln — konsistent über SKILL.md + references + evals:**
  1. **Ad Strength ist NICHT auslesbar** — nie behaupten, sie auszulesen/zu setzen; „nach Best-Practice gebaut, Wert nur im UI".
  2. **RSA-Änderung = `ads_replace_ad` = neue Ad = Lernhistorie-Reset** — nie „Headline editieren".
  3. **Kein Pinning via Tools** — nur UI-Empfehlung.
  4. **Nur RSA + Sitelinks schreibbar** — Callouts/Snippets/Promotion/Price nur als Text-Vorschlag; Bild/Video/PMax out of scope.
  5. **Belegpflicht für Claims (UWG):** unbelegte Superlative („Nr. 1"/„beste") blocken, nicht generieren.
  6. **Zeichen-/Anzahl-Limits selbst validieren** (30 Headline / 90 Description / Paths 15; 3–15 Headlines, 2–4 Descriptions) — Tools erzwingen sie NICHT.
  7. **Write nur als `PAUSED` + Selbst-Dry-Run + Bestätigung**; kein autonomes `ENABLED`; `ads_remove_ad` (irreversibel) meiden → pausieren.
- **Version-Bump 1.4.0 → 1.5.0** in allen drei Feldern (neuer Skill = MINOR).
- **Vor Commit validieren:** `check_skill_frontmatter.py`, `json.tool` (evals), `check_version_sync.py`, `claude plugin validate`.

## File Structure

| Datei | Verantwortung |
|---|---|
| `plugins/honeyfield-marketing-mcp/skills/ad-creative/references/rsa-mechanik.md` | RSA-Struktur (15/4/Limits), Ad-Strength-Best-Practices (obwohl Wert nicht auslesbar), Replace-Mechanik + Lernhistorie-Reset, Pinning (beratend/UI), Headline-Mix, Statistik-Hygiene für Iteration. Rückgrat der technischen Korrektheit + Ehrlichkeit. |
| `…/ad-creative/references/dach-ad-copy.md` | DACH-Werberecht (UWG/PAngV/Health-Claims, Verbotsliste + neutrale Reframes), Komposita-/Zeichen-Disziplin, AT/CH-Linter, Angle-Kategorien (Fallback-Heuristik). |
| `…/ad-creative/SKILL.md` | Orchestrierung: Schritt 0, 2 Modi, Werberecht-Check, Output-Format, Operator, Grenzen. Schlank. |
| `…/ad-creative/evals/evals.json` | 11 Verhaltens-Cases (Trigger/Defer/Tool-Reality/UWG/Operator). |
| `plugins/honeyfield-marketing-mcp/.claude-plugin/plugin.json` | Version 1.4.0 → 1.5.0. |
| `.claude-plugin/marketplace.json` | Plugin-Eintrag-`version` + `metadata.version` → 1.5.0. |

**Bau-Reihenfolge:** References zuerst (SKILL.md verweist darauf) — `rsa-mechanik.md` (technisches Rückgrat, aus Tool-Reality ableitbar) vor `dach-ad-copy.md` (Werberecht, WebSearch-Recherche). Dann SKILL.md, evals, Version-Bump.

---

### Task 1: `references/rsa-mechanik.md`

**Files:**
- Create: `plugins/honeyfield-marketing-mcp/skills/ad-creative/references/rsa-mechanik.md`

**Interfaces:**
- Produces: die technischen RSA-Fakten + Ehrlichkeits-Grenzen, auf die SKILL.md (Task 3) verweist.

- [ ] **Step 1: Datei schreiben** — Blöcke (Quelle: Spec §4, §7, Anhang):
  - **RSA-Struktur:** 15 Headlines à max 30 Zeichen, 4 Descriptions à max 90 Zeichen, Path1/Path2 à 15 Zeichen; Bounds (min 3 Headlines, 2 Descriptions). **Tools erzwingen Limits NICHT → selbst prüfen.**
  - **Headline-Mix** (Verteilung der 15): ≈ 3–4 keyword / 3–4 benefit / 2–3 social-proof / 2–3 CTA / 1–2 differentiator / 1 brand.
  - **Ad-Strength-Best-Practices:** was Strength treibt (Anzahl nahe 15, Unique/Diversität, Keyword-Einbindung, wenig Redundanz) — **explizit: Strength-Wert ist über die MCP-Tools NICHT auslesbar; nur im UI sichtbar. Nie einen Strength-Wert behaupten.**
  - **Replace-Mechanik:** RSA unveränderlich → `ads_replace_ad` (Remove+Create+Merge, `None`=Feld behalten); `keep_old=true` pausiert die alte (reversibel). **Jede inhaltliche Änderung = neue Ad = Lernhistorie-Reset.** `ads_update_ad` DEPRECATED (=Replace). Einzige In-Place-Mutation: `ads_update_ad_status` (nur Status). Kein In-Place-URL-Update für Ads (nur Sitelink-`final_url`).
  - **Pinning:** über die Tools NICHT setzbar (flache string[]). Nur als UI-Empfehlung (Brand/Disclaimer ggf. Pos 1, sparsam — reduziert Optimierung).
  - **Statistik-Hygiene (Iteration):** Mindest-Impressions/Conversions bevor „Gewinner/Verlierer" (Richtwert nennen, z.B. ~1.000 Impressions), eine Variable pro Zyklus.
  - **Zeichen-Zähl-Tipps:** Leerzeichen zählen, DKI `{KeyWord:default}` kann Limit sprengen, Umlaut/ß = 1 Zeichen.

- [ ] **Step 2: Verifikation**

Run: `grep -icE "ad strength|nicht auslesbar|replace|lernhistorie|pinning" plugins/honeyfield-marketing-mcp/skills/ad-creative/references/rsa-mechanik.md`
Expected: ≥5 Treffer. Sichtprüfung: Ad-Strength-nicht-auslesbar + Replace-Reset + Pinning-beratend + 15/4-Limits + Statistik-Hygiene vorhanden.

- [ ] **Step 3: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/ad-creative/references/rsa-mechanik.md
git commit -m "feat(ad-creative): RSA-Mechanik-Referenz (Struktur, Ad-Strength-Grenzen, Replace)"
```

---

### Task 2: `references/dach-ad-copy.md`

**Files:**
- Create: `…/ad-creative/references/dach-ad-copy.md`

**Interfaces:**
- Produces: DACH-Werberecht + Copy-Disziplin, auf die der Werberecht-Querschnitt in SKILL.md verweist.

**Empfohlener Research-Subagent (empfohlen):** Werberecht ist aktualitätssensibel. Ein Subagent/WebSearch verifiziert den aktuellen Stand: UWG (§5 Irreführung, §6 vergleichende Werbung, Spitzenstellungs-/Superlativwerbung), PAngV (Fassung 2022: Grundpreis, „ab"-Preise, Gesamtpreis/MwSt.), Health-Claims-VO (EG 1924/2006) + HWG (DE), AT (UWG AT) + CH (PBV Preisbekanntgabeverordnung, kein ß).

- [ ] **Step 1: Datei schreiben** — Pflichtinhalte (Quelle: Spec §5 Werberecht-Layer, §4 Regel 5):
  - **UWG:** Irreführungsverbot; Superlative/Spitzenstellung („Nr. 1", „beste", „führend") nur mit **nachweisbarem Beleg** — sonst Abmahnrisiko. Vergleichende Werbung nur unter §6-Bedingungen.
  - **PAngV:** wenn Preise in der Copy — Gesamtpreis inkl. MwSt., „ab"-Kennzeichnung, ggf. Grundpreis; keine irreführenden Streichpreise.
  - **Health-Claims / branchen-spezifisch:** über `compliance`-Flags; Verbotsliste (unzulässige Wirkversprechen) + **neutrale Reframes** (Muster: Verbotsformulierung → rechtssichere Alternative).
  - **AT/CH-Linter:** CH kein ß („Strasse"), CH-Preisformat, PBV; AT-UWG-Nuancen knapp.
  - **Komposita-/Zeichen-Disziplin:** deutsche Wortlänge gegen 30-Zeichen-Headline; Vermeidungs-Strategien (Kurzform „PM-Tool" statt „Projektmanagement-Software", Bindestrich/Trennung), Beispiele.
  - **Angle-Kategorien (Fallback-Heuristik):** Pain / Outcome / Social-Proof / Curiosity / Comparison / Urgency / Identity — als Fallback wenn keine Konto-Daten; nachrangig zur Datenfundierung.
  - Header: „Keine Rechtsberatung — Prüf-/Hinweischarakter."

- [ ] **Step 2: Verifikation**

Run: `grep -icE "UWG|PAngV|Superlativ|Komposita|Health|neutrale? Reframe" plugins/honeyfield-marketing-mcp/skills/ad-creative/references/dach-ad-copy.md`
Expected: ≥5 Treffer. Sichtprüfung: UWG-Superlativregel + PAngV + Health-Claims-Flag + Komposita-Disziplin + Verbotsliste/Reframes + Rechtsberatungs-Disclaimer.

- [ ] **Step 3: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/ad-creative/references/dach-ad-copy.md
git commit -m "feat(ad-creative): DACH-Ad-Copy-Referenz (UWG/PAngV, Komposita, Angles)"
```

---

### Task 3: `SKILL.md`

**Files:**
- Create: `…/ad-creative/SKILL.md`

**Interfaces:**
- Consumes: die zwei References (Task 1–2) per Verweis.
- Produces: den triggerbaren Skill; `evals` (Task 4) prüfen sein Verhalten.

- [ ] **Step 1: Frontmatter (description load-bearing — U+201D-Verifikation!)**

description-Entwurf (Kerntext ~858 Zeichen; **Skill-Namen in Backticks setzen**; **alle schließenden Anführungszeichen auf U+201D normalisieren**):

> Generiert und optimiert Google-Ads-Anzeigen-Copy (Responsive Search Ads + Sitelinks), daten-fundiert aus der Konto-Performance und kalibriert auf DACH (DE/AT/CH). Nutze diesen Skill, wenn Anzeigen oder Text-Assets erstellt oder erneuert werden sollen: „neue Anzeigen schreiben", „RSA erstellen", „Headlines/Descriptions generieren", „bessere Anzeigentexte", „Anzeigen austauschen", „Sitelinks anlegen", „Ad-Copy für Kampagne X", „mehr Headlines für die RSA". Leitet Angles aus echten Suchbegriffen ab, hält die harten Google-Zeichen-Limits gegen deutsche Komposita, prüft DACH-Werberecht (UWG/Preisangaben) über `compliance`-Flags und schreibt Anzeigen nach Bestätigung als pausierte Assets ins Konto. Für die Diagnose bestehender Anzeigen (welche sind schwach, Wasted Spend) nutze `google-ads-audit`; für Landingpage-Text `seo-audit`; fürs Reporting `wochenreport`.

Frontmatter: `name: ad-creative`, `metadata.version: 0.1.0`.

- [ ] **Step 2: Body — Creation-Struktur** (Quelle: Spec §5–§8):
  1. **Intro** (2–3 Sätze): Rolle + Moat (daten-fundiert, DACH-rechtssicher, sicherer Write — nicht „Claude schreibt Texte").
  2. **Ehrlichkeits-Modell:** Achse 1 (daten-fundiert vs. Heuristik) + Achse 2 Schreibbarkeits-Tabelle (RSA/Sitelinks schreibbar; Callouts/Snippets/Pinning/Visuals nicht) + die Load-bearing-Regeln kurz; Verweis `references/rsa-mechanik.md`.
  3. **Schritt 0:** kanonischer Projekt-Kontext-Absatz (Brand-Ton, USPs, **`compliance`-Flags**), `list_workspaces`/sources (`google_ads`?), Ziel-Kampagne/Ad-Group (`ads_list_campaigns`/`ads_list_ad_groups`; Ad-Group muss vor Ad existieren), Markt DE/AT/CH.
  4. **Modus A — Neu generieren:** Daten-Fundierung (`ads_search_terms`/`ads_ai_max_search_terms`/`ads_keyword_performance` → 3–5 Angles) → 15 Headlines nach Mix + 4 Descriptions, DACH-Zeichen-Disziplin, Themen-Cluster→Ad-Group-Bezug.
  5. **Modus B — Aus Performance iterieren:** `ads_list_ads`/`ads_ad_performance` (+ optional `google-ads-audit`-Befunde) → Gewinner verstärken, Verlierer ersetzen; Statistik-Hygiene (Mindest-Impressions).
  6. **DACH-Werberecht-Check** (Querschnitt, vor jedem Write): UWG/PAngV/Health via `compliance`-Flags; Verweis `references/dach-ad-copy.md`.
  7. **Output-Format** (selbstverifizierend): je Zeile Text · `(Zeichen)` · `✓`/`⚠ ÜBER LIMIT`/`⚠ UWG` · `[Mix-Typ]` · bei Problem getrimmte/rechtssichere Alternative. Abschluss: Angle-/Ad-Group-Zuordnung, daten-fundiert-vs-Heuristik, Ad-Strength-Best-Practice-Selbstcheck (**kein** behaupteter Wert).
  8. **Operator:** Neu = ggf. `ads_create_ad_group` → `ads_create_ad` (`status="PAUSED"`) → Selbst-Dry-Run + Bestätigung → Freigabe später `ads_update_ad_status ENABLED` (getrennt). Ersetzen = `ads_list_ads` → `ads_replace_ad` (`keep_old=true`) + „neue Ad, Historie-Reset". Sitelinks = `ads_create_sitelink`/`ads_update_sitelink`. **Tabu:** autonom `ENABLED`, `ads_remove_ad`.
  9. **Grenzen:** Ad Strength/Asset-Labels nicht auslesbar · kein Pinning · nur RSA+Sitelinks schreibbar · kein Bild/Video/PMax · kein Tool-Dry-Run · Replace resettet Historie · nur Google Search.
  10. **Tools nach Modus.** 11. **Verwandte Skills** (`projekt-kontext`, `google-ads-audit` [findet→füllt], `tracking-check`, `wochenreport`). 12. **Referenzen** (die zwei).

- [ ] **Step 3: Verifikation**

Run:
```bash
python3 .github/scripts/check_skill_frontmatter.py
python3 - <<'PY'
import re
t=open('plugins/honeyfield-marketing-mcp/skills/ad-creative/SKILL.md',encoding='utf-8').read()
m=re.search(r'description:\s*"?(.*?)"?\nmetadata',t,re.S); d=m.group(1)
print("description Zeichen:", len(d))
print("U+201E:", d.count(chr(0x201E)), "U+201D:", d.count(chr(0x201D)), "U+201C:", d.count(chr(0x201C)), "ASCII-quote:", d.count('"'))
print("Zeilen:", t.count(chr(10))+1)
PY
```
Expected: frontmatter `OK: …/ad-creative/SKILL.md` (6 Skills valide); description ≤1024; **U+201E-Count == U+201D-Count, U+201C == 0, ASCII-quote == 0**; Zeilen ≤~500. Sichtprüfung: 12 Abschnitte, Projekt-Kontext-Absatz, keine `kunden-kontext`-Reste, Ehrlichkeits-Regeln drin.

- [ ] **Step 4: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/ad-creative/SKILL.md
git commit -m "feat(ad-creative): SKILL.md (2 Modi, Ehrlichkeits-Modell, Dry-Run-Operator)"
```

---

### Task 4: `evals/evals.json`

**Files:**
- Create: `…/ad-creative/evals/evals.json`

**Interfaces:**
- Consumes: SKILL.md-Verhalten (Task 3); `files[]` referenziert `SKILL.md` + passende Referenz.

- [ ] **Step 1: 11 Cases** (Format wie `google-ads-audit/evals/evals.json`: `id`, `prompt` (deutsch, realistisch), `expected_output`, `assertions[]`, `files[]`). Cases (Quelle: Spec §10):

`trigger-basic-ad-creative`, `defer-to-google-ads-audit`, `data-founded-angles`, `dach-char-limit-komposita`, `uwg-superlativ-block`, `tool-reality-ad-strength`, `tool-reality-rsa-replace`, `tool-reality-no-pinning`, `tool-reality-callout-not-writable`, `operator-paused-confirmation`, `iterate-statistik-hygiene`.

Load-bearing Assertions:
- `tool-reality-ad-strength`: behauptet NICHT, Ad Strength auszulesen/zu setzen; baut nach Best-Practice.
- `tool-reality-rsa-replace`: erklärt Änderung als `ads_replace_ad` (neue Ad, Historie-Reset), nicht als In-Place-Edit.
- `tool-reality-no-pinning`: Pinning nur UI-Empfehlung, kein Pin-Write behauptet.
- `uwg-superlativ-block`: blockt unbelegtes „Nr. 1"/„beste", verlangt Beleg oder reframed.
- `operator-paused-confirmation`: RSA als `PAUSED`, Vorschau + Bestätigung, kein autonomes `ENABLED`.

- [ ] **Step 2: Verifikation**

Run: `python3 -m json.tool plugins/honeyfield-marketing-mcp/skills/ad-creative/evals/evals.json > /dev/null && python3 -c "import json;print(len(json.load(open('plugins/honeyfield-marketing-mcp/skills/ad-creative/evals/evals.json'))),'Cases')"`
Expected: valides JSON, `11 Cases`.

- [ ] **Step 3: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/skills/ad-creative/evals/evals.json
git commit -m "feat(ad-creative): evals.json (11 Trigger-/Defer-/Tool-Reality-Cases)"
```

---

### Task 5: Version-Bump + Wiring + Gesamt-Validierung

**Files:**
- Modify: `plugins/honeyfield-marketing-mcp/.claude-plugin/plugin.json` (`version` 1.4.0 → 1.5.0)
- Modify: `.claude-plugin/marketplace.json` (Plugin-Eintrag `version` → 1.5.0; `metadata.version` → 1.5.0)

- [ ] **Step 1: Drei Versionsfelder auf 1.5.0** (nur `honeyfield-marketing-mcp`, andere Plugins nicht anfassen).

- [ ] **Step 2: Verweis-Check (kein Edit erwartet)**

Run: `grep -rl "ad-creative" plugins/honeyfield-marketing-mcp/skills/*/SKILL.md`
Expected: mindestens `ad-creative` selbst; falls `google-ads-audit` einen Verweis „für Anzeigen-Erstellung siehe `ad-creative`" bekommen soll, das minimal ergänzen (optional, im Report begründen).

- [ ] **Step 3: Gesamt-Validierung**

Run:
```bash
python3 .github/scripts/check_skill_frontmatter.py
python3 .github/scripts/check_version_sync.py
python3 -m json.tool plugins/honeyfield-marketing-mcp/skills/ad-creative/evals/evals.json > /dev/null && echo "evals OK"
claude plugin validate plugins/honeyfield-marketing-mcp/
```
Expected: 6 Skills frontmatter-valide; `honeyfield-marketing-mcp @ 1.5.0` konsistent; evals OK; Manifest valide.

- [ ] **Step 4: Commit**

```bash
git add plugins/honeyfield-marketing-mcp/.claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "feat(ad-creative): Plugin-Version 1.5.0 (neuer Creation-Skill)"
```

---

## Self-Review (gegen den Spec)

**Spec-Coverage:** §1 Zweck→Task 3 Intro/Verwandte ✓ · §2 Scope (Google/RSA/Sitelinks, kein Batch/Callout/Pinning/Visual)→Task 3 Grenzen + Operator-Tabu ✓ · §3 Abgrenzung→Task 3 description + Task 4 defer ✓ · §4 Ehrlichkeits-Modell→Task 1 (rsa-mechanik) + Task 3 Abschnitt 2 + Global Constraints ✓ · §5 Struktur/Modi/Werberecht→Task 3 + Task 2 ✓ · §6 Output→Task 3 Abschnitt 7 ✓ · §7 Operator→Task 3 Abschnitt 8 ✓ · §8 Grenzen→Task 3 Abschnitt 9 ✓ · §9 References→Task 1+2 ✓ · §10 Evals→Task 4 ✓ · §11 Version→Task 5 ✓.

**Placeholder-Scan:** keine TBD; Inhalts-Anforderungen konkret; load-bearing Bausteine (description, Ehrlichkeits-Regeln, Output-Format) wörtlich; References-Volltext bewusst nicht dupliziert (Skill-Authoring, DRY).

**Typ-/Namens-Konsistenz:** Tool-Namen identisch über Tasks (`ads_create_ad`, `ads_replace_ad`, `ads_update_ad_status`, `ads_search_terms`, `ads_create_sitelink`); Ehrlichkeits-Regeln (Ad Strength nicht auslesbar / Replace-Reset / kein Pinning / PAUSED) in Task 1, 3, 4 identisch; Version `1.5.0` konsistent in Task 5.

## Execution Handoff
Subagent-Driven (siehe Konversation): ein Implementer pro Task + Task-Review, dann finaler whole-branch Review.
