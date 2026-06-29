# DACH-SEO — Detailreferenz

On-Demand-Tiefe für den `seo-audit`-Skill. Nur laden, wenn der jeweilige Punkt im Audit relevant wird.

## hreflang-Matrix DE/AT/CH
- Cluster: `de-DE`, `de-AT`, `de-CH` (optional `de` generisch + `x-default`).
- Jede Sprachversion **referenziert sich selbst** und verlinkt **alle anderen reziprok**. Fehlt eine Rückverlinkung → Google ignoriert das Paar.
- Canonical jeder Locale zeigt auf sich selbst. **Niemals Cross-Country-Canonical** (z.B. AT→DE) — das unterdrückt die nicht-kanonische Locale komplett.
- Die Canonical-URL **muss im hreflang-Set vorkommen**, sonst wird das gesamte hreflang ignoriert.
- Typischer DACH-Fehler: `.de`- und `.at`-Seite mit identischem Content ohne hreflang → Duplicate-Content, Google spielt die falsche Version aus (DE-Preise an CH-Nutzer, € statt CHF).
- Mit unseren Tools nur teilweise prüfbar: Canonical via `sc_url_inspection`/`dfs_onpage_instant`; die hreflang-Tags selbst aus dem Seitenquelltext.

## Pixel-Snippets (statt Zeichenzählung)
- Title kappt bei ~569 px (nicht „60 Zeichen"). Deutsch: Komposita + Breitbuchstaben (W/M) fressen Platz, schmale (i/l) sparen. Wichtigstes Keyword nach vorne.
- Meta-Description: Desktop ~990 px, Mobil ~1.300 px.
- `dfs_onpage_instant` liefert Title/Meta-Text → Zeichenlänge ist nur Näherung; bei langen Komposita-Titeln eher kürzen.

## Umlaut/ß-URLs
- In Pfaden: `ä→ae, ö→oe, ü→ue, ß→ss`. Keine rohen Umlaute (werden `%C3%A4`-encoded → unleserlich, brüchig beim Teilen) und kein Punycode im Pfad.
- Umlaut-Domains (`müller.de`) leben als Punycode (`xn--mller-...`). Prüfen: Canonical, hreflang, Sitemap, SSL-Zertifikat, Redirects **alle konsistent in EINER Form**.

## Impressum & Datenschutz (Trust-Gate)
- Impressum: vorhanden, ≤ 1 Klick (Footer), Pflichtangaben. DE seit 14.05.2024 DDG (löst TMG ab); AT ECG/Mediengesetz; CH eigene Regeln.
- Datenschutzerklärung: separat, datiert, aktuell, im Footer (DSGVO; CH revDSG).
- Indexierung bewusst entschieden (oft `noindex`) — prüfen, nicht Default.
- **Nur Vorhandensein/Erreichbarkeit prüfen. Keine Rechtsberatung.**

## Lokale Citations je Land (über GBP hinaus)
- **DE:** Das Örtliche, Gelbe Seiten, 11880, Cylex, MeineStadt, Yelp DE, Bing Places, Apple Maps.
- **AT:** Herold.at (größtes, do-follow), WKO Firmen A-Z (Pflichtmitgliedschaft → hohes Trust-Signal), FirmenABC.at.
- **CH:** local.ch (#1), search.ch, moneyhouse.ch (Handelsregister), help.ch, cylex.ch.
- NAP byte-genau konsistent („Str." vs. „Straße", `+43/+41/+49`). Qualität vor Menge (30 gute > 200 mittelmäßige).

## AEO / AI-Overviews (DACH, beratend)
- AI Overviews seit 03/2025 in DE live, wachsender Keyword-Anteil; CTR auf Position 1 sinkt bei AIO deutlich.
- Was zählt: konsistente Entity-Daten (NAP + Geschäftszweck über Website/GBP/LinkedIn/Verzeichnisse), Zitierfähigkeit über deutsche autoritative/institutionelle Quellen, konkrete Service-/Prozess-/Preis-Transparenz statt generischer „Was ist X"-Texte.
- Mit unseren Tools **nicht messbar** (kein AIO-/SERP-Feature-Tool) → als Empfehlung führen, nicht als Befund.

## AT/CH-Linter
- **CH:** kein ß — immer `ss` („ausser", „Strasse"). Ein ß auf einer CH-Seite = Lokalisierungsfehler. Zahlen/Währung: `1'234.56 CHF` (Apostroph-Tausender, Punkt-Dezimal). CH oft mehrsprachig (de/fr/it) → hreflang je Sprache; Schweizer suchen meist auf Hochdeutsch, nicht Mundart.
- **AT:** Austriazismen in der Keyword-Recherche (Jänner≠Januar, Erdäpfel≠Kartoffeln, Sackerl) — eigene Suchvolumina via `dfs_keyword_volume` mit `location="Austria"`. `.at` = starkes Geo-Signal.
- ccTLD: `.de/.at/.ch` senden je ein starkes Länder-Signal; `.com` braucht hreflang + ggf. GSC-Land-Targeting.

## Marktzahlen mit Vorsicht
Bing-Anteil DACH, AIO-Penetration etc. bewegen sich. Im Audit immer mit Datumsstempel führen, nicht als Konstante behaupten.
