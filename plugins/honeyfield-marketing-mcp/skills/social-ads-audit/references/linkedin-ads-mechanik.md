# LinkedIn-Ads-Mechanik — Tool-Reality & Diagnose

Ground Truth ist die Server-Implementierung des Marketing-Ops-MCP (LinkedIn Marketing API, Rest.li 2.0, versioniert). Die LinkedIn-Sektion des Audits ist bewusst schlanker als Meta — die Tool-Basis ist kleiner, und die Grenzen sind ehrlich zu benennen.

## Hierarchie-Mapping (anders als Meta!)
- **Campaign Group** (≈ Meta-Kampagne) trägt `totalBudget` → **Campaign** (≈ Meta-Adset: `dailyBudget`, Targeting, Objective) → **Creative** (≈ Meta-Ad, referenziert einen Page-Post).
- Befunde auf der richtigen Ebene ansetzen: Budget/Targeting/Objective leben auf der **Campaign**, nicht auf der Group.

## adAnalytics-Realität
- `linkedin_campaign_performance` / `linkedin_creative_performance`: `days`-Fenster (endet heute), `timeGranularity=ALL` → **eine Aggregat-Zeile pro Entität, keine Zeitreihe**.
- Felder: `impressions`, `clicks`, `cost` (Konto-Währung), `conversions` (= `externalWebsiteConversions`). **CTR und CPC selbst rechnen**; kein Conversion-Value → kein ROAS.
- **Namen nur best-effort:** URNs werden für max. ~20 Zeilen in Kampagnen-Namen aufgelöst — der Rest bleibt `urn:li:sponsoredCampaign:…` (ID hinten ablesen und via `linkedin_list_campaigns` zuordnen). Nicht als fehlende Kampagne deuten.
- **Conversion-Setup nicht prüfbar:** kein Insight-Tag-/Conversion-Regel-Tool. `conversions` dauerhaft 0 bei nennenswertem Traffic = Setup-Verdacht → im Campaign Manager prüfen lassen (beratend). Das ist die LinkedIn-Entsprechung des Meta-Signal-Gates — nur ohne Prüfwerkzeug.

## Objectives & Bidding
- Objectives: BRAND_AWARENESS · WEBSITE_VISIT · ENGAGEMENT · VIDEO_VIEW · LEAD_GENERATION · WEBSITE_CONVERSION · JOB_APPLICANT.
- `linkedin_create_campaign` setzt fest: Typ SPONSORED_UPDATES, `costType=CPM`, `optimizationTargetType=MAX_CLICK` (= „Maximale Auslieferung”, automatisches Gebot). **Manuelle Gebote sind über den MCP nicht steuerbar** — als Grenze benennen, nicht als Empfehlung umschiffen.

## Targeting
- Anlage: Geo (AT/DE/CH/US/GB/FR/NL/IT/ES als ISO-Code, weitere als `urn:li:geo:…`) + Profilsprache.
- **Interface-Sprachen-Footgun:** `language=de` targetet über `interfaceLocales` die **Profil-/Oberflächensprache**, nicht Standort oder Sprachkenntnis. DACH-Professionals mit englischem LinkedIn-Interface (Tech, Beratung, Konzerne — sehr verbreitet) werden ausgeschlossen. Diagnose-Frage bei unerklärlich kleiner Reichweite; Fix: EN-Zwillings-Kampagne aufs gleiche Geo.
- **Bestands-Targeting ist nicht im Detail lesbar** — `linkedin_list_campaigns` liefert Name/Status/Typ/Budget, nicht die Targeting-Kriterien. Diagnose auf Anlage-Wissen + Kunden-Auskunft stützen (beratend).

## Creatives
- `linkedin_list_creatives`: `intendedStatus` (Soll) + `isServing` (Ist) + `content_reference` (Post-URN). Inhalt nur über die Post-URL auf der Unternehmensseite sichtbar.
- **`intendedStatus=ACTIVE` + `isServing=false` = Auslieferungsproblem** → Ebenen durchgehen: Creative im Review? Kampagne/Gruppe pausiert oder DRAFT? Budget erschöpft?
- **Keine Dark Posts:** neue Anzeigen entstehen nur aus bestehenden Page-Posts (`urn:li:share:…` / `urn:li:ugcPost:…`) via `linkedin_create_ad_from_post` — der API-Scope `w_organization_social` fehlt der App. Creative-Nachschub heißt: erst organischer Post auf der Unternehmensseite (durch den Kunden), dann sponsern.

## B2B-DACH-Realität (beratend)
- Zielgruppen in AT/CH sind schnell zu klein — Matched Audiences brauchen ~300 Mitglieder als Serving-Untergrenze (Richtwert); bei engem Targeting DACH-weit denken statt AT-only.
- Kontaktpreise liegen deutlich über Meta — CPC-/CPM-Vergleiche zwischen den Plattformen sind sinnlos. LinkedIn rechnet sich über Lead-Qualität und Deal-Größe, nicht über den Klickpreis.
- Alle Write-Tools defaulten auf **DRAFT** — Aktivierung ist immer ein bewusster zweiter Schritt.
