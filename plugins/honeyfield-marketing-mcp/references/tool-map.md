# Tool-Map — Honeyfield Marketing-Ops MCP

Alle Tools außer `list_workspaces`, `ping`, `authenticate` und `complete_authentication` nehmen `workspace` (optional, wenn nur ein Workspace verbunden ist; bei gleichem Slug in mehreren Agenturen die Form `Agentur/slug` nutzen). Quelle = welche Workspace-source verbunden sein muss.
Lege Schreib-Tools (W) nie ohne write-guardrails.md an.

---

## Foundation

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `list_workspaces` | Workspaces + verbundene sources auflisten | — | R |
| `ping` | Connectivity-Check (liefert „pong") | — | R |
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
| `ads_list_conversion_actions` | Conversion-Aktionen mit Status, Typ, Counts — deckt totes Tracking auf | google_ads | R |
| `ads_conversion_performance` | Conversion-Performance pro Aktion + Tagesverlauf | google_ads | R |
| `ads_list_campaigns` | Alle Kampagnen (Name, Status, Budget, Channel Type, Bidding Strategy) | google_ads | R |
| `ads_list_ad_groups` | Ad Groups auflisten, optional nach Kampagne gefiltert | google_ads | R |
| `ads_list_keywords` | Keywords auflisten, optional nach Kampagne oder Ad Group gefiltert | google_ads | R |
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
| `ads_update_conversion_action` | Bestehende Conversion-Aktion ändern (Name, Status, primary_for_goal) | google_ads | W |
| `ads_create_campaign` | Neue Kampagne anlegen (Standard: PAUSED) | google_ads | W |
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
| `ga4_list_key_events` | Konfigurierte Key Events + Counts — feuern sie wirklich? | ga4 | R |
| `ga4_list_properties` | Alle GA4 Properties der verbundenen Google-Verbindung | ga4 | R |
| `ga4_list_data_streams` | Datenströme (Web/App) einer Property auflisten inkl. Measurement-ID | ga4 | R |
| `ga4_list_custom_dimensions` | Custom Dimensions einer Property auflisten | ga4 | R |
| `ga4_list_custom_metrics` | Custom Metrics einer Property auflisten | ga4 | R |

---

## GA4 — Mutation (source: ga4) ⚠ Guardrails

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `ga4_create_property` | Neue GA4 Property in einem Analytics-Account anlegen | ga4 | W |
| `ga4_create_data_stream` | Web-Datenstream für eine Property anlegen (liefert Measurement-ID) | ga4 | W |
| `ga4_update_property` | Property-Stammdaten ändern (Name, Zeitzone, Währung) | ga4 | W |
| `ga4_create_key_event` | GA4 Key Event (Conversion) anlegen | ga4 | W |
| `ga4_create_custom_dimension` | GA4 Custom Dimension anlegen (EVENT / USER / ITEM) | ga4 | W |
| `ga4_archive_custom_dimension` | GA4 Custom Dimension archivieren | ga4 | W |
| `ga4_create_custom_metric` | GA4 Custom Metric anlegen | ga4 | W |
| `ga4_archive_custom_metric` | GA4 Custom Metric archivieren | ga4 | W |
| `ga4_delete_key_event` | GA4 Key Event löschen | ga4 | W |
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
| `sc_url_inspection` | Indexierungsstatus, Canonical, Mobile Usability einer URL | search_console | R |
| `sc_list_sitemaps` | Eingereichte Sitemaps: Status, Warn- und Fehlerzahlen | search_console | R |
| `sc_submit_sitemap` | Sitemap-URL bei GSC einreichen | search_console | W |
| `sc_delete_sitemap` | Sitemap-URL aus GSC entfernen | search_console | W |

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

---

## DataForSEO (source: dataforseo)

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
| `dfs_onpage_instant` | Live On-Page Audit (Title, Meta, H1, Score, Issues) | dataforseo | R |
| `dfs_lighthouse_live` | Google Lighthouse Audit (Performance, Accessibility, SEO) | dataforseo | R |
| `dfs_keyword_overview` | Volumen, CPC, Difficulty und Haupt-Intent für eine Keyword-Liste in einem Call (max 700) | dataforseo | R |
| `dfs_domain_intersection` | Ranking-Schnittmenge zweier Domains — oder Gap-Modus: wofür Domain 2 rankt, Domain 1 nicht | dataforseo | R |
| `dfs_competitors_domain` | Domains mit den meisten gemeinsamen Rankings — echte SEO-Konkurrenten statt Branchen-Raten | dataforseo | R |
| `dfs_keyword_suggestions` | Keyword-Vorschläge zu einem Seed-Keyword inkl. Volumen, CPC, Difficulty | dataforseo | R |
| `dfs_backlinks_list` | Konkrete Backlink-Liste einer Domain, filterbar nach broken/dofollow/lost | dataforseo | R |
| `dfs_llm_mentions` | Marken-/Themen-Erwähnungen in LLM-Antworten je Keyword (~$0.10/Call) | dataforseo | R |
| `dfs_llm_mentions_metrics` | Aggregierte Mentions pro Engine, Gesamt-Citations + Share-of-Voice über LLM-Engines (~$0.10/Call) | dataforseo | R |
| `dfs_llm_top_domains` | Meistzitierte Domains in LLM-Antworten zu einer Keyword-Liste (~$0.10/Call) | dataforseo | R |
| `dfs_llm_responses` | Rohe LLM-Antwort + Zitate zu einem Prompt (ChatGPT/Claude/Gemini/Perplexity, ~$0.10/Call) | dataforseo | R |
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

## Google Business Profile (source: business_profile) — enthält W ⚠ Guardrails

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `gbp_list_locations` | Alle Standorte des verbundenen Google-Kontos | business_profile | R |
| `gbp_location_info` | Stammdaten des Standorts (Name, Adresse, Telefon, Kategorie, Öffnungszeiten) | business_profile | R |
| `gbp_get_profile` | Vollständiges Business-Profil inkl. Attribute und Sonderöffnungszeiten | business_profile | R |
| `gbp_performance` | Impressionen (Maps/Suche), Anrufe, Website-Klicks, Routenanfragen | business_profile | R |
| `gbp_search_keywords` | Suchbegriffe, über die Nutzer das Profil gefunden haben | business_profile | R |
| `gbp_reviews` | Rezensionen: Durchschnittswertung + neueste Bewertungen inkl. Antworten | business_profile | R |
| `gbp_reply_review` | Auf eine Rezension antworten (erstellt oder ersetzt bestehende Antwort) | business_profile | W |
| `gbp_get_review_link` | Direkten Bewertungs-Link (Kurz-URL) für einen Standort abrufen | business_profile | R |
| `gbp_local_rank` | Lokales Grid-Ranking für Keywords rund um den Standort (Local-Pack-Position) | business_profile | R |
| `gbp_local_seo_audit` | Lokaler SEO-Check des Profils (Vollständigkeit, Kategorien, NAP-Konsistenz) | business_profile | R |
| `gbp_manage_categories` | Primär- und Zusatzkategorien des Standorts lesen/setzen | business_profile | R/W |
| `gbp_manage_hours` | Reguläre + Sonderöffnungszeiten lesen/setzen | business_profile | R/W |
| `gbp_update_attributes` | Profil-Attribute setzen (z.B. Service-Optionen, Barrierefreiheit, Zahlungsarten) | business_profile | W |
| `gbp_update_profile` | Profildaten aktualisieren (Beschreibung, Website, Telefon) | business_profile | W |

---

## Meta Ads — Reporting (source: meta_ads)

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `meta_list_ad_accounts` | Erreichbare Meta-Ad-Accounts auflisten (id, Name, Status, Währung) | meta_ads | R |
| `meta_list_pages` | Facebook-Pages, die der Account bewerben darf — `page_id` ist Pflicht für `meta_create_ad` | meta_ads | R |
| `meta_list_pixels` | Meta-Pixel (Datasets) auflisten inkl. „zuletzt gefeuert" — schnellster Tracking-Check | meta_ads | R |
| `meta_pixel_stats` | Pixel-Event-Statistiken der letzten N Tage (Summen + Tagesverlauf) | meta_ads | R |
| `meta_campaign_performance` | Kampagnen-Performance (Impressionen, Klicks, Spend, Conversions) | meta_ads | R |
| `meta_adset_performance` | Adset-Performance der letzten N Tage, sortiert nach Spend | meta_ads | R |
| `meta_ad_performance` | Performance einzelner Anzeigen der letzten N Tage, sortiert nach Spend | meta_ads | R |
| `meta_list_campaigns` | Kampagnen auflisten (Status, Ziel, Budgets in EUR) | meta_ads | R |
| `meta_list_adsets` | Adsets auflisten, optional pro Kampagne (Status, Budget, Optimierungsziel, Targeting) | meta_ads | R |
| `meta_list_ads` | Ads auflisten, optional pro Adset (Status + Creative) | meta_ads | R |
| `meta_list_audiences` | Custom Audiences inkl. Customer-Match-Listen (IDs für Adset-Targeting) | meta_ads | R |
| `meta_video_status` | Verarbeitungsstatus eines hochgeladenen Ad-Videos (`ready` = nutzbar) | meta_ads | R |

---

## Meta Ads — Mutation (source: meta_ads) ⚠ Guardrails

Alle Meta-Schreib-Tools akzeptieren `validate_only=true` (echter API-Dry-Run; `meta_create_ad` simuliert lokal als `would_create`-Vorschau).

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `meta_create_pixel` | Neues Pixel (Dataset) anlegen — liefert Pixel-ID + Einbau-Code | meta_ads | W |
| `meta_create_campaign` | Neue Kampagne anlegen (Standard: PAUSED) — `daily_budget` gesetzt = CBO, optional `bid_strategy` | meta_ads | W |
| `meta_update_campaign` | Kampagne ändern: Name, Status, Tagesbudget in EUR (Budget nur bei CBO) | meta_ads | W |
| `meta_delete_campaign` | Kampagne endgültig löschen inkl. Adsets/Ads — zum Stoppen besser Status PAUSED/ARCHIVED | meta_ads | W |
| `meta_create_adset` | Neues Adset anlegen (Standard: PAUSED) — Budget (erkennt CBO selbst) + Zielgruppe, Bidding, DSA-Angaben (EU-Pflicht), `advantage_audience` | meta_ads | W |
| `meta_update_adset` | Adset ändern: Name, Status, Budget, Bidding, DSA-Angaben (EU-Pflicht), `advantage_audience`, Targeting (wird gemerged) | meta_ads | W |
| `meta_update_ad_status` | Ad-Status ändern (ACTIVE/PAUSED/ARCHIVED/DELETED) | meta_ads | W |
| `meta_upload_ad_image` | Bild von öffentlicher URL in die Bildbibliothek laden (max. 8 MB) — liefert `image_hash` | meta_ads | W |
| `meta_upload_ad_video` | Video von öffentlicher URL laden — asynchron, Status via `meta_video_status` | meta_ads | W |
| `meta_create_ad` | Neue Ad anlegen (Bild ODER Video) — Creative + Ad in einem Schritt (Standard: PAUSED) | meta_ads | W |

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
| `linkedin_campaign_performance` | Kampagnen-Performance (Impressionen, Klicks, Kosten, Conversions) | linkedin_ads | R |
| `linkedin_creative_performance` | Performance einzelner Anzeigen, sortiert nach Kosten | linkedin_ads | R |

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
| `strapi_get_entry` | Einzelnen Strapi-Eintrag abrufen | strapi | R |
| `strapi_list_media` | Dateien aus der Medienbibliothek auflisten | strapi | R |
| `strapi_list_content_types` | Alle Content-Types auflisten (Schema-Discovery) | strapi | R |
| `strapi_create_entry` | Neuen Eintrag in einer Collection anlegen | strapi | W |
| `strapi_update_entry` | Bestehenden Eintrag aktualisieren | strapi | W |
| `strapi_delete_entry` | Eintrag löschen | strapi | W |
| `strapi_publish_entry` | Eintrag veröffentlichen (setzt publishedAt auf jetzt) | strapi | W |
| `strapi_unpublish_entry` | Eintrag depublizieren (setzt publishedAt auf null) | strapi | W |
| `strapi_upload_media` | Datei in die Medienbibliothek hochladen | strapi | W |
| `strapi_delete_media` | Datei aus der Medienbibliothek löschen | strapi | W |

---

## WordPress CMS (source: wordpress) — enthält W ⚠ Guardrails

| Tool | Was | Quelle | R/W |
|---|---|---|---|
| `wp_list_posts` | Beiträge oder Seiten auflisten (post_type, Volltext, Status, paginiert) | wordpress | R |
| `wp_get_post` | Einzelnen Beitrag/Seite/Site-Editor-Vorlage mit vollem Inhalt abrufen | wordpress | R |
| `wp_list_media` | Dateien aus der Medienbibliothek auflisten (paginiert) | wordpress | R |
| `wp_list_terms` | Kategorien oder Tags auflisten (id, name, slug, count) — IDs für `wp_create_post` | wordpress | R |
| `wp_create_post` | Beitrag/Seite anlegen — status default `draft`; `publish` = sofort live | wordpress | W |
| `wp_update_post` | Beitrag/Seite/Vorlage aktualisieren (nur gesetzte Felder); `status=publish` = live | wordpress | W |
| `wp_delete_post` | Beitrag/Seite löschen — `force=False` → Papierkorb, `force=True` → endgültig | wordpress | W |
| `wp_upload_media` | Datei in die Medienbibliothek hochladen (`source_url` ODER `file_base64`) | wordpress | W |
| `wp_delete_media` | Datei aus der Medienbibliothek löschen (`force=True` Default → endgültig) | wordpress | W |
| `wp_create_term` | Kategorie/Tag anlegen — idempotent (existierender Name → vorhandener Term, kein Duplikat) | wordpress | W |
