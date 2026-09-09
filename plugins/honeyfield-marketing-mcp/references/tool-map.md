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

## Diagnostik (source: google_ads)

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `budget_pacing` | Budget-Pacing laufender Monat: Ausgaben vs. Projektion pro Kampagne | google_ads | R |
| `anomaly_check` | Anomalie-Check: Kostenspitzen, Conversion-Ausfälle, CTR-Einbrüche | google_ads | R |

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
| `meta_list_pages` | Facebook-Pages, die der Account bewerben darf — `page_id` ist Pflicht für `meta_create_ad`; je Page `leadgen_tos_accepted` (`true` = ein Page-Admin hat die Lead-Ads-Nutzungsbedingungen akzeptiert — Voraussetzung für jede Lead-Anzeige; `false` = noch nicht, ein Admin muss sie unter facebook.com/ads/leadgen/tos für genau diese Page annehmen, per API nicht möglich; `null` = nicht lesbar: Scope `pages_show_list` fehlt oder die Page ist nur über das Werbekonto sichtbar) + `leadgen_tos_acceptance_time` | meta_ads | R |
| `meta_list_lead_forms` | Lead-Formulare (Instant Forms) je Facebook-Page — Name, ID, Status, `leads_count`; beantwortet „wie heißt Formular X?” ohne Raten (Meta führt die Formulare an der Page, nicht am Werbekonto). Braucht die Scopes `pages_show_list` + `leads_retrieval` — fehlen sie, kommt `{error, code, hint}` zurück (Meta-Verbindung mit diesen Scopes neu herstellen); `page_id` optional: bei mehreren Pages `error=page_id_required` mit Auswahl, unbekannte `page_id` → `error=page_not_found` mit `available_pages`; `limit` (Default 100) — nur die erste Seite, weitere Formulare werden ohne Hinweis abgeschnitten | meta_ads | R |
| `meta_list_pixels` | Meta-Pixel (Datasets) auflisten inkl. „zuletzt gefeuert” — schnellster Tracking-Check | meta_ads | R |
| `meta_pixel_stats` | Pixel-Event-Statistiken der letzten N Tage (Summen + Tagesverlauf) | meta_ads | R |
| `meta_campaign_performance` | Kampagnen-Performance (Impressionen, Klicks, Spend, Conversions); bei leeren Insights trotz Kampagnen: `{"result": [], "info": "<Erklärung>"}` | meta_ads | R |
| `meta_adset_performance` | Adset-Performance der letzten N Tage, sortiert nach Spend; bei leeren Insights trotz Kampagnen: `{"result": [], "info": "<Erklärung>"}` | meta_ads | R |
| `meta_ad_performance` | Performance einzelner Anzeigen der letzten N Tage, sortiert nach Spend; bei leeren Insights trotz Kampagnen: `{"result": [], "info": "<Erklärung>"}` | meta_ads | R |
| `meta_list_campaigns` | Kampagnen auflisten (Status, Ziel, `daily_budget_eur`/`lifetime_budget_eur` — CBO = eines davon gesetzt, nicht-leere `issues`); `start_time`/`stop_time` leitet Meta aus den Adsets ab (`null` ohne Adset-Enddatum) — ein Kampagnen-Enddatum gibt es nicht, `end_time` wird je Adset gesetzt; `limit` (Default 50) — wird abgeschnitten (Meta meldet weitere Seiten), kommt `{result, warning}` statt der Liste, dann `limit` erhöhen | meta_ads | R |
| `meta_list_adsets` | Adsets auflisten, optional pro Kampagne (Status, Budget in EUR inkl. `lifetime_budget_eur`, `billing_event`, Optimierungsziel, Targeting, `start_time`/`end_time` = Zeitplan, `promoted_object` (z.B. `{page_id}` bei Lead-Adsets, `{pixel_id, custom_event_type}` bei Conversion-Adsets) und `destination_type` so, wie Meta sie führt (`None` = nicht gesetzt) — zum Zurücklesen nach `meta_create_adset`/`meta_update_adset` (Meta braucht nach dem Schreiben ein paar Sekunden, bis der neue Stand sichtbar ist), nicht-leere `issues`; DSA-Felder immer, `null` = fehlt; `eu_eea_targeting` mit EU-/EWR-Treffern der erfassten Geo-Formen, `[]` = keiner, `UNKNOWN` = nicht auswertbar); `limit` (Default 50) — wird abgeschnitten, kommt `{result, warning}` statt der Liste, dann `campaign_id` einschränken oder `limit` erhöhen | meta_ads | R |
| `meta_list_ads` | Ads auflisten, optional pro Adset (Status, Creative inkl. `creative.link_url` = Zielseite und `creative.url_tags` = UTM-Parameter, nicht-leere `issues`, vorhandenes `review_feedback`); Lead-Anzeigen (Instant Form) tragen `creative.lead_gen_form_id` (Formular via `meta_list_lead_forms` auflösbar; `link_url` ist dort Metas Platzhalter `https://fb.me/`) — fehlt das Feld, nutzt die Anzeige kein Instant Form; `name_contains` filtert serverseitig, `status` filtert den KONFIGURIERTEN Status schon beim Laden (blättert weiter, bis `limit` passende Anzeigen vorliegen, höchstens 20 Seiten à 100 — vorzeitiger Abbruch steht in `warning`); `limit` (Default 50) — wird abgeschnitten, kommt `{result, warning}` statt der Liste | meta_ads | R |
| `meta_list_audiences` | Custom Audiences inkl. Customer-Match-Listen (IDs für Adset-Targeting) | meta_ads | R |
| `meta_video_status` | Verarbeitungsstatus eines hochgeladenen Ad-Videos (`ready` = nutzbar) | meta_ads | R |

---

## Meta Ads — Mutation (source: meta_ads) ⚠ Guardrails

Alle Meta-Schreib-Tools akzeptieren `validate_only=true` (echter API-Dry-Run; `meta_create_ad` simuliert lokal als `would_create`-Vorschau).

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `meta_create_pixel` | Neues Pixel (Dataset) anlegen — liefert Pixel-ID + Einbau-Code | meta_ads | W |
| `meta_create_campaign` | Neue Kampagne anlegen (Standard: PAUSED) — `daily_budget` ODER `lifetime_budget` in EUR gesetzt = CBO, nie beides (`error=budget_conflict`); `lifetime_budget` = Gesamtsumme bis zum Enddatum, und das Enddatum liegt bei Meta an den Adsets: jedes Adset dieser Kampagne braucht `end_time` (`meta_create_adset` lehnt sonst mit `error=end_time_required` ab) — ein Kampagnen-Enddatum gibt es nicht, Meta leitet Start/Ende aus den Adsets ab; `bid_strategy` NUR zusammen mit einem Kampagnenbudget (CBO), sonst bricht das Tool mit `error=bid_strategy_requires_budget` ab (nichts wird angelegt) — dann Budget mitgeben oder die Strategie je Adset in `meta_create_adset` setzen | meta_ads | W |
| `meta_update_campaign` | Kampagne ändern: Name, Status, `daily_budget` ODER `lifetime_budget` in EUR (nie beides → `error=budget_conflict`; nur bei CBO, sonst `error=budget_not_on_campaign` → Budget je Adset via `meta_update_adset`); ein Wechsel Tages↔Laufzeitbudget ist bei Meta nicht erlaubt (Meta lehnt ab, nichts wird geändert) → neues Adset bzw. neue Kampagne anlegen; kein Kampagnen-Enddatum — Meta leitet Start/Ende aus den Adsets ab, `end_time` je Adset via `meta_update_adset` | meta_ads | W |
| `meta_delete_campaign` | Kampagne endgültig löschen inkl. Adsets/Ads — zum Stoppen besser Status PAUSED/ARCHIVED | meta_ads | W |
| `meta_create_adset` | Neues Adset anlegen (Standard: PAUSED) — Budget: `daily_budget` ODER `lifetime_budget` in EUR, genau eines (`error=budget_conflict` bei beiden; ohne CBO Pflicht → `error=budget_required`, bei CBO-Kampagne wird das Adset-Budget ignoriert); `lifetime_budget` = Gesamtsumme bis `end_time` und braucht `end_time` (`error=end_time_required`) — ebenso jedes Adset in einer Kampagne mit Laufzeitbudget; + Zielgruppe, Bidding, DSA-Angaben (EU-Pflicht), `advantage_audience`; `promoted_object`: `promoted_page_id` (Page, deren Instant Forms beworben werden — Pflicht bei `optimization_goal=LEAD_GENERATION`, sonst `error=promoted_page_required`; ID aus `meta_list_pages`) bzw. `pixel_id` + `custom_event_type` immer zusammen (Pflicht bei `OFFSITE_CONVERSIONS`, sonst `error=pixel_event_required`; Pixel aus `meta_list_pixels`, Ereignis laut Meta-Enum z.B. LEAD/PURCHASE/COMPLETE_REGISTRATION/CONTACT/SUBMIT_APPLICATION/SUBSCRIBE/ADD_TO_CART/INITIATED_CHECKOUT, sonst `error=invalid_custom_event_type`); `destination_type` laut Meta-Enum (WEBSITE, ON_AD = Instant Form direkt in der Anzeige, MESSENGER, WHATSAPP, INSTAGRAM_DIRECT, APP, FACEBOOK_PAGE; sonst `error=invalid_destination_type`); **Lead-Adset (Instant Form):** `optimization_goal='LEAD_GENERATION'` + `promoted_page_id` + `destination_type='ON_AD'`, Anzeige danach mit `meta_create_ad(lead_gen_form_id=…)` — Voraussetzung: `meta_list_pages` → `leadgen_tos_accepted`, sonst lehnt Meta die Anzeige ab; Zeitplan `start_time`/`end_time` (`end_time` = Traffic-Enddatum, danach pausiert Meta die Auslieferung; je als Datum `2026-09-30` (= Tagesende) oder ISO-Zeitstempel, ohne Offset wird die Zeitzone des Werbekontos angehängt — Meta würde sonst UTC annehmen); Budget/Zeitplan/`promoted_object`/`destination_type` mit `meta_list_adsets` zurücklesen; nicht-blockierende DSA-Warnung für alle Geo-Einträge mit Ländercode und `country_groups` `europe`/`eea`/`worldwide` | meta_ads | W |
| `meta_update_adset` | Adset ändern: Name, Status, `daily_budget` ODER `lifetime_budget` in EUR (nie beides → `error=budget_conflict`; `lifetime_budget` braucht `end_time` — mitgegeben oder schon am Adset gesetzt, sonst `error=end_time_required`; ein Wechsel Tages↔Laufzeitbudget ist bei Meta eingeschränkt — lehnt Meta ab, kommt der Fehler durch), Bidding, DSA-Angaben (EU-Pflicht), `advantage_audience`, `promoted_object` (`promoted_page_id` bzw. `pixel_id` + `custom_event_type` immer zusammen, sonst `error=pixel_event_required`; unbekanntes Ereignis `error=invalid_custom_event_type`; nur Übergebenes wird gesendet — ob Meta das `promoted_object` eines bestehenden Adsets ändern lässt, hängt vom Optimierungsziel ab, eine Ablehnung kommt durch), `destination_type` (Meta-Enum, sonst `error=invalid_destination_type`), Zeitplan `start_time`/`end_time` (`end_time` = Traffic-Enddatum; Datum `2026-09-30` (= Tagesende) oder ISO-Zeitstempel, ohne Offset wird die Zeitzone des Werbekontos angehängt — Meta würde sonst UTC annehmen), Targeting (wird gemerged); alles mit `meta_list_adsets` zurücklesen — Meta braucht nach dem Schreiben ein paar Sekunden, bis der neue Stand sichtbar ist; `bid_amount` OHNE `bid_strategy` liest die bestehende Strategie des Adsets und behält sie bei (COST_CAP bleibt COST_CAP; nur LOWEST_COST_WITHOUT_CAP wechselt auf LOWEST_COST_WITH_BID_CAP), die Antwort nennt in `bid_strategy`, was gesendet wurde (bei CBO-Adsets ohne eigene Strategie fehlt das Feld) — ist die Strategie nicht lesbar, bricht das Tool ohne Änderung ab; gleiche DSA-Coverage, bei `status=ACTIVE` zusätzlicher Best-effort-Advisory-Check (Ausfall → `dsa_check: "unavailable"` + Warnung) | meta_ads | W |
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

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `strapi_list_entries` | Einträge einer Collection paginiert auflisten | strapi | R |
| `strapi_get_entry` | Einzelnen Strapi-Eintrag abrufen — `status` (`'draft'`\|`'published'`, nur v5): ohne `status` liefert v5 die VERÖFFENTLICHTE Version (nie publizierter Draft → `{error: http_error, status: 404}`, geänderter Draft erscheint als unveränderte Live-Version) — Drafts nach create/update mit `status='draft'` zurücklesen | strapi | R |
| `strapi_list_media` | Dateien aus der Medienbibliothek auflisten — Rückgabe `{data, _meta: {total, page, page_size}}`, `data` standardmäßig kompakt (id, documentId, name, url, mime, size_kb, width, height); `full=true` liefert die vollständigen File-Objekte (formats, hash, ext, alternativeText … — nötig für Bild-Nodes in Blocks-Rich-Text), `ids=[…]` filtert auf Datei-IDs (z.B. `strapi_list_media(ids=[42], full=True)`); page/page_size und ids wirken auf die komplett geladene Mediathek, `_meta.total` zählt nach dem ids-Filter | strapi | R |
| `strapi_list_content_types` | Alle Content-Types auflisten (Schema-Discovery) | strapi | R |
| `strapi_create_entry` | Neuen Eintrag als Draft anlegen (Draft-first; live erst via publish) | strapi | W |
| `strapi_update_entry` | Bestehenden Eintrag aktualisieren — trifft nur den Draft, Live-Version bleibt | strapi | W |
| `strapi_delete_entry` | Eintrag löschen — `locale` wählt die Sprachversion (v5-i18n), `'*'` löscht ALLE Sprachversionen; ohne `locale` löscht v5 nur die Default-Locale-Version (andere bleiben, auch live — Antwort enthält `hint`); Rückgabe bestätigt nur den Aufruf, Ergebnis mit `strapi_list_entries(locale=…)` prüfen | strapi | W |
| `strapi_publish_entry` | Eintrag veröffentlichen (v5: Content-Manager, braucht Admin-Token mit Publish-Recht; v4: setzt publishedAt) | strapi | W |
| `strapi_unpublish_entry` | Eintrag depublizieren (v5: Content-Manager, braucht Admin-Token; v4: publishedAt=null) | strapi | W |
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
