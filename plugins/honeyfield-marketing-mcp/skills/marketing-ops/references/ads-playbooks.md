# Ads-Playbooks

Jeder mutierende Flow folgt [write-guardrails.md](write-guardrails.md): erst lesen, Diff zeigen, bestätigen lassen.
Tool-Namen: unprefixed, alle verifiziert gegen server.py. Quelle immer "google_ads".

---

## Budget anpassen

1. `ads_list_campaigns` + `ads_budget_status` → Ist-Budget und Auslastung pro Kampagne lesen.
2. `budget_pacing` → über/unter Plan? Tagesbudget realistisch?
3. Preview zeigen: Kampagne · Feld "daily_budget" · **alt → neu** · Reversibel: ja.
4. Bestätigen → `ads_update_campaign_budget`. ⚠ Hochrisiko — einzeln bestätigen.

---

## Kampagne pausieren / aktivieren

1. `ads_list_campaigns` → Status lesen.
2. Preview zeigen: Kampagne · Feld "status" · **ENABLED → PAUSED** (oder umgekehrt) · Wirkung: stoppt/startet Auslieferung sofort · Reversibel: ja.
3. Bestätigen → `ads_update_campaign_status`. ⚠ Hochrisiko — einzeln bestätigen.

---

## Neue Kampagne

1. `ads_list_campaigns` → Namens-/Struktur-Kontext prüfen.
2. Preview der Eckdaten (Name, Bidding, Budget, Channel, Netzwerk) zeigen → bestätigen.
3. `ads_create_campaign` mit `status=PAUSED` anlegen.
4. `ads_create_ad_group` → Ad Group in der neuen Kampagne.
5. `ads_add_keyword` (einzeln) oder `ads_bulk_add_keywords` (Batch) — Preview je Element.
6. `ads_create_ad` → Responsive Search Ad anlegen.
7. Review von Struktur und Inhalten (Keywords, Headlines, URLs). Erst danach:
8. `ads_update_campaign_status` → ENABLED. ⚠ Hochrisiko — einzeln bestätigen.

---

## Suchbegriff-Hygiene

1. `ads_search_terms` (Zeitraum: ≥ 14 Tage) → verschwendete oder irrelevante Terms identifizieren.
2. Vorschlagsliste mit Match-Type zeigen → bestätigen.
3. `ads_add_negative_keyword` (einzeln) oder `ads_bulk_add_negative_keywords` (Batch, Preview je Term).
4. Optional: `ads_manage_shared_negative_list` für kampagnenübergreifende Listen.

---

## Gebote — Keyword-Ebene

1. `ads_keyword_performance` (≥ 14 Tage) + `ads_keyword_quality` → welche Keywords über/unter CPA-Ziel?
2. Preview: Keyword · Feld "cpc_bid_micros" · **alt → neu** · Reversibel: ja.
3. Bestätigen → `ads_update_keyword_bid`.

---

## Gebote — Ad-Group-Ebene

1. `ads_list_ad_groups` → aktuellen Ad-Group-CPC lesen.
2. `ads_campaign_performance` + `ads_ad_performance` → Performance-Kontext.
3. Preview: Ad Group · Feld "cpc_bid_micros" · **alt → neu** · Reversibel: ja.
4. Bestätigen → `ads_update_ad_group_bid`.

---

## Bidding Strategy ändern

1. `ads_list_campaigns` → aktuelle Bidding Strategy lesen.
2. Preview: Kampagne · Feld "bidding_strategy" · **alt → neu** · Wirkung: ändert Lernphase, kann Performance kurzfristig destabilisieren · Reversibel: ja.
3. Bestätigen → `ads_update_campaign_bidding_strategy`. ⚠ Hochrisiko — einzeln bestätigen.

---

## Keyword-Status ändern

1. `ads_list_keywords` (optional nach Kampagne/Ad Group gefiltert) → Status lesen.
2. Preview: Keyword · Feld "status" · **ENABLED → PAUSED** (oder umgekehrt) · Reversibel: ja.
3. Bestätigen → `ads_update_keyword_status`.

---

## Anzeige ersetzen / updaten

> `ads_update_ad` ist deprecated — stattdessen immer `ads_replace_ad` verwenden.

1. `ads_list_ads` → aktuelle Headlines, Descriptions, URLs lesen.
2. `ads_ad_performance` → welche Anzeige ersetzen und warum?
3. Preview: Ad-ID · alle geänderten Felder · **alt → neu** · Wirkung: Genehmigungsprozess startet neu · Reversibel: nein (Original gelöscht).
4. Bestätigen → `ads_replace_ad`.

---

## Recommendations — anwenden / verwerfen

1. `ads_list_recommendations` → offene Empfehlungen lesen (Typ, potenzielle Impact-Metriken).
2. Für jede Empfehlung einzeln: Typ + erwarteten Effekt zeigen.
3. Bestätigen → `ads_apply_recommendation` oder `ads_dismiss_recommendation`.
   Nicht gebündelt anwenden — jede Empfehlung einzeln bestätigen lassen.

---

## Geo-Targeting anpassen

1. `ads_get_geo_targeting` → aktuelle Standorte + Presence-vs-POI-Einstellung lesen.
2. `ads_geo_performance` (≥ 30 Tage) → Performance nach Standort prüfen.
3. Preview: Kampagne · Standort-Änderungen · Reversibel: ja.
4. Bestätigen → `ads_update_geo_targeting`.

---

## Device-Bid-Modifier setzen

1. `ads_device_performance` (≥ 30 Tage) → CPA/ROAS nach Gerätetyp lesen.
2. Preview: Kampagne · Gerät (`MOBILE`/`DESKTOP`/`TABLET`) · **alt → neu** · Reversibel: ja.
3. Bestätigen → `ads_set_device_bid_modifier`.

---

## Sitelink anlegen / ändern

1. `ads_list_assets` (asset_type=`SITELINK`) → bestehende Sitelinks lesen.
2. Preview: Felder (Text, URL, Beschreibung) · Neu oder Ersatz · Reversibel: ja (deaktivierbar).
3. Bestätigen → `ads_create_sitelink` (neu) oder `ads_update_sitelink` (Text per Ersatz-Asset, URL direkt).
