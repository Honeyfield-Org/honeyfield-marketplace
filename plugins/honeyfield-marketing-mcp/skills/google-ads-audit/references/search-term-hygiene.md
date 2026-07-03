# Suchbegriff-Hygiene & Negatives (Wasted Spend)

Vertiefung zu Phase 3. Dieser Skill **besitzt** die Suchbegriff-Hygiene voll — Diagnose **und** Umsetzung.

## Match-Types heute (mit Close-Variants)
Google matcht alle Positiv-Keywords inkl. **Close-Variants**: Tippfehler, Singular/Plural, Abkürzungen, Akzente, und (bei Phrase/Broad) bedeutungsgleiche Varianten.
- **Exact `[...]`:** engste Steuerung, aber matcht Close-Variants/„gleiche Bedeutung” → der Suchbegriff ≠ das Keyword. Deshalb **immer den Suchbegriff-Bericht prüfen**, nicht nur die Keyword-Liste.
- **Phrase `"..."`:** Bedeutung in Reihenfolge, mit Zusätzen drumherum.
- **Broad (ohne Symbol):** breiteste Reichweite, nutzt zusätzlich Kontext (Landingpage, andere Keywords, Nutzer-Historie). **Nur tragbar mit:** sauberem Conversion-Tracking + Smart Bidding (das Broad steuert) + laufender Negatives-Hygiene. Ohne diese drei → Geldgrab.

## n-gram-Analyse (der Profi-Schritt)
Einzelne Suchbegriffe durchklicken skaliert nicht. Stattdessen nach **Tokens** gruppieren:
1. Aus `ads_search_terms` die Begriffe + Spend + Conversions ziehen (großzügiges Limit, ganzes Analysefenster).
2. Begriffe in Tokens / Bigramme zerlegen (z. B. „kostenlose excel vorlage” → „kostenlos”, „excel”, „vorlage”, „excel vorlage”).
3. Spend und Conversions **pro Token** aggregieren.
4. Tokens mit **viel Spend, ~0 Conversions** = systematische Lecks (z. B. „kostenlos”, „gratis”, „job”, „gebraucht”, „selber machen”, „pdf”).
Das findet Muster, die einzeln unter dem Radar bleiben, und zeigt, ob ein **Wort** (Broad-Negative) oder eine **Phrase** das Leck ist.

## Negative-Ebenen — welche wofür
| Ebene | Wirkung | Einsatz |
|---|---|---|
| **Ad Group** | nur diese Ad Group | Begriff soll in anderer Ad Group laufen (Steuerung zwischen Gruppen) |
| **Kampagne** | ganze Kampagne | kampagnenspezifisch irrelevant |
| **Shared Negative List** (`ads_manage_shared_negative_list`) | auf viele Kampagnen anwendbar | Konto-weite Universal-Negatives (Jobs, gratis, Konkurrenz-Marken, Erwachsenen-Begriffe) |

Faustregel: **universelle Müll-Begriffe → Shared List** (einmal pflegen, überall wirken); **Steuerung zwischen Ad Groups → Ad-Group-Ebene**.

## Negative-Match-Types — die Fallstricke
- **Negatives matchen KEINE Close-Variants/Tippfehler.** Ein Negative `gratis` blockiert **nicht** „gratiss” oder „kostenlos”. Häufige Müll-Schreibweisen einzeln aufnehmen.
- **Negativ Broad** `gratis` blockiert jede Anfrage, die das Wort enthält (Reihenfolge egal), aber **alle** Wörter eines Mehrwort-Negatives müssen vorkommen: Negativ-Broad `günstige schuhe` blockiert nur Anfragen mit *beiden* Wörtern.
- **Negativ Phrase** `"günstige schuhe"` = in dieser Reihenfolge.
- **Negativ Exact** `[günstige schuhe]` = nur exakt diese Anfrage.
- **Single-Word-Broad-Negatives sind gefährlich:** `frei` würde auch „Freiberufler”, „Freizeit” wegschneiden. Vor breiten Single-Word-Negatives prüfen, was sie sonst noch blockieren.

## Konflikte (Negative blockiert aktives Keyword)
Ein zu breites Negative kann ein **aktives, bezahltes Keyword** aushebeln (das Keyword bekommt keine Impressionen mehr). Vor jedem Bulk-Ausschluss gegen die aktive Keyword-Liste (`ads_list_keywords`) prüfen — ein Negative, das ein Performer-Keyword killt, ist schlimmer als der ausgeschlossene Müll. Bestehende Konflikte via `ads_list_negative_keywords` aufdecken.

## Brand vs. Non-Brand trennen
Brand-Suchbegriffe (eigener Markenname) haben hohe CTR, niedrigen CPC, hohen ROAS — sie **blähen jeden Blended-Wert auf**. Ein Konto kann „profitabel” aussehen, während das Non-Brand-Geschäft Geld verliert. Immer getrennt auswerten:
- Brand identifizieren (Markenname + Varianten/Tippfehler aus dem Projekt-Kontext / `projekt-kontext`).
- Performance Brand vs. Non-Brand getrennt berichten.
- Achtung: Konkurrenz, die auf den eigenen Brand bietet, und eigene Kampagnen, die Brand + Generic mischen.

## Unattribuierter Spend
Der Suchbegriff-Bericht zeigt aus Datenschutzgründen **nicht alle** Begriffe (Low-Volume-Schwelle). Differenz zwischen Kampagnen-Spend und Summe der sichtbaren Suchbegriff-Spends = **unattribuierter Anteil**. Beziffern und als Sichtbarkeitslücke nennen („~X % des Spends nicht auf Suchbegriff-Ebene einsehbar”) — nicht ignorieren, nicht überdramatisieren.

## Bulk-Ausschluss-Workflow (Operator)
1. Kandidaten aus n-gram + Einzelbegriffen sammeln (Spend ohne Conversion, klar irrelevant).
2. Pro Kandidat **Ebene** (Ad Group / Kampagne / Shared List) und **Match-Type** festlegen.
3. **Konfliktprüfung** gegen aktive Keywords.
4. **Dry-Run zeigen:** Begriffe + Ebene + Match-Type + geschätzter eingesparter Spend.
5. Erst nach ausdrücklicher Bestätigung ausführen (`ads_bulk_add_negative_keywords` / `ads_manage_shared_negative_list`).
