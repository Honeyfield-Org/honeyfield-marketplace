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

**Budget / Status / Bidding**

- `ads_update_campaign_budget`, `ads_update_campaign_status` (pause/enable)
- `linkedin_update_campaign_budget`, `linkedin_update_campaign_status`
- `ads_update_campaign_bidding_strategy`

**Conversions / Customer-Match (Daten-Upload / PII)**

- `ads_upload_conversions`, `ads_upload_customer_match_members`, `ads_remove_customer_match_members`

**Live-Publish / Einreichung**

- `gtm_publish_version`, `sc_submit_sitemap`, `strapi_publish_entry`
- `wp_create_post` / `wp_update_post` mit `status='publish'` (Default `draft`) — geht sofort live

**Live-Profil (GBP) — wirkt sofort auf das öffentliche Google-Profil**

- `gbp_update_profile`, `gbp_update_attributes`, `gbp_manage_hours` / `gbp_manage_categories` (Setz-Modus)
- `gbp_manage_open_info` (Setz-Modus) — `CLOSED_PERMANENTLY` lehnt das Tool selbst ab (Dashboard-Aufgabe)
- `gbp_reply_review` — **ersetzt** eine bestehende Antwort; vorher `gbp_reviews` lesen und die alte Antwort im Preview zeigen. „Alle offenen beantworten” NUR nach vollständigem Scan: erst `gbp_reviews` mit `unanswered_only=True` + hohem `max_pages` durchpaginieren (bis `next_page_token` leer ist) und alle `review_id` als Snapshot sammeln, DANACH erst antworten — nie Lesen und Antworten verschränken (eine Antwort bumpt `updateTime` und verschiebt die Sortierung)
- `gbp_delete_reply` — löscht eine bestehende Antwort (Review gilt danach wieder als unbeantwortet)
- `gbp_create_post`, `gbp_upload_media` — veröffentlichen sofort öffentlich sichtbaren Content (Post bzw. Foto) im Business-Profil
- `gbp_delete_post`, `gbp_delete_media` — entfernen veröffentlichten Content endgültig

## Defaults

- Wo möglich erst `PAUSED`/Draft statt destruktiv löschen.
- Nie Bulk-Mutation (`ads_bulk_add_keywords`, `ads_bulk_add_negative_keywords`) ohne aufgezählten Preview je Element.
- Fehlt Schreib-Scope oder source-Verbindung → sagen, nicht versuchen.
