# DACH-Layer für Social Ads (DE/AT/CH)

Diese Punkte hat ein US-/Englisch-Audit nicht. Alles Rechtliche ist beratend (keine Rechtsberatung) — auf Vorhandensein/Plausibilität hinweisen, nicht juristisch bewerten.

## Consent-Untererfassung (EU) — der stille CPA-Verzerrer
- In DE/AT/CH feuert das Meta-Pixel erst nach Einwilligung (§25 TDDDG / §165 TKG / nDSG + DSGVO). Typische Ablehner-Quoten dämpfen die gemessenen Events **zweistellig** — die Plattform-CPA ist strukturell **überschätzt**, Conversions **unterzählt**.
- Diagnose-Konsequenzen:
  1. Pixel-Zahlen vs. GA4 vs. Kunden-Backend nie 1:1 erwarten — Größenordnungen vergleichen, Abweichung erklärbar machen.
  2. „Conversions eingebrochen” zuerst gegen Consent-/CMP-Änderungen halten (Banner-Update? CMP-Wechsel? neues Blocking?) — via `meta_pixel_stats`-Tagesverlauf den Knick datieren.
  3. Niedrige absolute Zahlen ≠ schlechte Kampagne — erst Signal-Qualität, dann Performance-Urteil.
- **CAPI (Conversions API)** federt Browser-Verluste ab; ob sie läuft und korrekt dedupliziert, ist via MCP **nicht sichtbar** → Events Manager / Kunde fragen (beratend). Die Website-Seite der Messung (GA4/GTM/Consent Mode) prüft `tracking-check`.

## DSA-Transparenzpflicht (EU)
- Jede in der EU ausgelieferte Anzeige braucht deklarierten **Begünstigten** und **Zahler**. Der Operator setzt `dsa_beneficiary`/`dsa_payor` bei **jeder** Adset-Anlage (Default: Zahler = Begünstigter) — Meta blockt EU-Anlagen ohne Angaben teils serverseitig.
- Bestands-Adsets sind über die Tools **nicht** auf DSA-Vollständigkeit prüfbar (beratend erfragen).
- Anzeigen sind öffentlich in der EU-Ad-Library einsehbar — Transparenz gilt in beide Richtungen (manuell auch für Konkurrenz-Recherche nutzbar; kein MCP-Tool dafür).

## Special Ad Categories (Meta)
- Kredit/Finanzen, Beschäftigung, Wohnen, Politik/Gesellschaft → bei Kampagnen-Anlage deklarieren (`special_ad_categories` in `meta_create_campaign`); das Targeting wird dann eingeschränkt (kein Alters-/Geschlechts-/PLZ-Feintuning).
- Einschlägige, aber nicht deklarierte Kampagnen riskieren Ablehnung und Konto-Flags — bei einschlägiger Branche im Projekt-Kontext (`compliance`) aktiv prüfen.

## Werberecht-Leitplanken für Creative-Urteile
Gilt für jede Creative-Empfehlung und jeden `meta_create_ad`-Text (message/headline/description). `compliance`-Flags aus `projekt-kontext` sind hart.
- **UWG:** Superlative/Zahlen-Claims („Nr. 1”, „Testsieger”, „10.000+ Kunden”) nur mit Beleg — Belegpflicht liegt beim Werbenden. Ohne Beleg blocken, Alternative anbieten.
- **HWG / Health-Claims** (`compliance: [HWG]`/`[HealthClaims]`): keine Wirk-/Heilversprechen; nur EU-zugelassene Angaben, neutraler Reframe.
- **PAngV:** Preise inkl. MwSt.; „ab”-Preis = echter Einstiegspreis; Streichpreise brauchen das 30-Tage-Minimum als Basis.
- **Impressum/Anbieterkennzeichnung** auf der beworbenen Landingpage erreichbar (Klick-Tiefe ≤ 2).
- Umfangreiche Copy-Erstellung ist nicht Scope dieses Skills — kurze Ad-Texte für den Operator laufen durch diese Leitplanken; für systematische Google-RSA-Copy → `ad-creative`.

## Markt-Kalibrierung
- **Währung:** Meta-Budgets/Spend kommen aus den Tools in EUR normalisiert; LinkedIn in Konto-Währung (`currencyCode` — CH oft CHF). CPA-Ziele in Konto-Währung besprechen.
- **DE ≠ AT ≠ CH:** ein Meta-Adset mit DE+AT+CH wird vom bevölkerungsstärksten Markt (DE) dominiert — AT-/CH-Fokus braucht eigene Adsets bzw. Kampagnen. LinkedIn: AT/CH-Zielgruppen schnell unter der Serving-Schwelle.
- **Saisonalität/Feiertage** sind regional verschieden (AT/CH/DE) — Fenster-Vergleiche entsprechend einordnen, bevor ein „Einbruch” diagnostiziert wird.
- **Keine importierten Benchmarks:** CTR-/CPM-/CPA-Benchmarks aus US-Quellen nicht auf DACH übertragen — Vergleichsbasis ist immer das eigene Konto (Ad vs. Ad, Fenster vs. Fenster).
