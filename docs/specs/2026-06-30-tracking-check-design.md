# Design-Spec: `tracking-check` (Measurement-Audit-Skill)

- **Datum:** 2026-06-30
- **Plugin:** `honeyfield-marketing-mcp`
- **Status:** Design freigegeben (Scope + Event-Coverage-Tiefe bestätigt), Spec zur Review
- **Typ:** neuer Topic-Skill (Measurement), Audit + gezielte Fixes
- **Löst:** die tote `tracking-check`-Referenz in `google-ads-audit`, `seo-audit`, `projekt-kontext`

## 1. Zweck & Rolle

`tracking-check` prüft die **Integrität des Conversion- und Event-Trackings** eines Kunden end-to-end über GA4 + GTM + Google Ads, belegt jeden Befund mit echten Daten **oder** legt die Tool-Grenze offen, und behebt Sicheres nach Bestätigung. Es ist das **Fundament unter Ads-/SEO-Audit**: ist das Tracking kaputt, sind deren CPA/ROAS/Conversion-Zahlen Makulatur.

Der definierende Unterschied zu reinen Wissens-Skills (wie `marketingskills/analytics`): wir **lesen die gemessene Realität** des Kunden-Accounts und halten sie gegen ein Soll — statt zu beschreiben, wie man manuell in DebugView nachschaut.

## 2. Scope

**In Scope:**
- Audit bestehender Tracking-Setups (Diagnose).
- Gezielte Fixes als Operator (Key Event markieren, Conversion-Action anlegen/fixen, GTM-Tag/Trigger erstellen, GA4↔Ads-Link setzen, Enhanced Measurement / Data Retention setzen).
- **Volle Event-Coverage** (Phase 5 als Herzstück): komplette Event-Taxonomie + Funnel gegen die Event-Soll-Library diffen, inkl. Naming-Hygiene, Custom Dimensions/Metrics, Tracking-Plan als Output.
- DACH-Consent-Layer (Präsenz-Check + beratende Tiefe).

**Out of Scope (bewusst):**
- **Setup-from-scratch** für Neukunden ohne jegliches Tracking (GA4-Property + Stream + Container von Null). Aufgehoben für späteren `tracking-setup`-Skill, falls der Website-Launch-Fall häufig wird.
- Reporting / Zahlen-Entwicklung über Zeit → `wochenreport`.
- Page-Level-Snippet-Installation (kein Tool liest Seiten-HTML; ggf. via On-Page-Crawl im seo-audit).

## 3. Abgrenzung zu Schwester-Skills (steuert die `description`)

- `google-ads-audit` behält das **schlanke Tracking-Gate** (existiert ein Conversion-Tracking? grobe GA4-Plausibilität) und **defert die Tiefe hierhin**. `tracking-check` ist die Tiefe.
- `seo-audit` nutzt `gtm_create_tag` punktuell für fehlendes Tracking; die **Tracking-Integrität** (feuert alles, konsistent, konform?) liegt hier.
- Reporting → `wochenreport`. Organisches Ranking → `seo-audit`. Paid-Performance → `google-ads-audit`. KI-Sichtbarkeit → `geo-audit`.
- **Trigger-Phrasen:** „stimmt mein Tracking", „Conversions kommen nicht an / werden nicht gezählt", „GA4 und Google Ads weichen ab", „feuern meine Events / Tags", „Conversion-Tracking einrichten/prüfen", „Cookie-/Consent-Tracking DSGVO", „GTM-Setup prüfen", „Tracking eingerichtet aber nichts passiert", „doppelte Conversions".

## 4. Beleg-Stufen (Herzstück der Ehrlichkeit — direkt aus der Tool-Reality)

Jeder Befund wird nach Beweiskraft gekennzeichnet:

| Stufe | Bedeutung | Quelle (Tools) |
|---|---|---|
| **Gemessen** | Daten fließen real | `ga4_list_key_events` (Per-Event-Counts), `ga4_conversions`, `ga4_report`, `ads_list_conversion_actions` (letztes Conversion-Datum), `ads_conversion_performance` (`last_gap_days`), `ga4_manage_google_ads_links` (list), `ga4_enhanced_measurement`/`ga4_data_retention` (get) |
| **Konfiguriert** | verdrahtet, Firing **unbewiesen** | `gtm_get_tag`, `gtm_list_tags`/`_triggers`/`_variables`, `gtm_get_version`, `ads_list_conversion_actions` (Inventar), `ga4_list_custom_dimensions`/`_metrics` |
| **Nicht prüfbar** | Tool-Grenze, nur beratend | Consent-Mode-v2 *greift korrekt*, sGTM-Gesundheit, Attributionsmodell, Page-Snippet-Installation, echte Doppelzählung |

**Load-bearing Regeln:**
1. **„Feuert" nie aus GTM-Config allein** behaupten — GTM-API liefert kein Browser-Firing-Signal. „Feuert" = Kreuzcheck *Config vorhanden (GTM) + Counts > 0 (GA4/Ads) im selben Zeitraum*. Config ohne Daten → **Verdacht** „feuert nicht / Consent blockt / Trigger greift nicht", keine Gewissheit.
2. **Workspace-Draft ≠ Live-Version.** `gtm_list_tags`/`gtm_get_tag` lesen den **Workspace-Entwurf**; `gtm_container_info`/`gtm_get_version` die **gepublishte Live-Version**. Ein nie gepublishter Tag ist nicht live. Immer beide vergleichen, Quelle benennen — Draft/Live-Drift ist der häufigste reale Tracking-Bug.
3. **`ga4_realtime_users` ist kein Event-Firing-Beweis** (nur aggregierte aktive User). Für Event-Smoketest `ga4_list_key_events`/`ga4_report`.
4. **Zählmethode (jede/eine) & primär/sekundär** ggf. nicht in `ads_list_conversion_actions`-Response — reale Response prüfen, nicht aus dem Schema schließen; sonst „nicht ausgelesen" markieren.

## 5. Phasen (Blocker zuerst)

### Schritt 0 — Vorbereitung (immer zuerst)
- **Projekt-Kontext zuerst** (kanonischer Absatz, letzter Satz aufgabenspezifisch). `compliance`-Flags als harte Leitplanke (für den Consent-Layer zentral).
- `list_workspaces` + sources-Check: `ga4`, `gtm`, `google_ads` verbunden? Phasen nur fahren, wo die Quelle da ist; fehlende Quelle als Lücke benennen.
- Markt-Kalibrierung (DE/AT/CH) — relevant für Data-Retention-Recht & Consent.

### Phase 1 — Lebt das Conversion-Tracking überhaupt? (Gate/Blocker)
- `ads_list_conversion_actions` + `ads_conversion_performance` → `last_gap_days`, letztes Conversion-Datum → **totes Tracking** erkennen.
- `ga4_conversions` / `ga4_list_key_events` → kommen Conversion-Events real an?
- **Kein / totes Conversion-Tracking = Top-Blocker** (alles Nachgelagerte steht still).

### Phase 2 — Key-Event-/Conversion-Konfiguration
- `ga4_list_key_events` → sind die conversion-relevanten Events als Key Event markiert? Zählmethode (`ONCE_PER_EVENT`/`SESSION`) plausibel?
- `ads_list_conversion_actions` → Status/Typ/Kategorie; primär vs. sekundär für Smart Bidding (**nur wenn Response es hergibt**, sonst als „nicht ausgelesen").
- `ga4_list_custom_dimensions`/`_metrics` → relevante Dimensionen/Metriken vorhanden?

### Phase 3 — GA4 ↔ Google-Ads-Konsistenz
- `ga4_manage_google_ads_links` (list) → Link gesetzt? (stärkster „grüner" Check + Operator.)
- Kreuzcheck `ga4_conversions` vs. `ads_conversion_performance` → fehlender Import / **Doppelzählung als Verdacht** (GA4-Import-Conversion *und* nativer Ads-Tag für denselben Abschluss). Auto-Dedup leisten die Tools nicht → manuell kennzeichnen.

### Phase 4 — GTM-Hygiene & Workspace-Drift
- `gtm_container_info` (Live) **vs.** `gtm_list_tags`/`_triggers`/`_variables` (Workspace-Draft) → **Drift** explizit ausweisen.
- `gtm_get_tag` für Schlüssel-Tags → Typ, Parameter, `firing_trigger_ids`, `paused`; verwaiste/pausierte/doppelte Tags.
- Feuert-Kreuzcheck (Config + Counts aus Phase 1/2).

### Phase 5 — Event-Coverage / Soll-Ist-Diff (Herzstück)
- Erwartete Event-/Funnel-Kette aus `references/event-soll-dach.md` (DACH-lokalisierte Corey-Event-Library + Funnel-Sequenzen) als **Soll**. **Geschäftstyp-relevante Sektion wählen** (aus `projekt-kontext`: E-Commerce / Lead-Gen / SaaS / lokaler Dienstleister) — nicht die ganze Library gegen jeden Kunden halten, sonst wird der Diff zu Lärm (ein Klempner braucht kein `video_start`).
- Gemessener Event-Bestand via `ga4_list_key_events` / `ga4_report` (eventCount pro eventName) als **Ist**.
- Diff: **fehlende Funnel-Glieder** („Soll-Funnel 5 Schritte, gemessen 3 — `checkout_started`, `payment_info_entered` fehlen"), **Naming-Hygiene** (Object-Action, lowercase_underscore), Kontext-in-Properties-statt-Eventname.
- Output speist den Tracking-Plan (siehe Output-Format).

### Phase 6 — Datenqualität
- `ga4_enhanced_measurement` (get) → Auto-Events sinnvoll konfiguriert (Scroll/Outbound/Site-Search/Form)?
- `ga4_data_retention` (get) → `TWO_MONTHS` vs. `FOURTEEN_MONTHS`; **DACH oft unnötig kurz** → Hebel.
- Interne IPs / Bot-Filter, Cross-Domain — soweit aus den Tools lesbar; sonst beratend.

### Querschnitt — DACH-Consent-Layer (immer, gemischt prüfbar/beratend)
- **Präsenz prüfbar (konfiguriert):** Consent-/CMP-Tag bzw. tag-level Consent-Settings im GTM via `gtm_list_tags`/`gtm_get_tag` vorhanden/fehlt.
- **Nicht prüfbar (beratend):** ob Consent Mode **v2** korrekt greift (Default-denied → Update-on-grant, `ad_user_data`/`ad_personalization`), Tag-Firing vor Consent. Ausdrücklich als Tool-Grenze (GTM-Preview/Tag-Assistant nötig).
- DACH-Recht: §25 TTDSG / Cookie-Banner-Pflicht, CMP-konkret (Usercentrics/Cookiebot), Server-Side-Tagging als Option. `compliance`-Flags als harte Leitplanke.
- Detail in `references/dach-consent.md`.

### Querschnitt — Tool-Grenzen / Footguns (eigene Sektion, nicht als Befund verkaufen)
Die „Nicht prüfbar"-Liste explizit: Tag-Firing aus Config, Consent-v2-Korrektheit, sGTM-Gesundheit, Attributionsmodell, Page-Snippet, Doppelzählung. Detail in `references/tracking-tool-grenzen.md`.

## 6. Output-Format
1. **Kurz-Fazit:** 2–3 Sätze Gesamtbild + Top-3–5-Blocker + schnellste Quick Wins.
2. **Befunde nach Phase:** Problem · Wirkung (Hoch/Mittel/Niedrig) · **Beleg** (echte Zahl + Beleg-Stufe) · Fix · Priorität (1–5).
3. **4-Stufen-Maßnahmenplan:** Kritisch (Tracking tot/blockiert) · High-Impact · Quick Wins · Langfristig.
4. **Tracking-Plan (optional, aus Phase 5):** Soll-Tabelle (Event · Beschreibung · Properties · Trigger; Key Events mit Zählmethode; Custom Dimensions) — Coreys Template, als Soll-Dokumentation für den Kunden.

## 7. Operator (Schreib-Aktionen — Dry-Run + Bestätigung)

**Dry-Run-Lage (kritisch, weil uneinheitlich):**
- **`validate_only` vorhanden:** `ads_create_conversion_action`, `ads_update_conversion_action`, `ads_upload_conversions`, `ga4_manage_audiences`.
- **KEIN Dry-Run:** alle GA4-Writes (`ga4_create_key_event`/`_delete_key_event`/`_create_custom_dimension`/`_metric`/Property, `ga4_enhanced_measurement`/`_data_retention` set) und **alle GTM-Writes** → der Skill muss den Dry-Run **selbst simulieren** (zeigen, was sich ändert), besonders bei `ga4_delete_key_event`.

**Sichere Einzelaktionen:** Key Event markieren (`ga4_create_key_event`), Data Retention / Enhanced Measurement setzen, GA4↔Ads-Link (`ga4_manage_google_ads_links` create), Conversion-Action anlegen/ändern (`ads_*` mit `validate_only` zuerst).

**GTM-Flow (4-stufig, einziger live-wirksamer Schritt ist publish):**
`gtm_list_workspaces` → `gtm_create_trigger` → `gtm_create_tag` (Trigger-ID in `firing_trigger_ids`) → `gtm_create_version` (Snapshot, **nicht live**) → **Bestätigung** → `gtm_publish_version` (**LIVE**). Als benannte Version mit Change-Notes (Corey-Muster).

**Tabu ohne ausführliche Rücksprache:** `gtm_publish_version` ungefragt, `ga4_delete_key_event`, `ga4_update_property` (Stammdaten), `ga4_create_property`/`_data_stream` (= Setup, out of scope).

## 8. References
- `references/event-soll-dach.md` — **vollständige** Corey-Event-Library (alle Geschäftstypen: Marketing-Site, E-Commerce, SaaS/Product, Monetization) + Funnel-Sequenzen, DACH-lokalisiert (EUR, dt. Kontext), **plus gezielte Erweiterung** um DACH-Lead-Gen / lokale Dienstleister (Anfrageformular, `tel:`-/Anruf-Klick, Terminbuchung, WhatsApp-Klick, Routenplaner) — der von Coreys US-SaaS-Liste unterrepräsentierte Bereich. **Nach Geschäftstyp gegliedert**, damit Phase 5 nur die relevante Sektion zieht (on-demand, bläht SKILL.md nicht auf). Das Soll für Phase 5.
- `references/dach-consent.md` — Consent Mode v2, §25 TTDSG, Cookie-Banner-Pflicht, CMP-Liste, Server-Side-Tagging; was prüfbar vs. nicht.
- `references/tracking-tool-grenzen.md` — Beleg-Stufen-Mapping + Footgun-Tabelle (was die MCP-Tools können/nicht können).

## 9. Evals (`evals/evals.json`)
- `trigger-basic-tracking-check` — Standard-Trigger → Schritt 0, sources-Check, Beleg-Stufen, Blocker zuerst.
- `defer-to-google-ads-audit` — reine Paid-Performance-Frage → google-ads-audit.
- `defer-to-wochenreport` — „wie entwickeln sich die Zahlen" → wochenreport (sobald gebaut; sonst seo/ads).
- `tool-reality-config-vs-firing` — behauptet nicht „Tag feuert" aus GTM-Config; verlangt Counts-Kreuzcheck.
- `tool-reality-workspace-drift` — vergleicht Live-Version vs. Workspace-Draft, benennt die Quelle.
- `tool-reality-consent-v2-not-verifiable` — prüft Consent-Tag-Präsenz, deklariert Consent-v2-Korrektheit als nicht prüfbar.
- `tool-reality-realtime-not-firing-proof` — nutzt nicht `ga4_realtime_users` als Firing-Beweis.
- `ga4-ads-consistency` — Kreuzcheck GA4 vs. Ads-Conversions, Doppelzählung nur als Verdacht.
- `event-coverage-funnel-gap` — Soll-Ist-Diff der Funnel-Kette, benennt fehlende Glieder.
- `operator-confirmation-gtm-publish` — Bestätigung VOR `gtm_publish_version`, Change-Notes.
- `dach-data-retention` — erkennt `TWO_MONTHS` als unnötig kurz, empfiehlt 14 Monate.

## 10. Offene Punkte (vor Implementierung klären/entscheiden)
- `description`-Länge ≤1024 Zeichen mit deutschen Quotes-Footgun beachten (Ziel ~950).
- Version: neuer Skill → Plugin-Version-Bump in **allen drei Feldern** (`plugin.json`, marketplace-Eintrag, `metadata.version`).
- Reihenfolge der Phasen 2–4 final justieren beim Schreiben (Konfiguration vs. Konsistenz vs. GTM-Hygiene — alle „nach dem Gate").
- **Entschieden (2026-06-30):** `event-soll-dach.md` = volle Corey-Library (alle Geschäftstypen) + DACH-Lead-Gen/lokale-Dienstleister-Erweiterung, nach Geschäftstyp gegliedert; Phase-5-Diff zieht nur die geschäftstyp-relevante Sektion.

## Anhang — Tool-Inventar (aus Tool-Reality-Research)
**GA4:** `ga4_conversions`, `ga4_list_key_events`, `ga4_report`, `ga4_list_custom_dimensions`/`_metrics`, `ga4_list_data_streams`, `ga4_list_properties`, `ga4_realtime_users`, `ga4_enhanced_measurement` (R/W), `ga4_data_retention` (R/W), `ga4_manage_google_ads_links` (R/W), `ga4_manage_audiences` (R/W, `validate_only`), `ga4_create_key_event`/`_delete_key_event`, `ga4_create_custom_dimension`/`_metric` (+`archive_*`), `ga4_create_data_stream`, `ga4_create_property`/`_update_property`.
**GTM:** `gtm_container_info` (Live), `gtm_list_workspaces`, `gtm_list_tags`/`_triggers`/`_variables`/`_versions`, `gtm_get_tag`/`_version`, `gtm_create_tag`/`_update_tag`/`_remove_tag`, `gtm_create_trigger`, `gtm_create_version`, `gtm_publish_version`.
**Ads-Conversions:** `ads_list_conversion_actions`, `ads_conversion_performance`, `ads_create_conversion_action`/`_update_conversion_action`/`ads_upload_conversions` (alle `validate_only`).
