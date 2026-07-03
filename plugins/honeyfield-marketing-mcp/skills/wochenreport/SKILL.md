---
name: wochenreport
description: "Erstellt einen kanalübergreifenden Wochen- oder Monatsreport für einen Kunden — zieht die Kern-KPIs aus allen verbundenen Kanälen (Google Ads, Meta/LinkedIn Ads, Search Console, GA4, Google Business Profile, AI-Sichtbarkeit) und stellt sie als Zeitraum-Vergleich (Woche-über-Woche / Monat-über-Monat) zusammen. Nutze diesen Skill für regelmäßiges Reporting: „Wochenreport”, „Monatsreport”, „wie lief die Woche”, „wie war der Monat”, „KPI-Übersicht”, „Performance-Report”, „Reporting für Kunde X”, „fass mir die Zahlen zusammen”, „Report erstellen”. Read-only — der Report ändert nichts am Konto. Er orchestriert statt zu duplizieren: bei Auffälligkeiten verweist er auf den passenden Audit. Für die tiefe Diagnose eines konkreten Problems nutze direkt `google-ads-audit` (bezahlte Suche), `seo-audit` (organisch), `geo-audit` (KI-Sichtbarkeit) oder `tracking-check` (Conversion-Tracking). Kalibriert auf DACH (DE/AT/CH)."
metadata:
  version: 0.3.0
---

# Wochenreport

Du erstellst einen **kanalübergreifenden Report** für einen Kunden — kompakt, ehrlich, entscheidungs-orientiert. Ziel ist nicht die tiefe Diagnose (das leisten die Audit-Skills), sondern ein schneller, belastbarer Überblick: **Was hat sich diese Periode bewegt, wo lohnt ein genauerer Blick?**

Zwei Eigenschaften definieren diesen Skill:
- **Read-only.** Ein Report schreibt nichts ins Konto. Keine Schreib-Aktionen, kein Operator — nur lesen und zusammenstellen.
- **Orchestrieren, nicht duplizieren.** Du ziehst die **Kern-KPIs** jedes Kanals (nicht die Audit-Tiefe) und machst sie zeitraum-vergleichbar. Fällt etwas auf, **markierst du es und verweist auf den zuständigen Audit-Skill** — du diagnostizierst die Ursache nicht selbst.

**Drei Beleg-Stufen:** **gemessen** (harte Zahlen aus Konto/Property, inkl. AI-Sichtbarkeit über `dfs_llm_mentions_metrics` bei aktivem DataForSEO-AI-Optimization-Abo); **mit Tracking-Vorbehalt** (abhängige KPIs wie CPA/ROAS, solange das Conversion-Tracking unklar ist — nicht als belastbar verkaufen); **beratend** (AI-Sichtbarkeit über GA4-Referrer = Näherung, kein Beweis — Default ohne Abo, sonst Ergänzung). Kennzeichne, welcher Pfad greift.

## Schritt 0 — Vorbereitung (immer zuerst)

**Projekt-Kontext zuerst.** Liegt für dieses Projekt ein Projekt-Kontext vor — als **Projektwissen** in diesem Claude-Projekt oder als `projekt-kontext.md` im Arbeitsverzeichnis —, nutze ihn, bevor du fragst, und frage nur nach, was dort fehlt oder für diese Aufgabe spezifisch ist. Beachte gesetzte `compliance`-Flags als harte Leitplanke. Fehlt der Kontext, biete an, ihn per `projekt-kontext` anzulegen, oder frage knapp: welcher Kunde/Workspace, welcher Zeitraum, welche Ziel-KPIs.

**Workspace + Datenquellen klären.** Rufe `list_workspaces` auf und prüfe die `sources` des Ziel-Workspace. **Der Report ist adaptiv:** Nimm nur die Kanäle auf, deren Quelle verbunden ist. Fehlt eine Quelle (z.B. kein `search_console`), nenne sie als Lücke im Report — rate keine Zahlen zusammen.
- `google_ads` → Ads-Block · `meta_ads` / `linkedin_ads` → Social-Ads-Block · `search_console` → SEO-Block · `business_profile` → Local-Block · `ga4` → Web-Block · `dataforseo` → AI-Sichtbarkeit als echte KPI (`dfs_llm_mentions_metrics`, unabhängig von `ga4`); ohne `dataforseo` (oder bei `subscription_required`) fällt AI-Sichtbarkeit auf die `ga4`-Referrer-Näherung zurück — fehlen beide Quellen, entfällt der Block ganz.

**Zeitraum festlegen.** Default: letzte abgeschlossene **Woche** (ISO-KW, Mo–So) vs. Vorwoche (WoW). Auf Wunsch Monat vs. Vormonat (MoM) oder frei. **Attributions-Lag beachten:** die letzten 1–3 Tage sind unvollständig — entweder ausklammern oder als vorläufig kennzeichnen. Viele Tools nehmen nur `days` (Fenster endet heute) — wie die Vorperiode je Tool sauber zu beschaffen ist: **Zeitraum-Mechanik in `references/report-kpis.md` (Pflicht vor jedem Δ).**

**Markt (DE/AT/CH)** für Feiertags-/Saisonkontext (regionale Feiertage AT/CH/DE unterscheiden sich).

## Report-Aufbau (adaptiv, nur verbundene Kanäle)

Arbeite die verbundenen Kanäle durch und ziehe je die Kern-KPIs mit Zeitraum-Vergleich. Welche KPIs, welche Tools, ab wann ein Delta auffällt und welcher Audit die Tiefe übernimmt: **`references/report-kpis.md`** (bei Bedarf laden).

1. **Tracking-Health (Gate, zuerst).** Kurzer Plausibilitäts-Check: kommen Conversions überhaupt an (`ads_conversion_performance` `last_gap_days`, `ga4_conversions`)? Bei totem Tracking / großer Ads-vs-GA4-Klaffung: **ganz oben als Blocker markieren** + auf `tracking-check` verweisen — sonst steht jede weitere Zahl auf Sand.
2. **Google Ads** (`ads_campaign_performance`, `ads_conversion_performance`, `ads_impression_share`, `ads_budget_status`/`budget_pacing`): Spend, Conversions, CPA, ROAS, Klicks/CTR — je mit WoW-Δ nach der Zeitraum-Mechanik; Impression Share als **Snapshot ohne Vorperiode** kennzeichnen.
3. **Social Ads (Meta/LinkedIn)** (`meta_campaign_performance`, `linkedin_campaign_performance`): Impressionen, Klicks, Spend, Conversions. **Read-only bleibt hart:** `linkedin_update_campaign_budget`/`linkedin_update_campaign_status` nie nutzen.
4. **SEO / Search Console** (`sc_performance`, `sc_top_queries`, `sc_top_pages`): Klicks, Impressionen, Ø-Position, Top-Query-Bewegung.
5. **Local / Google Business Profile** (`gbp_performance`): Anrufe, Website-Klicks, Routenanfragen, Impressionen (Maps/Suche) — für lokale Kunden Kern-Zahlen.
6. **Web / GA4** (`ga4_report`, `ga4_conversions`, `ga4_traffic_sources`): Sessions, Conversions/Key Events, Engagement, Traffic nach Quelle.
7. **AI-Sichtbarkeit** (`dfs_llm_mentions_metrics`, max. 10 Marken-/Themen-Keywords pro Call): Mentions/Citations/Share-of-Voice als WoW-KPI (Index nicht tagesaktuell, Lag nicht API-verifiziert — bei Stichtag-nahen WoW-Vergleichen vorsichtig sein). Ohne aktives DataForSEO-AI-Optimization-Abo (`subscription_required`) Degradation auf `ga4_traffic_sources` (`sessionSource`, days≥28) — grobe AI-Referrer-Menge, dann explizit als **beratend/Näherung** kennzeichnen.

**Anomalie-Assist:** `anomaly_check` / `budget_pacing` können Ausreißer vorschlagen — als Hinweis nutzen, nicht als alleinige Wahrheit.

## Anomalien → Deep-Dives (der Kern der Hub-Rolle)

Für jede Auffälligkeit: **benennen (mit Zahl + Δ), einordnen (Kontext/Fallstrick prüfen), verweisen.** Nicht selbst tief diagnostizieren.
- Conversions/Tracking auffällig → `tracking-check` zuerst, dann der Kanal.
- Spend/CPA/ROAS/Impression-Share → `google-ads-audit`.
- Organische Klicks/Position/Traffic-Einbruch → `seo-audit`.
- Local (GBP-Anrufe/Klicks/Routen) auffällig → `seo-audit` (deckt `gbp_*` ab).
- Social Ads (Meta/LinkedIn) auffällig → ehrlich benennen: (noch) kein Audit-Skill vorhanden — nur berichten und markieren.
- AI-Sichtbarkeit weg/verändert → `geo-audit`.

**Vor dem Alarm prüfen (report-kpis.md):** niedriges Volumen = Rauschen (kein Trend behaupten), Attributions-Lag, DACH-Feiertage/Saison. Eine Auffälligkeit sagt *dass* und *wo* — nicht *warum*.

## Output-Format
1. **Executive Summary** (3–5 Sätze): Gesamtbild der Periode + die 2–3 wichtigsten Bewegungen + offene Blocker (z.B. Tracking).
2. **KPI-Tabelle je Kanal:** KPI · aktuelle Periode · Vorperiode · **Δ (% + Richtung)** · Beleg-Stufe. Nur verbundene Kanäle.
3. **Auffälligkeiten:** je Befund kurz — was, wie groß, wahrscheinlicher Kontext, **empfohlener Deep-Dive (welcher Audit-Skill)**.
4. **Was gut lief** (kurz — Reports sind oft zu negativ; nenne die positiven Bewegungen belegt).

Halte den Report scanbar (Tabellen, kurze Bullets). Jede Zahl ist echt aus den Tools — kein „ungefähr".

## Grenzen (ehrlich benennen)
- **Read-only** — dieser Skill ändert nie etwas; Fixes laufen über die Audit-Skills.
- **Keine Ursachen-Diagnose** — der Report zeigt Bewegungen und wo man tiefer schaut, nicht warum (das ist Audit-Arbeit).
- Delta-Fallstricke (niedriges Volumen = Rauschen, Attributions-Lag, Saison): `references/report-kpis.md`.
- **Nicht jedes Tool liefert eine Vorperiode** — viele nehmen nur `days` (Fenster endet heute). Deltas nur nach der Zeitraum-Mechanik in `references/report-kpis.md` bilden; `ads_impression_share` bleibt Snapshot, MoM ist für Ads-KPIs nur über Tagesverlauf-Tools sauber.
- AI-Sichtbarkeit ist bei aktivem AI-Optimization-Abo eine echte WoW-KPI (`dfs_llm_mentions_metrics`); ohne Abo bleibt sie Näherung über GA4-Referrer, kein Fetch-/Zitat-Beweis.
- Für Social Ads (Meta/LinkedIn) existiert kein Audit-Skill — der Report kann berichten, aber keinen Deep-Dive empfehlen.
- Nur verbundene Kanäle — fehlende Quellen sind Lücken, keine Nullen.

## Tools nach Kanal
- Ads: `ads_campaign_performance`, `ads_conversion_performance`, `ads_impression_share`, `ads_budget_status`, `budget_pacing`, `anomaly_check`
- Social Ads (read-only): `meta_campaign_performance`, `linkedin_campaign_performance`, `linkedin_list_campaigns`
- SEO: `sc_performance`, `sc_top_queries`, `sc_top_pages`
- Local: `gbp_performance`
- Web/AI: `ga4_report`, `ga4_conversions`, `ga4_traffic_sources`, `dfs_llm_mentions_metrics` (AI-Sichtbarkeit, Subscription-gated — Fallback `ga4_traffic_sources`)
- Vorbereitung: `list_workspaces`

## Verwandte Skills
`projekt-kontext` (Foundation, zuerst lesen) · `google-ads-audit` · `seo-audit` · `geo-audit` · `tracking-check` — der Report **verweist** bei Auffälligkeiten auf diese; sie liefern die Tiefe, die der Report bewusst auslässt.

## Referenzen
- `references/report-kpis.md` — Zeitraum-Mechanik (Vorperioden-Beschaffung je Tool), KPIs + Tools je Kanal, Anomalie-Schwellen (Richtwerte), WoW-Fallstricke, Verweis-Logik.
