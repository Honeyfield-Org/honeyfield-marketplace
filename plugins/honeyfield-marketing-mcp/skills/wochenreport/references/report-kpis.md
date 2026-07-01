# Report-KPIs & Anomalie-Schwellen

Referenz für `wochenreport`. Pro Kanal: welche KPIs, welche Tools, was ein auffälliges WoW-Delta ist, und welcher Audit-Skill die Tiefe übernimmt. On-demand laden.

**Grundprinzip:** Der Report zieht die **Kern-KPIs** (nicht die Audit-Tiefe) und macht sie WoW-vergleichbar. Auffälligkeiten werden **markiert und an den passenden Audit-Skill verwiesen** — der Report diagnostiziert nicht selbst.

---

## Beleg-Stufen (wie in den Audits)
- **Gemessen:** harte Zahlen aus dem Konto/der Property (Ads-Spend, GSC-Klicks, GA4-Sessions).
- **Beratend:** GEO/AI-Sichtbarkeit (GA4-Referrer = Näherung, kein Fetch-Beweis).
Jede Report-Zeile trägt die Stufe implizit über die Quelle; AI-Traffic explizit als Näherung kennzeichnen.

---

## Google Ads (Quelle: `google_ads` verbunden)

| KPI | Tool | WoW-Auffällig ab | Deep-Dive |
|---|---|---|---|
| Spend | `ads_campaign_performance`, `ads_budget_status` | ±30 % ohne Budget-Änderung | `google-ads-audit` (Budget/Pacing) |
| Conversions | `ads_conversion_performance` | −25 % | `tracking-check` zuerst (Tracking?), dann `google-ads-audit` |
| CPA | abgeleitet (Spend/Conv) | +40 % | `google-ads-audit` |
| ROAS / Conv-Value | `ads_conversion_performance` | −25 % | `google-ads-audit` |
| Impression Share | `ads_impression_share` | −10 %-Punkte | `google-ads-audit` (Lost IS Budget vs. Rank) |
| Klicks / CTR | `ads_campaign_performance` | ±30 % | `google-ads-audit` |

**Pacing-Check:** `budget_pacing` — liegt der Monats-Spend auf Kurs? Über-/Unter-Pacing als Auffälligkeit.
**Anomalie-Assist:** `anomaly_check` kann statistische Ausreißer vorschlagen — als Hinweis nutzen, nicht als alleinige Wahrheit.

---

## SEO / Search Console (Quelle: `search_console` verbunden)

| KPI | Tool | WoW-Auffällig ab | Deep-Dive |
|---|---|---|---|
| Klicks (organisch) | `sc_performance` (`dimensions=["date"]`) | −20 % | `seo-audit` |
| Impressionen | `sc_performance` | −25 % | `seo-audit` |
| Ø-Position | `sc_performance` | +3 Positionen schlechter | `seo-audit` (Rankings/Traffic-Einbruch) |
| Top-Query-Bewegung | `sc_top_queries` | Top-Query fällt aus Top-10 | `seo-audit` |

**Traffic-Einbruch:** Zeitlich verorten (date-Dimension), gegen bekannte Google-Update-Termine legen → dann `seo-audit`.

---

## Web / GA4 (Quelle: `ga4` verbunden)

| KPI | Tool | WoW-Auffällig ab | Deep-Dive |
|---|---|---|---|
| Sessions | `ga4_report` / `ga4_traffic_sources` | ±25 % | Kanal isolieren (organisch/paid/direct) |
| Conversions / Key Events | `ga4_conversions` | −25 % | `tracking-check` (kommen Events an?) |
| Engagement-Rate | `ga4_report` (`engagementRate`) | −15 %-Punkte | `seo-audit` (Landingpage/UX) |
| Traffic nach Quelle | `ga4_traffic_sources` (`sessionSource`) | Kanal bricht weg | je nach Kanal an Ads/SEO |

---

## GEO / AI-Sichtbarkeit (beratend, nur wenn relevant)

- `ga4_traffic_sources` (days≥28, nach `sessionSource`) → AI-Referrer (chatgpt.com, perplexity.ai, copilot.microsoft.com/copilot.com, gemini) grob quantifizieren. **Näherung, kein Fetch-Beweis** — als beratend kennzeichnen.
- Auffällig: AI-Traffic verschwindet oder verdoppelt sich → `geo-audit`.

---

## Tracking-Health (Gate, kurz — nicht die Tiefe)

- Kurzer Plausibilitäts-Check: kommen Conversions überhaupt an? `ads_conversion_performance` (`last_gap_days`) + `ga4_conversions`. Wenn Conversions bei 0 / großer Ads-vs-GA4-Klaffung → **oben im Report als Blocker markieren** und auf `tracking-check` verweisen (ohne den würde jede andere Zahl im Report auf Sand stehen).

---

## WoW-Interpretation (Fallstricke)
- **Kurze Zeiträume schwanken.** Bei niedrigem Volumen (< ~20 Conversions/Woche) ist ein WoW-Delta oft Rauschen — als „zu wenig Daten für belastbaren Trend" kennzeichnen, nicht als Trend verkaufen.
- **Attributions-Lag:** die letzten 1–3 Tage sind unvollständig (Conversions tropfen nach). Frische Kurzfenster nicht hart bewerten.
- **Saisonalität / Feiertage:** DACH-Feiertage (regional unterschiedlich AT/CH/DE) und Wochenend-Muster erklären viele Deltas — vor dem Alarm prüfen.
- **Eine Auffälligkeit ≠ eine Ursache.** Der Report zeigt *dass* etwas auffällt und *wo* man tiefer schaut — die Ursache findet der jeweilige Audit.

## Schwellen sind Richtwerte, kein Gesetz
Die %-Schwellen oben sind Ausgangspunkte für „lohnt einen Blick", kalibriert auf mittlere Konten. Bei sehr großen/kleinen Konten anpassen. Immer die absolute Größe mitdenken (−30 % von 3 Conversions ist kein Notfall).
