# Design-Spec: `ad-creative` (Google-Ads-Copy/Asset-Generator)

- **Datum:** 2026-07-01
- **Plugin:** `honeyfield-marketing-mcp`
- **Status:** Design freigegeben (Scope: Google + Write; Umfang: fokussiert 1 RSA + Iteration), Spec zur Review
- **Typ:** neuer Skill — erster **Creation-Skill** im Plugin (bisher nur Audits + Foundation)
- **Deliverable:** daten-fundierte, DACH-rechtssichere Google-Ads-Textassets (RSA + Sitelinks), sicher ins Konto geschrieben

## 1. Zweck & Rolle

`ad-creative` generiert Google-Ads-**Textassets** (Responsive Search Ads + Sitelinks) für einen Kunden — **daten-fundiert** aus der echten Konto-Performance, **RSA-struktur-korrekt**, **DACH-rechtssicher**, und schreibt sie nach Bestätigung als **pausierte** Assets ins Konto. Es ist der Creation-Gegenpart zu `google-ads-audit`: der Audit *findet* schwache/fehlende Creatives, `ad-creative` *füllt* die Lücke.

Warum ein Skill und nicht „Claude schreibt Texte": der Moat ist (1) Angles aus echten Konto-Daten statt erfundener Kategorien, (2) harte DACH-Zeichen-Disziplin gegen deutsche Komposita, (3) DACH-Werberecht als Leitplanke, (4) sicherer Write-Operator, (5) Belegpflicht für Claims (UWG). Keins davon hat generisches Claude oder Coreys tool-agnostischer `ad-creative`.

## 2. Scope

**In Scope:**
- **Google Search — RSA** (bis 15 Headlines / 4 Descriptions) + **Sitelinks**. Die einzigen via MCP schreibbaren Text-Asset-Typen.
- **Modus A — neu generieren** (aus projekt-kontext + Konto-Suchdaten).
- **Modus B — aus Performance iterieren** (Gewinner verstärken, Verlierer ersetzen; koppelt an `google-ads-audit`).
- Write-Operator: Anlage als `PAUSED`, Dry-Run selbst simuliert, Bestätigung.
- DACH-Werberecht-Layer + Zeichen-Disziplin.

**Out of Scope (bewusst):**
- **Batch/Bulk** über viele Ad-Groups (Corey-Waves) — spätere Erweiterung.
- **Callouts / Structured Snippets / Promotion / Price** — via MCP nicht schreibbar (nur lesbar); als Text-Vorschlag liefern, User baut im UI.
- **Pinning** — kein Tool-Parameter; nur als Empfehlung fürs UI.
- **Bild/Video/Display/PMax-Assets** — kein Write-Tool, anderes Deliverable.
- **Meta/LinkedIn/andere Plattformen** — MCP hat dort keine Creative-Write-Tools.
- **Landing-Page-Copy** — CMS/Content, nicht hier.
- **Kampagnen-Strategie/Budget/Gebote** — das ist Audit/Operator-Terrain, nicht Creation.

## 3. Abgrenzung (steuert die `description`)
- `google-ads-audit` = Diagnose bestehender Anzeigen (findet „Ad Strength schwach / nur 3 Headlines / RSA fehlt") → **defert die Creative-Erstellung hierhin**.
- `ad-creative` = Erstellung/Iteration der Anzeigen-Copy + Write.
- Reporting → `wochenreport`. Tracking → `tracking-check`. Organisch → `seo-audit`.
- **Trigger:** „neue Anzeigen / RSA schreiben", „Anzeigentexte erstellen", „Headlines/Descriptions generieren", „bessere Anzeigen", „Anzeigen erneuern/austauschen", „Sitelinks anlegen", „Ad-Copy für Kampagne X", „RSA mit mehr Headlines".

## 4. Ehrlichkeits-Modell (der Moat — direkt aus der Tool-Reality)

Zwei Achsen, jede Ausgabe wird danach gekennzeichnet:

**Achse 1 — Herkunft der Copy:**
- **Daten-fundiert:** Angles/Themen/Sprache aus `ads_search_terms`, `ads_ai_max_search_terms`, `ads_list_ads`, `ads_ad_performance`, `ads_keyword_performance` — auf ein reales Query-Thema / Conversion-Signal zurückführbar.
- **Heuristik (Fallback):** ohne Konto-Daten aus projekt-kontext + Angle-Kategorien (Corey-Muster) generiert — als solche kennzeichnen.

**Achse 2 — Schreibbarkeit:**
| Asset | Schreibbar via MCP? | Handhabung |
|---|---|---|
| RSA (Headlines/Descriptions/Paths/URLs) | **Ja** (`ads_create_ad`/`ads_replace_ad`) | Anlage als `PAUSED`, Dry-Run + Bestätigung |
| Sitelinks | **Ja** (`ads_create_sitelink`/`ads_update_sitelink`) | dito |
| Callouts, Structured Snippets, Promotion, Price | **Nein** (nur lesbar) | als Text liefern, User baut im UI |
| Pinning, Bild/Video/PMax | **Nein** | Pinning = Empfehlung; Visuals out of scope |

**Load-bearing Ehrlichkeits-Regeln:**
1. **Ad Strength ist NICHT auslesbar.** Nie „ich verbessere deine Ad Strength von Poor auf Excellent" behaupten. Ehrlich: „nach Best-Practice gebaut (Menge/Diversität/Keyword-Bezug) — den Strength-Wert siehst du nur im UI".
2. **Per-Asset-Labels (Best/Good/Low) nicht lesbar.** Argumentation über Ad-Level-Performance + Suchbegriffe, nicht über Googles Asset-Rating.
3. **RSA-Änderung = Replace = neue Ad = Lernhistorie reset.** Nie „ich editiere Headline 3" — immer „ich erstelle eine neue Version und pausiere die alte". Auch URL-Änderung an einer Ad läuft über Replace (nur Sitelink-`final_url` geht in-place).
4. **Belegpflicht für Claims (UWG):** Superlative/Zahlen („Nr. 1", „beste", „10.000+ Kunden") nur mit Beleg aus Konto/projekt-kontext — sonst blocken, nicht generieren.
5. **Zeichen-Limits selbst prüfen:** Schema erzwingt 30/90 + Anzahl NICHT → der Skill validiert vor jedem Write, sonst failt Google serverseitig spät.

## 5. Struktur

### Schritt 0 — Vorbereitung
- **Projekt-Kontext zuerst** (kanonischer Absatz): Brand-Tonalität, USPs/Value-Props, Ziel-Keywords, **`compliance`-Flags als harte Leitplanke** (z.B. Health-Claims bei Medizin, keine Superlative). Fehlt er → anbieten via `projekt-kontext`.
- `list_workspaces` + sources (`google_ads` verbunden?); Ziel-Kampagne + Ad-Group klären (`ads_list_campaigns`/`ads_list_ad_groups`). Ad-Group muss existieren, bevor eine Ad angelegt wird.
- Markt (DE/AT/CH) — für AT/CH-Linter (kein ß auf CH, Preisformat) und Rechtslage.

### Modus A — Neu generieren
1. **Daten-Fundierung:** `ads_search_terms` / `ads_ai_max_search_terms` (gewinnende Suchsprache/Themen), `ads_keyword_performance` (QS/Conversions der Ziel-Keywords). Daraus 3–5 **Angles** ableiten (daten-fundiert; Fallback: Angle-Kategorien).
2. **RSA-Copy:** 15 Headlines nach **Mix** (≈ 3–4 keyword / 3–4 benefit / 2–3 social-proof / 2–3 CTA / 1–2 differentiator / 1 brand) + 4 Descriptions. **DACH-Zeichen-Disziplin**: 30/90 hart, Komposita-Vermeidung („PM-Tool" statt „Projektmanagement-Software" wo möglich), Umlaut/ß = 1 Zeichen, DKI `{KeyWord:default}` kann Limit sprengen.
3. **Themen-Cluster → Ad-Group-Bezug:** Headlines auf das Keyword-Thema der Ad-Group ausrichten (Ad-Strength-Best-Practice: Keyword-Einbindung + Diversität + genug Unique Headlines).

### Modus B — Aus Performance iterieren
1. `ads_list_ads` + `ads_ad_performance` (Ist-Copy + Ad-Level-Performance). Optional: Befunde aus `google-ads-audit` als Input.
2. Gewinner-Muster (Themen/Formulierungen der besseren Ads) verstärken; schwache Ads ersetzen.
3. **Statistik-Hygiene:** Mindest-Impressions/Conversions bevor „Gewinner/Verlierer" behauptet wird; eine Variable pro Zyklus; kein Urteil auf dünner Datenbasis.

### DACH-Werberecht-Check (quer, vor jedem Write)
- **UWG:** Irreführung/Superlative nur mit Beleg; keine unklaren Spitzenstellungs-Behauptungen.
- **PAngV:** Preise korrekt (Grundpreis, „ab"-Kennzeichnung, MwSt.-Klarheit) wenn Preise in der Copy.
- **Health-Claims / branchen-spezifisch:** über `compliance`-Flags gesteuert (Verbotsliste + neutrale Reframes, Muster wie Coreys CFM-Block, aber DACH).
- Detail in `references/dach-ad-copy.md`.

## 6. Output-Format
**Selbstverifizierend** (Corey-Muster, adaptiert), pro Zeile die Zeichenzahl:
```
Headlines:
  1. Projektmanagement einfach        (28) ✓  [keyword]
  2. In 5 Minuten startklar           (24) ✓  [benefit]
  3. Die beste PM-Software überhaupt  (30) ⚠ UWG: unbelegter Superlativ → „PM-Software für Teams" (23)
  ...
Descriptions:
  1. …                                (88) ✓
```
- Jede Zeile: Text · `(Zeichen)` · `✓`/`⚠ ÜBER LIMIT`/`⚠ UWG` · `[Mix-Typ]` · bei Problem die getrimmte/rechtssichere Alternative.
- Abschluss: Angle-Zuordnung, Ad-Group-Bezug, was daten-fundiert vs. Heuristik ist, Ad-Strength-Best-Practice-Selbstcheck (Menge/Diversität/Unique/Keyword — **kein** behaupteter Strength-Wert).

## 7. Operator (Write — kein Tool-Dry-Run, Skill simuliert selbst)
- **Neu:** ggf. `ads_create_ad_group` (falls keine passende existiert) → `ads_create_ad` mit **`status="PAUSED"`** → Vorschau/Selbst-Dry-Run zeigen → Bestätigung → (Freigabe später via `ads_update_ad_status ENABLED`, bewusst getrennt).
- **Ersetzen:** `ads_list_ads` (aktuelle Felder) → `ads_replace_ad` mit `keep_old=true` (alte wird **pausiert**, nicht gelöscht — reversibel) → Hinweis „neue Ad-Entität, Lernhistorie startet neu".
- **Sitelinks:** `ads_create_sitelink` / `ads_update_sitelink` (Text-Änderung erzeugt Ersatz-Asset + Re-Linking → dem Nutzer sagen).
- **Zwingend vor jedem Write:** Zeichen-/Anzahl-Validierung + Vorschau + explizite Bestätigung.
- **Tabu ohne ausdrückliche Rücksprache:** Anlage/Umschaltung auf `ENABLED` (nie autonom live schalten), `ads_remove_ad` (irreversibel — stattdessen pausieren), Keyword-/Ad-Group-Bulk-Änderungen.

## 8. Grenzen (ehrlich benennen)
Ad Strength & Asset-Labels nicht auslesbar · kein Pinning via Tools · nur RSA + Sitelinks schreibbar (Callouts/Snippets beratend) · kein Bild/Video/PMax · kein Tool-Dry-Run (Skill simuliert) · RSA-Replace resettet Lernhistorie · nur Google Search.

## 9. References
- `references/dach-ad-copy.md` — DACH-Werberecht (UWG/PAngV/Health-Claims, Verbotsliste + neutrale Reframes), Komposita-/Zeichen-Disziplin, AT/CH-Linter, Headline-Mix-Empfehlung, Angle-Kategorien (Fallback-Heuristik).
- `references/rsa-mechanik.md` — RSA-Struktur (15/4, Limits), Ad-Strength-Best-Practices (was Strength treibt, obwohl nicht auslesbar), Replace-Mechanik + Lernhistorie-Reset, Pinning-Strategie (beratend/UI), Statistik-Hygiene für Iteration.

## 10. Evals (`evals/evals.json`)
- `trigger-basic-ad-creative` — „schreib neue Anzeigen für Kampagne X" → Schritt 0, sources, Modus A.
- `defer-to-google-ads-audit` — „welche meiner Anzeigen sind schlecht / soll ich Budget umschichten" → Audit.
- `data-founded-angles` — leitet Angles aus `ads_search_terms`/`ai_max_search_terms` ab, nicht aus erfundenen Kategorien.
- `dach-char-limit-komposita` — hält 30/90 ein, vermeidet Komposita-Überlänge, zeigt Zeichenzahl.
- `uwg-superlativ-block` — blockt unbelegtes „Nr. 1"/„beste", verlangt Beleg oder reframed.
- `tool-reality-ad-strength` — behauptet NICHT, Ad Strength auszulesen/zu setzen; baut nach Best-Practice.
- `tool-reality-rsa-replace` — erklärt RSA-Änderung als Replace (neue Ad, Historie-Reset), nicht als In-Place-Edit.
- `tool-reality-no-pinning` — bietet Pinning nur als UI-Empfehlung, behauptet keinen Pin-Write.
- `tool-reality-callout-not-writable` — Callouts/Snippets als Text-Vorschlag, kein Konto-Write behauptet.
- `operator-paused-confirmation` — legt RSA als `PAUSED` an, Vorschau + Bestätigung, kein autonomes `ENABLED`.
- `iterate-statistik-hygiene` — kein „Gewinner/Verlierer"-Urteil auf dünner Datenbasis (Mindest-Impressions).

## 11. Offene Punkte (vor/bei Implementierung)
- `description` ≤1024 mit deutschen Quotes-Footgun (schließend U+201D), Ziel ~950.
- Version-Bump 1.4.0 → **1.5.0** in allen drei Feldern (neuer Skill = MINOR).
- CLAUDE.md „Creation-Skill"-Kategorie: prüfen, ob die Audit-Skill-Struktur-Konvention einen Creation-Zusatz braucht (dieser Skill ist der erste Nicht-Audit-Nicht-Foundation-Skill).
- DACH-Werberecht in `dach-ad-copy.md`: aktueller Stand per WebSearch verifizieren (UWG-Novelle, PAngV 2022, Health-Claims-VO).

## Anhang — Tool-Inventar (aus Tool-Reality)
**Write:** `ads_create_ad` (RSA, default ENABLED → PAUSED setzen), `ads_replace_ad` (=Edit via Remove+Create, `keep_old`), `ads_update_ad_status` (einzige In-Place-Mutation), `ads_create_sitelink`/`ads_update_sitelink`, `ads_create_ad_group`, `ads_add_keyword`. `ads_update_ad` DEPRECATED. `ads_remove_ad` irreversibel (meiden). **Kein `validate_only` bei irgendeinem Write.**
**Read (Fundierung):** `ads_list_ads` (Copy+Status+Approval, KEIN Ad Strength), `ads_list_assets` (liest auch Callouts/Snippets), `ads_ad_performance`, `ads_search_terms`, `ads_ai_max_search_terms` (Headline-Granularität), `ads_keyword_performance`, `ads_list_ad_groups`/`ads_list_campaigns`.
