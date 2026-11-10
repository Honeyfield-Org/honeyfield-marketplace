# Schreib-Guardrails

Grundregel: **read before write.** Erst den Ist-Zustand lesen (passendes R-Tool),
dann den exakten Diff zeigen, dann erst — nach expliziter Bestätigung — mutieren.

## Preview-Format (vor JEDER Mutation zeigen)

> Aktion: `<tool>` · Workspace: `<ws>`
> Entität: <name/id> · Feld: <feld> · **alt → neu**
> Wirkung/Reichweite: <1 Satz> · Reversibel: ja/nein

## Hochrisiko / irreversibel — EINZELN bestätigen (nie gebündelt)

**Löschen / Entfernen**

- `ads_remove_campaign`, `ads_remove_ad_group`, `ads_remove_ad`, `ads_remove_keyword`
- `ads_replace_ad` / `ads_update_ad` — Default `keep_old=False` entfernt die alte Anzeige irreversibel; bevorzugt `keep_old=True` setzen (alte Ad wird nur pausiert)
- `ads_remove_negative_keyword`, `ga4_delete_key_event`
- `ga4_archive_custom_dimension`, `ga4_archive_custom_metric`
- `ga4_data_retention` im Setz-Modus (Verkürzung 14→2 Monate = älterer Event-Datenzugriff geht unwiederbringlich verloren)
- `gtm_remove_tag`, `sc_delete_sitemap`, `strapi_delete_entry`, `strapi_delete_media`
- `wp_delete_post`, `wp_delete_media` (`force=True` → endgültig statt Papierkorb)
- `ads_unlink_asset` (löst dauerhaft — reversibel stattdessen `ads_set_asset_link_status` mit `PAUSED`), `ads_set_asset_link_status` mit `REMOVED`
- `ads_manage_account_negatives` mit `remove_criterion_ids` — löst die **ganze** kontoweite Liste vom Konto
- `bing_remove_sitemap`, `lemlist_delete_sequence_step`, `meta_archive_lead_form` (Löschen gibt es bei Meta nicht; Korrektur = archivieren + neu anlegen)

**Budget / Status / Bidding**

- `ads_update_campaign_budget`, `ads_update_campaign_status` (pause/enable)
- `linkedin_update_campaign_budget`, `linkedin_update_campaign_status`
- `ads_update_campaign_bidding_strategy`, `ads_set_campaign_conversion_goals` (ändert, worauf Smart Bidding optimiert)
- `linkedin_update_campaign_bid`
- `openai_ads_set_status` mit `active` (startet echte Auslieferung mit Kosten), `openai_ads_update_campaign` (Budget)
- `workspace_create` mit `confirm=true` — kann die Rechnung erhöhen; erst `confirm=false` und Abrechnung vorher/nachher zeigen

**Conversions / Customer-Match (Daten-Upload / PII)**

- `ads_upload_conversions`, `ads_upload_customer_match_members`, `ads_remove_customer_match_members`
- `openai_ads_upload_conversions` (erst `validate_only=true`)
- `lemlist_add_leads` — Personendaten; nur Leads mit Rechtsgrundlage; in laufenden Kampagnen (`allow_running_campaign=True`) versendet lemlist sofort

**Live-Publish / Einreichung**

- `gtm_publish_version`, `sc_submit_sitemap`, `strapi_publish_entry`
- `wp_create_post` / `wp_update_post` mit `status='publish'` (Default `draft`) — geht sofort live
- `wp_tracking_configure` — bindet GTM sofort live ein; nie bei `scan_hinweis` in `wp_tracking_status` (doppelte Ladung)
- `bing_submit_urls`, `bing_submit_sitemap`, `site_indexnow_submit`
- `meta_create_lead_form` — Meta veröffentlicht sofort, danach nicht mehr änderbar; erst `dry_run=True`

**Outbound (lemlist) — echte Nachrichten, nicht rückholbar**

- `lemlist_start_campaign` — verschickt echte E-Mails/LinkedIn-Nachrichten: erst `validate_only=True`, `summary` zeigen, dann mit `expected_leads` starten
- `lemlist_add_sequence_step` / `lemlist_update_sequence_step` in laufenden Kampagnen — gelten sofort für die folgenden Sendungen

**Live-Profil (GBP) — wirkt sofort auf das öffentliche Google-Profil**

- `gbp_update_profile`, `gbp_update_attributes`, `gbp_manage_hours` / `gbp_manage_categories` (Setz-Modus)
- `gbp_manage_open_info` (Setz-Modus) — `CLOSED_PERMANENTLY` lehnt das Tool selbst ab (Dashboard-Aufgabe)
- `gbp_reply_review` — **ersetzt** eine bestehende Antwort; vorher `gbp_reviews` lesen und die alte Antwort im Preview zeigen. „Alle offenen beantworten” NUR nach vollständigem Scan: erst `gbp_reviews` mit `unanswered_only=True` + hohem `max_pages` durchpaginieren (bis `next_page_token` leer ist) und alle `review_id` als Snapshot sammeln, DANACH erst antworten — nie Lesen und Antworten verschränken (eine Antwort bumpt `updateTime` und verschiebt die Sortierung)
- `gbp_delete_reply` — löscht eine bestehende Antwort (Review gilt danach wieder als unbeantwortet)
- `gbp_create_post`, `gbp_upload_media` — veröffentlichen sofort öffentlich sichtbaren Content (Post bzw. Foto) im Business-Profil
- `gbp_delete_post`, `gbp_delete_media` — entfernen veröffentlichten Content endgültig

## Defaults

- Wo möglich erst `PAUSED`/Draft statt destruktiv löschen.
- Nie Bulk-Mutation (`ads_bulk_add_keywords`, `ads_bulk_add_negative_keywords`, `ads_manage_account_negatives`, `lemlist_add_leads`) ohne aufgezählten Preview je Element.
- Fehlt Schreib-Scope oder source-Verbindung → sagen, nicht versuchen.
