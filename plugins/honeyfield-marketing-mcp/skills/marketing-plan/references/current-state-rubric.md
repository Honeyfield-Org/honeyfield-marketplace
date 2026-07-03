# Current-State-Rubric — 10 Dimensionen, 0–5 aus Live-Daten

Herzstück von Phase 1 des `marketing-plan`-Skills. Sie macht den Ist-Zustand eines Kunden **messbar aus echten MCP-Daten** statt aus Selbstauskunft. Jede Dimension wird 0–5 gescort, mit Beleg und Beleg-Stufe. Detail-Diagnose passiert hier nicht — dafür gibt es die unter „Tiefe” genannten Topic-Skills.

## Scoring-Regeln

- **Jeder Score trägt eine Beleg-Stufe** (identisch zu den Stufen der SKILL.md):
  - **gemessen** — Score aus einer verbundenen MCP-Quelle mit konkreter Zahl/Beobachtung.
  - **mit Tracking-Vorbehalt** — Aussage hängt an Conversion-Tracking, das unvollständig sein kann (v.a. CPA/ROAS/Conversion-Zahlen).
  - **beratend** — Heuristik, Proxy-Signal oder Selbstauskunft; keine belastbaren Live-Daten.
- **Score immer mit Beleg.** Nie aus dem Bauch — nenne die konkrete Zahl oder Beobachtung aus dem genannten Tool.
- **Kein Diagnostizieren.** Der Score sagt, *wo* der Kunde steht, nicht *warum*. Ursache und Fix gehören dem unter „Tiefe” genannten Topic-Skill — hier nur verweisen.
- **Tracking-Gate.** Conversion-Tracking-Fundament (Dimension 1) ist die Gate-Dimension. Bei Score ≤2 sind Conversions/CPA/ROAS unzuverlässig — jede darauf gestützte Aussage (v.a. Paid-Search-Effizienz, Social-Ads-Reife) trägt zwingend den **Tracking-Vorbehalt** und wird nicht als „gemessen” verkauft.
- **Fehlende Quelle ≠ Score 0.** Ist die Quelle nicht verbunden, greift der dimensionsspezifische Fallback (Lücke benennen oder auf beratend degradieren). Eine nicht messbare oder strategisch irrelevante Dimension wird **nicht** als Schwäche gewertet.
- **Nur Lese-Tools.** Die Rubric verändert nichts am Konto.

---

## 1. Conversion-Tracking-Fundament (Gate)

**Was wird bewertet:** Ob überhaupt verlässlich gemessen wird, was zählt (Leads, Käufe, Anrufe) — das Fundament, auf dem jede Effizienz-Aussage des Plans steht.

**0–5-Anker (DACH-KMU):**
- 0 = Keine aktive Conversion-Aktion; weder Ads noch GA4 zählen ein zählbares Ereignis.
- 1 = Conversion-Aktionen existieren, feuern aber nicht (Counts = 0) oder nur „Seitenaufruf” als Pseudo-Conversion.
- 2 = Eine Quelle zählt, die andere nicht (z.B. GA4 ja, Ads-Import nein) oder die Zahlen driften stark auseinander.
- 3 = Zentrale Conversion (Kontakt/Kauf/Anruf) feuert konsistent in mindestens einer Quelle; Wert/Zuordnung teils unklar.
- 4 = Conversions feuern konsistent, GA4 und Ads plausibel deckungsgleich, Micro und Macro getrennt.
- 5 = Sauberes Setup: Macro-Conversions mit Wert, konsistent über GA4 + Ads, dedupliziert, primär/sekundär korrekt.

**Beleg:** `ads_conversion_performance` (feuern die Conversion-Aktionen, Counts > 0 je Aktion?) + `ga4_conversions` (Conversion-/Key-Event-Counts > 0 und plausibel?). Zählwert: Anzahl aktiver, feuernder Conversion-Aktionen und ob beide Quellen dieselbe Größenordnung zeigen. Beleg-Stufe: **gemessen**.

**Fallback wenn Quelle fehlt:** Weder `google_ads` noch `ga4` verbunden → Dimension als **Lücke** benennen (Gate „unbekannt”), NICHT auf beratend degradieren — ohne funktionierendes Gate tragen alle Effizienz-Dimensionen den Tracking-Vorbehalt. Nur eine der beiden Quellen verbunden → damit scoren, die Deckungsgleich-Kriterien entfallen (Score dann max. 3).

**Tiefe:** `tracking-check`.

---

## 2. Organische Sichtbarkeit

**Was wird bewertet:** Wie sichtbar die Website in der organischen Google-Suche ist — jenseits des eigenen Markennamens.

**0–5-Anker (DACH-KMU):**
- 0 = Nicht indexiert / keine GSC-Klicks; rankt für nichts.
- 1 = Nur für den eigenen Markennamen sichtbar, kein generischer Traffic.
- 2 = Ein paar generische Keywords ranken, aber überwiegend Seite 2+; Klicks marginal.
- 3 = Solide Marken-Sichtbarkeit plus erste generische Money-Keywords auf Seite 1; GSC-Klicks wachsen langsam.
- 4 = Mehrere relevante Nicht-Marken-Keywords auf Seite 1, spürbarer organischer Nicht-Marken-Traffic, thematische Cluster erkennbar.
- 5 = Organik ist ein tragender Kanal: breite Seite-1-Abdeckung der Money-Keywords, stabil wachsende Klicks, klare Themen-Cluster.

**Beleg:** `sc_performance` (organische Klicks/Impressionen, Marken- vs. Nicht-Marken-Split, durchschnittliche Position) + `dfs_keyword_rankings` (für wie viele Keywords rankt die Domain, wie viele davon in Top 10). Zählwert: Anteil Nicht-Marken-Klicks + Anzahl Keywords in Top 10. Beleg-Stufe: **gemessen**.

**Fallback wenn Quelle fehlt:** Keine `search_console`-Quelle → allein auf `dfs_keyword_rankings` stützen (extern gemessen, bleibt **gemessen**, ohne Marken-/Nicht-Marken-Split). Auch keine `dataforseo`-Quelle → Dimension als **Lücke** benennen.

**Tiefe:** `seo-audit`.

---

## 3. Paid-Search-Effizienz

**Was wird bewertet:** Ob bezahlte Google-Suche strukturiert läuft und Budget in messbare Ergebnisse fließt — nicht, warum einzelne Kampagnen schwächeln.

**0–5-Anker (DACH-KMU):**
- 0 = Keine aktiven Such-Kampagnen (mit Paid-Budget-Ziel eine Lücke; ohne Paid-Ziel neutral — siehe Fallback).
- 1 = Kampagnen laufen, aber ohne Conversion-Ziel/Tracking — Budget fließt blind.
- 2 = Kampagnen mit Conversion-Ziel, aber hoher Streuverlust / niedriger Impression Share / kaum Conversions.
- 3 = Kampagnen konvertieren, aber messbar unter Potenzial: Ziel-CPA (laut projekt-kontext) verfehlt **oder** Impression-Share-Verlust überwiegend Budget-bedingt.
- 4 = Ziel-CPA gehalten, Impression-Share-Verlust überwiegend Rang- statt Budget-bedingt, wenig offensichtlicher Streuverlust.
- 5 = Effizienter Paid-Search-Motor: guter CPA, hoher Impression Share auf Money-Terms, Budget nicht durch Rank/Budget-Limit gedeckelt.

**Beleg:** `ads_campaign_performance` (Spend, Conversions, CPC, CTR) + `ads_impression_share` (Search Impression Share + Budget-/Rank-Verlust). Zählwert: Conversions je Kampagne + CPA vs. Ziel-CPA + Impression Share inkl. Budget-/Rang-Verlust-Split. Fehlt ein Ziel-CPA im projekt-kontext, CPA am Ø-Kundenwert einordnen und das Fehlen als offene Entscheidung notieren. Beleg-Stufe: **gemessen**; bei Gate-Score ≤2 nur Volumen/Impression-Share bewerten, alle CPA-/Conversion-Aussagen tragen den **Tracking-Vorbehalt**.

**Fallback wenn Quelle fehlt:** Keine `google_ads`-Quelle → **Lücke** benennen. Kein Paid-Search-Budget/-Ziel laut projekt-kontext → als **N/A** markieren (Score 0 ohne Wertung als Schwäche — spiegelt die Strategie, nicht ein Versäumnis).

**Tiefe:** `google-ads-audit`.

---

## 4. Social-Ads-Reife

**Was wird bewertet:** Reifegrad bezahlter Kampagnen auf Meta/LinkedIn — laufen strukturierte Kampagnen mit Ziel, oder nur Boost-Posts ohne System.

**0–5-Anker (DACH-KMU):**
- 0 = Keine bezahlten Social-Kampagnen.
- 1 = Nur vereinzelte Boost-Posts, kein Kampagnen-Ziel, kein Pixel/Tracking.
- 2 = Kampagnen laufen mit Ziel, aber ohne sauberes Conversion-Signal (Pixel feuert nicht / nur auf Reichweite optimiert).
- 3 = Strukturierte Kampagnen mit Conversion-Ziel und feuerndem Pixel; erste Conversions, Creatives dünn.
- 4 = Mehrere Adsets/Zielgruppen getestet, Conversions kommen konsistent, Creatives werden iteriert.
- 5 = Reifes Setup: klare Kampagnenstruktur, getestete Zielgruppen, konsistente Conversions, laufende Creative-Iteration.

**Beleg:** `meta_campaign_performance` bzw. `linkedin_campaign_performance` (Spend, Impressionen, Klicks, Conversions). Zählwert: Anzahl aktiver Kampagnen mit Conversion-Ziel + ob Conversions ankommen. Ehrlich: Diese Daten liefern **kein ROAS/keine Frequency** — nicht auf ROAS scoren. Beleg-Stufe: **gemessen**; bei Gate-Score ≤2 oder nicht feuerndem Pixel tragen Conversion-Aussagen den **Tracking-Vorbehalt**.

**Fallback wenn Quelle fehlt:** Weder `meta_ads` noch `linkedin_ads` verbunden → Dimension als **Lücke** benennen (nicht raten). Kein Social-Paid-Ziel laut projekt-kontext → **N/A** (Score 0 ohne Schwäche-Wertung).

**Tiefe:** `social-ads-audit`.

---

## 5. Content-Fundament

**Was wird bewertet:** Ob die Website inhaltlich die Themen abdeckt, nach denen die Zielgruppe sucht — Breite und Ziehkraft des Content-Bestands, nicht die Detail-Gap-Diagnose.

**0–5-Anker (DACH-KMU):**
- 0 = Reine Visitenkarten-Site, kaum indexierbarer Inhalt, kein Blog/Ratgeber.
- 1 = Ein paar statische Seiten, keine Content-Fläche zu Suchintentionen.
- 2 = Blog/Ratgeber existiert, aber dünn/veraltet, zieht kaum organische Klicks.
- 3 = Aktive Content-Fläche zu Kernthemen; einige Seiten ziehen organische Klicks; erkennbare Lücken zum Keyword-Bedarf.
- 4 = Breite Abdeckung der Kernthemen, mehrere Seiten mit stabilen Klicks, wenige große Lücken.
- 5 = Content deckt das Themenfeld weitgehend ab, viele ziehende Seiten, nur kleine Rest-Gaps.

**Beleg:** `sc_top_pages` (wie viele Seiten ziehen organische Klicks/Impressionen?) + `dfs_keyword_ideas_for_domain` (Themen-/Keyword-Bedarf vs. Bestand = grobe Gap-Menge). Zählwert: Anzahl Seiten mit nennenswerten Klicks im Verhältnis zur Größe des ungedeckten Themen-Bedarfs. Beleg-Stufe: **gemessen**.

**Fallback wenn Quelle fehlt:** Keine `search_console`-Quelle → Bestand grob über `dfs_keyword_ideas_for_domain` schätzen, aber als **beratend** kennzeichnen (kein Klick-Beleg für Ziehkraft). Auch keine `dataforseo`-Quelle → **Lücke** benennen.

**Tiefe:** `content-strategie` (Themen-Backlog/Briefs); Competitor-Gap-Diagnose → `seo-audit`.

---

## 6. Local Presence

**Was wird bewertet:** Sichtbarkeit im lokalen Google-Umfeld (Maps/Local Pack, Business-Profil) — für Kunden mit physischem Einzugsgebiet der zentrale Kanal.

**0–5-Anker (DACH-KMU):**
- 0 = Kein (beanspruchtes) Google-Business-Profil.
- 1 = Profil existiert, aber unvollständig (fehlende Kategorie/Öffnungszeiten/Fotos), kaum Bewertungen.
- 2 = Profil grundständig gepflegt, aber schwache Local-Pack-Sichtbarkeit und wenige/alte Bewertungen.
- 3 = Vollständiges Profil, regelmäßige Impressionen/Aktionen, solide Bewertungsbasis; Local-Pack-Position durchwachsen.
- 4 = Gut gepflegtes Profil, gute Local-Pack-Präsenz für Kern-Keywords, aktiver Bewertungsfluss.
- 5 = Dominante lokale Präsenz: Top-Local-Pack für Money-Keywords, viele frische Bewertungen, vollständiges optimiertes Profil.

**Beleg:** `gbp_performance` (Impressionen Maps/Suche, Anrufe, Website-Klicks, Routenanfragen) + `gbp_local_seo_audit` (Profil-Vollständigkeits-Score über Kategorien, Beschreibung, Öffnungszeiten, Attribute, Reviews, Fotos ≥3, Post ≤30 Tage — **kein NAP-/Citation-Abgleich**; Review-/Foto-/Post-Checks laufen unbewertet, wenn die v4-API nicht freigeschaltet ist). Zählwert: Vollständigkeits-Score + Aktions-Volumen (Anrufe + Website-Klicks + Routenanfragen). Beleg-Stufe: **gemessen**.

**Fallback wenn Quelle fehlt:** Keine `business_profile`-Quelle → laut projekt-kontext prüfen, ob ein lokales Geschäft relevant ist: relevant → **Lücke** benennen (ein fehlendes/unverbundenes Profil ist selbst ein Befund); rein online/überregional → **N/A** ohne Schwäche-Wertung.

**Tiefe:** `seo-audit` (Local-SEO-Teil).

---

## 7. AI-Sichtbarkeit

**Was wird bewertet:** Ob die Marke in Antworten generativer Suchsysteme (ChatGPT, Perplexity, Google AI Overviews) auftaucht — die entstehende Sichtbarkeitsebene neben der klassischen SERP.

**0–5-Anker (DACH-KMU):**
- 0 = In keiner LLM-Antwort zu relevanten Themen erwähnt oder zitiert.
- 1 = Nur bei direkter Markenabfrage erwähnt, nie bei generischen Themen-Prompts.
- 2 = Vereinzelte Erwähnungen ohne Zitation/Link, kein Muster.
- 3 = Bei mehreren Themen-Prompts erwähnt, teils mit Quellen-Zitation; Share-of-Voice niedrig.
- 4 = Regelmäßig erwähnt und zitiert über mehrere Engines, spürbarer Share-of-Voice.
- 5 = Feste Referenz im Themenfeld: hoher Share-of-Voice, häufig zitiert über ChatGPT/Perplexity/Gemini.

**Beleg:** `dfs_llm_mentions_metrics` (Mentions je Engine, Gesamt-Citations, Share-of-Voice zu Kern-Prompts; ~$0.10/Call). Zählwert: Share-of-Voice + Zahl der Engines mit Erwähnung. Beleg-Stufe: **gemessen**.

**Fallback wenn Quelle fehlt:** `dataforseo` nicht verbunden ODER `subscription_required` → auf `ga4_traffic_sources` degradieren (kommt Referral-Traffic von chatgpt.com/perplexity.ai etc.? = grobe Proxy) und als **beratend** kennzeichnen. Auch keine `ga4`-Quelle → **Lücke** benennen.

**Tiefe:** `geo-audit`.

---

## 8. Website/UX-Basis

**Was wird bewertet:** Technische und erlebnisbezogene Grundgesundheit der Website — lädt sie schnell, funktioniert sie mobil, stolpern Nutzer sichtbar. Keine tiefe CRO-/Conversion-Diagnose.

**0–5-Anker (DACH-KMU):**
- 0 = Grob kaputt: sehr langsam, mobil unbrauchbar, Lighthouse-Performance rot.
- 1 = Läuft, aber schwache Core Web Vitals und erkennbare Mobile-Probleme.
- 2 = Durchschnittliche Ladezeit, einzelne UX-Reibungen (Rage Clicks / tote Scrolls sichtbar).
- 3 = Solide Basis: Lighthouse im grünen Mittelfeld, mobil nutzbar, keine groben Reibungssignale.
- 4 = Schnell, mobil sauber, gute Core Web Vitals, nur kleinere UX-Optimierungen offen.
- 5 = Technisch exzellent: durchweg grüne Core Web Vitals, schnelle mobile Erfahrung, keine auffälligen Reibungssignale.

**Beleg:** `dfs_lighthouse_live` (Performance-/Accessibility-/SEO-Score, Core Web Vitals) + `clarity_get_insights` (Rage Clicks, Scroll Depth, Session-Signale). Zählwert: Lighthouse-Performance-Score + Präsenz auffälliger Clarity-Reibungssignale. Beleg-Stufe: **gemessen**.

**Fallback wenn Quelle fehlt:** Keine `clarity`-Quelle → allein auf `dfs_lighthouse_live` stützen (bleibt **gemessen**, ohne Verhaltens-Signal). Keine `dataforseo`-Quelle und kein Clarity → **Lücke** benennen.

**Tiefe:** `seo-audit` (technische Basis + Clarity-Reibung).

---

## 9. Messbarkeit/Analytics

**Was wird bewertet:** Ob das Analytics-Fundament so steht, dass Entscheidungen auf Daten beruhen — feuern die konfigurierten Key Events, ist GA4 mit den Kanälen verzahnt. (Nicht identisch mit Dimension 1: dort geht es um die Conversion-*Zählung*, hier um die Analytics-*Infrastruktur* dahinter.)

**0–5-Anker (DACH-KMU):**
- 0 = Kein GA4 / keine Key Events konfiguriert.
- 1 = GA4 läuft, aber keine Key Events definiert — nur Pageviews.
- 2 = Key Events definiert, feuern aber nicht (Counts = 0) oder GA4 ist nicht mit Google Ads verknüpft.
- 3 = Zentrale Key Events feuern; GA4↔Ads-Verknüpfung vorhanden; Custom-Dimensions/Attribution teils unklar.
- 4 = Key Events feuern konsistent, GA4↔Ads verknüpft, Traffic sauber Quellen zugeordnet.
- 5 = Vollständiges, sauberes Setup: Key Events mit Werten, Kanal-Verknüpfungen, konsistente Quellen-Attribution.

**Beleg:** `ga4_list_key_events` (welche Key Events sind konfiguriert, feuern sie — Counts > 0?) + `ga4_traffic_sources` (werden die Kanäle inkl. Paid sauber als Quelle erfasst = Verzahnungs-Proxy). Zählwert: Anteil feuernder Key Events. Die GA4↔Ads-Verknüpfung ist ein Konfigurations-Signal; die Detail-Prüfung übernimmt `tracking-check`. Beleg-Stufe: **gemessen**.

**Fallback wenn Quelle fehlt:** Keine `ga4`-Quelle → **Lücke** benennen. Ohne Analytics ist keine der gemessenen Dimensionen voll belastbar — diesen Vorbehalt oben im Plan spiegeln.

**Tiefe:** `tracking-check`.

---

## 10. Marken-Fundament (Selbstauskunft)

**Was wird bewertet:** Klarheit von Positionierung, Zielgruppe (ICP), Kern-Botschaft und rechtlichem Rahmen — die strategische Grundlage, auf der alle Kanäle aufsetzen.

**Hinweis:** **Einzige Selbstauskunfts-Dimension.** Quelle ist der `projekt-kontext`, nicht Live-MCP-Daten. Immer Beleg-Stufe **beratend** — nie als „gemessen” ausweisen.

**0–5-Anker (DACH-KMU):**
- 0 = Kein projekt-kontext; Positionierung/ICP/Ziele nirgends festgehalten.
- 1 = Nur rudimentäre Angaben (was die Firma macht), keine geschärfte Positionierung/ICP.
- 2 = Geschäftsziel + grobe Zielgruppe vorhanden, aber unscharf oder über die Kanäle widersprüchlich.
- 3 = Klares Geschäftsziel, definierte ICP und Kern-Botschaft; `ziel_kpi` gesetzt; `compliance`-Rahmen benannt.
- 4 = Geschärfte, differenzierende Positionierung, klare ICP, konsistente Marken-Begriffe, KPI + Compliance sauber.
- 5 = Distinkt positioniert, ICP + Botschaft konsistent über alle Flächen, KPI/Compliance/Brand-Begriffe vollständig gepflegt.

**Beleg:** `projekt-kontext` (Felder `geschaeftsziel`, `ziel_kpi`, `maerkte`, `compliance`, `brand_begriffe` + ICP-Teil) — Selbstauskunft, kein Live-Tool. Zählwert: Vollständigkeit + Schärfe der Kontext-Felder. Beleg-Stufe: **beratend** (Selbstauskunft).

**Fallback wenn Quelle fehlt:** Kein projekt-kontext vorhanden → Score 0 / **Lücke**; anbieten, ihn per `projekt-kontext` anzulegen (Fundament vor Planung).

**Tiefe:** `projekt-kontext`.
