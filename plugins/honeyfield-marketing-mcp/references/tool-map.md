# Tool-Map — Honeyfield Marketing-Ops MCP

Alle Tools außer `list_workspaces`, `ping`, `authenticate` und `complete_authentication` nehmen `workspace` (optional, wenn nur ein Workspace verbunden ist; bei gleichem Slug in mehreren Agenturen die Form `Agentur/slug` nutzen). Quelle = welche Workspace-source verbunden sein muss.
Lege Schreib-Tools (W) nie ohne write-guardrails.md an.

---

## Foundation

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `list_workspaces` | Workspaces + verbundene sources auflisten | — | R |
| `ping` | Connectivity-Check (liefert „pong”) | — | R |
| `workspace_configure_source` | Source-IDs am Workspace setzen (`source`: google_ads/ga4/search_console/gtm/business_profile + `ids`) — ersetzt den Portal-Roundtrip beim Onboarding | — | W |
| `journal_add_note` | Notiz ins Änderungsjournal des Workspace (`note` mit Vorher→Nachher + Warum, optional `source`) — nach JEDER Schreib-Aktion aufrufen; Ersatz für die Google-Ads-Notizen, die Googles API nicht anbietet | — | W |
| `journal_list` | Änderungsjournal lesen (`days`, `limit`, `kind`: note/auto) — automatische Protokolle aller Schreib-Tools + Notizen; für Wochenreports und um Performance-Knicke Änderungen zuzuordnen | — | R |
| `authenticate` | OAuth-Flow zum MCP starten — nur Plugin-Kontext (Claude Code); in Claude Web ist der Connector vorauthentifiziert | — | — |
| `complete_authentication` | OAuth-Flow abschließen — nur Plugin-Kontext (Claude Code) | — | — |

---

## Diagnostik (source: google_ads — `anomaly_check` zusätzlich ga4 / search_console, Clarity opt-in)

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `budget_pacing` | Budget-Pacing laufender Monat: Ausgaben vs. Projektion pro Kampagne — **nur Google Ads**. Meta: Budgets via `meta_list_campaigns`/`meta_list_adsets`, Ausgaben via `meta_campaign_performance(daily=True)` (Tagesverlauf) oder `totals_only=True` (Kontosumme) | google_ads | R |
| `anomaly_check` | Anomalie-Check der letzten `days` Tage (Default 14, Mindestlänge 6) über **alle verbundenen Quellen** des Workspace — Google Ads, GA4, Search Console und (nur mit `include_clarity=True`) Clarity; läuft auch ohne Google-Ads-Konto. Checks je Quelle — **Google Ads** (Fenster bis gestern, heute nicht enthalten): `conversions_zero` (≥3 Tage Kosten ohne Conversion, critical; Conversions = primäre Aktionen), `cost_spike` (gestern >2,5× Ø der Vortage), `cost_drop_to_zero`, `clicks_no_conversions` (≥50 Klicks, 0 Conversions), `ctr_drop` (CTR letzte 3 Tage <50 % der Vorperiode), `ads_no_data` (info). **GA4** (sessions + keyEvents je Datentag; GA4 verarbeitet bis zu 24–48 h nach — fehlt nur gestern: warn, morgen erneut prüfen; critical ab 2 Tagen Lücke): `sessions_drop_to_zero`, `sessions_drop` (erst ab Ø 5 Sitzungen/Tag), `key_events_zero`, `key_events_none` (info), `sessions_spike` (info), `ga4_no_data`. **Search Console** (Daten kommen 2–3 Tage verzögert, Fenster `days`+3; fehlende letzte Tage sind NICHT 0 und werden nicht bewertet): `sc_clicks_drop` / `sc_impressions_drop` (Impressionen = Indexierungs-/Sichtbarkeitsproblem), `sc_no_recent_data` (letzter Datentag >5 Tage her). **Clarity** (letzte 72 h, unabhängig von `days`; verbraucht 1 der 10 Aufrufe je Projekt und Tag): info `js_errors_high` / `dead_clicks_high` / `rage_clicks_high` (Heuristik-Schwellen), warn `clarity_no_data` (Snippet prüfen) / `clarity_metrics_unreadable`. Rückgabe wie bisher `findings` / `ok` / `daily` (Google-Ads-Tagesreihe, `[]` ohne Google Ads) — neu: `source` je Finding (google_ads/ga4/search_console/clarity) und `sources{<quelle>: {status checked/not_connected/not_permitted/skipped/error, days_with_data, last_data_date, …}}`. `ok` = kein warn-/critical-Finding UND mindestens eine Quelle `checked`. Keine Quelle verbunden → `{error: no_sources, hint}`; Zugänge mit eingeschränkten Datenquellen bekommen nur freigeschaltete Quellen (übrige `not_permitted`); fällt eine Quelle aus, laufen die anderen weiter (`status=error` + Finding `sources_unavailable`, warn) — nie ein Fehler-Dict fürs ganze Tool, solange eine Quelle verbunden ist. Bewertet nur — Gesamtzahlen via `ads_campaign_performance`, `ga4_report`, `sc_performance(dimensions=[])` | google_ads / ga4 / search_console (mind. eine; clarity opt-in via `include_clarity`) | R |

---

## Google Ads — Reporting (source: google_ads)

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `ads_campaign_performance` | Kampagnen-KPIs (Impressions, Clicks, Cost, CTR, CPC, Conversions) | google_ads | R |
| `ads_impression_share` | Impression Share + Budget-/Rank-Verluste pro Kampagne | google_ads | R |
| `ads_search_terms` | Search-Terms-Report — was User wirklich gesucht haben | google_ads | R |
| `ads_ai_max_search_terms` | AI-Max-Quelle-Split pro Suchbegriff × Headline × Landing-Page | google_ads | R |
| `ads_budget_status` | Tagesbudget, Ausgaben und Budget-Auslastung pro Kampagne | google_ads | R |
| `ads_keyword_performance` | Keyword-Performance inkl. Quality Score, CPC, Conversions | google_ads | R |
| `ads_ad_performance` | Anzeigen-Performance — welche Ads performen, welche nicht | google_ads | R |
| `ads_geo_performance` | Performance nach Standort (Land): Impressions, Clicks, Cost | google_ads | R |
| `ads_device_performance` | Performance nach Gerätetyp (Mobile, Desktop, Tablet) | google_ads | R |
| `ads_schedule_performance` | Performance nach Wochentag und Stunde | google_ads | R |
| `ads_change_history` | Änderungshistorie: wer hat wann was geändert (max. 29 Tage) | google_ads | R |
| `ads_list_conversion_actions` | Conversion-Aktionen mit Status, Typ, Counts (`conversions_{N}d`) — deckt totes Tracking auf. Zählt nach **Conversion-Datum**: Offline-Importe zählen am Tag der Conversion, nicht am Klick-Tag — nicht 1:1 mit den klick-datierten Kampagnen-Tools vergleichbar | google_ads | R |
| `ads_conversion_performance` | Conversion-Performance pro Aktion + Tagesverlauf; alle Datumsangaben (`first/last_date`, `daily_total`, `last_gap_days`) beziehen sich auf das **Conversion-Datum** — Offline-Importe zählen am Tag der Conversion, nicht am Klick-Tag (ein heute verbuchter Import senkt `last_gap_days`); Fenster bis gestern | google_ads | R |
| `ads_list_campaigns` | Alle Kampagnen (Name, Status, Budget, Channel Type, Bidding Strategy) | google_ads | R |
| `ads_list_ad_groups` | Ad Groups auflisten, optional nach Kampagne gefiltert | google_ads | R |
| `ads_list_keywords` | Keywords auflisten, optional nach Kampagne oder Ad Group gefiltert; `limit` (Default 200, max. 1000) — wird abgeschnitten, kommt `{result, warning}` statt der Liste (dann `campaign_id`/`ad_group_id` einschränken oder `limit` erhöhen); enthält auch Ad-Group-Negatives, gekennzeichnet über `negative=true` | google_ads | R |
| `ads_list_negative_keywords` | Negative Keywords auflisten, optional nach Kampagne gefiltert | google_ads | R |
| `ads_list_ads` | Alle Anzeigen (Headlines, Descriptions, URLs, Status, Approval) | google_ads | R |
| `ads_list_assets` | Assets auflisten (Sitelinks, Callouts, Structured Snippets) | google_ads | R |
| `ads_get_geo_targeting` | Geo-Targeting pro Kampagne + Einstellung (Presence vs. POI) | google_ads | R |
| `ads_list_recommendations` | Offene Google-Ads-Empfehlungen des Kontos | google_ads | R |
| `ads_keyword_quality` | Quality-Score-Komponenten je Keyword (Expected CTR, Ad Relevance, LPE) | google_ads | R |
| `ads_list_audiences` | Verfügbare Zielgruppenlisten und Verknüpfungen (Kampagne/Ad Group) | google_ads | R |
| `ads_demographic_performance` | Performance nach Alter und Geschlecht | google_ads | R |
| `ads_list_experiments` | Kampagnen-Experimente (A/B-Tests) mit Status und Laufzeit | google_ads | R |
| `ads_list_customer_match_lists` | CRM-basierte Customer-Match-Userlisten auflisten | google_ads | R |

---

## Google Ads — Mutation (source: google_ads) ⚠ Guardrails

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `ads_upload_conversions` | Offline-/Enhanced-Conversions via Data Manager API hochladen | google_ads | W |
| `ads_create_conversion_action` | Neue Conversion-Aktion anlegen | google_ads | W |
| `ads_update_conversion_action` | Bestehende Conversion-Aktion ändern (Name, Status, `default_value`, `primary_for_goal`) — auch `primary_for_goal=False` (Herabstufung auf sekundär) und `default_value=0` werden übernommen; Name/Status danach mit `ads_list_conversion_actions` zurücklesen. `primary_for_goal` und `default_value` zeigt kein Lese-Tool — die Antwort enthält `primary_for_goal` nur als Echo des gesendeten Werts und `default_value` gar nicht; beide sind ausschließlich in der Google-Ads-Oberfläche prüfbar | google_ads | W |
| `ads_create_campaign` | Neue Kampagne anlegen (Standard: PAUSED) — `channel_type` SEARCH/DISPLAY/VIDEO/PERFORMANCE_MAX; SHOPPING wird vor dem API-Aufruf mit `{error: unsupported_channel, hint}` abgelehnt; der Parameter `url_expansion_opt_out` existiert nicht mehr (PMax-Final-URL-Expansion bleibt auf Googles Standard, nur in der Google-Ads-Oberfläche abschaltbar) | google_ads | W |
| `ads_update_campaign_status` | Kampagne aktivieren oder pausieren | google_ads | W |
| `ads_update_campaign_name` | Kampagnen-Name ändern | google_ads | W |
| `ads_update_campaign_budget` | Tagesbudget einer Kampagne ändern | google_ads | W |
| `ads_update_campaign_bidding_strategy` | Bidding Strategy einer Kampagne ändern | google_ads | W |
| `ads_update_campaign_network` | Such-Partner-/Display-Netzwerk einer Kampagne an-/ausschalten | google_ads | W |
| `ads_remove_campaign` | Kampagne entfernen (Soft Delete — nicht rückgängig machbar) | google_ads | W |
| `ads_create_ad_group` | Neue Ad Group in einer Kampagne anlegen | google_ads | W |
| `ads_remove_ad_group` | Ad Group entfernen (nicht rückgängig machbar) | google_ads | W |
| `ads_update_ad_group_status` | Ad Group aktivieren oder pausieren | google_ads | W |
| `ads_update_ad_group_bid` | CPC-Gebot einer Ad Group ändern | google_ads | W |
| `ads_update_ad_group_name` | Ad Group Name ändern | google_ads | W |
| `ads_add_keyword` | Keyword zu einer Ad Group hinzufügen | google_ads | W |
| `ads_bulk_add_keywords` | Mehrere Keywords in einer Ad Group anlegen (ein API-Call) | google_ads | W |
| `ads_move_keyword` | Keyword von einer Ad Group in eine andere verschieben | google_ads | W |
| `ads_add_negative_keyword` | Negatives Keyword zu einer Kampagne hinzufügen | google_ads | W |
| `ads_bulk_add_negative_keywords` | Mehrere negative Keywords in einer Kampagne anlegen (ein API-Call) | google_ads | W |
| `ads_remove_negative_keyword` | Negatives Keyword von einer Kampagne entfernen | google_ads | W |
| `ads_manage_shared_negative_list` | Geteilte Negativ-Keyword-Listen auflisten, erstellen, befüllen, an Kampagnen anhängen (`validate_only` = Dry-Run) | google_ads | R/W |
| `ads_update_keyword_status` | Keyword aktivieren oder pausieren | google_ads | W |
| `ads_update_keyword_bid` | CPC-Gebot eines Keywords ändern | google_ads | W |
| `ads_remove_keyword` | Keyword entfernen (nicht rückgängig machbar) | google_ads | W |
| `ads_create_ad` | Responsive Search Ad anlegen (**Standard: ENABLED** — für sichere Anlage explizit `status="PAUSED"` setzen) | google_ads | W |
| `ads_replace_ad` | Anzeige ersetzen (Google erlaubt kein direktes In-Place-Editieren) | google_ads | W |
| `ads_update_ad` | DEPRECATED — identisch mit ads_replace_ad, wird künftig entfernt | google_ads | W |
| `ads_update_ad_status` | Anzeige aktivieren oder pausieren | google_ads | W |
| `ads_remove_ad` | Anzeige entfernen (nicht rückgängig machbar) | google_ads | W |
| `ads_create_sitelink` | Neues Sitelink-Asset anlegen und verknüpfen | google_ads | W |
| `ads_update_sitelink` | Sitelink ändern (URL direkt; Text per Ersatz-Asset) | google_ads | W |
| `ads_update_geo_targeting` | Geo-Targeting einer Kampagne ändern (Standorte, Presence vs. POI) | google_ads | W |
| `ads_set_ad_schedule` | Werbezeitplan einer Kampagne setzen | google_ads | W |
| `ads_set_device_bid_modifier` | Geräte-Gebotsanpassung setzen (MOBILE / DESKTOP / TABLET) | google_ads | W |
| `ads_apply_recommendation` | Google-Ads-Empfehlung anwenden | google_ads | W |
| `ads_dismiss_recommendation` | Google-Ads-Empfehlung verwerfen | google_ads | W |
| `ads_add_audience_signal` | Zielgruppenliste an Kampagne oder Ad Group anhängen | google_ads | W |
| `ads_create_customer_match_list` | CRM-basierte Customer-Match-Userliste anlegen | google_ads | W |
| `ads_upload_customer_match_members` | Mitglieder in Customer-Match-Userliste hochladen (gehasht) | google_ads | W |
| `ads_remove_customer_match_members` | Mitglieder aus Customer-Match-Userliste entfernen (gehasht) | google_ads | W |

---

## Microsoft Clarity (source: clarity)

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `clarity_get_insights` | Sessions, Scroll Depth, Rage Clicks nach Dimension (max 10 Calls/Tag) | clarity | R |

---

## GA4 — Reporting (source: ga4)

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `ga4_report` | GA4 Custom Report (frei wählbare Metrics + Dimensions) | ga4 | R |
| `ga4_realtime_users` | Aktive User in den letzten 30 Minuten | ga4 | R |
| `ga4_top_pages` | Meistbesuchte Seiten (pageviews, sessions, engagementRate) | ga4 | R |
| `ga4_traffic_sources` | Traffic-Quellen (sessions, newUsers, engagedSessions) | ga4 | R |
| `ga4_conversions` | Conversion Events mit Count und Value | ga4 | R |
| `ga4_list_key_events` | Konfigurierte Key Events + Counts — feuern sie wirklich? Je Zeile `key_event_id` (numerisch) und `name` (`properties/<pid>/keyEvents/<id>`) — beides für `ga4_delete_key_event` geeignet | ga4 | R |
| `ga4_list_properties` | Alle GA4 Properties der verbundenen Google-Verbindung | ga4 | R |
| `ga4_list_data_streams` | Datenströme (Web/App) einer Property auflisten inkl. Measurement-ID | ga4 | R |
| `ga4_list_custom_dimensions` | Custom Dimensions einer Property auflisten | ga4 | R |
| `ga4_list_custom_metrics` | Custom Metrics einer Property auflisten | ga4 | R |

---

## GA4 — Mutation (source: ga4) ⚠ Guardrails

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `ga4_create_property` | Neue GA4 Property in einem Analytics-Account anlegen — `account_id` ohne Präfix (Feld `account_id` aus `ga4_list_properties`; `accounts/<id>` wird akzeptiert, Präfix entfernt); danach `workspace_configure_source(source='ga4', ids={'property_id': <neue ID>})`, sonst lehnen die `ga4_*`-Tools die neue Property als workspace-fremd ab | ga4 | W |
| `ga4_create_data_stream` | Web-Datenstream für eine Property anlegen (liefert Measurement-ID) | ga4 | W |
| `ga4_update_property` | Property-Stammdaten ändern (Name, Zeitzone, Währung) | ga4 | W |
| `ga4_create_key_event` | GA4 Key Event (Conversion) anlegen | ga4 | W |
| `ga4_create_custom_dimension` | GA4 Custom Dimension anlegen (EVENT / USER / ITEM) | ga4 | W |
| `ga4_archive_custom_dimension` | GA4 Custom Dimension archivieren | ga4 | W |
| `ga4_create_custom_metric` | GA4 Custom Metric anlegen — `restricted_metric_types` (COST_DATA und/oder REVENUE_DATA) bei `measurement_unit=CURRENCY` Pflicht, sonst `{error: restricted_metric_types_required}` ohne API-Aufruf | ga4 | W |
| `ga4_archive_custom_metric` | GA4 Custom Metric archivieren | ga4 | W |
| `ga4_delete_key_event` | GA4 Key Event löschen — `key_event_name` akzeptiert die numerische ID, den vollen Pfad `properties/<pid>/keyEvents/<id>` oder den Event-Namen (z.B. `purchase`, wird zur ID aufgelöst; unbekannt → `{error: not_found}` mit vorhandenen Key Events, mehrdeutig → `{error: ambiguous, candidates}`) | ga4 | W |
| `ga4_enhanced_measurement` | Enhanced Measurement lesen/setzen (Scroll, Outbound, Site-Search, Video, Downloads) | ga4 | R/W |
| `ga4_data_retention` | Event-Daten-Aufbewahrung lesen/setzen (2 vs. 14 Monate) | ga4 | R/W |
| `ga4_manage_google_ads_links` | GA4↔Google-Ads-Verknüpfung auflisten/anlegen | ga4 | R/W |
| `ga4_manage_audiences` | Remarketing-Audiences auflisten/anlegen (`validate_only` = Dry-Run) | ga4 | R/W |

---

## Search Console (source: search_console) — enthält W ⚠ Guardrails

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `sc_top_queries` | Top organische Suchanfragen (clicks, impressions, ctr, position) | search_console | R |
| `sc_top_pages` | Top Landing Pages aus der Google-Suche | search_console | R |
| `sc_performance` | Flexibler Search Analytics Report (query, page, country, device, date) | search_console | R |
| `sc_url_inspection` | Indexierungsstatus, Canonicals und Crawl-Signale einer URL: `verdict`, `coverage_state`, `indexing_state`, `google_canonical`/`user_canonical`, `last_crawl`, `robots_txt_state` (ALLOWED/DISALLOWED), `page_fetch_state` (SUCCESSFUL, SOFT_404, BLOCKED_ROBOTS_TXT, NOT_FOUND, …); `mobile_verdict`/`mobile_issues` nur, wenn Google den eingestellten Mobile-Usability-Teil noch mitliefert — fehlen sie, wurde nichts geprüft | search_console | R |
| `sc_list_sitemaps` | Eingereichte Sitemaps: Status, Warn- und Fehlerzahlen | search_console | R |
| `sc_submit_sitemap` | Sitemap-URL bei GSC einreichen | search_console | W |
| `sc_delete_sitemap` | Sitemap-URL aus GSC entfernen | search_console | W |
| `sc_list_sites` | Alle GSC-Properties der Google-Verbindung inkl. Verifizierungsstatus — geht auch ohne konfigurierte Site-URL | search_console | R |
| `sc_add_site` | GSC-Property anlegen (`https://…` URL-Prefix oder `sc-domain:…`) — liefert erst nach Verifizierung Daten | search_console | W |
| `sc_verification_token` | Site-Verification-Token holen (Domain: DNS_TXT/DNS_CNAME, URL: META/FILE; ANALYTICS/TAG_MANAGER brauchen keins) | search_console | R |
| `sc_verify_site` | Site-Eigentümerschaft verifizieren — nach Platzieren des Nachweises bzw. direkt via ANALYTICS/TAG_MANAGER, wenn GA/GTM schon auf der Site läuft. Braucht neuen siteverification-Scope (ggf. Verbindung im Portal erneuern) | search_console | W |

---

## Google Tag Manager — Lesen (source: gtm)

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `gtm_container_info` | Container-Metadaten + aktuell live-gepublishte Version | gtm | R |
| `gtm_list_workspaces` | Alle Workspaces des Containers (Default + ggf. Dev-Branches) | gtm | R |
| `gtm_list_tags` | Tags in einem Workspace | gtm | R |
| `gtm_list_triggers` | Trigger in einem Workspace | gtm | R |
| `gtm_list_variables` | User-Defined Variablen in einem Workspace | gtm | R |
| `gtm_list_versions` | Versions-Historie des Containers | gtm | R |
| `gtm_get_version` | Details einer Version inkl. aller Tags, Trigger, Variablen | gtm | R |
| `gtm_get_tag` | Vollständige Tag-Definition (Parameter + Trigger-IDs) | gtm | R |
| `gtm_workspace_status` | Offene Änderungen + Merge-Konflikte eines Workspace — Diagnose bei fehlgeschlagenem `gtm_create_version` | gtm | R |
| `gtm_list_accounts` | GTM-Accounts der Google-Verbindung — geht auch ohne konfigurierten Container | gtm | R |
| `gtm_list_containers` | Container eines GTM-Accounts (`account_id` aus `gtm_list_accounts`) | gtm | R |

---

## Google Tag Manager — Mutation (source: gtm) ⚠ Guardrails

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `gtm_create_version` | Workspace in neue Version snapshotten (publiziert noch nicht) | gtm | W |
| `gtm_publish_version` | Version live schalten — wirkt sofort auf Kunden-Website | gtm | W |
| `gtm_create_tag` | Neuen Tag im Workspace anlegen | gtm | W |
| `gtm_update_tag` | Tag ändern (Name, Parameter, Trigger, paused) | gtm | W |
| `gtm_remove_tag` | Tag aus Workspace löschen | gtm | W |
| `gtm_create_trigger` | Neuen Trigger anlegen (pageview, click, customEvent, …) | gtm | W |
| `gtm_sync_workspace` | Workspace mit neuester Container-Version synchronisieren (bei merge_conflict); Rest-Konflikte werden gelistet | gtm | W |
| `gtm_create_workspace` | Neuen Workspace aus neuester Container-Version anlegen — Recovery bei nicht mehr synchronisierbarem Workspace | gtm | W |
| `gtm_create_container` | Neuen GTM-Container anlegen (web/server/android/ios/amp) — danach mit `workspace_configure_source` verknüpfen | gtm | W |
| `gtm_create_variable` | Neue Variable anlegen; Default-Typ Data-Layer-Variable, Key wird aus dem Namen abgeleitet (`dlv - foo` → `foo`) — Voraussetzung für GA4-Event-Tags mit Parameter-Mapping | gtm | W |

---

## DataForSEO (source: dataforseo)

Leere DataForSEO-Antworten (`"items": null`) brechen die `dfs_*`-Tools nicht mehr ab — Listen-Tools liefern dann eine leere Liste (`dfs_onpage_instant`: `{error: no_items}`).

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `dfs_serp_google_organic` | Top-N organische Google-Ergebnisse für ein Keyword inkl. SERP-Features, AI-Overview-Präsenz + Quellen und People-Also-Ask | dataforseo | R |
| `dfs_keyword_rankings` | Wofür rankt eine Domain aktuell? (DataForSEO Labs) | dataforseo | R |
| `dfs_serp_google_ads` | Paid Ads auf einem Keyword in der Google SERP | dataforseo | R |
| `dfs_keyword_volume` | Search Volume + CPC für eine Keyword-Liste (max 1 000) | dataforseo | R |
| `dfs_related_keywords` | Verwandte Keywords zu einem Seed (Volume + CPC) | dataforseo | R |
| `dfs_keyword_ideas_for_domain` | Keyword-Ideen basierend auf Domain-Inhalten und Ranking-Historie | dataforseo | R |
| `dfs_backlink_summary` | Backlink-Profil einer Domain (Links, Referring Domains, Rank) | dataforseo | R |
| `dfs_backlink_competitors` | Domains mit ähnlichem Backlink-Profil | dataforseo | R |
| `dfs_onpage_instant` | Live On-Page Audit (Title, Meta, H1, Score, Issues) — `checks_failed` = echte Issue-Flags (`no_title`, `no_h1_tag`, `no_description`, `duplicate_title_tag`, `high_loading_time`, `is_broken`, …; Positivflags wie `has_html_doctype`/`is_https` zählen nicht), `fetched_at` (UTC-Zeitstempel; ersetzt `fetch_time_ms`), `page_timing_ms` (Ladezeiten in ms oder `null`); keine Core Web Vitals — dafür `dfs_lighthouse_live` | dataforseo | R |
| `dfs_lighthouse_live` | Google Lighthouse Audit (Performance, Accessibility, SEO) | dataforseo | R |
| `dfs_keyword_overview` | Volumen, CPC, Difficulty und Haupt-Intent für eine Keyword-Liste in einem Call (max 700) | dataforseo | R |
| `dfs_domain_intersection` | Ranking-Schnittmenge zweier Domains — oder Gap-Modus: wofür Domain 2 rankt, Domain 1 nicht | dataforseo | R |
| `dfs_competitors_domain` | Domains mit den meisten gemeinsamen Rankings — echte SEO-Konkurrenten statt Branchen-Raten | dataforseo | R |
| `dfs_keyword_suggestions` | Keyword-Vorschläge zu einem Seed-Keyword inkl. Volumen, CPC, Difficulty | dataforseo | R |
| `dfs_backlinks_list` | Konkrete Backlink-Liste einer Domain, filterbar nach broken/dofollow/lost | dataforseo | R |
| `dfs_llm_mentions` | Marken-/Themen-Erwähnungen in LLM-Antworten je Keyword (~$0.10/Call); `platform` `'google'` (Google AI Overview, Default) oder `'chat_gpt'` — ein Call deckt genau eine Plattform ab; bei `chat_gpt` nur United States/Englisch (location/language werden überschrieben) | dataforseo | R |
| `dfs_llm_mentions_metrics` | Aggregierte Mentions pro Engine, Gesamt-Citations + Share-of-Voice über LLM-Engines (~$0.10/Call); `platform` wie bei `dfs_llm_mentions` (`share_of_voice_by_engine` ist bei einer Plattform pro Call immer 1.0) | dataforseo | R |
| `dfs_llm_top_domains` | Meistzitierte Domains in LLM-Antworten zu einer Keyword-Liste (~$0.10/Call); `platform` wie bei `dfs_llm_mentions` | dataforseo | R |
| `dfs_llm_responses` | Rohe LLM-Antwort + Zitate zu einem Prompt (ChatGPT/Claude/Gemini/Perplexity, ~$0.10/Call); `web_search=True` schaltet die Websuche des Modells ein (höhere Kosten) — bei ChatGPT/Claude/Gemini sind `citations` nur damit zu erwarten; `perplexity` zitiert immer (sonar sucht von sich aus, `web_search` wird dort nicht gesendet) | dataforseo | R |
| `dfs_onpage_crawl` | Seitenweiten Crawl einer Domain starten (asynchron, `max_crawl_pages` Pflicht — Kosten skalieren pro Seite) | dataforseo | R |
| `dfs_onpage_crawl_results` | Crawl-Ergebnisse abrufen (Summary, Pages, Links, Redirects, Duplicate Content u.a.) | dataforseo | R |
| `dfs_reviews` | Rezensionen von Trustpilot oder Google abrufen (task-basiert, ggf. Folge-Call mit task_id) | dataforseo | R |
| `dfs_serp_bing_organic` | Organische Bing-Ergebnisse für ein Keyword — Bing-Index-Präsenz prüfen | dataforseo | R |
| `dfs_domain_technologies` | Eingesetzter Tech-Stack einer Domain (Analytics, Tag-Manager, Advertising-Pixel, CMS) | dataforseo | R |
| `dfs_raw_html` | Rohes HTML einer URL abrufen (z.B. für JSON-LD-Check im Quelltext) | dataforseo | R |
| `dfs_content_parsing` | Strukturierter Seiteninhalt einer URL (Headings, Absätze) | dataforseo | R |
| `dfs_historical_rank_overview` | Monatliche Ranking-Historie einer Domain (organische Keywords, ETV, Top3/Top10) | dataforseo | R |
| `dfs_keyword_trends` | Google-Trends-Verlauf für bis zu 5 Keywords über einen Zeitraum | dataforseo | R |
| `dfs_google_ads_advertisers` | Werbetreibende auf einem Keyword laut Google Ads Transparency Center | dataforseo | R |

---

## Google Business Profile (source: business_profile, außer `gbp_local_rank`: dataforseo) — enthält W ⚠ Guardrails

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `gbp_list_locations` | Alle Standorte des verbundenen Google-Kontos — paginiert vollständig über Accounts und Standorte; bei Erreichen der Seiten-Obergrenze (50 je Schleife) zusätzliches Warn-Element `{"warning": "truncated", ...}` am Listenende | business_profile | R |
| `gbp_location_info` | Stammdaten des Standorts (Name, Adresse, Telefon, Kategorie, Öffnungszeiten) | business_profile | R |
| `gbp_get_profile` | Vollständiges Business-Profil inkl. Attribute und Sonderöffnungszeiten (nur als `special_hours_count`); `attributes` je Attribut `id` plus alle Wertfelder — `values` (Enum/Bool), `uriValues` (URL-Attribute wie `url_linkedin`), `repeatedEnumValue` (Mehrfachauswahl mit `setValues`/`unsetValues`), gleiche Struktur wie `gbp_update_attributes(action="get")`; schlägt die Attribut-Abfrage fehl, ist `attributes=[]` | business_profile | R |
| `gbp_performance` | Impressionen (Maps/Suche), Anrufe, Website-Klicks, Routenanfragen, Buchungen, Essensbestellungen, Menü-Klicks — Zeitraum via `days` (rollierend) oder `start_date`+`end_date`; `metrics` filtert auf eine Teilmenge; `include_time_series=True` liefert Tageswerte statt nur Summen | business_profile | R |
| `gbp_search_keywords` | Suchbegriffe, über die Nutzer das Profil gefunden haben | business_profile | R |
| `gbp_reviews` | Rezensionen: Durchschnittswertung + Bewertungen inkl. Antworten. Fenster: max. 50/Seite (API-Cap, `limit` wird gedeckelt); kein serverseitiges Unbeantwortet-Filter — `unanswered_only=True` + `max_pages` paginiert durch und liefert nur unbeantwortete Reviews plus `pages_scanned`/`next_page_token` (kann dabei bis zu eine Seite mehr als `limit` enthalten); `order_by` (`updateTime desc`, `rating` oder `rating desc`) und `page_token` für Sortierung/Fortsetzung. **Antworten bumpt `updateTime`** — bei `updateTime desc` springt ein gerade beantwortetes Review nach oben: nie Lesen und Antworten verschränken, erst per `unanswered_only` vollständigen Snapshot sammeln, dann antworten | business_profile | R |
| `gbp_reply_review` | Auf eine Rezension antworten (erstellt oder **ersetzt** bestehende Antwort; `comment` max. 4096 Bytes UTF-8) | business_profile | W |
| `gbp_delete_reply` | Löscht die Antwort auf eine Rezension (gilt danach wieder als unbeantwortet) | business_profile | W |
| `gbp_update_profile` | Stammdaten aktualisieren: `title`, `description`, `website_uri`, `phone` (nur gesetzte Felder) | business_profile | W |
| `gbp_manage_categories` | Primär-/Zusatzkategorien suchen (`search_term`), lesen (`get`) oder setzen (`set`) | business_profile | R/W |
| `gbp_update_attributes` | Attribute lesen (`get`) oder setzen (`set`) — Wertformen: URL (String/Liste), Bool, `{'enum': 'WERT'}`, `{'set': […], 'unset': […]}` (Mehrfachauswahl), `None` löscht das Attribut | business_profile | R/W |
| `gbp_manage_hours` | Reguläre + Sonderöffnungszeiten **setzen** — kein Lese-Modus, Ist-Zustand über `gbp_get_profile` | business_profile | W |
| `gbp_manage_open_info` | Öffnungsstatus (openInfo) lesen (`get`) oder setzen (`set`, nur `OPEN` oder `CLOSED_TEMPORARILY`) — `CLOSED_PERMANENTLY` wird bewusst abgelehnt (gehört ins Google-Dashboard) | business_profile | R/W |
| `gbp_get_review_link` | „Bewertung schreiben”-Link des Standorts; ohne `newReviewUri` Fallback auf die lange `writereview`-URL (kein Kurzlink) | business_profile | R |
| `gbp_local_seo_audit` | Profil-Vollständigkeits-Score (Kategorien, Beschreibung, Öffnungszeiten, Attribute, Reviews, Fotos ≥3, Post ≤30 Tage) — **kein NAP-/Citation-Abgleich**; Review-/Foto-/Post-Checks laufen unbewertet, wenn die v4-API nicht freigeschaltet ist | business_profile | R |
| `gbp_local_rank` | Tatsächliche Position im Google-Maps/Local-Pack für ein Keyword + Standort — **Einzelpunkt-Abfrage, kein Grid** | dataforseo | R |
| `gbp_list_posts` | Local Posts des Standorts (Update/Angebot/Veranstaltung) mit Status und CTA, paginiert | business_profile | R |
| `gbp_create_post` | Neuen Local Post veröffentlichen (STANDARD/EVENT/OFFER) — sofort öffentlich sichtbar | business_profile | W |
| `gbp_delete_post` | Löscht einen Local Post | business_profile | W |
| `gbp_list_media` | Hochgeladene Fotos/Medien des Standorts, paginiert | business_profile | R |
| `gbp_upload_media` | Foto per Quell-URL hochladen — sofort öffentlich sichtbar | business_profile | W |
| `gbp_delete_media` | Löscht ein hochgeladenes Foto/Medium | business_profile | W |

---

## Meta Ads — Reporting (source: meta_ads)

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `meta_list_ad_accounts` | Erreichbare Meta-Ad-Accounts auflisten (id, Name, Status, Währung) | meta_ads | R |
| `meta_account_status` | Zustand des Werbekontos: Status, Sperrgrund, Ausgabenlimit, verbrauchtes Budget, Guthaben, hinterlegtes Zahlungsmittel — der schnellste Weg, ein erreichtes Konto-Ausgabenlimit oder ein fehlendes Zahlungsmittel als Ursache für ausbleibende Auslieferung auszuschließen; bei Auffälligkeiten `warnings` im Klartext. Dazu `timezone_name`/`timezone_offset_hours_utc` (Zeitzone des Kontos — Zeitstempel ohne Offset in `meta_create_adset`/`meta_update_adset` gelten in dieser Zeitzone) und `min_daily_budget_eur` (Basis-Minimum des Kontos laut Meta; das tatsächliche Minimum je Adset hängt vom Optimierungsziel ab — Klick-, Conversion- oder Video-optimierte Adsets liegen höher, nur Impressions-optimierte kommen mit dem Basiswert aus; lehnt Meta ein Budget ab, kommt der Fehler durch) | meta_ads | R |
| `meta_list_pages` | Facebook-Pages, die der Account bewerben darf — `page_id` ist Pflicht für `meta_create_ad`; je Page `leadgen_tos_accepted` (`true` = ein Page-Admin hat die Lead-Ads-Nutzungsbedingungen akzeptiert — Voraussetzung für jede Lead-Anzeige; `false` = noch nicht, ein Admin muss sie unter facebook.com/ads/leadgen/tos für genau diese Page annehmen, per API nicht möglich; `null` = nicht lesbar: Scope `pages_show_list` fehlt oder die Page ist nur über das Werbekonto sichtbar) + `leadgen_tos_acceptance_time` | meta_ads | R |
| `meta_list_lead_forms` | Lead-Formulare (Instant Forms) je Facebook-Page — Name, ID, Status, `leads_count`; beantwortet „wie heißt Formular X?” ohne Raten (Meta führt die Formulare an der Page, nicht am Werbekonto). Braucht die Scopes `pages_show_list` + `leads_retrieval` — fehlen sie, kommt `{error, code, hint}` zurück (Meta-Verbindung mit diesen Scopes neu herstellen); `page_id` optional: bei mehreren Pages `error=page_id_required` mit Auswahl, unbekannte `page_id` → `error=page_not_found` mit `available_pages`; `limit` (Default 100) — nur die erste Seite, weitere Formulare werden ohne Hinweis abgeschnitten | meta_ads | R |
| `meta_list_pixels` | Meta-Pixel (Datasets) auflisten inkl. „zuletzt gefeuert” — schnellster Tracking-Check | meta_ads | R |
| `meta_pixel_stats` | Pixel-Event-Statistiken der letzten N Tage (Summen + Tagesverlauf) | meta_ads | R |
| `meta_list_custom_conversions` | Custom Conversions des Werbekontos auflisten (Regel, Ereignistyp, Wert; `limit` Default 50) — ohne definierte Custom Conversion lässt sich nur auf rohe Pixel-Ereignisse optimieren | meta_ads | R |
| `meta_campaign_performance` | Kampagnen-Performance (Impressionen, Klicks, Spend, Conversions; dazu `link_clicks` = echte Link-Klicks — `clicks` zählt Likes/Profilaufrufe mit —, `landing_page_views`, `landing_page_rate_pct`, `reach`, `frequency`, `cpm`, `cpc`, `cost_per_link_click`) — je Zeile `campaign_id` + `campaign` (die ID ist der Schlüssel für `meta_update_campaign` & Co.). **Zeitraum:** `days` (Default 30) = heute minus N Tage bis heute EINSCHLIESSLICH (N+1 Kalendertage, heute unvollständig; für Vergleiche mit Google-Ads-Zahlen `daily=True` und heute herausrechnen); `since`/`until` (`YYYY-MM-DD`, beide zusammen, einschließlich — sonst `error=date_range_incomplete`, `until` vor `since` → `error=date_range_invalid`) hat Vorrang vor `date_preset`, das Vorrang vor `days` hat; `date_preset` nur aus Metas Positivliste: today, yesterday, this_month, last_month, this_quarter, last_quarter, this_year, last_year, last_3d/7d/14d/28d/30d/90d, last_week_mon_sun, last_week_sun_sat, this_week_mon_today, this_week_sun_today, maximum, data_maximum (sonst `error=invalid_date_preset`); jede Zeile trägt `date_start`/`date_stop` = die tatsächlich summierte Spanne, wie Meta sie meldet (bei `daily=True` stattdessen `date` je Tag) — im Report die gemeldete Spanne nennen. `totals_only=True` = Gesamtzahlen des Kontos als EINE Zeile ohne `campaign`/`campaign_id` — für Kontosummen diesen Weg nehmen statt Zeilen zu addieren (bei `breakdown` überschneiden sich `reach`-Werte); mit `breakdown`/`daily` kombinierbar, nicht mit `campaign_id` (`error=totals_only_with_campaign`). Zahlen folgen der Attributionseinstellung der Adsets (unified attribution, wie im Ads Manager — nicht Metas API-Default). `breakdown` = Aufschlüsselung statt Summenzeile (`publisher_platform`, `platform_position`, `device_platform`, `age`, `gender`, `country`, `region`); `daily=True` = Zeitreihe je Tag (ein kürzeres Fenster ersetzt das nicht); `campaign_id` = nur diese Kampagne, ohne Angabe ALLE Kampagnen; `conversions` zählt AUSSCHLIESSLICH Käufe und Leads — Custom Conversions getrennt in `custom_conversions`, alle Ereignistypen in `actions` (`conversions=0` heißt nicht „konvertiert nicht”); bei leeren Insights trotz Kampagnen: `{"result": [], "time_range"/"date_preset": …, "info": "<Erklärung>"}`; Obergrenze ~2.000 Zeilen → `{result, warning}`, Sortierung gilt dann nur für den Ausschnitt | meta_ads | R |
| `meta_adset_performance` | Adset-Performance (Impressionen, Klicks, Spend, Conversions + `link_clicks`, `landing_page_views`, `landing_page_rate_pct`, `reach`, `frequency`, `cpm`, `cpc`, `cost_per_link_click`), sortiert nach Spend — je Zeile `campaign_id`/`campaign` und `adset_id`/`adset` (die IDs sind der Schlüssel für `meta_update_adset`). Zeitraum wie `meta_campaign_performance`: `days` (heute EINSCHLIESSLICH), `since`/`until` (`YYYY-MM-DD`, beide zusammen; `error=date_range_incomplete`/`date_range_invalid`) > `date_preset` (gleiche Positivliste, sonst `error=invalid_date_preset`) > `days`; jede Zeile trägt `date_start`/`date_stop` (bei `daily` `date`). Zahlen folgen der Attributionseinstellung der Adsets (unified attribution, wie im Ads Manager); Kontosummen über `meta_campaign_performance(totals_only=True)` statt Zeilen zu addieren. `campaign_id` = nur die Adsets DIESER Kampagne — ohne Angabe ALLE Adsets des Kontos (kontoweite Zahlen nicht als Kampagnenzahlen lesen); `breakdown`/`daily` wie bei `meta_campaign_performance`; `conversions` = nur Käufe/Leads (`custom_conversions`/`actions` gegenprüfen); bei leeren Insights trotz Kampagnen: `{"result": [], "time_range"/"date_preset": …, "info": "<Erklärung>"}`; Obergrenze ~2.000 Zeilen → `{result, warning}` | meta_ads | R |
| `meta_ad_performance` | Performance einzelner Anzeigen (Kennzahlen wie `meta_campaign_performance` inkl. `reach`/`frequency`; dazu je Anzeige `quality_ranking`, `engagement_rate_ranking`, `conversion_rate_ranking` — UNKNOWN = zu wenig Volumen für eine Einstufung, nicht „schlecht”), sortiert nach Spend — je Zeile `campaign_id`/`campaign`, `adset_id`/`adset` und `ad_id`/`ad` (Schlüssel für `meta_update_ad_status` und `ad_id`-Vergleiche). Zeitraum wie `meta_campaign_performance`: `days` (heute EINSCHLIESSLICH), `since`/`until` (`YYYY-MM-DD`, beide zusammen; `error=date_range_incomplete`/`date_range_invalid`) > `date_preset` (gleiche Positivliste, sonst `error=invalid_date_preset`) > `days`; jede Zeile trägt `date_start`/`date_stop` (bei `daily` `date`). Zahlen folgen der Attributionseinstellung der Adsets (unified attribution, wie im Ads Manager); Kontosummen über `meta_campaign_performance(totals_only=True)`. `ad_id`/`adset_id`/`campaign_id` schränken ein, die feinere Angabe gewinnt (`ad_id` vor `adset_id` vor `campaign_id`; `ad_id` = direkter Weg, zwei Anzeigen zu vergleichen) — ohne Angabe ALLE Anzeigen des Kontos; `breakdown`/`daily` wie bei `meta_campaign_performance`; `conversions` = nur Käufe/Leads (`custom_conversions`/`actions` gegenprüfen); bei leeren Insights trotz Kampagnen: `{"result": [], "time_range"/"date_preset": …, "info": "<Erklärung>"}`; Obergrenze ~2.000 Zeilen → `{result, warning}` | meta_ads | R |
| `meta_list_campaigns` | Kampagnen auflisten — je Kampagne `status`, `effective_status`, `objective`, `daily_budget_eur`/`lifetime_budget_eur` (CBO = eines davon gesetzt), `bid_strategy` (nur bei CBO, sonst `null` — dann liegt sie am Adset), `spend_cap_eur` (Ausgabenlimit der Kampagne; `null` = kein Limit — auch Metas „kein Limit”-Sentinelwert kommt als `null`, nicht als Riesenbetrag), `budget_remaining_eur` (nur bei CBO; `null` ohne Kampagnenbudget — dann liegt das Budget an den Adsets), `special_ad_categories` (Liste, `[]` = keine), `buying_type` (AUCTION/RESERVED), `start_time`/`stop_time`, `updated_time`, nicht-leere `issues` — zum Zurücklesen nach `meta_create_campaign`/`meta_update_campaign`; `start_time`/`stop_time` leitet Meta aus den Adsets ab (`null` ohne Adset-Enddatum) — ein Kampagnen-Enddatum gibt es nicht, `end_time` wird je Adset gesetzt; `limit` (Default 50) — wird abgeschnitten (Meta meldet weitere Seiten), kommt `{result, warning}` statt der Liste, dann `limit` erhöhen | meta_ads | R |
| `meta_list_adsets` | Adsets auflisten, optional pro Kampagne (Status, Budget in EUR inkl. `lifetime_budget_eur`, `billing_event`, Optimierungsziel, Targeting-Zusammenfassung, `start_time`/`end_time` = Zeitplan, Gebot zum Zurücklesen: `bid_strategy` (`null` bei CBO — dann liegt sie an der Kampagne, `meta_list_campaigns`), `bid_amount_eur` (Bid Cap / Cost Cap), `bid_constraints` (roh) und `min_roas` (Mindest-ROAS als Verhältnis, 2.5 = 250 %; aus `bid_constraints.roas_average_floor` / 10000; `null` ohne), `promoted_object` (z.B. `{page_id}` bei Lead-Adsets, `{pixel_id, custom_event_type}` bei Conversion-Adsets) und `destination_type` so, wie Meta sie führt (`None` = nicht gesetzt) — zum Zurücklesen nach `meta_create_adset`/`meta_update_adset` (Meta braucht nach dem Schreiben ein paar Sekunden, bis der neue Stand sichtbar ist), nicht-leere `issues`; je Adset `learning` = Stand der Lernphase (`status` LEARNING = lernt noch, Auslieferung schwankt; LEARNING_LIMITED = abgebrochen, zu wenig Conversions; `"unbekannt"` = Meta liefert nichts dazu, üblich wenn das Adset nicht auf ein Conversion-Ereignis optimiert — jeweils mit Klartext-Hinweis; andere Meta-Werte wie SUCCESS = Lernphase abgeschlossen werden unverändert und ohne Hinweis durchgereicht); `targeting.placements` = aktive Plattformen, Positionen und Geräte (`publisher_platforms: "automatisch (alle Plattformen)"` = läuft auch im Audience Network); `targeting` zeigt neben `countries` auch Geo-Verfeinerungen `regions`/`cities`/`zips`/`custom_locations` (je `key`, `name`, `country`, `region`, `radius`/`distance_unit` bzw. Koordinaten/Adresse), `country_groups`, `location_types`, `excluded_geo_locations` (gleiche Struktur), `excluded_custom_audiences`, `interests`, `behaviors` und `locales` — diese Schlüssel erscheinen NUR, wenn gesetzt; ein Adset nur mit `countries` läuft landesweit; DSA-Felder immer, `null` = fehlt; `eu_eea_targeting` mit EU-/EWR-Treffern der erfassten Geo-Formen, `[]` = keiner, `UNKNOWN` = nicht auswertbar); `limit` (Default 50) — wird abgeschnitten, kommt `{result, warning}` statt der Liste, dann `campaign_id` einschränken oder `limit` erhöhen | meta_ads | R |
| `meta_list_ads` | Ads auflisten, optional pro Adset (Status, Creative inkl. `creative.link_url` = Zielseite und `creative.url_tags` = UTM-Parameter, nicht-leere `issues`, vorhandenes `review_feedback`); Lead-Anzeigen (Instant Form) tragen `creative.lead_gen_form_id` (Formular via `meta_list_lead_forms` auflösbar; `link_url` ist dort Metas Platzhalter `https://fb.me/`) — fehlt das Feld, nutzt die Anzeige kein Instant Form; `name_contains` filtert serverseitig, `status` filtert den KONFIGURIERTEN Status schon beim Laden (blättert weiter, bis `limit` passende Anzeigen vorliegen, höchstens 20 Seiten à 100 — vorzeitiger Abbruch steht in `warning`); `limit` (Default 50) — wird abgeschnitten, kommt `{result, warning}` statt der Liste | meta_ads | R |
| `meta_list_audiences` | Custom Audiences des Meta-Ad-Accounts inkl. Customer-Match-Listen — IDs als `custom_audience_ids` (einschließen) oder `excluded_custom_audience_ids` (ausschließen, z.B. Bestandskunden) in `meta_create_adset`/`meta_update_adset` verwendbar | meta_ads | R |
| `meta_targeting_search` | Meta-Targeting-Schlüssel suchen (Metas Targeting Search) — DAS Werkzeug, bevor in `meta_create_adset`/`meta_update_adset` Städte, Regionen, PLZ, Interessen, Behaviors oder Sprachen gesetzt werden; Schlüssel nie raten. `kind`: `city` (Städte; `key` + `supports_region`/`country_code`), `region` (Bundesländer/Regionen), `zip` (Postleitzahlen; `key` mit Landespräfix wie `AT:5020`, `primary_city`), `country` (ISO-Code als `key`), `geo` (country+region+city+zip in einer Suche, `type` je Treffer), `interest` (Interessen: `id`, `name`, `path`, `audience_size_lower/upper_bound`, `topic` — `q` Pflicht, sonst `error=query_required`), `behavior` (Behaviors: `id`, `name`, `path`, `description`, Größe — Meta liefert die komplette Liste, `q` filtert sie über Name und Pfad), `locale` (Sprachen: `key` als Ganzzahl, `name` — `q` darf leer sein = alle Sprachen bis `limit`); anderer Wert → `error=invalid_kind`. `q` = Suchbegriff (z.B. `Salzburg`, `5020`, `Wandern`, `German`); `country_code` grenzt die Geo-Suche ein (z.B. `AT` — sonst findet `Salzburg` auch Orte in anderen Ländern); `limit` (Default 25; Metas eigener Default wären 8) — gibt es mehr Treffer, kommt `{result, warning}` (auch bei Behaviors/Sprachen, wo Meta keine Seiten meldet), dann `limit` erhöhen oder `q` präzisieren. Jeder Treffer trägt `verwendung` mit dem fertigen Parameter, z.B. `cities=[{'key': '2420605', 'radius_km': 17}]`, `regions=['1234']`, `zips=['AT:5020']`, `countries=['AT']`, `interest_ids=['6003…']`, `behavior_ids=['…']`, `locales=[5]`; dieselben Schlüssel gelten in `excluded_geo_locations` (z.B. `{'zips': ['AT:5020']}`). Leere Trefferliste = nichts gefunden (kein Fehler) — Schreibweise oder `country_code` prüfen. Nur Lesezugriff | meta_ads | R |
| `meta_video_status` | Verarbeitungsstatus eines hochgeladenen Ad-Videos (`ready` = nutzbar) | meta_ads | R |

---

## Meta Ads — Mutation (source: meta_ads) ⚠ Guardrails

`validate_only=true` gibt es bei `meta_create_campaign`, `meta_update_campaign`, `meta_create_adset`, `meta_update_adset` und `meta_update_ad_status` (echter API-Dry-Run: Meta prüft den Aufruf, ohne etwas zu ändern — ein Erfolg heißt, Meta würde die Änderung annehmen) sowie bei `meta_create_ad` (reine Parameter-Vorschau OHNE API-Calls, lokal als `would_create` — ob Meta die Ad wirklich akzeptiert, zeigt erst der echte Aufruf). **Kein `validate_only`:** `meta_create_pixel`, `meta_delete_campaign`, `meta_upload_ad_image`, `meta_upload_ad_video` (der Parameter existiert dort nicht — Preview zeigen, einzeln bestätigen lassen) und `meta_create_custom_conversion` (Meta ignoriert das Flag an diesem Endpunkt und würde trotzdem echt anlegen — das Tool bricht bei `validate_only=true` mit einem Fehler ab, statt einen Probelauf vorzutäuschen).

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `meta_create_pixel` | Neues Pixel (Dataset) anlegen — liefert Pixel-ID + Einbau-Code; Pixel lassen sich per API nicht löschen — vorher mit `meta_list_pixels` prüfen, ob schon eines existiert | meta_ads | W |
| `meta_create_custom_conversion` | Custom Conversion anlegen — meist eine Danke-Seite als Lead-Ereignis; Regel über GENAU EINE der drei Angaben: `url_contains` (z.B. `'/danke'`, vergleicht case-insensitiv), `url_equals` (case-SENSITIV, Meta kennt kein i_eq — im Zweifel `url_contains` nehmen) oder `rule` (Metas Regelsyntax direkt); `custom_event_type` LEAD (Default), PURCHASE, COMPLETE_REGISTRATION, CONTACT, SCHEDULE, SUBMIT_APPLICATION, START_TRIAL, SUBSCRIBE, ADD_TO_CART, INITIATED_CHECKOUT, CONTENT_VIEW, SEARCH, OTHER; `default_conversion_value` = Betrag in Kontowährung (kein Cent-Wert); `pixel_id` aus `meta_list_pixels`; **`validate_only` NICHT unterstützt** — Meta ignoriert das Flag an diesem Endpunkt und würde trotzdem echt anlegen, das Tool bricht deshalb mit einem Fehler ab, statt einen Probelauf vorzutäuschen; ohne `validate_only` aufrufen, wenn die Conversion entstehen soll. ACHTUNG: es gibt in diesem Toolset KEIN Werkzeug zum Löschen oder Archivieren — das geht nur im Meta Werbeanzeigenmanager | meta_ads | W |
| `meta_create_campaign` | Neue Kampagne anlegen (Standard: PAUSED) — `daily_budget` ODER `lifetime_budget` in EUR gesetzt = CBO, nie beides (`error=budget_conflict`); `lifetime_budget` = Gesamtsumme bis zum Enddatum, und das Enddatum liegt bei Meta an den Adsets: jedes Adset dieser Kampagne braucht `end_time` (`meta_create_adset` lehnt sonst mit `error=end_time_required` ab) — ein Kampagnen-Enddatum gibt es nicht, Meta leitet Start/Ende aus den Adsets ab; `bid_strategy` NUR zusammen mit einem Kampagnenbudget (CBO; Default LOWEST_COST_WITHOUT_CAP, alternativ LOWEST_COST_WITH_BID_CAP/COST_CAP — `bid_amount` dann je Adset Pflicht — oder LOWEST_COST_WITH_MIN_ROAS — der Mindest-ROAS liegt ebenfalls am Adset: `meta_create_adset(min_roas=…)`, dort Pflicht, ohne eigene `bid_strategy` am Adset; die Kampagne kennt kein `bid_constraints`, und die Strategie einer Kampagne ist nachträglich über die Tools nicht änderbar — `meta_update_campaign` kennt kein `bid_strategy`), sonst bricht das Tool mit `error=bid_strategy_requires_budget` ab (nichts wird angelegt) — dann Budget mitgeben oder die Strategie je Adset in `meta_create_adset` setzen; Zurücklesen: `meta_list_campaigns` → `bid_strategy`, `spend_cap_eur`, `special_ad_categories`; `special_ad_categories` = Meta-Literale als Liste, z.B. `['HOUSING']`, `['CREDIT']`, `['EMPLOYMENT']`, `['ISSUES_ELECTIONS_POLITICS']` — nur wenn zutreffend (Wohnen/Kredit/Jobs/Politik), wird ungeprüft an Meta durchgereicht | meta_ads | W |
| `meta_update_campaign` | Kampagne ändern: Name, `status` (ACTIVE = starten; PAUSED = pausieren — zum Stoppen PAUSED nehmen, jederzeit umkehrbar; ARCHIVED = gestoppt und nur noch lesbar, Berichte bleiben, keine Auslieferung mehr; DELETED = endgültig gelöscht, NICHT umkehrbar — wie `meta_delete_campaign`), `daily_budget` ODER `lifetime_budget` in EUR (nie beides → `error=budget_conflict`; nur bei CBO, sonst `error=budget_not_on_campaign` → Budget je Adset via `meta_update_adset`); ein Wechsel Tages↔Laufzeitbudget ist bei Meta nicht erlaubt (Meta lehnt ab, nichts wird geändert) → neues Adset bzw. neue Kampagne anlegen; kein Kampagnen-Enddatum — Meta leitet Start/Ende aus den Adsets ab, `end_time` je Adset via `meta_update_adset` | meta_ads | W |
| `meta_delete_campaign` | Kampagne endgültig löschen inkl. Adsets/Ads, nicht umkehrbar — zum bloßen Stoppen besser `meta_update_campaign` mit `status=PAUSED` (umkehrbar) oder ARCHIVED (nur noch lesbar); `deleted=True` kommt nur, wenn Meta die Löschung bestätigt (`success=true`) — sonst `error=delete_failed` bzw. `meta_api_error` mit Metas Begründung (HTTP 200 ohne JSON-Body: `error=invalid_response`): nichts gilt als gelöscht, was Meta nicht bestätigt hat → Stand mit `meta_list_campaigns` prüfen | meta_ads | W |
| `meta_create_adset` | Neues Adset anlegen (Standard: PAUSED) — Budget: `daily_budget` ODER `lifetime_budget` in EUR, genau eines (`error=budget_conflict` bei beiden; ohne CBO Pflicht → `error=budget_required`, bei CBO-Kampagne wird das Adset-Budget ignoriert); `lifetime_budget` = Gesamtsumme bis `end_time` und braucht `end_time` (`error=end_time_required`) — ebenso jedes Adset in einer Kampagne mit Laufzeitbudget; + Zielgruppe: `countries` (ISO-Codes; Default `['AT']` gilt NUR, wenn keine Geo-Verfeinerung übergeben wird), `age_min`/`age_max`, `genders` (nur `male`/`female`, Default alle — andere Werte werden still ignoriert), `custom_audience_ids`/`excluded_custom_audience_ids` (IDs aus `meta_list_audiences`; Ausschluss z.B. Bestandskunden), `interest_ids`/`behavior_ids` (IDs aus `meta_targeting_search` kind `interest`/`behavior`), `locales` (Meta-Locale-Schlüssel als Ganzzahlen aus kind `locale`, sonst `error=invalid_locales`); **Geo-Verfeinerung** — Schlüssel immer via `meta_targeting_search` holen, nie raten: `cities=[{'key': '2420605', 'radius_km': 17}]` (Umkreis um eine Stadt 17–80 km, ohne `radius_km` nur das Stadtgebiet; `error=invalid_city_radius`), `regions=['1234']` (Bundesland/Region), `zips=['AT:5020']` (Landespräfix Pflicht, `error=invalid_zip_key`), `custom_locations=[{'latitude': 47.8, 'longitude': 13.04, 'radius_km': 10}]` oder `[{'address_string': 'Getreidegasse 9, Salzburg', 'radius_km': 5, 'name': 'Altstadt'}]` (Umkreis 1–80 km, `error=invalid_custom_location`); Städte/Umkreise aus `meta_list_adsets` (`{'key', 'radius', 'distance_unit': 'kilometer', …}`) dürfen 1:1 übernommen werden, Meilen und unbekannte Felder werden abgelehnt (`error=invalid_city_radius`/`invalid_cities`); leere Listen sind beim Anlegen keine Angabe (auch `countries=[]`). **Konfliktregel von Meta** (Subcode 1487756 „Some locations conflict with each other” — der Fehler kommt mit `hint` zurück): Orte, die ineinander liegen, dürfen nicht gemeinsam EINGESCHLOSSEN werden — `countries=['AT']` + Stadt Salzburg, Region Salzburg + Stadt Salzburg, Stadt-Umkreis + PLZ darin, Stadt + `custom_location` im selben Gebiet lehnt Meta ab → nur die Verfeinerung gemeint: `countries` weglassen (dann kein AT-Default — deshalb gilt der Default nur ohne Verfeinerung); `countries` UND Verfeinerung zusammen nur länderübergreifend (z.B. DE komplett + Salzburg/AT); `excluded_geo_locations` = Gebiete INNERHALB eines eingeschlossenen Gebiets AUSSCHLIESSEN (erlaubt: Region Salzburg minus Stadt Salzburg, Land minus Stadt, Stadt-Umkreis minus PLZ), gleiche Struktur als Dict, z.B. `{'zips': ['AT:5020']}`, `{'cities': [{'key': '…', 'radius_km': 17}]}`, `{'countries': ['CH']}` (andere Schlüssel `error=invalid_excluded_geo_locations`); Platzierungen: `publisher_platforms` (z.B. `['facebook','instagram']` — OHNE Angabe laufen automatische Platzierungen, also auch Audience Network), `positions` je Plattform (die Plattform muss auch in `publisher_platforms` stehen), `device_platforms`; **Gebot:** `bid_strategy` (Default LOWEST_COST_WITHOUT_CAP = „Highest Volume”; LOWEST_COST_WITH_BID_CAP/COST_CAP brauchen `bid_amount` in EUR; LOWEST_COST_WITH_MIN_ROAS braucht `min_roas` (`error=min_roas_required`), kennt KEIN `bid_amount` (`error=bid_amount_not_applicable`) und bei Meta `optimization_goal='VALUE'` plus ein für Wertoptimierung freigeschaltetes Konto) — bei einer CBO-Kampagne liegt die Strategie an der Kampagne und gilt für jedes Adset: `bid_strategy` hier weglassen (abweichende Angabe → `error=bid_strategy_campaign_level`) und je nach Kampagnenstrategie nur `bid_amount` (BID_CAP/COST_CAP, Pflicht) bzw. `min_roas` (MIN_ROAS, Pflicht) mitgeben — das Tool liest die Kampagnenstrategie und prüft dagegen; `min_roas` = Mindest-ROAS als Verhältnis (2.5 = 250 %, erlaubt 0.01–1000, sonst `error=invalid_min_roas`), geht als `bid_constraints.roas_average_floor` (×10000) raus — nur mit LOWEST_COST_WITH_MIN_ROAS (am Adset oder bei CBO an der Kampagne), sonst `error=min_roas_not_applicable`; Zurücklesen: `meta_list_adsets` → `bid_strategy`/`bid_amount_eur`/`min_roas` (Strategie bei CBO via `meta_list_campaigns`); DSA-Angaben (EU-Pflicht), `advantage_audience` (Pflichtentscheidung; Default False = konfiguriertes Targeting gilt exakt); `promoted_object`: `promoted_page_id` (Page, deren Instant Forms beworben werden — Pflicht bei `optimization_goal=LEAD_GENERATION`, sonst `error=promoted_page_required`; ID aus `meta_list_pages`) bzw. `pixel_id` + `custom_event_type` immer zusammen (Pflicht bei `OFFSITE_CONVERSIONS`, sonst `error=pixel_event_required`; Pixel aus `meta_list_pixels`, Ereignis laut Meta-Enum z.B. LEAD/PURCHASE/COMPLETE_REGISTRATION/CONTACT/SUBMIT_APPLICATION/SUBSCRIBE/ADD_TO_CART/INITIATED_CHECKOUT, sonst `error=invalid_custom_event_type`); `destination_type` laut Meta-Enum (WEBSITE, ON_AD = Instant Form direkt in der Anzeige, MESSENGER, WHATSAPP, INSTAGRAM_DIRECT, APP, FACEBOOK_PAGE; sonst `error=invalid_destination_type`); **Lead-Adset (Instant Form):** `optimization_goal='LEAD_GENERATION'` + `promoted_page_id` + `destination_type='ON_AD'`, Anzeige danach mit `meta_create_ad(lead_gen_form_id=…)` — Voraussetzung: `meta_list_pages` → `leadgen_tos_accepted`, sonst lehnt Meta die Anzeige ab; Zeitplan `start_time`/`end_time` (`end_time` = Traffic-Enddatum, danach pausiert Meta die Auslieferung; je als Datum `2026-09-30` (= Tagesende) oder ISO-Zeitstempel, ohne Offset wird die Zeitzone des Werbekontos angehängt — Meta würde sonst UTC annehmen); Budget/Zeitplan/`promoted_object`/`destination_type`/Geo-Verfeinerungen/Ausschlüsse/Interessen/Behaviors/`locales` mit `meta_list_adsets` zurücklesen; nicht-blockierende DSA-Warnung für alle Geo-Einträge mit Ländercode und `country_groups` `europe`/`eea`/`worldwide` | meta_ads | W |
| `meta_update_adset` | Adset ändern: Name, `status` (ACTIVE = starten; PAUSED = pausieren — zum Stoppen PAUSED nehmen, umkehrbar; ARCHIVED = gestoppt und nur noch lesbar, Berichte bleiben; DELETED = endgültig gelöscht, NICHT umkehrbar), `daily_budget` ODER `lifetime_budget` in EUR (nie beides → `error=budget_conflict`; `lifetime_budget` braucht `end_time` — mitgegeben oder schon am Adset gesetzt, sonst `error=end_time_required`; ein Wechsel Tages↔Laufzeitbudget ist bei Meta eingeschränkt — lehnt Meta ab, kommt der Fehler durch), Gebot (`bid_strategy`/`bid_amount`/`min_roas` — Regeln am Ende dieser Zeile), DSA-Angaben (EU-Pflicht), `advantage_audience`, `promoted_object` (`promoted_page_id` bzw. `pixel_id` + `custom_event_type` immer zusammen, sonst `error=pixel_event_required`; unbekanntes Ereignis `error=invalid_custom_event_type`; nur Übergebenes wird gesendet — ob Meta das `promoted_object` eines bestehenden Adsets ändern lässt, hängt vom Optimierungsziel ab, eine Ablehnung kommt durch), `destination_type` (Meta-Enum, sonst `error=invalid_destination_type`), Zeitplan `start_time`/`end_time` (`end_time` = Traffic-Enddatum; Datum `2026-09-30` (= Tagesende) oder ISO-Zeitstempel, ohne Offset wird die Zeitzone des Werbekontos angehängt — Meta würde sonst UTC annehmen), Targeting (Länder, Geo-Verfeinerung, Ausschlüsse, Audiences, Interessen, Sprachen) — wird gemerged: nur übergebene Teile werden ersetzt; Listen (`countries`, `cities`, `regions`, `zips`, `custom_locations`, `interest_ids`, `behavior_ids`, `locales`, `excluded_custom_audience_ids`) ersetzen ihren Bestand komplett, eine LEERE Liste entfernt ihn (`cities=[]` löscht alle Städte, `interest_ids=[]` alle Interessen, `excluded_geo_locations={'zips': []}` den PLZ-Ausschluss; `countries=[]` entfernt `countries` UND `country_groups` aus `geo_locations` — ausdrückliche Anfrage, daher ohne Warnung); `geo_locations`/`excluded_geo_locations` werden schlüsselweise gemergt; `custom_audience_ids=[]` und `genders=[]` sind dagegen keine Angabe (unverändert). Geo-Verfeinerung — Schlüssel via `meta_targeting_search`: `cities=[{'key': '2420605', 'radius_km': 17}]` (17–80 km, `error=invalid_city_radius`), `regions=['1234']`, `zips=['AT:5020']` (Landespräfix Pflicht, `error=invalid_zip_key`), `custom_locations=[{'latitude': 47.8, 'longitude': 13.04, 'radius_km': 10}]` oder `[{'address_string': '…', 'radius_km': 5}]` (1–80 km, `error=invalid_custom_location`); Städte/Umkreise aus `meta_list_adsets` (`{'key', 'radius', 'distance_unit': 'kilometer', …}`) dürfen 1:1 zurückgegeben werden, Meilen (`distance_unit='mile'`) und unbekannte Felder werden abgelehnt (`error=invalid_city_radius`/`invalid_cities`), nie still umgedeutet. Konfliktregel von Meta (Subcode 1487756 „Some locations conflict with each other”): Orte, die ineinander liegen, dürfen nicht gemeinsam EINGESCHLOSSEN werden (Land + Stadt darin, Region + Stadt darin, Stadt-Umkreis + PLZ darin) — Meta lehnt den Aufruf ab, der Fehler kommt mit `hint` → eine Verfeinerung OHNE `countries` ENTFERNT bestehende `countries` UND `country_groups` (z.B. `europe` aus dem Ads Manager) aus dem Targeting und meldet das in `warnings` (für Ländergruppen ist der Konflikt nicht live geprüft — „wird dasselbe angenommen”); soll ein Land zusätzlich gelten (nur sinnvoll für Orte in ANDEREN Ländern, z.B. DE + Salzburg/AT), `countries` mitgeben — dann bleibt es stehen, ohne Warnung (liegt der Ort im Land, beantwortet Meta den Konflikt selbst mit 1487756 + `hint`); `countries` ersetzt eine bestehende `country_groups` (mit Warnung) — Ländergruppen lassen sich über dieses Tool nicht setzen; Länder gezielt entfernen: `countries=[]`; bleibt nach dem Merge kein Geo-Eintrag übrig (auch nach `countries=[]`) → `error=geo_required`, nichts geändert. Ausschlüsse INNERHALB eines Gebiets sind erlaubt (z.B. `countries=['AT']` minus Stadt Salzburg, Region minus Stadt, Stadt-Umkreis minus PLZ): `excluded_geo_locations` als Dict wie `{'zips': ['AT:5020']}`, `{'cities': […]}`, `{'regions': […]}`, `{'countries': ['CH']}`, `{'custom_locations': […]}` (andere Schlüssel `error=invalid_excluded_geo_locations`); `excluded_custom_audience_ids` (IDs aus `meta_list_audiences`); `interest_ids`/`behavior_ids` (IDs aus `meta_targeting_search` kind `interest`/`behavior`); `locales` (Ganzzahlen aus kind `locale`, sonst `error=invalid_locales`); `publisher_platforms` schränkt die Plattformen ein (`['facebook','instagram']` schaltet z.B. Audience Network ab; Positionen abgewählter Plattformen werden mit entfernt); alles mit `meta_list_adsets` zurücklesen (gemergter Stand im `targeting`) — Meta braucht nach dem Schreiben ein paar Sekunden, bis der neue Stand sichtbar ist; **Gebot:** `bid_strategy` = LOWEST_COST_WITHOUT_CAP, LOWEST_COST_WITH_BID_CAP, COST_CAP oder LOWEST_COST_WITH_MIN_ROAS (BID_CAP/COST_CAP brauchen `bid_amount`; MIN_ROAS braucht `min_roas` → sonst `error=min_roas_required`, und kennt KEIN `bid_amount` → `error=bid_amount_not_applicable`); `min_roas` = Mindest-ROAS als Verhältnis (2.5 = 250 %, erlaubt 0.01–1000), geht als `bid_constraints.roas_average_floor` (×10000) raus — Umstellen auf Mindest-ROAS zusammen mit `bid_strategy=LOWEST_COST_WITH_MIN_ROAS`; `min_roas` OHNE `bid_strategy` liest die bestehende Strategie (Adset; bei CBO die der Kampagne) und sendet nur den neuen Floor, wenn sie schon LOWEST_COST_WITH_MIN_ROAS ist (bei CBO ohne `bid_strategy` — die liegt an der Kampagne) — jede andere Strategie → `error=min_roas_not_applicable`, nichts geändert (kein stilles Umschalten); die Antwort nennt den gesendeten Wert in `min_roas`; `bid_amount` OHNE `bid_strategy` liest die bestehende Strategie des Adsets und behält sie bei (COST_CAP bleibt COST_CAP; nur LOWEST_COST_WITHOUT_CAP wechselt auf LOWEST_COST_WITH_BID_CAP) — nutzt das Adset (oder bei CBO die Kampagne) LOWEST_COST_WITH_MIN_ROAS, gibt es kein `bid_amount` → `error=bid_amount_not_applicable`; die Antwort nennt in `bid_strategy`, was gesendet wurde (bei CBO-Adsets ohne eigene Strategie fehlt das Feld) — ist die Strategie nicht lesbar, bricht das Tool ohne Änderung ab; Zurücklesen: `meta_list_adsets` → `bid_strategy`/`bid_amount_eur`/`min_roas`; gleiche DSA-Coverage, bei `status=ACTIVE` zusätzlicher Best-effort-Advisory-Check (Ausfall → `dsa_check: "unavailable"` + Warnung) | meta_ads | W |
| `meta_update_ad_status` | Ad-Status ändern (ACTIVE/PAUSED/ARCHIVED/DELETED) | meta_ads | W |
| `meta_upload_ad_image` | Bild von öffentlicher URL in die Bildbibliothek laden (max. 8 MB) — liefert `image_hash` | meta_ads | W |
| `meta_upload_ad_video` | Video von öffentlicher URL laden — asynchron, Status via `meta_video_status` | meta_ads | W |
| `meta_create_ad` | Neue Ad anlegen (Bild ODER Video; Website- oder Lead-Anzeige) — Creative + Ad in einem Schritt (Standard: PAUSED); `link` = Zielseite, Pflicht außer bei Lead-Anzeigen (`error=link_required`); `lead_gen_form_id` (Instant Form, ID aus `meta_list_lead_forms`) macht die Anzeige zur Lead-Anzeige: als `link` erlaubt Meta dann nur den Platzhalter `https://fb.me/` (wird automatisch gesetzt; anderer `link` → `error=link_not_allowed_for_lead_ad`), das Adset muss auf `LEAD_GENERATION` mit `promoted_page_id` derselben Page laufen (`meta_create_adset`); `call_to_action` bei Lead-Anzeigen Default SIGN_UP (LEAD_GENERATION ist KEIN CTA-Typ) und nur APPLY_NOW/DOWNLOAD/GET_QUOTE/LEARN_MORE/SIGN_UP/SUBSCRIBE — andere Typen lehnt das Tool vorab ab (`error=invalid_lead_ad_cta`); lehnt Meta mit Subcode 1815089 ab, hat kein Page-Admin die Lead-Ads-Nutzungsbedingungen akzeptiert (Antwort enthält `hint`; Stand vorab in `meta_list_pages` → `leadgen_tos_accepted`); `url_tags` = UTM-Parameter als eigenes Creative-Feld, z.B. `utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}`; Zurücklesen: `meta_list_ads` zeigt `creative.lead_gen_form_id` und `url_tags` | meta_ads | W |

---

## LinkedIn Ads — Reporting (source: linkedin_ads)

Hierarchie: Campaign Group (≈ Meta-Kampagne) → Campaign (Budget + Targeting, ≈ Meta-Adset) → Creative (≈ Meta-Ad, referenziert einen Page-Post).

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `linkedin_list_accounts` | Verbundene LinkedIn-Ad-Accounts auflisten | linkedin_ads | R |
| `linkedin_list_campaign_groups` | Kampagnengruppen auflisten (Name, Status, Gesamtbudget) | linkedin_ads | R |
| `linkedin_list_campaigns` | Kampagnen auflisten (Name, Status, Typ, Tagesbudget) | linkedin_ads | R |
| `linkedin_list_creatives` | Creatives (Anzeigen) auflisten, optional pro Kampagne — Status + Post-URN | linkedin_ads | R |
| `linkedin_list_audiences` | Matched Audiences (DMP-Segmente): Retargeting- und Kontaktlisten | linkedin_ads | R |
| `linkedin_campaign_performance` | Kampagnen-Performance (Impressionen, Klicks, Kosten, `conversions` = Website-Conversions, `leads` = abgeschickte Lead-Gen-Formulare, `lead_form_opens` = geöffnete Formulare) — bei Lead-Gen-Kampagnen `leads` auswerten, nicht `conversions` | linkedin_ads | R |
| `linkedin_creative_performance` | Performance einzelner Anzeigen, sortiert nach Kosten — Felder wie `linkedin_campaign_performance` (`conversions` = Website-Conversions, `leads`/`lead_form_opens` = Lead-Gen-Formulare) | linkedin_ads | R |

---

## LinkedIn Ads — Mutation (source: linkedin_ads) ⚠ Guardrails

Alle LinkedIn-Schreib-Tools akzeptieren `validate_only=true` (Vorschau ohne API-Call).

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `linkedin_create_campaign_group` | Neue Kampagnengruppe anlegen (Standard: DRAFT) | linkedin_ads | W |
| `linkedin_update_campaign_group` | Kampagnengruppe ändern (Name, Status) | linkedin_ads | W |
| `linkedin_create_campaign` | Neue Kampagne anlegen (Standard: DRAFT) — Budget, Geo-/Sprach-Targeting, Auto-Bidding | linkedin_ads | W |
| `linkedin_update_campaign_status` | Kampagne aktivieren/pausieren/archivieren | linkedin_ads | W |
| `linkedin_update_campaign_budget` | Tagesbudget einer Kampagne ändern | linkedin_ads | W |
| `linkedin_create_ad_from_post` | Bestehenden Page-Post als Anzeige schalten (Sponsored Content) — Dark Posts gehen mangels `w_organization_social` nicht | linkedin_ads | W |
| `linkedin_update_creative_status` | Creative-Status ändern (ACTIVE/PAUSED/DRAFT/ARCHIVED) | linkedin_ads | W |

---

## Strapi CMS (source: strapi) — enthält W ⚠ Guardrails

`strapi_publish_entry`, `strapi_unpublish_entry` und `strapi_list_content_types` brauchen den **Admin Token** des Workspace (Strapi Settings → Administration Panel → Admin Tokens, ab Strapi 5.47) — NICHT den API-Token aus Settings → API Tokens, der wird auf Admin-Routen abgelehnt. `{error: admin_token_invalid}` = Token abgelehnt; `message` sagt, ob im Admin-Token-Feld ein Content-API-Token steckt oder der Token ungültig/abgelaufen ist — der Kunde trägt dann im Portal-Workspace unter Strapi (CMS) → Admin-Token einen Admin Token ein. Dynamic Zones (z.B. `content`) werden bei `strapi_create_entry`/`strapi_update_entry` als GANZES ersetzt — Rezept (mit `status='draft'` und Dict-Populate komplett lesen, ändern, komplett zurückgeben) bei `strapi_update_entry`.

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `strapi_list_entries` | Einträge einer Collection paginiert auflisten — `collection` = Plural-API-ID (z.B. `articles`); `filters` = Strapi-Filter-Dict wie in der Strapi-Doku, verschachtelt (z.B. `{"slug": {"$eq": "mein-artikel"}}`); `populate` lädt Relationen mit (`'*'` eine Ebene tief, `'cover'` gezielt, tief als Dict wie in der Strapi-Doku, z.B. `{"content": {"populate": "*"}}` — Details bei `strapi_get_entry`); `sort` z.B. `createdAt:desc`; `locale` = Sprachversion (v5-i18n, ohne Angabe Default-Locale); `status` filtert nach `'draft'` oder `'published'` — ohne `status` liefert v5 nur VERÖFFENTLICHTE Einträge, neu angelegte oder geänderte Drafts sind nur mit `status='draft'` sichtbar (`status` wirkt nur bei v5; bei v4 sind Drafts über dieses Tool nicht erreichbar) | strapi | R |
| `strapi_get_entry` | Einzelnen Strapi-Eintrag abrufen (`entry_id` v4 = numerische id, v5 = documentId; `locale` = Sprachversion) — `populate` lädt Relationen und Medien mit: `'*'` genau eine Ebene tief (Sektionen einer Dynamic Zone kommen mit, Medien und Repeatables INNERHALB der Sektionen fehlen), `'cover'` oder `'cover,seo'` gezielt; tiefes Populate als Dict wie in der Strapi-Doku, z.B. `populate={"content": {"populate": "*"}}` (entspricht `populate[content][populate]=*`) — lädt jede Sektion einer Dynamic Zone eine Ebene tief (Medien, Relationen und Repeatables direkt in der Sektion); für Medien innerhalb von Repeatables tiefer verschachteln, z.B. per on-Strategie je Komponente `populate={"content": {"on": {"sections.faq": {"populate": {"items": {"populate": "*"}}}}}}`; der fertige Query-String `populate[content][populate]=*` oder das Dict als JSON-String gehen ebenfalls. Vor dem Zurückschreiben per `strapi_update_entry` prüfen, dass alle Medien der Sektionen im GET enthalten sind. `status` (`'draft'`\|`'published'`, nur v5): ohne `status` liefert v5 die VERÖFFENTLICHTE Version (nie publizierter Draft → `{error: http_error, status: 404}`, geänderter Draft erscheint als unveränderte Live-Version) — Drafts nach create/update mit `status='draft'` zurücklesen | strapi | R |
| `strapi_list_media` | Dateien aus der Medienbibliothek auflisten — Rückgabe `{data, _meta: {total, page, page_size}}`, `data` standardmäßig kompakt (id, documentId, name, url, mime, size_kb, width, height); `full=true` liefert die vollständigen File-Objekte (formats, hash, ext, alternativeText … — nötig für Bild-Nodes in Blocks-Rich-Text), `ids=[…]` filtert auf Datei-IDs (z.B. `strapi_list_media(ids=[42], full=True)`); page/page_size und ids wirken auf die komplett geladene Mediathek, `_meta.total` zählt nach dem ids-Filter | strapi | R |
| `strapi_list_content_types` | Alle Content-Types auflisten (Schema-Discovery: uid, API-IDs, Anzeigename, Attribut-Schlüssel) — hierfür muss im Workspace der Admin Token hinterlegt sein (Strapi Settings → Administration Panel → Admin Tokens, ab Strapi 5.47 — nicht der API-Token aus Settings → API Tokens, der wird auf Admin-Routen abgelehnt); `{error: admin_token_invalid}` = Token abgelehnt, `message` sagt, ob im Admin-Token-Feld ein Content-API-Token steckt oder der Token ungültig/abgelaufen ist → Admin Token im Portal-Workspace unter Strapi (CMS) → Admin-Token eintragen | strapi | R |
| `strapi_create_entry` | Neuen Eintrag als DRAFT anlegen — danach NICHT öffentlich, live erst über `strapi_publish_entry` (separater, bewusster Schritt); `data` = Feldwerte; Media-Felder (z.B. cover) nehmen die Media-ID aus `strapi_upload_media` bzw. `strapi_check_upload_status`, Bild-Nodes in Blocks-Rich-Text das komplette File-Objekt (`strapi_upload_media(full=True)` bzw. `strapi_list_media(ids=[…], full=True)`, sonst 400 ValidationError); `locale` bei lokalisierten Content-Types immer explizit angeben (ohne `locale` legt Strapi den Eintrag stillschweigend in der Default-Locale an); Dynamic Zones (z.B. `content`): jede Sektion ist ein Objekt mit `__component` (z.B. `sections.hero`) plus ihren Feldern — das Tool sortiert `__component` automatisch an die erste Stelle jeder Sektion (Strapi lehnt sonst mit 400 `Invalid key __component` ab); Medien in Sektionen als `{"id": <Media-ID>}` oder als volles File-Objekt; den angelegten Draft zurücklesen mit `strapi_get_entry(..., status='draft')` — ohne `status` liefert v5 für einen unveröffentlichten Draft 404 | strapi | W |
| `strapi_update_entry` | Bestehenden Eintrag aktualisieren — v5: schreibt NUR den Draft, die veröffentlichte Version bleibt unverändert (live erst über `strapi_publish_entry`); v4: keine getrennte Draft-Kopie, ein Update eines bereits veröffentlichten Eintrags ändert die Live-Version sofort (vorher ggf. `strapi_unpublish_entry`); `entry_id` v4 = numerische id, v5 = documentId; `locale` bei lokalisierten Content-Types immer explizit (ohne `locale` trifft das Update stillschweigend die Default-Locale); Bild-Nodes in Blocks-Rich-Text brauchen das komplette File-Objekt (`strapi_upload_media(full=True)` / `strapi_list_media(ids=[…], full=True)`); **Dynamic Zones** (z.B. `content`): Strapi ersetzt das Feld als GANZES, ein Mergen einzelner Sektionen gibt es nicht — deshalb vorher mit `strapi_get_entry(collection, entry_id, status='draft', populate={"content": {"populate": "*"}})` komplett lesen (tiefes Populate — `populate='*'` lädt nur eine Ebene, Medien und Repeatables INNERHALB der Sektionen fehlen dann im gelesenen Stand; nur vollständig gelesene Sektionen lassen sich verlustfrei zurückschreiben), die Sektionen ändern und das komplette Array zurückgeben; Komponenten-ids, documentId/Timestamps und volle Media-Objekte aus dem GET können unverändert mitgeschickt werden (Medien auch als `{"id": …}`); das Tool sortiert `__component` automatisch an die erste Stelle jeder Sektion (Strapi lehnt sonst mit 400 `Invalid key __component` ab); Kontrolle des Drafts: `strapi_get_entry(collection, entry_id, status='draft')` — ohne `status` zeigt v5 die alte Live-Version | strapi | W |
| `strapi_delete_entry` | Eintrag löschen — `locale` wählt die Sprachversion (v5-i18n), `'*'` löscht ALLE Sprachversionen; ohne `locale` löscht v5 nur die Default-Locale-Version (andere bleiben, auch live — Antwort enthält `hint`); Rückgabe bestätigt nur den Aufruf, Ergebnis mit `strapi_list_entries(locale=…)` prüfen | strapi | W |
| `strapi_publish_entry` | Eintrag veröffentlichen — v5 (Standard): content-manager publish-Action, braucht den Admin Token des Workspace (Strapi Settings → Administration Panel → Admin Tokens, ab Strapi 5.47; NICHT den API-Token aus Settings → API Tokens, der wird auf Admin-Routen abgelehnt); `{error: admin_token_invalid}` = Token abgelehnt — `message` sagt, ob im Admin-Token-Feld ein Content-API-Token steckt oder der Token ungültig/abgelaufen ist; der Kunde trägt dann im Portal-Workspace unter Strapi (CMS) → Admin-Token einen Admin Token ein; v4: setzt publishedAt auf jetzt; `locale` wählt die zu veröffentlichende Sprachversion (ohne Angabe Default-Locale) | strapi | W |
| `strapi_unpublish_entry` | Eintrag depublizieren (aus der öffentlichen API nehmen) — v5 (Standard): content-manager unpublish-Action, braucht den Admin Token des Workspace (wie `strapi_publish_entry`: Admin Tokens ab Strapi 5.47, NICHT der API-Token); `{error: admin_token_invalid}` = Token abgelehnt, `message` sagt, ob ein Content-API-Token statt Admin Token hinterlegt ist oder der Token ungültig/abgelaufen ist; v4: setzt publishedAt auf null; `locale` wählt die zu depublizierende Sprachversion (ohne Angabe Default-Locale) | strapi | W |
| `strapi_upload_media` | Datei in die Medienbibliothek hochladen (`source_url`, max. 25 MB, ODER `file_base64`) — liefert `{success, uploaded: [{id, name, url, mime, size_kb}]}`; `full=true` liefert das komplette File-Objekt (width, height, formats, hash, ext, documentId …) direkt in `uploaded` — nötig für Bild-Nodes in Blocks-Rich-Text, für Media-Felder (z.B. cover) reicht die id | strapi | W |
| `strapi_delete_media` | Datei aus der Medienbibliothek löschen | strapi | W |

---

## WordPress CMS (source: wordpress) — enthält W ⚠ Guardrails

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `wp_list_posts` | Beiträge oder Seiten auflisten (post_type, Volltext, Status, paginiert) | wordpress | R |
| `wp_get_post` | Einzelnen Beitrag/Seite/Site-Editor-Vorlage mit vollem Inhalt abrufen | wordpress | R |
| `wp_list_media` | Dateien aus der Medienbibliothek auflisten (paginiert) | wordpress | R |
| `wp_list_terms` | Kategorien oder Tags auflisten (id, name, slug, count) — IDs für `wp_create_post` | wordpress | R |
| `wp_create_post` | Beitrag/Seite anlegen — status default `draft`; `publish` = sofort live; `future` (terminiert) braucht `date` (ISO 8601 ohne Zeitzonen-Suffix in der Site-Zeitzone, z.B. `2026-10-01T09:00:00`) — ohne `date` kommt `{error: date_required}` zurück, bevor etwas angelegt wird | wordpress | W |
| `wp_update_post` | Beitrag/Seite/Vorlage aktualisieren (nur gesetzte Felder); `status=publish` = live | wordpress | W |
| `wp_delete_post` | Beitrag/Seite löschen — `force=False` → Papierkorb, `force=True` → endgültig | wordpress | W |
| `wp_upload_media` | Datei in die Medienbibliothek hochladen (`source_url` ODER `file_base64`) | wordpress | W |
| `wp_delete_media` | Datei aus der Medienbibliothek löschen (`force=True` Default → endgültig) | wordpress | W |
| `wp_create_term` | Kategorie/Tag anlegen — idempotent (existierender Name → vorhandener Term, kein Duplikat) | wordpress | W |

### WordPress Honeyfield-Connector (Builder + SEO — braucht das Connector-Plugin auf der Kundenseite)

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `wp_bridge_status` | Connector-Verbindung prüfen: Plugin-Version, erkannte Builder (Elementor/Bricks), SEO-Plugin, Module | wordpress | R |
| `wp_builder_get_content` | Page-Builder-Inhalt als Text-Baum lesen (`element_id` + `field` je Textfeld) — für Seiten, bei denen `wp_get_post` leer bleibt | wordpress | R |
| `wp_builder_replace_text` | Texte in Builder-Elementen gezielt ändern (Feld setzen oder Teilstring) — Layout bleibt unangetastet, Bricks-Code-Elemente tabu | wordpress | W |
| `wp_seo_get_meta` | SEO-Metadaten (Yoast/Rank Math) lesen: Title, Description, Canonical, noindex | wordpress | R |
| `wp_seo_update_meta` | SEO-Metadaten schreiben (nur übergebene Felder) | wordpress | W |
