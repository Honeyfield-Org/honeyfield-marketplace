# Report-KPIs & Anomalie-Schwellen

Referenz für `wochenreport`. Pro Kanal: welche KPIs, welche Tools, was ein auffälliges WoW-Delta ist, und welcher Audit-Skill die Tiefe übernimmt. On-demand laden.

**Grundprinzip:** Der Report zieht die **Kern-KPIs** (nicht die Audit-Tiefe) und macht sie WoW-vergleichbar. Auffälligkeiten werden **markiert und an den passenden Audit-Skill verwiesen** — der Report diagnostiziert nicht selbst.

---

## Beleg-Stufen (Rahmen wie in den Audits; Mittelstufe je Domäne verschieden)
- **Gemessen:** harte Zahlen aus dem Konto/der Property (Ads-Spend, GSC-Klicks, GA4-Sessions, GEO/AI-Sichtbarkeit über `dfs_llm_mentions_metrics` bei verbundenem DataForSEO-Zugang, pay-as-you-go).
- **Mit Tracking-Vorbehalt:** abhängige KPIs (Conversions, CPA, ROAS), solange das Conversion-Tracking unklar ist — nicht als belastbar verkaufen.
- **Beratend:** GEO/AI-Sichtbarkeit über GA4-Referrer — Fallback bei `subscription_required` oder ohne `dataforseo`, sonst Ergänzung zu `dfs_llm_mentions_metrics` (Näherung, kein Fetch-Beweis).
Jede Report-Zeile trägt die Stufe implizit über die Quelle; AI-Traffic ohne DataForSEO-Zugang explizit als Näherung kennzeichnen.

---

## Zeitraum-Mechanik (Pflicht vor jedem Δ)

Viele Tools nehmen nur `days` — das Fenster endet **heute**, eine Vorperiode ist damit nicht direkt abrufbar (`ads_campaign_performance`, `ads_impression_share`, `ga4_conversions`, `ga4_traffic_sources`, `linkedin_campaign_performance`). Perioden wirklich trennen können `ga4_report` (`start_date`/`end_date`), `sc_performance`, `sc_top_queries` und `sc_top_pages` (je `start_date`/`end_date` im Format `YYYY-MM-DD`, nur gemeinsam) und `ads_conversion_performance` (Tagesverlauf). Deshalb:

- **Woche = ISO-Kalenderwoche Mo–So** (DACH-Konvention „KW”). Default: letzte abgeschlossene KW vs. die davor.
- **GA4-Deltas:** `ga4_report` mit `start_date`/`end_date` — zwei exakte Fenster abrufen. Für Vergleiche nicht `ga4_conversions` nutzen (nur `days`).
- **SEO-Deltas:** `sc_performance` mit `start_date`/`end_date` und `dimensions=[]` — ein Aufruf je Periode, liefert die Gesamtsumme inkl. anonymisierter Suchanfragen. Alternativ `dimensions=["date"]` über beide Perioden und die Tageszeilen selbst splitten. GSC-Daten laufen 2–3 Tage hinterher: prüfen, ob das Ende der Berichtswoche schon vollständig ist.
- **Ads-Conversions:** Tagesverlauf aus `ads_conversion_performance` in die zwei Perioden splitten.
- **Additive Ads-KPIs** (Spend, Klicks, Impressions): notfalls per Differenz ableiten — days=14 minus days=7 = Vorwoche. **CTR/CPC aus den additiven Werten je Periode neu berechnen — nie Raten differenzieren.**
- **`ads_impression_share`:** Snapshot ohne belastbare Vorperiode — als Grenze kennzeichnen (Beleg-Stufe), kein Pseudo-Δ bauen.
- **MoM für Ads-KPIs ist eingeschränkt:** sauber nur über Tagesverlauf-Tools (`ads_conversion_performance`); für days-only-Tools MoM als Näherung kennzeichnen oder weglassen.

Kein Δ ohne saubere Perioden-Trennung — überlappende `days`-Fenster als Vergleich zu präsentieren wäre ein Pseudo-Delta, keine „echte Zahl aus den Tools”.

---

## Google Ads (Quelle: `google_ads` verbunden)

| KPI | Tool | WoW-Auffällig ab | Deep-Dive |
|---|---|---|---|
| Spend | `ads_campaign_performance`, `ads_budget_status` | ±30 % ohne Budget-Änderung | `google-ads-audit` (Budget/Pacing) |
| Conversions | `ads_conversion_performance` | −25 % | `tracking-check` zuerst (Tracking?), dann `google-ads-audit` |
| CPA | abgeleitet (Spend/Conv) | +40 % | `google-ads-audit` |
| ROAS / Conv-Value | `ads_conversion_performance` | −25 % | `google-ads-audit` |
| Impression Share | `ads_impression_share` | Snapshot ohne Vorperiode — −10 %-Punkte nur, wenn eine Vorwochen-Messung (früherer Report) vorliegt | `google-ads-audit` (Lost IS Budget vs. Rank) |
| Klicks / CTR | `ads_campaign_performance` | ±30 % | `google-ads-audit` |

**Beleg-Stufe:** Conversions, CPA und ROAS tragen **„mit Tracking-Vorbehalt”**, solange das Tracking-Gate (unten) nicht grün ist.
**Pacing-Check:** `budget_pacing` — liegt der Monats-Spend auf Kurs? Über-/Unter-Pacing als Auffälligkeit.

---

## Social Ads (Quelle: `meta_ads` / `linkedin_ads` verbunden)

| KPI | Tool | Auffällig ab | Deep-Dive |
|---|---|---|---|
| Spend | `meta_campaign_performance` / `linkedin_campaign_performance` | ±30 % ohne Budget-Änderung | `social-ads-audit` |
| Klicks / Impressionen | `meta_campaign_performance` / `linkedin_campaign_performance` | ±30 % | `social-ads-audit` |
| Conversions | `meta_campaign_performance` / `linkedin_campaign_performance` | −25 % | `social-ads-audit` (Signal-Gate: Pixel/Events) — Site-Messung via `tracking-check` |

- Kampagnen-Inventar: `linkedin_list_campaigns` (Name, Status, Budget).
- **LinkedIn-Ebenen:** Seit 10/2025 heißt im Campaign Manager die alte „Campaign Group” jetzt **„Campaign”** und die alte „Campaign” jetzt **„Ad set”**. API und MCP-Tools nutzen weiter die alten Namen — `linkedin_list_campaigns` und `linkedin_campaign_performance` liefern also UI-„Ad sets”. Im Kunden-Report beide Namen nennen, z. B. „Kampagne (UI: Ad set)”.
- **Read-only hart:** `linkedin_update_campaign_budget` / `linkedin_update_campaign_status` sind Schreib-Tools — im Report **nie** nutzen.
- Für Δs gilt die Zeitraum-Mechanik oben: nur vergleichen, was sauber in zwei Perioden trennbar ist — sonst als Snapshot kennzeichnen.

---

## SEO / Search Console (Quelle: `search_console` verbunden)

| KPI | Tool | WoW-Auffällig ab | Deep-Dive |
|---|---|---|---|
| Klicks (organisch) | `sc_performance` (`dimensions=["date"]`) | −20 % | `seo-audit` |
| Impressionen | `sc_performance` | −25 % | `seo-audit` |
| Ø-Position | `sc_performance` | +3 Positionen schlechter | `seo-audit` (Rankings/Traffic-Einbruch) |
| Top-Query-Bewegung | `sc_top_queries` | Top-Query fällt aus Top-10 | `seo-audit` |

- **Keine Summen aus Query-Zeilen.** GSC lässt auf Query-Ebene anonymisierte Suchanfragen weg (über alle Properties ca. 47 % der Klicks, Stand 04/2025). Summen über `sc_top_queries`- oder `query`-Zeilen sind daher kleiner als die Gesamtwerte — Totals nur über `sc_performance` mit `dimensions=[]` oder `["date"]`.
- **Marke vs. Nicht-Marke (optional):** Der native GSC-Markenfilter ist im MCP nicht verfügbar. Split per `sc_performance` mit `dimension_filter` `{"dimension": "query", "operator": "includingRegex", "expression": "<marke1>|<marke2>"}` (Nicht-Marke: `excludingRegex`), Markenbegriffe aus dem Projekt-Kontext, Regex in RE2-Syntax. Beide Teile enthalten keine anonymisierten Suchanfragen — ihre Summe ist kleiner als der Gesamtwert, als Anteil ausweisen. Fallen nur die Marken-Klicks und Nicht-Marke bleibt stabil, ist das eher Marken-Nachfrage (Saison, Kampagnen, Journal) als ein Ranking-Problem: einordnen, nicht automatisch an `seo-audit` verweisen.

**Traffic-Einbruch:** Zeitlich verorten (date-Dimension), gegen bekannte Google-Update-Termine **und** bekannte Ereignisse außerhalb von Updates legen (`references/bekannte-ereignisse.md` im Plugin, z. B. Wegfall der Gratis-Produkt-Listings in der EEA ab 17.–18.09.2026) → dann `seo-audit`.

---

## Local / Google Business Profile (Quelle: `business_profile` verbunden)

| KPI | Tool | Auffällig ab | Deep-Dive |
|---|---|---|---|
| Anrufe | `gbp_performance` | −25 % | `seo-audit` (deckt `gbp_*` ab) |
| Website-Klicks | `gbp_performance` | −25 % | `seo-audit` |
| Routenanfragen | `gbp_performance` | −25 % | `seo-audit` |
| Impressionen (Maps/Suche) | `gbp_performance` | −25 % | `seo-audit` |

Für lokale Kunden (Praxis, Bäckerei, Handwerk) sind das Kern-Zahlen — oft wichtiger als Website-KPIs. Niedrig-Volumen-Regel gilt hier besonders (wenige Anrufe/Woche = Rauschen).

---

## Web / GA4 (Quelle: `ga4` verbunden)

| KPI | Tool | WoW-Auffällig ab | Deep-Dive |
|---|---|---|---|
| Sessions | `ga4_report` / `ga4_traffic_sources` | ±25 % | Kanal isolieren (organisch/paid/direct) |
| Conversions / Key Events | `ga4_conversions` | −25 % | `tracking-check` (kommen Events an?) |
| Engagement-Rate | `ga4_report` (`engagementRate`) | −15 %-Punkte | `seo-audit` (Landingpage/UX) |
| Traffic nach Quelle | `ga4_traffic_sources` (`sessionSource`) | Kanal bricht weg | je nach Kanal an Ads/SEO |

---

## GEO / AI-Sichtbarkeit (WoW-KPI bei DataForSEO-Zugang, sonst Näherung, nur wenn relevant)

| KPI | Tool | WoW-Auffällig ab | Deep-Dive |
|---|---|---|---|
| Mentions / Citations / Share-of-Voice | `dfs_llm_mentions_metrics` (max. 10 Marken-/Themen-Keywords pro Call) | Share-of-Voice −20 %-Punkte oder Mentions halbieren sich | `geo-audit` |

- **Pay-as-you-go, kein Abo:** `dfs_llm_mentions_metrics` läuft über das normale DataForSEO-Guthaben. Liefert der Call `{"error": "subscription_required", ...}` (Zugriffsproblem, z. B. Guthaben aufgebraucht), auf die alte Näherung degradieren: `ga4_traffic_sources` (days≥28, nach `sessionSource`) → AI-Referrer (chatgpt.com, perplexity.ai, copilot.microsoft.com/copilot.com, gemini) grob quantifizieren. **Näherung, kein Fetch-/Zitat-Beweis** — als beratend kennzeichnen.
- **AI-Referrer-Key-Events:** Neben der Session-Menge auch die Key Events der AI-Referrer ausweisen — `ga4_traffic_sources` liefert keine Key Events, deshalb `ga4_report` mit `dimensions=["sessionSource"]`, `metrics=["sessions", "keyEvents"]` und `start_date`/`end_date` je Periode; die AI-Referrer-Zeilen herausgreifen. Das ist der Business-Nachweis zur Menge, bleibt aber **beratend** (Referrer fehlen oft, Consent-Lücken).
- **Lag:** Index nicht tagesaktuell; die genaue Lag-Dauer ist nicht über die DataForSEO-Docs API-verifiziert — bei WoW-Vergleichen kurz vor dem Report-Stichtag entsprechend vorsichtig sein.
- Auffällig: AI-Traffic/Mentions verschwinden oder verdoppeln sich → `geo-audit`.

---

## Tracking-Health (Gate, kurz — nicht die Tiefe)

Plausibilitäts-Check über `ads_conversion_performance` (`last_gap_days`) + `ga4_conversions`. Konkrete Gate-Schwellen:
- `last_gap_days` > 7 (trotz laufendem Spend) = **Verdacht** — im Report kennzeichnen.
- Conversions bei 0 trotz Spend **oder** Ads-vs-GA4-Klaffung > Faktor 2 = **Blocker** — ganz oben im Report markieren, auf `tracking-check` verweisen.
- Solange das Gate nicht grün ist: Conversions/CPA/ROAS mit Beleg-Stufe **„mit Tracking-Vorbehalt”** ausweisen.
- **DACH-Consent-Vorbehalt:** Fehlende Einwilligung drückt GA4- und Ads-Zahlen unterschiedlich stark. Consent Mode **Basic** modelliert nur mit einem allgemeinen Modell; **Advanced** nutzt Pings vor der Einwilligung, braucht aber eine Mindest-Datenmenge, die kleine DACH-Konten mit niedriger Einwilligungsrate oft nicht erreichen. Ein Teil der Ads-vs-GA4-Klaffung ist dann Consent, kein Defekt — im Report so benennen; die Prüfung bleibt bei `tracking-check`.

---

## WoW-Interpretation (Fallstricke)
- **Kurze Zeiträume schwanken.** Primär-Anker ist Googles eigener Wert: Smart-Bidding-Performance erst über Zeiträume mit mind. **30 Conversions** bewerten (**50** bei tROAS; https://support.google.com/google-ads/answer/7065882). Liegt die Woche darunter (erst recht unter ~20), ist ein WoW-Delta oft Rauschen — als „zu wenig Daten für belastbaren Trend” kennzeichnen, nicht als Trend verkaufen, und das Fenster verlängern (MoM oder 4 Wochen rollierend) statt das WoW-Δ zu bewerten.
- **Attributions-Lag:** die letzten 1–3 Tage sind unvollständig (Conversions tropfen nach). Frische Kurzfenster nicht hart bewerten.
- **Saisonalität / Feiertage:** DACH-Feiertage (regional unterschiedlich AT/CH/DE) und Wochenend-Muster erklären viele Deltas — vor dem Alarm prüfen.
- **Eine Auffälligkeit ≠ eine Ursache.** Der Report zeigt *dass* etwas auffällt und *wo* man tiefer schaut — die Ursache findet der jeweilige Audit.

## Schwellen sind Richtwerte, kein Gesetz
Die %-Schwellen oben sind Ausgangspunkte für „lohnt einen Blick”, kalibriert auf mittlere Konten. Bei sehr großen/kleinen Konten anpassen. Immer die absolute Größe mitdenken (−30 % von 3 Conversions ist kein Notfall).
