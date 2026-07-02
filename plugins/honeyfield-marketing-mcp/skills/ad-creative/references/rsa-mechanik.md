# RSA-Mechanik — Technische Referenz

Technisches Rückgrat für den `ad-creative`-Skill. On-demand laden, hält SKILL.md schlank.

---

## RSA-Struktur & Limits

**Responsive Search Ads bestehen aus:**

| Feld | Max. Anzahl | Max. Zeichen | Min. Pflicht |
|---|---|---|---|
| Headlines | 15 | 30 | 3 |
| Descriptions | 4 | 90 | 2 |
| Path1 | 1 | 15 | — |
| Path2 | 1 | 15 | — |
| Final URL | 1 | — | 1 |

**Wichtig: Die MCP-Tools erzwingen diese Limits NICHT.** Ein zu langer Text schlägt erst serverseitig bei Google fehl. Der Skill muss vor jedem Write-Aufruf selbst validieren:
- Zeichen zählen (Leerzeichen zählen mit)
- Anzahl der Headlines/Descriptions prüfen (min/max)
- DKI `{KeyWord:default}` kann das 30-Zeichen-Limit sprengen, je nach Keyword-Länge
- Umlaute (ä, ö, ü) und ß zählen als **je 1 Zeichen**

---

## Headline-Mix (Verteilung der 15)

Kanonische Mix-Verteilung (Anzahl je Typ: keyword/benefit/social-proof/CTA/differentiator/brand) und Unique-Regel: **SKILL.md, Modus A Schritt 2** — hier bewusst nicht dupliziert.

---

## Ad Strength — Best Practices (NICHT auslesbar)

**Der Ad-Strength-Wert ist über die MCP-Tools NICHT auslesbar.** `ads_list_ads` liefert kein `ad_strength`-Feld. Kein Tool gibt einen Strength-Wert zurück. Den aktuellen Wert (Poor / Average / Good / Excellent) sieht man **ausschließlich im Google Ads UI**.

Behauptung „ich verbessere deine Ad Strength von Poor auf Excellent" ist unzulässig — nie einen Strength-Wert behaupten oder vortäuschen, ihn auszulesen.

Was Ad Strength **treibt** (Best Practices, nach denen der Skill baut):

1. **Anzahl nahe 15 Headlines / 4 Descriptions** — Google braucht Kombinationsspielraum
2. **Unique Headlines** — inhaltliche Diversität, kein Paraphrasieren
3. **Keyword-Einbindung** — mindestens 1–2 Headlines enthalten das Haupt-Keyword der Ad Group
4. **Wenig Redundanz** — Headlines/Descriptions nicht mit ähnlichen Formulierungen füllen
5. **Themen-Diversität** — verschiedene Angles (Nutzen, Beweis, CTA) statt monothematisch

Selbstcheck im Output: „RSA nach Best-Practice gebaut (15 Headlines, Unique, Keyword-Einbindung, Mix) — den Strength-Wert siehst du nur im Google Ads UI."

---

## Replace-Mechanik & Lernhistorie-Reset

### RSA sind unveränderlich — jede inhaltliche Änderung = neue Ad

Google erlaubt keine echte In-Place-Bearbeitung von RSA-Inhalten. Der MCP-Workflow:

**`ads_replace_ad`** = Remove + Create + Merge:
- Erstellt eine neue Ad-Entität mit den neuen Inhalten
- Verknüpft sie mit derselben Ad Group
- `keep_old=true`: Die alte Ad wird **pausiert** (nicht gelöscht) — reversibel, ältere Performance-Daten bleiben erhalten
- `keep_old=false` (default): Die alte Ad wird entfernt — irreversibel

**`ads_update_ad` ist DEPRECATED** — in der Praxis verhält es sich wie Replace, aber die Semantik ist veraltet. `ads_replace_ad` verwenden.

**Einzige echte In-Place-Mutation: `ads_update_ad_status`** — ändert nur den Status (ENABLED/PAUSED), kein Inhalt.

**Kein In-Place-URL-Update für Ads.** Eine geänderte Final URL an einer RSA erfordert Replace. Ausnahme: Sitelink-`final_url` kann per `ads_update_sitelink` in-place geändert werden.

### Lernhistorie-Reset

Jede inhaltliche Änderung über Replace erzeugt eine **neue Ad-Entität** — neue Ad-ID, **Lernhistorie startet bei null**. Google braucht erneut ausreichend Impressions/Klicks, um die neue RSA zu optimieren.

Konsequenz für Iteration:
- Nicht jede schlechte Headline durch Replace „fixen" — die Kosten (Lernhistorie-Reset) gegen den Nutzen abwägen
- Wenn Replace nötig: `keep_old=true`, alte pausierte Ad als Rückfall-Option behalten
- Dem Nutzer vor jedem Replace erklären: „diese Aktion erstellt eine neue Ad — die bisherige Lernhistorie wird nicht übertragen"

---

## Pinning — beratend, nicht schreibbar

**Pinning ist über die MCP-Tools NICHT setzbar.** Die Tool-Parameter für `ads_create_ad` und `ads_replace_ad` nehmen Headlines/Descriptions als flache `string[]` — keine Pin-Position.

Pinning (Festhalten einer Headline auf Position 1, 2 oder 3) ist **nur im Google Ads UI** konfigurierbar.

### Empfehlung für UI-Pinning (beratend):
- **Brand-Headline:** Pos 1 sinnvoll, wenn Markenschutz-Kampagne
- **Disclaimer/Pflichtangaben:** Pos 1 oder 3, falls rechtlich erforderlich
- **Sparsam einsetzen:** Jeder Pin reduziert Googles Kombinationsfreiheit → schlechtere Optimierung
- Faustregel: Maximal 1–2 Pins pro RSA, nur wenn rechtlich oder strategisch zwingend

Im Output als Empfehlung formulieren: „Falls du X auf Pos 1 halten möchtest → im UI pinnen (Schraubenschlüssel-Icon an der Ad)"

---

## Statistik-Hygiene für Iteration (Modus B)

Bevor Headlines oder Descriptions als „Gewinner" oder „Verlierer" eingestuft werden:

**Mindest-Datengrundlage (Richtwerte):**
- Impressions: **≥ 1.000** pro verglichener Ad/Zeitraum
- Conversions: **≥ 10–20** für Conversion-basierte Urteile (je nach Branche)
- Zeitraum: vergleichbarer Zeitraum (Saison, Wochentage), kein Vergleich Peak vs. Off-Peak

**Grundprinzip: Eine Variable pro Zyklus**
- Nie gleichzeitig Headline-Text + Bid-Strategie + Targeting ändern und dann die Anzeigen-Performance beurteilen
- Isoliert iterieren: erst Copy ändern, Ergebnis abwarten, dann nächste Variable

**Verbotene Urteile auf dünner Datenbasis:**
- „Headline 3 performt schlechter" bei < 500 Impressions: kein Urteil — zu wenig Daten
- „Diese Ad hat schlechtere CTR" bei 2 Wochen Laufzeit nach einem Replace (Lernphase noch aktiv)

Im Output: Wenn die Datenlage dünn ist → explizit sagen: „Zu wenig Daten für ein zuverlässiges Urteil (X Impressions). Empfehlung: noch Y Wochen laufen lassen."

---

## Zeichen-Zähl-Tipps

Deutsche Eigenheiten, die Limits sprengen:

| Problem | Detail |
|---|---|
| **Leerzeichen** | Zählen mit — „PM Tool" (7) vs. „PM-Tool" (6) |
| **Umlaute & ß** | Je 1 Zeichen (ä=1, ö=1, ü=1, ß=1) — kein UTF-8-Mehrfachzählung |
| **DKI `{KeyWord:default}`** | Wird durch das auslösende Keyword ersetzt — kann Limit sprengen, wenn Keywords lang sind. Default-Text wählen, der sicher < 30 Zeichen ist |
| **Lange Komposita** | „Projektmanagement-Software" (27) verbraucht fast das gesamte Limit → kürzen: „PM-Software" (11) |
| **Satzzeichen** | Ausrufezeichen in Headlines erlaubt; Ausrufezeichen in Display-URL/Path nicht |
| **Groß-/Kleinschreibung** | Jedes signifikante Wort groß (Title Case) erhöht Lesbarkeit, kein Zeicheneffekt |

**Validierungs-Routine vor Write:**
1. Für jede Headline: `len(text.strip()) <= 30` — sonst kürzen oder streichen
2. Für jede Description: `len(text.strip()) <= 90`
3. Für Paths: `len(path.strip()) <= 15`
4. Headlines-Anzahl: 3 ≤ n ≤ 15; Descriptions: 2 ≤ n ≤ 4
5. DKI-Texte: Default-Wert im Limit prüfen, **und** längste realistische Keyword-Ersetzung prüfen — Ad-Group-Keywords per `ads_list_keywords` ziehen, das längste gegen das 30er-Limit rechnen

---

## Tool-Referenz (Kurzform)

**Write-Tools:**
- `ads_create_ad` — neue RSA anlegen; default ENABLED → immer `status="PAUSED"` setzen
- `ads_replace_ad` — inhaltliche Änderung; `keep_old=true` pausiert die alte (empfohlen)
- `ads_update_ad_status` — einzige In-Place-Mutation (Status ENABLED/PAUSED)
- `ads_create_sitelink` / `ads_update_sitelink` — Sitelinks neu anlegen / final_url in-place ändern; **kein `status`-Parameter** (kein PAUSED — nach Anlage sofort aktiv, ohne `campaign_id` Konto-weit) und kein Remove-Tool via MCP

**Read-Tools (Fundierung):**
- `ads_list_ads` — liefert Copy + Status; **kein Ad-Strength-Wert**
- `ads_list_assets` — Sitelinks/Callouts/Structured Snippets inkl. `asset_id` (Filter `asset_type`); Pflicht-Read vor jedem Sitelink-Write (Duplikate vermeiden, `asset_id` fürs Update). Promotion/Price deckt es nicht ab
- `ads_ad_performance` — Ad-Level CTR/Conversions (keine per-Asset-Labels)
- `ads_search_terms` / `ads_ai_max_search_terms` — reale Suchsprache der Nutzer
- `ads_keyword_performance` — QS + Conversion-Signale der Ziel-Keywords
- `ads_list_keywords` — alle Keywords der Ziel-Ad-Group (DKI-Längen-Check, auch impression-lose)

**Kein Tool liefert:** Ad Strength, per-Asset-Labels (Best/Good/Low), Pinning-Status.
