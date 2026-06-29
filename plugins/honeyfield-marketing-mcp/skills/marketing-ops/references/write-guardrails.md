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
- `ads_remove_negative_keyword`, `ga4_delete_key_event`
- `ga4_archive_custom_dimension`, `ga4_archive_custom_metric`
- `gtm_remove_tag`, `sc_delete_sitemap`, `strapi_delete_entry`

**Budget / Status / Bidding**

- `ads_update_campaign_budget`, `ads_update_campaign_status` (pause/enable)
- `ads_update_campaign_bidding_strategy`

**Conversions / Customer-Match (Daten-Upload / PII)**

- `ads_upload_conversions`, `ads_upload_customer_match_members`, `ads_remove_customer_match_members`

**Live-Publish / Einreichung**

- `gtm_publish_version`, `sc_submit_sitemap`

## Defaults

- Wo möglich erst `PAUSED`/Draft statt destruktiv löschen.
- Nie Bulk-Mutation (`ads_bulk_add_keywords`, `ads_bulk_add_negative_keywords`) ohne aufgezählten Preview je Element.
- Fehlt Schreib-Scope oder source-Verbindung → sagen, nicht versuchen.
