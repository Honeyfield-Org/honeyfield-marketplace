# DACH-Layer für Google Ads

Punkte, die ein US-/Englisch-Audit nicht hat. Quer über alle Phasen mitdenken.

## Standort-Targeting: „Anwesenheit” vs. „Anwesenheit oder Interesse”
Das wichtigste stille Wasted-Spend-Leck in DACH-Konten.
- **„Anwesenheit oder Interesse”** (Google-Default): zeigt Anzeigen Leuten, die im Zielort sind **ODER sich dafür interessieren / danach suchen**. Folge: jemand in Hamburg, der „Hotel Wien” sucht, sieht die Anzeige eines Wiener Hotels — meist irrelevant fürs lokale Geschäft.
- **„Anwesenheit”** (Presence): nur Leute, die regelmäßig im Zielort sind. Für **lokales/regionales** Geschäft (Handwerk, Praxis, Gastro, lokaler Handel) fast immer die richtige Wahl.
- **Ausschluss-Einstellung analog prüfen:** ausgeschlossene Orte sollten ebenfalls auf „Anwesenheit” stehen, sonst greift der Ausschluss zu breit/zu eng.
- Im Audit: Targeting-Methode der Kampagnen via `ads_get_geo_targeting` prüfen (liefert Standorte + Presence-vs.-POI-Einstellung); bei lokalem Geschäft + „Interesse”-Default = High-Impact-Befund. Umstellung via `ads_update_geo_targeting` (Operator, nach Bestätigung).

## Sprache: Anzeige und Landingpage müssen zusammenpassen
Seit Ende 09/2026 entfernt Google die Spracheinstellung auf Kampagnenebene für **Search und AI Max**. Google ermittelt die Sprache aus Anzeige und Landingpage (Beleg: https://www.searchenginejournal.com/google-is-removing-language-targeting-from-search-campaigns/585592/).
- **Prüfpunkt:** Passen Sprache von Anzeigentext und Landingpage je Zielmarkt zusammen? Mehrsprachige CH-Konten: DE/FR/IT in getrennten Kampagnen/Ad Groups mit eigener Landingpage je Sprache. Gemischt (deutscher Text → französische LP) = Befund.
- Anzeigentexte via `ads_list_ads` (Headlines/Descriptions + `final_urls`) lesen; die LP-Sprache aus der URL/Seite ableiten. Befund-Stufe: beratend (der MCP misst die LP-Sprache nicht).
- **Tool-Hinweis:** `ads_get_language_targeting` liefert die Alt-Einstellung je Kampagne (Kampagne ohne Eintrag = alle Sprachen). Für Search/AI Max ist sie nicht mehr maßgeblich — keinen Befund daraus ableiten und sie dort nicht per `ads_update_language_targeting` „reparieren”.
- Für andere Kampagnentypen gilt die alte Mechanik weiter, soweit die Einstellung dort noch existiert: Sie zielt auf die **Google-UI-Sprache** des Nutzers, nicht auf die Suchsprache. Nur „Deutsch” schließt DACH-Nutzer mit englischer UI aus (Expats, viele in CH).

## Markt & Währung trennen (DE / AT / CH)
- **DE, AT, CH als getrennte Geo-Targets** behandeln — unterschiedliche Wettbewerbsdichte, CPC-Niveaus, Suchvolumina und Sprachvarianten.
- **Kontowährung** beachten: CH-Konten laufen oft in **CHF**. CPA/ROAS/Spend immer in Kontowährung lesen und so berichten (nicht stillschweigend in EUR umdeuten).
- Streuung über Landesgrenzen prüfen: zielt eine „Österreich”-Kampagne versehentlich auf DE mit?
- Für SERP-Wettbewerbs-Beifang (`dfs_serp_google_ads`) `location`/`language` exakt zum Zielmarkt setzen (DE→`Germany`/`de`, AT→`Austria`/`de`, CH→`Switzerland`/`de`). Default ist AT/de.

## Deutsche Morphologie & Negatives
- **Komposita** („Kinderfahrrad” vs. „Fahrrad für Kinder”) und **Flexion/Deklination** streuen die Suchbegriffe stärker als im Englischen. Close-Variants fangen viel, aber nicht alles.
- Folge: die **n-gram-Suchbegriff-Analyse (Phase 3)** wiegt in DE schwerer — Müll-Muster verstecken sich in Wortzusammensetzungen.
- Negatives auf deutsche Tippfehler/Umlaut-Varianten achten (Negatives matchen keine Close-Variants — s. `search-term-hygiene.md`): ggf. „ae/oe/ue”- und ß/ss-Schreibweisen separat aufnehmen.

## Rechtliches (beratend — KEINE Rechtsberatung)
Nur auf Vorhandensein/Plausibilität hinweisen, nie rechtlich bewerten. Im Zweifel an die Rechtsberatung des Kunden verweisen.
- **HWG (Heilmittelwerbegesetz):** Werbung für Gesundheit/Medizin/Heilmittel ist stark reglementiert (verbotene Heilversprechen, Vorher-Nachher etc.) — sowohl in der Anzeige als auch auf der Landingpage relevant. Bei Health-Konten als Risiko-Hinweis aufnehmen.
- **Google-generierte Texte (AI Max Text Customization):** Ist sie aktiv, schreibt Google eigene Anzeigentexte — die laufen am UWG/HWG-Check vorbei. Automatisch erstellte Assets wurden ab 09/2026 auf AI Max / Text Customization migriert. Bei gesetzten `compliance`-Flags: **Text Guidelines** setzen (Beta; bis 25 Term Exclusions, bis 40 Messaging Restrictions, alle Sprachen) oder Text Customization abschalten. Kein MCP-Tool liest oder setzt das → im Ads-UI, beratend. Belege: https://support.google.com/google-ads/answer/11259373 · https://support.google.com/google-ads/answer/16489313
- **Google-Rolle (DSGVO):** Für Google-Ads-/GA4-Messung gelten grundsätzlich die Controller-Controller-Bedingungen. Google ist **Auftragsverarbeiter (Processor)** nur bei Customer Match, Enhanced Conversions (inkl. für Leads) und Store-Sales-Uploads. Sind Enhanced Conversions aktiv (Phase 1) oder gibt es Customer-Match-Listen (`ads_list_customer_match_lists`), beim Kunden die Data Processing Terms/AVV erfragen. Beleg: https://business.safety.google/adsservices/
- **Preisangaben (PAngV):** wenn Preise beworben werden, müssen Grund-/Endpreise korrekt sein (inkl. USt., ggf. Grundpreis pro Einheit). Betrifft v. a. E-Commerce-Anzeigen + Landingpage.
- **Impressum:** Erreichbarkeit eines Impressums auf der Landingpage prüfen (Trust + rechtliche Pflicht in DACH). Nur Vorhandensein/Erreichbarkeit prüfen.
