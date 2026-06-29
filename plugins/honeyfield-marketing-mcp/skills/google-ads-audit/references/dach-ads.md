# DACH-Layer für Google Ads

Punkte, die ein US-/Englisch-Audit nicht hat. Quer über alle Phasen mitdenken.

## Standort-Targeting: „Anwesenheit" vs. „Anwesenheit oder Interesse"
Das wichtigste stille Wasted-Spend-Leck in DACH-Konten.
- **„Anwesenheit oder Interesse"** (Google-Default): zeigt Anzeigen Leuten, die im Zielort sind **ODER sich dafür interessieren / danach suchen**. Folge: jemand in Hamburg, der „Hotel Wien" sucht, sieht die Anzeige eines Wiener Hotels — meist irrelevant fürs lokale Geschäft.
- **„Anwesenheit"** (Presence): nur Leute, die regelmäßig im Zielort sind. Für **lokales/regionales** Geschäft (Handwerk, Praxis, Gastro, lokaler Handel) fast immer die richtige Wahl.
- **Ausschluss-Einstellung analog prüfen:** ausgeschlossene Orte sollten ebenfalls auf „Anwesenheit" stehen, sonst greift der Ausschluss zu breit/zu eng.
- Im Audit: Targeting-Methode der Kampagnen prüfen; bei lokalem Geschäft + „Interesse"-Default = High-Impact-Befund.

## Sprach-Targeting basiert auf der Oberflächensprache
Google-Sprach-Targeting zielt auf die **Google-UI-Sprache des Nutzers**, **nicht** auf die Sprache der Suchanfrage.
- Nur „Deutsch" → schließt DACH-Nutzer aus, die ihr Google auf Englisch gestellt haben (Expats, Tech-affine, viele in CH).
- Je nach Zielgruppe Englisch oder „alle Sprachen" ergänzen und über Keywords/Negatives steuern.
- Häufiger Fehler: Sprache zu eng → unsichtbar verlorene Reichweite, taucht in keinem Performance-Report direkt auf (nur als niedrigere Impressionen).

## Markt & Währung trennen (DE / AT / CH)
- **DE, AT, CH als getrennte Geo-Targets** behandeln — unterschiedliche Wettbewerbsdichte, CPC-Niveaus, Suchvolumina und Sprachvarianten.
- **Kontowährung** beachten: CH-Konten laufen oft in **CHF**. CPA/ROAS/Spend immer in Kontowährung lesen und so berichten (nicht stillschweigend in EUR umdeuten).
- Streuung über Landesgrenzen prüfen: zielt eine „Österreich"-Kampagne versehentlich auf DE mit?
- Für SERP-Wettbewerbs-Beifang (`dfs_serp_google_ads`) `location`/`language` exakt zum Zielmarkt setzen (DE→`Germany`/`de`, AT→`Austria`/`de`, CH→`Switzerland`/`de`). Default ist AT/de.

## Deutsche Morphologie & Negatives
- **Komposita** („Kinderfahrrad" vs. „Fahrrad für Kinder") und **Flexion/Deklination** streuen die Suchbegriffe stärker als im Englischen. Close-Variants fangen viel, aber nicht alles.
- Folge: die **n-gram-Suchbegriff-Analyse (Phase 3)** wiegt in DE schwerer — Müll-Muster verstecken sich in Wortzusammensetzungen.
- Negatives auf deutsche Tippfehler/Umlaut-Varianten achten (Negatives matchen keine Close-Variants — s. `search-term-hygiene.md`): ggf. „ae/oe/ue"- und ß/ss-Schreibweisen separat aufnehmen.

## Rechtliches (beratend — KEINE Rechtsberatung)
Nur auf Vorhandensein/Plausibilität hinweisen, nie rechtlich bewerten. Im Zweifel an die Rechtsberatung des Kunden verweisen.
- **HWG (Heilmittelwerbegesetz):** Werbung für Gesundheit/Medizin/Heilmittel ist stark reglementiert (verbotene Heilversprechen, Vorher-Nachher etc.) — sowohl in der Anzeige als auch auf der Landingpage relevant. Bei Health-Konten als Risiko-Hinweis aufnehmen.
- **Preisangaben (PAngV):** wenn Preise beworben werden, müssen Grund-/Endpreise korrekt sein (inkl. USt., ggf. Grundpreis pro Einheit). Betrifft v. a. E-Commerce-Anzeigen + Landingpage.
- **Impressum:** Erreichbarkeit eines Impressums auf der Landingpage prüfen (Trust + rechtliche Pflicht in DACH). Nur Vorhandensein/Erreichbarkeit prüfen.
