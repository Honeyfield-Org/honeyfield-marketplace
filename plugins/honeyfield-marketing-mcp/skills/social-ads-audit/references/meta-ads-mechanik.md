# Meta-Ads-Mechanik — Tool-Reality & Diagnose-Methodik

Ground Truth ist die Server-Implementierung des Marketing-Ops-MCP (Graph API v25). Alles hier beschreibt, was die Tools **wirklich** liefern — nicht, was die Marketing API theoretisch könnte.

## Die conversions-Zählung (wichtigste Grenze)
- Die Performance-Tools (`meta_campaign_performance`, `meta_adset_performance`, `meta_ad_performance`) zählen als „conversions” ausschließlich diese vier Action-Types: `purchase`, `offsite_conversion.fb_pixel_purchase`, `lead`, `offsite_conversion.fb_pixel_lead`.
- Folge: klassischer Kauf (purchase) und klassische Lead-Gen (lead) werden korrekt gezählt. **Custom Conversions, `complete_registration`, `add_to_cart`, Messaging-Ziele, App-Events: unsichtbar** — die Spalte zeigt dann 0 oder untertreibt systematisch.
- Diagnose-Regel: vor jeder CPA-Aussage via `meta_pixel_stats` (aggregation=event) prüfen, welche Events real ankommen. Purchase/Lead nicht im Event-Mix → conversions-Spalte für diesen Kunden strukturell blind → CPA-Urteile über `ga4_conversions` herleiten (beratend, andere Attribution) und die Grenze im Report benennen.
- **Kein Conversion-Value in den Antworten → ROAS nicht berechenbar.** Nie einen ROAS behaupten; GA4-Umsatz ÷ Meta-Spend ist eine Näherung (beratend, Attributions-Bruch benennen).

## Fenster-Mathe (days-Mechanik)
- Alle Performance-Tools nehmen nur `days` (Fenster endet heute) und liefern **eine Aggregat-Zeile pro Entität** — kein Tagesverlauf, keine frei wählbaren Zeiträume.
- Trend-/Fatigue-Näherung über zwei Calls, z. B. `days=7` und `days=30`. Das 7er-Fenster ist im 30er **enthalten**: CTR(7d) deutlich unter CTR(30d) heißt, die jüngste Woche zieht den Schnitt nach unten — Verdacht auf Creative-Abnutzung oder Auktionsverschiebung.
- Grobe Lesart (beratend, keine harte Schwelle): CTR(7d) unter ~⅔ der CTR(30d) bei stabilem Setup und relevantem Spend-Anteil → Fatigue-Verdacht, Rotation prüfen. Ohne Frequency-Daten bleibt es ein Verdacht.
- **Echtes WoW (Vorwoche vs. Woche davor) ist nicht sauber möglich** — die Fenster überlappen immer. Für Zeitraum-Reports → `wochenreport` (dort ist dieselbe Grenze dokumentiert).
- CPM und CPC selbst rechnen (spend ÷ impressions × 1000 bzw. spend ÷ clicks) — die Tools liefern nur CTR fertig.

## CBO vs. ABO
- **CBO** (Campaign Budget Optimization): `daily_budget`/`lifetime_budget` steht auf der **Kampagne** (`meta_list_campaigns`), die Bid-Strategie ebenfalls; Adset-Budgets werden ignoriert.
- **ABO**: Budget je **Adset** (`meta_list_adsets`), Bid je Adset.
- `meta_update_campaign(daily_budget)` wirkt **nur bei CBO**. `meta_create_adset` erkennt CBO selbst und verlangt bei ABO ein eigenes `daily_budget`.
- Befund-Muster: Budgets auf beiden Ebenen sichtbar = unklare Steuerung → vereinheitlichen (welches Modell, entscheidet der Kunde; CBO bündelt Signale, ABO gibt Kontrolle).

## Bid-Strategien
- `LOWEST_COST_WITHOUT_CAP` („Highest Volume”, Default — kein Gebot nötig), `LOWEST_COST_WITH_BID_CAP` (+`bid_amount`), `COST_CAP` (+`bid_amount` als Ziel-Kosten), `LOWEST_COST_WITH_MIN_ROAS`.
- Cost Cap / Bid Cap zu niedrig = erstickte Auslieferung (Analogie: zu niedriger tCPA bei Google) — sichtbar als Spend deutlich unter Budget bei aktivem Status.

## Signal-Fragmentierung (beratend)
- Die Auslieferung lernt **pro Adset**. Meta-Faustregel: ~50 Conversion-Events pro Adset und Woche für stabiles Lernen.
- Viele kleine Adsets mit je < ~10 Conversions/Woche = Dauerlernen ohne Konvergenz. Empfehlung: konsolidieren (Adsets zusammenlegen, Budget bündeln), bevor am Feintuning gedreht wird.
- Die Lernphase selbst ist über die Tools **nicht sichtbar** — nur die Mechanik erklären, nie „ist in der Lernphase” als Befund verkaufen.

## Status-Deutung
- `status` = gesetzter Soll-Status; **`effective_status`** = tatsächliche Auslieferung inkl. vererbter und Review-Zustände (z. B. `CAMPAIGN_PAUSED`, `PENDING_REVIEW`, `WITH_ISSUES`, `DISAPPROVED` — Graph-API-Werte, durchgereicht). **Diagnose immer auf `effective_status`.**
- `account_status` (aus `meta_list_ad_accounts`): ACTIVE · DISABLED · UNSETTLED (offene Rechnung!) · PENDING_RISK_REVIEW · IN_GRACE_PERIOD · PENDING_CLOSURE · CLOSED. Alles außer ACTIVE ist ein Gate-Befund.

## validate_only (Operator-Grundlage)
- **Alle** Meta-Schreib-Tools akzeptieren `validate_only=true` → serverseitige Validierung über die Graph API (`execution_options`) ohne Ausführung. Fehler (Budget-Format, fehlende Pflichtfelder, Policy) tauchen so **vor** dem Write auf.
- Ausnahme-Verhalten: `meta_create_ad` simuliert bei `validate_only` **lokal** (zeigt `would_create`, macht keine Uploads/API-Calls) — die echte Validierung passiert erst beim Write.
- Workflow immer: `validate_only=true` → Preview zeigen → Bestätigung einholen → echter Call.

## meta_create_ad-Ablauf
- Pflicht: `adset_id`, `name`, `page_id` (via `meta_list_pages` — Ads laufen im Namen einer Page), `message` (Text über dem Medium), `link`. Optional `headline`/`description` (unter dem Medium), `call_to_action` (LEARN_MORE, SHOP_NOW, SIGN_UP, CONTACT_US, BOOK_NOW …).
- **Bild-Ad:** `image_hash` (aus `meta_upload_ad_image` — öffentliche URL, max. 8 MB) oder `image_url` direkt (wird dann automatisch hochgeladen).
- **Video-Ad:** `meta_upload_ad_video` (asynchron) → `meta_video_status` pollen bis `ready` → dann `meta_create_ad` mit `video_id`. Thumbnail ist Pflicht (explizit oder Auto-Thumbnail des Videos).
- Creative + Ad entstehen in **einem** Schritt, Default PAUSED. Schlägt der Ad-Teil fehl, existiert das Creative bereits (`creative_id` in der Fehler-Antwort — wiederverwendbar, kein Duplikat anlegen).
- **Targeting-Update-Footgun (`meta_update_adset`):** jedes übergebene Targeting-Feld ersetzt den bestehenden Wert **komplett** (z. B. Länderliste immer vollständig angeben); nicht übergebene Felder bleiben erhalten. DSA-Felder (`dsa_beneficiary`/`dsa_payor`) bei Updates mitführen.
