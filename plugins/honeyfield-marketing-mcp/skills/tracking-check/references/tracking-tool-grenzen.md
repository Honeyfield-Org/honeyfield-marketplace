# Tool-Grenzen & Beleg-Stufen

Referenz für `tracking-check`. Auf diese Datei verweist SKILL.md — Begriffe (gemessen / nur konfiguriert / nicht prüfbar) dort verbatim übernommen.

---

## A — Beleg-Stufen-Mapping

| Stufe | Bedeutung | Quelle (Tools) |
|---|---|---|
| **Gemessen** | Daten fließen real | `ga4_list_key_events` (Per-Event-Counts), `ga4_conversions`, `ga4_report` (auch PII-Muster in `pageLocation`, Self-Referrals in `sessionSource`, Test-Hosts in `hostName` — s. §D), `ads_list_conversion_actions` (letztes Conversion-Datum), `ads_conversion_performance` (`last_gap_days`) |
| **Nur konfiguriert** | verdrahtet bzw. gesetzt, Datenfluss **unbewiesen** | `gtm_get_tag`, `gtm_list_tags`/`_triggers`/`_variables`, `gtm_get_version`, `ads_list_conversion_actions` (Inventar), `ga4_list_custom_dimensions`/`_metrics`, `ga4_manage_google_ads_links` (list — Link gesetzt ≠ Import fließt), `ga4_enhanced_measurement`/`ga4_data_retention` (get — Setting ≠ ankommende Daten) |
| **Nicht prüfbar** | Tool-Grenze, nur beratend | Consent-Mode-v2 *greift korrekt*, Umfang der Consent-Modellierung, sGTM-Gesundheit, Attributionsmodell/Attributions-Kanal-Einstellung, Google Signals, echte Doppelzählung, Data Redaction, Datenfilter (intern/Developer), Cross-Domain-Domains und Unwanted-Referral-Liste, User-Daten-Retention, Property-Größe (Standard/Large/XL) und 360-Status |

Jeder Befund im Audit trägt eine dieser drei Stufen. Config-ohne-Daten = **Verdacht**, nicht Befund. Page-Snippet-Installation ist **nicht** mehr pauschal „nicht prüfbar” — sie ist **prüfbar mit Einschränkung** über `dfs_domain_technologies` / `dfs_raw_html` (Präsenz-Nachweis, kein seitenweiter Feuer-Beweis), s. Footgun #8 unten.

---

## B — Footgun-Liste

Situationen, in denen ein naiver Audit falsche Gewissheit erzeugt. Begriffe sind bindend für SKILL.md.

| # | Was ein naiver Skill behaupten würde | Was die Tools wirklich hergeben | Ehrliche Formulierung |
|---|---|---|---|
| 1 | „Tag X feuert” | GTM-API liefert nur Config, kein Browser-Firing-Signal | Getrennt: „konfiguriert + an Trigger verdrahtet” vs. „Daten kommen an (Counts > 0)”; Config ohne Daten = **Verdacht** (feuert nicht / Consent blockt / Trigger greift nicht), keine Gewissheit |
| 2 | „Consent Mode v2 korrekt konfiguriert” | Nicht verifizierbar über MCP-Tools | Höchstens Consent-Tag-Präsenz prüfbar; Korrektheit (Default-denied → Update-on-grant, `ad_user_data`/`ad_personalization`) als **nicht prüfbar** ausweisen — GTM-Preview/Tag-Assistant nötig |
| 3 | „kein sGTM” / „sGTM aktiv” | Nur aus `transport_url`-Parameter im GA4-Config-Tag ableitbar | „sGTM-Endpoint im GA4-Config-Tag hinterlegt: ja/nein”; Live-Gesundheit des sGTM-Servers nicht bestätigbar |
| 4 | „Attributionsmodell ist X” | Nirgends über die verfügbaren Tools lesbar | Weglassen oder explizit als Tool-Grenze benennen |
| 5 | Zählmethode (jede/eine) & primär/sekundär aus `ads_list_conversion_actions` | Schema verspricht es, Response nicht garantiert | Erst Response prüfen; wenn nicht vorhanden: „nicht ausgelesen” markieren, nicht aus dem Schema schließen |
| 6 | `ga4_realtime_users` als Firing-Beweis nutzen | Liefert nur aggregierte aktive User, kein Event-Detail | Für Event-Smoketest `ga4_list_key_events`/`ga4_report` nutzen |
| 7 | „Tag ist live” aus `gtm_list_tags` | `gtm_list_tags`/`gtm_get_tag` lesen den **Workspace-Entwurf (Draft)**, nicht die gepublishte Version | Immer `gtm_container_info`/`gtm_get_version` (Live) vs. Workspace-Draft vergleichen, Quelle explizit benennen — Workspace-Draft ≠ Live ist der häufigste reale Tracking-Bug |
| 8 | „GA4-Snippet auf jeder Seite installiert” | Kein MCP-Tool liest Seiten-HTML direkt, aber `dfs_domain_technologies` erkennt GA4/GTM/Pixel im Domain-Tech-Stack (domain-level, ggf. lagged) und `dfs_raw_html` liefert das rohe HTML einer konkreten URL | **Prüfbar mit Einschränkung:** `dfs_domain_technologies` bestätigt Präsenz im Stack, `dfs_raw_html` bestätigt das Snippet auf einer konkreten Seite — keins beweist, dass der Tag auf **jeder** Seite/bei jedem Request feuert; für den seitenweiten Nachweis ggf. On-Page-Crawl in `seo-audit` |
| 9 | Enhanced Measurement = vollständiges Tracking | Deckt nur GA4-Auto-Events (Scroll, Outbound, etc.) | Nicht als „Tracking vollständig” verkaufen; Custom-Events und Funnel-Glieder separat prüfen |
| 10 | „Doppelzählung erkannt” | Tools enumerieren Conversion-Actions, erkennen keine Semantik | Nur als **Verdacht** benennen: „potenzielle Dublette (GA4-Import-Conversion + nativer Ads-Tag für denselben Abschluss) — manuell zu bestätigen” |

---

## C — Operator-Dry-Run-Lage

Uneinheitlich — explizit ausweisen, bevor eine Schreib-Aktion angeboten wird.

**`validate_only` vorhanden (Ads + Audiences):**
- `ads_create_conversion_action`, `ads_update_conversion_action`, `ads_upload_conversions`
- `ga4_manage_audiences`

**Kein Dry-Run (Skill simuliert selbst):**
- Alle GA4-Writes: `ga4_create_key_event`, `ga4_delete_key_event`, `ga4_create_custom_dimension`, `ga4_create_custom_metric`, `ga4_enhanced_measurement` (set), `ga4_data_retention` (set), `ga4_update_property`
- Alle GTM-Writes: `gtm_create_tag`, `gtm_create_trigger`, `gtm_create_version`, `gtm_publish_version`, `gtm_update_tag`, `gtm_remove_tag`

Bei „kein Dry-Run”: Skill zeigt vorher, was sich ändert (Simulation), wartet auf Bestätigung — besonders kritisch bei `ga4_delete_key_event`.

**GTM-Flow (6-stufig, einziger live-wirksamer Schritt ist publish):**

1. `gtm_list_workspaces` — Workspace-ID ermitteln
2. `gtm_create_trigger` — Trigger anlegen
3. `gtm_create_tag` — Tag anlegen, `firing_trigger_ids` setzen
4. `gtm_create_version` — Snapshot erstellen (**nicht live**)
5. **Bestätigung einholen**
6. `gtm_publish_version` — **LIVE**, nicht rückgängig zu machen ohne neuen Publish

Als benannte Version mit Change-Notes. `gtm_publish_version` niemals ohne explizite Bestätigung.

---

## D — Datenqualität (Phase 6): Abfragen, Stufe, Beleg

Alle Abfragen über `ga4_report` (Parameter: `metrics`, `dimensions`, `days` oder `start_date`/`end_date`, `limit` max. 500, `dimension_filter` als `{"field","value","match_type"}` mit `EXACT`/`CONTAINS`/`BEGINS_WITH`/`ENDS_WITH`/`FULL_REGEXP`). Treffer sind **gemessen**. Zeilen sind durch `limit` und Thresholding gekappt — Treffer belegen ein Problem, „keine Treffer” beweist keine Sauberkeit.

| Check | Abfrage | Befund | Nicht prüfbar (beratend) | Beleg |
|---|---|---|---|---|
| **PII in URLs** | `metrics=["screenPageViews"]`, `dimensions=["pageLocation"]`, `dimension_filter` = PII-Regex (Code-Block unter der Tabelle) | E-Mail, Telefon oder Name in Pfad, Query- oder UTM-Parameter = Verstoß gegen die Google-Richtlinie (Pfad und Parameter müssen PII-frei sein) + DSGVO-Thema. Treffer manuell sichten (`name=` kann harmlos sein). `pageLocation` statt `pagePath` — `pagePath` enthält keine Query-Parameter. | Data Redaction (gibt es nur für Web-Streams) ist über die Tools nicht lesbar | https://support.google.com/analytics/answer/6366371 |
| **Self-Referral / Cross-Domain** | `metrics=["sessions","keyEvents"]`, `dimensions=["sessionSource"]` | Eigene Domain, Checkout-Domain oder Payment-Anbieter (z. B. `paypal.com`) als Quelle = Verdacht auf fehlendes Cross-Domain-Measurement bzw. fehlende Unwanted-Referral-Regel. Key Events landen dann bei der falschen Quelle. | Cross-Domain-Domains, `_gl`-Linker, Unwanted-Referral-Liste (max. 50 Regeln pro Stream) | https://support.google.com/analytics/answer/10327750 |
| **Test-/Dev-Traffic** | `metrics=["sessions"]`, `dimensions=["hostName"]` | `localhost`, Staging-/Dev-Domains oder fremde Hosts in der Prod-Property = Test-Traffic in den Zahlen | Datenfilter für interne und Developer-Zugriffe; DebugView-Traffic muss laut Google gefiltert werden | https://support.google.com/analytics/answer/7201382 |
| **Data Retention** | `ga4_data_retention` (`action="get"`, `property_id`) → `event_data_retention`, `reset_user_data_on_new_activity` | Standard-Property: `TWO_MONTHS` vs. `FOURTEEN_MONTHS`. Large-/XL-Properties sind laut Google auf 2 Monate begrenzt — dort kein Quick Win. GA4 360: auch `TWENTY_SIX_`/`THIRTY_EIGHT_`/`FIFTY_MONTHS`. Eine **Erhöhung** wirkt auch auf schon erhobene, noch gespeicherte Daten; schon gelöschte Daten kommen nicht zurück. | User-Daten-Retention (eigene Optionsliste), Property-Größe, 360-Status | https://support.google.com/analytics/answer/7667196 |

PII-Filter für `ga4_report` (`FULL_REGEXP` muss die ganze URL treffen, daher `.*` an beiden Enden):

```json
{"field": "pageLocation", "value": ".*(@|%40|email=|e-mail=|tel=|phone=|name=).*", "match_type": "FULL_REGEXP"}
```

**GA4 ↔ Google Ads — beratende Abweichungsgründe (Phase 3, alle nicht prüfbar):**
- Attributions-Kanal-Einstellung in GA4: Seit 06/2023 ist bei neuer Verknüpfung „Google Paid Channels” der Default.
- Cross-Device-Conversions zählt GA4 nur mit aktivem Google Signals.
- Berichtszeit: Google Ads bucht auf die Interaktionszeit (Klick), GA4 auf die Event-Zeit.
- Zeitzone.

Diese Gründe erklären kleine Abweichungen. Eine Faktor-2+-Diskrepanz bleibt Tracking-Verdacht. Beleg: https://support.google.com/analytics/answer/10632359
