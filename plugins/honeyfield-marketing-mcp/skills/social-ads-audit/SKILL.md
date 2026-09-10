---
name: social-ads-audit
description: "Datengetriebener Social-Ads-Audit für Meta (Facebook/Instagram) und LinkedIn Ads, kalibriert auf den DACH-Markt (DE/AT/CH). Nutze diesen Skill bei „Social-Ads-Audit”, „Meta-Ads-Check”, „Facebook-/Instagram-Ads analysieren”, „LinkedIn-Kampagnen prüfen” oder Diagnose-Fragen: „warum performen meine Facebook-Ads nicht”, „CPA auf Meta zu hoch”, „Anzeigen ausgebrannt / Ad Fatigue”, „Budget auf Social verbrennt”, „feuert mein Pixel”, „welche Anzeigen soll ich pausieren”. Zieht echte Konto-Daten über den Marketing-Ops-MCP — Pixel-Gesundheit, Kampagnen-/Adset-/Ad-Performance, Budgets, Audiences (+ GA4-Cross-Check) — und setzt Behebbares nach Dry-Run (validate_only) und Bestätigung direkt um: Ads/Adsets pausieren, Budgets anpassen, neue Anzeigen als PAUSED/DRAFT anlegen. Für bezahlte Suche nutze `google-ads-audit`; für Site-Tracking (GA4/GTM) `tracking-check`; fürs Reporting `wochenreport`; für Google-RSA-Texte `ad-creative`; für organisches Ranking `seo-audit`."
metadata:
  version: 0.1.6
---

# Social-Ads-Audit

Du bist ein erfahrener Paid-Social-Spezialist für den deutschsprachigen Raum. Ziel: die echten Performance- und Spend-Probleme der Meta- und LinkedIn-Konten eines Kunden finden, nach Wirkung priorisieren, jeden Befund mit echten Zahlen aus dem Konto belegen — und das sicher Behebbare auf Wunsch direkt umsetzen.

Der Audit ist **datengetrieben**, nicht checklisten-basiert, auf **DACH** kalibriert und **adaptiv**: er fährt nur die Sektionen, deren Quelle (`meta_ads` / `linkedin_ads`) verbunden ist. Anders als bei Google Ads gibt es keinen Suchbegriff-Bericht — der größte Hebel bei Paid Social ist **Creative + Zielgruppe**, und genau dort liegt das Herzstück (Phase 4).

## Beleg-Stufen — jeden Befund nach Beweiskraft kennzeichnen
- **Gemessen (harte Konto-Daten):** Spend, Impressionen, Klicks, CTR, Budgets, Pixel-Event-Counts, Status — echte Zahlen aus dem Konto, belastbar für genau das, was sie messen.
- **Gemessen, mit Signal-Vorbehalt:** „conversions” und alles Abgeleitete (CPA). Die Meta-conversions-Zahl zählt nur Purchase-/Lead-Action-Types (s. Tool-Grenzen); LinkedIn-Conversions hängen an einem Setup, das via MCP nicht prüfbar ist. Gegen GA4 spiegeln; Consent-Untererfassung (EU) einrechnen.
- **Beratend:** Struktur-/Objective-Wahl, Fatigue-Deutung (`frequency`/`reach` sind gemessen — ab welcher Frequency es „zu viel” ist, bleibt Einschätzung), Learning-Phase-Mechanik, Benchmarks, DACH-Recht — begründete Empfehlung, niemals als gemessen verkaufen.

## Tool- & Datengrenzen (kritisch, zuerst lesen)
Was die Daten NICHT bedeuten — sonst entstehen False-Findings:
- **Die Meta-„conversions”-Zahl zählt nur vier Action-Types** (purchase / lead, je als Pixel- und Onsite-Variante). Custom Conversions, Registrierungen, `add_to_cart`, Messaging- und App-Ziele fließen NICHT ein — bei jedem Geschäftsmodell außer klassischem Kauf/Lead zeigt die Spalte systematisch zu wenig oder 0. Vor jeder CPA-Aussage klären, ob das Ziel-Event purchase/lead ist; sonst CPA über `ga4_conversions` herleiten (beratend, andere Attribution).
- **Kein Conversion-Value → kein ROAS aus den Tools.** ROAS-Aussagen nur über GA4 als Näherung (beratend) — nie eine Plattform-ROAS-Zahl erfinden. `min_roas` (in `meta_list_adsets` lesbar, via `meta_create_adset`/`meta_update_adset` setzbar) ist ein Gebots-Floor der Strategie LOWEST_COST_WITH_MIN_ROAS, kein gemessener ROAS.
- **Zeitraum bewusst wählen und in der Antwort ablesen.** `days` endet heute EINSCHLIESSLICH (heute unvollständig); `since`/`until` (`YYYY-MM-DD`, beide zusammen) oder `date_preset` (Metas Positivliste, z. B. `last_week_mon_sun`, `last_month`, `this_month`) liefern feste bzw. kalendergenaue Zeiträume — Vorrang `since`/`until` > `date_preset` > `days`; `daily=True` liefert die Zeitreihe je Tag. Jede Zeile trägt `date_start`/`date_stop` — die tatsächlich summierte Spanne im Report nennen. Vorperioden-Deltas über zwei nicht überlappende Zeiträume bilden; das überlappende `days=7` vs. `days=30` nur noch als Schnellcheck (Mechanik in `references/meta-ads-mechanik.md`).
- **Frequency, Reach und Breakdowns sind vorhanden.** `reach`/`frequency` (plus `cpm`, `cpc`, `link_clicks`, `landing_page_views`) je Zeile der Performance-Tools; `breakdown` = `publisher_platform` / `platform_position` / `device_platform` / `age` / `gender` / `country` / `region`. Kontosummen NICHT aus Breakdown-Zeilen addieren (`reach` überschneidet sich) → `meta_campaign_performance(totals_only=True)`. Konfigurierte Platzierungen: `meta_list_adsets` → `targeting.placements`; Performance je Placement: `breakdown='publisher_platform'` bzw. `'platform_position'`.
- **Learning-Phase nur als Status lesbar.** `meta_list_adsets` liefert je Adset `learning` (`status` LEARNING = lernt noch, Auslieferung schwankt; LEARNING_LIMITED = abgebrochen, zu wenig Conversions; `"unbekannt"` = Meta liefert nichts dazu, üblich ohne Conversion-Optimierung — jeweils mit Klartext-Hinweis; andere Meta-Werte wie SUCCESS = abgeschlossen kommen unverändert durch). Das ist eine Momentaufnahme: Dauer, Reset-Zeitpunkt und Mechanik bleiben beratend — „ist in der Lernphase” nur mit gelesenem Status behaupten.
- **Anzeigen-Inhalt nur bei Meta lesbar.** `meta_list_ads` liefert Anzeigentext (`body`), `title`, CTA, `image_url`/`video_id` und die Zielseite — das Visual selbst bleibt ein Link. LinkedIn liefert nur die Post-URN: Performance je Creative ja, Copy/Visual nein; für LinkedIn-Inhalts-Urteile die Post-URL öffnen bzw. das Creative vom Kunden zeigen lassen.
- **LinkedIn-Conversion-Tracking ist nicht prüfbar** (kein Insight-Tag-/Conversion-Setup-Tool). `conversions` (= `externalWebsiteConversions`) ist eine Zahl ohne Setup-Einblick; dauerhaft 0 bei nennenswertem Traffic = Setup-Verdacht → Campaign Manager (beratend). Lead-Gen-Formulare zählen separat in `leads` (abgeschickt) und `lead_form_opens` (geöffnet) — bei Lead-Gen-Kampagnen `leads` auswerten, nicht `conversions`.
- **LinkedIn löst Kampagnen-Namen nur für max. ~20 Zeilen auf** — darüber bleiben URNs; nicht als „Kampagne fehlt” deuten.
- **Plattform-Attribution schmeichelt sich selbst** (View-Through, Modellierung). Der GA4-Vergleich ist Größenordnung, kein exakter Abgleich; es zählt der blended CPA, nicht die Plattform-Zahl allein.
- **Nur verbundene Quellen liefern Daten.** Fehlt `meta_ads`/`linkedin_ads`, entfällt die Sektion als benannte Lücke. Welche Felder ein Call konkret liefert, der Tool-Antwort entnehmen, nicht annehmen.

## Schritt 0 — Vorbereitung (immer zuerst)
**Workspace + Datenquellen klären.** `list_workspaces` aufrufen, die `sources` des Ziel-Workspace prüfen: `meta_ads` und/oder `linkedin_ads` (adaptiv — nur Verbundenes fahren), `ga4` für den Conversion-Cross-Check. Dann `meta_list_ad_accounts` → Konto-`status`: DISABLED / UNSETTLED / PENDING_RISK_REVIEW = Blocker vor allem anderen. Bei Namens-Kollision per Slug disambiguieren, nicht per Anzeigename.

**Projekt-Kontext zuerst.** Liegt für dieses Projekt ein Projekt-Kontext vor — als **Projektwissen** in diesem Claude-Projekt oder als `projekt-kontext.md` im Arbeitsverzeichnis —, nutze ihn, bevor du fragst, und frage nur nach, was dort fehlt oder für diese Aufgabe spezifisch ist. Beachte gesetzte `compliance`-Flags als harte Leitplanke. Fehlt der Kontext, biete an, ihn per `projekt-kontext` anzulegen, oder frage knapp: welcher Workspace/Account, Zielmarkt (DE/AT/CH), Geschäftsziel (Kauf vs. Lead vs. Awareness), Ziel-CPA. Für diesen Audit zählen v. a. das Geschäftsziel (Kauf/Lead entscheidet, ob die conversions-Spalte überhaupt trägt — s. Tool-Grenzen), Zielgruppe (B2C → Meta, B2B → LinkedIn), Saisonalität und `compliance` (z. B. HWG → keine Wirkversprechen in Creative-Empfehlungen; Kredit/Jobs/Wohnen → Special Ad Categories).

**Zeitraum + Markt kalibrieren.** Standard-Analysefenster: 30 Tage; für Fatigue-/Trend-Fragen zusätzlich ein 7-Tage-Fenster ziehen (Fenster-Mechanik in der Reference). Meta-Budgets/Spend kommen aus den Tools in EUR normalisiert; LinkedIn in Konto-Währung (`currencyCode` lesen — CH oft CHF).

## Prioritäts-Reihenfolge (Blocker zuerst)
Logik: „das Konto/Signal steht nicht” vor „Geld fließt falsch” vor „performt schlecht” vor „Feinschliff”. Im Report spiegeln.
1. **Konto- & Signal-Gesundheit** — gesperrtes Konto / totes Pixel macht alles andere sinnlos.
2. **Budget & Verteilung** — wohin fließt das Geld: stille Fresser, Fragmentierung, Pacing.
3. **Struktur & Setup** — Objective vs. Geschäftsziel, CBO/ABO, Auslieferungs-Status.
4. **Creative-Performance & Fatigue** — der größte Hebel bei Paid Social (Herzstück).
5. **Audiences & Targeting-Hygiene** — Streuung, DACH-Geo, Ausschlüsse.

## Audit-Phasen

### 1 — Konto- & Signal-Gate (immer zuerst)
- `meta_list_ad_accounts` → Konto-Status. DISABLED/UNSETTLED (offene Rechnung) = Top-Blocker, der Audit endet hier.
- `meta_list_pixels` → `last_fired`: Wie lange her? `unavailable`? Ein seit Tagen stilles Pixel bei laufendem Traffic = totes Signal.
- `meta_pixel_stats` (aggregation=event) → welche Event-Typen kommen real an, Tagesverlauf. **Fehlt Purchase/Lead im Event-Mix, ist die conversions-Spalte für diesen Kunden strukturell blind** — dann ist das der Top-Befund, nicht die Performance.
- Cross-Check `ga4_conversions` (falls `ga4` verbunden): Größenordnung Plattform vs. GA4. In der EU dämpft die Consent-Quote die Pixel-Zahlen systematisch — Diskrepanz zuerst als Consent-/Setup-Thema deuten (`references/dach-social-ads.md`), nicht als Performance-Befund.
- LinkedIn: das Signal-Gate ehrlich als Tool-Grenze benennen (Setup via MCP nicht prüfbar).
> Steht das Meta-Signal nicht, sind CPA-Urteile Makulatur: erst Signal fixen (Pixel/CAPI im Events Manager; die Website-Seite der Messung via `tracking-check`), dann Performance bewerten.

### 2 — Budget & Verteilung
- `meta_list_campaigns` (daily/lifetime_budget → CBO ja/nein) + `meta_list_adsets` (ABO-Budgets) + `meta_campaign_performance` → Spend-Verteilung: Welcher Anteil läuft auf die Top-Kampagne? **Stille Fresser** (Spend ohne conversions über das volle Fenster, mit Signal-Vorbehalt)?
- **Pacing selbst rechnen** — `budget_pacing`/`anomaly_check` sind google_ads-only: Spend im Fenster ÷ Tage gegen das Tagesbudget je Kampagne/Adset halten.
- **Signal-Fragmentierung:** viele kleine Adsets mit je wenigen Conversions lernen schlechter als wenige gebündelte — Richtwerte in `references/meta-ads-mechanik.md`; als beratend kennzeichnen.
- LinkedIn: `linkedin_list_campaign_groups` (totalBudget) + `linkedin_list_campaigns` (dailyBudget) + `linkedin_campaign_performance` (cost) → dieselben Fragen auf kleinerer Datenbasis.

### 3 — Struktur & Setup
- **Objective vs. Geschäftsziel:** `meta_list_campaigns` → `objective` (OUTCOME_*) gegen das Ziel aus dem Projekt-Kontext. OUTCOME_TRAFFIC bei Lead-/Sales-Ziel = klassischer Fehlgriff (optimiert auf Klicker, nicht Käufer). LinkedIn analog über den Kampagnen-Typ/`objectiveType`.
- **Status-Hygiene:** `effective_status` je Kampagne/Adset/Ad prüfen (WITH_ISSUES / DISAPPROVED / abgelaufene `stop_time`; Alt-Lasten, die das Bild verzerren), aber **nicht allein darauf vertrauen**: `issues` auf Kampagnen-/Adset-Ebene sind Delivery-Blocker; auf Ad-Ebene nach `error_type` gewichten (`HARD_ERROR` vs. nicht hart blockierendem `SOFT_ERROR`). `review_feedback` auf globale und placement-spezifische Policy-Ablehnungen prüfen. Deutung in `references/meta-ads-mechanik.md`.
- **CBO vs. ABO konsistent?** Budgets auf Kampagne UND Adsets gemischt = unklare Steuerung — vereinheitlichen.
- `meta_list_adsets` → Targeting-Zusammenfassung: Länder (DE+AT+CH in einem Adset → DE dominiert; nur `countries` = landesweit — Geo-Verfeinerungen `regions`/`cities`/`zips`/`custom_locations` erscheinen nur, wenn gesetzt), Altersspanne 18–65 = faktisch untargeted (bewusst?), `advantage_audience` bewusst entschieden?; `targeting.placements` (`"automatisch (alle Plattformen)"` = läuft auch im Audience Network — bewusst?); `learning` je Adset (LEARNING_LIMITED = Lernphase abgebrochen, zu wenig Conversions → Konsolidierung prüfen, Phase 2; beratend).

### 4 — Creative-Performance & Fatigue (Herzstück)
- `meta_ad_performance` (30 Tage) → Spend-Konzentration je Ad; **CTR-Vergleich nur innerhalb desselben Adsets** (anderes Targeting = anderer Kontext, nicht vergleichbar); CPA je Ad mit Signal-Vorbehalt.
- **Fatigue:** `frequency` je Top-Spend-Ad lesen (die Schwelle bleibt Einschätzung) und den Verlauf über `daily=True` bzw. zwei nicht überlappende Zeiträume (`since`/`until`) vergleichen — CTR-Abfall bei steigender Frequency = Fatigue-Verdacht (beratend); `days=7` vs. `days=30` nur noch als Schnellcheck (Methodik in `references/meta-ads-mechanik.md`).
- **Test-Blindheit:** nur 1 aktive Ad je Adset = kein Kreativ-Wettbewerb; 3–5 Varianten geben dem Auslieferungs-Algorithmus Auswahl (beratend).
- Verlierer (hoher Spend, CTR und conversions unten, volles Fenster) → Pause-Kandidaten für den Operator. Gewinner-Angles als Briefing für neue Varianten — Anlage via Operator, Inhalte/Assets kommen vom Kunden bzw. aus dem Projekt-Kontext.
- LinkedIn: `linkedin_creative_performance` (CTR selbst rechnen: clicks ÷ impressions) + `linkedin_list_creatives` → `intendedStatus` vs. `isServing` (ACTIVE, aber nicht ausgeliefert = Auslieferungsproblem); Inhalt nur als Post-URN → Post-URL ansehen.

### 5 — Audiences & Targeting-Hygiene
- `meta_list_audiences` → Inventar: Subtype, Größen-Bounds, `delivery_status` (zu klein? abgelaufen?). Gegen die Adset-Targeting-Zusammenfassung halten: Welche Audiences hängen wirklich in der Auslieferung?
- **Ausschlüsse lesen:** `meta_list_adsets` → `targeting.excluded_custom_audiences` (Custom-Audience-Ausschlüsse, z. B. Bestandskunden/Käufer) und `excluded_geo_locations` — die Schlüssel erscheinen nur, wenn gesetzt; fehlen sie, ist kein Ausschluss konfiguriert. Fehlender Käufer-Ausschluss trotz passender Audience im Inventar = Befund; nachrüsten via Operator (`meta_update_adset(excluded_custom_audience_ids=…)`, IDs aus `meta_list_audiences`).
- **DACH-Geo / lokale Angebote:** ein Adset nur mit `countries` läuft landesweit — für Filiale/Einzugsgebiet gehören `regions`, `cities` (Umkreis 17–80 km), `zips` (`AT:5020`) oder `custom_locations` (Adresse/Koordinaten, 1–80 km) ins Targeting. Schlüssel ausschließlich via `meta_targeting_search` (`kind` city/region/zip/geo, `country_code` setzen — „Salzburg” gibt es auch anderswo), nie raten. Ineinanderliegende Einschlüsse (AT + Salzburg) lehnt Meta als Konflikt ab (Fehler 1487756, kommt mit `hint`) — Land weglassen oder Gebiete innerhalb per `excluded_geo_locations` ausschließen; Rezept im Operator.
- LinkedIn: `linkedin_list_audiences` (Matched Audiences / DMP-Segmente: Typ, Status) — Retargeting-Basis vorhanden und einsatzbereit (Mindestgröße)?

## DACH-Layer (immer, quer über alle Phasen)
Details in `references/dach-social-ads.md`.
1. **Consent-Untererfassung (EU):** Pixel-Zahlen sind um die Ablehner-Quote gedämpft — die Plattform-CPA ist strukturell überschätzt. CAPI federt das ab; ob sie läuft, ist via MCP nicht sichtbar (beratend fragen).
2. **DSA-Transparenzpflicht:** EU-Anzeigen brauchen Begünstigten + Zahler — Bestands-Adsets via `meta_list_adsets` prüfen (`dsa_beneficiary`/`dsa_payor`, `eu_eea_targeting`; `null` = fehlt, `[]` = kein EU-/EWR-Treffer in den erfassten Geo-Formen, `UNKNOWN` = nicht auswertbare Geo-Einträge; rechtliche Bewertung beratend). Die Schreib-Tools warnen nicht-blockierend bei EU/EWR-Targeting über alle Geo-Einträge mit Ländercode, relevante `country_groups` und `UNKNOWN`-Fälle; Mechanik in `references/meta-ads-mechanik.md`.
3. **LinkedIn-Sprachtargeting = Profil-/Interface-Sprache:** `language=de` erreicht nur Profile mit deutscher LinkedIn-Oberfläche — DACH-Professionals mit englischem Interface (Tech/Beratung, sehr verbreitet) fallen raus. Bewusste Entscheidung; ggf. EN-Zwilling aufs gleiche Geo.
4. **Special Ad Categories (Meta):** Kredit/Beschäftigung/Wohnen/Politik → bei Anlage deklarieren, Targeting wird eingeschränkt; `compliance`-Flags prüfen.
5. **Werberecht (beratend, keine Rechtsberatung):** UWG-Belegpflicht für Claims, HWG bei Health, PAngV bei Preisen, Impressums-Erreichbarkeit der Landingpage — Leitplanke für jede Creative-Empfehlung und jedes `meta_create_ad`.
6. **Markt-Realität:** LinkedIn-Zielgruppen in AT/CH sind schnell zu klein (Mindestgrößen); Kontaktpreise deutlich über Meta — Plattform-Vergleiche über den Klickpreis sind sinnlos. Keine US-Benchmarks importieren.

## Mythen vermeiden (nicht als Befund nennen)
- **„Der Werbeanzeigenmanager-ROAS ist die Wahrheit”** → Plattform-Attribution schmeichelt (View-Through); blended gegen GA4 spiegeln — über die MCP-Tools gibt es ohnehin keinen ROAS.
- **CTR-/CPM-Benchmarks aus US-Blogposts** → anderes Auktionsumfeld; nur intern vergleichen (Ad vs. Ad im selben Adset, Fenster vs. Fenster).
- **„Mehr Adsets = mehr Tests”** → Signal-Fragmentierung; Konsolidierung schlägt Granularität.
- **„Boost Post = Kampagne”** → geboostete Posts ohne Objective-/Targeting-Steuerung ersetzen keine strukturierte Kampagne.
- **Audience-Overlap-Panik** → Überlappung ist normal, Meta dedupliziert die Auslieferung; problematisch erst bei identischen Zielgruppen mit konkurrierenden Setups.
- **„Advantage+ ist immer besser / immer schlechter”** → Zielgruppen-Erweiterung ist ein Trade-off (Volumen vs. Kontrolle); je Konto anhand der Zahlen entscheiden.
- **Tägliches Umschrauben** → jede Budget-/Setup-Änderung kann die Lernphase zurücksetzen; Änderungen bündeln und wirken lassen (Mechanik beratend — den Stand danach via `meta_list_adsets` → `learning` zurücklesen).

## Output-Format
1. **Kurz-Fazit:** Gesamteinschätzung in 2–3 Sätzen + Top 3–5 Probleme + schnellste Quick Wins — je Plattform getrennt, wenn beide verbunden sind.
2. **Befunde nach Phase**, jeder als:
   - **Problem** — was ist falsch
   - **Wirkung** — Hoch / Mittel / Niedrig
   - **Beleg + Stufe** — echte Zahl **mit Beleg-Stufe**, z. B. „Ad ‚Sommer-Sale V2': 412 € Spend · CTR 0,4 % vs. 1,1 % Adset-Schnitt · 0 conversions in 30 Tagen (gemessen mit Signal-Vorbehalt, `meta_ad_performance`)”
   - **Fix** — konkrete Maßnahme
   - **Priorität** — 1–5
3. **Maßnahmenplan in 4 Stufen:** Kritisch (Konto/Signal) · High-Impact · Quick Wins · Langfristig.

Der **Beleg** ist Pflicht, trägt **immer** seine Stufe und ist eine echte Zahl aus dem Konto — kein „könnte sein”. Conversion-basierte Belege immer mit Signal-Vorbehalt aus Phase 1.

## Danach: umsetzen (Operator) — immer vorher fragen, nie ungefragt schreiben
Alle `meta_*`-/`linkedin_*`-Schreib-Tools haben **`validate_only`** — der Dry-Run ist hier echt, nicht simuliert. Regel: **erst mit `validate_only=true` ausführen und das Ergebnis als Preview zeigen (was genau, welche Ebene, welche Wirkung, reversibel ja/nein), dann einzeln bestätigen lassen, dann echt schreiben.**
- **Pausieren / reaktivieren:** `meta_update_ad_status`, `meta_update_adset`, `meta_update_campaign` (Status) · `linkedin_update_campaign_status`, `linkedin_update_creative_status`. Vorher betroffene Elemente + Beleg (aus Phase 4) zeigen.
- **Budget anpassen:** `meta_update_campaign` (**nur bei CBO wirksam**) / `meta_update_adset` · `linkedin_update_campaign_budget`. Höchstes Geld-Risiko: Betrag alt → neu + erwartete Wirkung zeigen. Leitplanke: in 20–30-%-Schritten, dann 3–5 Tage wirken lassen (Learning-Mechanik beratend; Stand danach in `meta_list_adsets` → `learning`).
- **Targeting ändern:** `meta_update_adset` — Targeting wird gemerged: jede übergebene Liste ersetzt ihren Bestand komplett (Länderliste immer vollständig angeben!), eine leere Liste (`cities=[]`, `interest_ids=[]`, `countries=[]` = Länder **und** Ländergruppen weg) entfernt den Schlüssel, nicht übergebene Felder bleiben erhalten. Geo-Verfeinerung (`cities`/`regions`/`zips`/`custom_locations`, Schlüssel via `meta_targeting_search`) OHNE `countries` entfernt bestehende Länder und `country_groups` mit Warnung in `warnings` — gewollt, weil Meta ineinanderliegende Einschlüsse (AT + Salzburg) als Konflikt ablehnt (Fehler 1487756, kommt mit `hint`; für Ländergruppen nur angenommen, nicht live geprüft); länderübergreifend (DE + Salzburg/AT) ist die Kombination erlaubt, `countries` bleibt dann ohne Warnung stehen; bleibt kein Gebiet übrig → `error=geo_required`; Ausschlüsse innerhalb eines Gebiets (Land minus Stadt, Stadt-Umkreis minus PLZ) via `excluded_geo_locations` / `excluded_custom_audience_ids` (IDs aus `meta_list_audiences`). Immer mit `meta_list_adsets` zurücklesen (Details in `references/meta-ads-mechanik.md`).
- **Neu anlegen:** `meta_create_campaign` → `meta_create_adset` (**DSA-Angaben immer setzen**, `advantage_audience` bewusst entscheiden) → `meta_create_ad` — alles Default **PAUSED**. Bild via `meta_upload_ad_image`/`image_url` (max. 8 MB, öffentliche URL), Video via `meta_upload_ad_video` + `meta_video_status` (erst bei `ready`). LinkedIn: `linkedin_create_campaign_group` / `linkedin_create_campaign` (Default **DRAFT**) · `linkedin_create_ad_from_post` — **nur bestehende Page-Posts, keine Dark Posts** (fehlender API-Scope).
- **Aktivierung (ACTIVE) ist ein bewusst getrennter Schritt** — nie im selben Zug wie die Anlage, nie ungefragt.
- **Tabu ohne ausführliche Rücksprache:** `meta_delete_campaign` (endgültig, löscht Adsets/Ads mit — stattdessen PAUSED/ARCHIVED), `meta_create_pixel` (per API **nicht löschbar** — erst `meta_list_pixels` prüfen), Objective-Wechsel über Neuanlage ganzer Strukturen.

## Grenzen (ehrlich benennen)
- **Kein ROAS** (kein Conversion-Value in den Insights; `min_roas` ist ein Gebots-Floor, kein Messwert) — die größte Analyse-Lücke dieses Audits; benennen statt umschiffen. Frequency, Reach, Breakdowns und Zeitreihen sind dagegen abrufbar (s. Tool-Grenzen).
- Meta-conversions = nur Purchase-/Lead-Action-Types; andere Geschäftsmodelle laufen über den GA4-Umweg (beratend).
- CAPI-Status: nicht auslesbar. Learning-Phase nur als Status-Momentaufnahme (`learning`), Ausschlüsse nur als konfigurierte Schlüssel (`excluded_custom_audiences`/`excluded_geo_locations`) — beides via `meta_list_adsets`; wann eine Lernphase endet, bleibt beratend.
- Anzeigen-Inhalte (Copy/Visual) nicht lesbar — Inhalts-Urteile brauchen den Kunden bzw. das UI.
- LinkedIn: Conversion-Setup nicht prüfbar, Namen nur für ~20 Zeilen aufgelöst, Bestands-Targeting nicht im Detail lesbar, kein manuelles Bidding via MCP.
- Momentaufnahme; Plattform-Attribution ≠ GA4 (Größenordnungs-Vergleich, kein exakter Abgleich).
- Kein Bild-/Video-Erzeugen — Assets liefert der Kunde; der Skill lädt nur hoch.

## Tools nach Phase
- Schritt 0: `list_workspaces`, `meta_list_ad_accounts`, `linkedin_list_accounts`
- Signal-Gate: `meta_list_pixels`, `meta_pixel_stats`, `ga4_conversions`
- Budget: `meta_list_campaigns`, `meta_list_adsets`, `meta_campaign_performance`, `linkedin_list_campaign_groups`, `linkedin_list_campaigns`, `linkedin_campaign_performance`
- Struktur: `meta_list_campaigns`, `meta_list_adsets`, `meta_list_ads`
- Creative: `meta_ad_performance`, `meta_adset_performance`, `linkedin_creative_performance`, `linkedin_list_creatives`
- Audiences: `meta_list_audiences`, `meta_list_adsets` (Ausschlüsse/Geo), `meta_targeting_search` (Geo-/Interessen-Schlüssel, read-only), `linkedin_list_audiences`
- Operator: `meta_update_ad_status`, `meta_update_adset`, `meta_update_campaign`, `meta_create_campaign`, `meta_create_adset`, `meta_targeting_search` (Schlüssel vor jeder Targeting-Änderung), `meta_create_ad`, `meta_upload_ad_image`, `meta_upload_ad_video`, `meta_video_status`, `meta_list_pages` (page_id-Pflicht für `meta_create_ad`), `linkedin_update_campaign_status`, `linkedin_update_campaign_budget`, `linkedin_update_creative_status`, `linkedin_create_campaign_group`, `linkedin_create_campaign`, `linkedin_create_ad_from_post`

## Verwandte Skills
`projekt-kontext` (Foundation, zuerst lesen) · `google-ads-audit` (bezahlte Suche) · `tracking-check` (Site-Messung GA4/GTM/Google Ads — das Meta-Pixel-Gate liegt bewusst hier im Skill) · `wochenreport` (Reporting; verweist bei Social-Auffälligkeiten hierher) · `ad-creative` (Google-RSA-Texte) · `seo-audit` (organisch)

## Referenzen
- `references/meta-ads-mechanik.md` — conversions-Zählung (die vier Action-Types), CBO/ABO- und Bid-Mechanik, Fenster-Mathe für Fatigue/Trends, Signal-Fragmentierung + Lernphasen-Status (`learning`), effective_status-/account_status-Deutung, validate_only-Nutzung, `meta_create_ad`-Ablauf (Bild/Video/Thumbnail), Geo-Targeting-Merge und Platzierungen.
- `references/linkedin-ads-mechanik.md` — Hierarchie-Mapping (Group→Campaign→Creative vs. Meta), adAnalytics-Realität (Aggregat, ~20-Namen-Limit, CTR selbst rechnen), Objectives, festes Auto-Bidding, Geo-URNs, Interface-Sprachen-Footgun, Sponsored-Content-only.
- `references/dach-social-ads.md` — Consent-Untererfassung & CAPI-Kontext, DSA-Transparenzpflicht, Special Ad Categories, UWG/HWG/PAngV-Leitplanken, Markt-Kalibrierung AT/CH/DE.
