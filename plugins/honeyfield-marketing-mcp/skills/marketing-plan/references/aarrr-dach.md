# AARRR für DACH-KMU — Stage-Zwang & Ops-Stack-Mapping

Das Rückgrat jedes Plans: jede Empfehlung bekommt genau eine AARRR-Stage, jede Stage einen ehrlichen Tool-Anker. On-demand laden. Framework nach Dave McClure („Pirate Metrics”), eingedeutscht und auf DACH-KMU statt SaaS kalibriert — Anleihen aus Corey Haines' `marketingskills`.

## (a) Die fünf Stages — KMU-Primer

KMU-Metriken statt SaaS: kein DAU/MRR/viral coefficient. Für Physiopraxis, Handwerksbetrieb, B2B-Dienstleister zählen Anrufe, Anfragen, Termine, Aufträge, Bewertungen.

| Stage | Frage | KMU-Metriken (statt SaaS) |
|---|---|---|
| **A**cquisition | Wie werden Fremde auf uns aufmerksam? | Website-Sitzungen, GBP-/Maps-Aufrufe, organische Impressionen/Klicks, Ad-Klicks, Anrufe aus dem Profil |
| **A**ctivation | Macht der Interessent den ersten wertvollen Schritt? | Kontaktformular ab, Termin gebucht, Angebot angefordert, Anruf getätigt, Rückrufbitte |
| **R**etention | Bleibt der Kunde und kommt wieder? | Folgetermine, Wartungsverträge, Wiederbestellung, wiederkehrende Website-Besucher als Proxy |
| **R**eferral | Bringen zufriedene Kunden neue Kunden? | Google-Bewertungen (Anzahl + Schnitt), Weiterempfehlungen, Mundpropaganda |
| **R**evenue | Was zahlen sie, wer zahlt, wie wächst der Wert? | Auftragswert, Umsatz pro Kunde, Angebots-Annahmequote, größeres Leistungspaket/Retainer |

**Grenze Acquisition↔Activation (KMU-Fassung).** Anfrage-*Absicht* (jemand landet auf der Kontakt-/Terminseite) = Acquisition. Anfrage-*Abschluss* (Formular ab, Termin gebucht, Anruf getätigt) und alles danach = Activation. Diese Grenze konsistent über den ganzen Plan ziehen.

**Beispiel-Durchlauf Physiopraxis:** gefunden über „Physiotherapie [Stadt]” in Maps (Acquisition) → bucht online einen Ersttermin (Activation) → kommt zu Folgeterminen (Retention) → hinterlässt eine 5-Sterne-Bewertung, die neue Patienten anzieht (Referral) → bucht ein Reha-Paket statt Einzelsitzung (Revenue).

## (b) Zuordnungsregeln

**1. Jede Empfehlung genau eine Stage.** Zuordnen zu der Stage, wo die *primäre messbare Wirkung* landet — nicht wo die Maßnahme nebenbei auch wirkt. Beispiel: „Kontaktseite in Marken-Tonalität neu schreiben” berührt Acquisition (Auffindbarkeit) und Activation (Anfrage-Rate). Primäre Wirkung = Anfrage-Rate → Activation, Crossover erwähnen.

**2. Brand & Content sind Querschnitt, keine sechste Stage.** Marken-Tonalität regelt jede Copy über alle Stages. Content speist alle Stages (SEO/Social → Acquisition, Anfrage-/Onboarding-Copy → Activation, Newsletter → Retention, Bewertungs-Bausteine → Referral, Preis-/Leistungsseiten → Revenue). Im Plan erscheinen Brand/Content als strategischer Rahmen, **nie** als eigene AARRR-Sektion.

**3. Im Zweifel: die Stage mit dem aktuellen Engpass.** Wenn eine Maßnahme wirklich zwischen zwei Stages steht — fragen: *Wo würde das Entfernen dieser Maßnahme am meisten wehtun?* Dort zuordnen. Der Plan sequenziert ohnehin zuerst am Engpass.

**Engpass bestimmen (binding constraint).** Für jeden Kunden sind ein bis zwei Stages der Flaschenhals. Faustregeln:

- **Keine Sichtbarkeit / kaum Besucher** → Engpass Acquisition. (Neuer Betrieb, keine Rankings, GBP dünn.)
- **Besucher da, aber keine Anfragen** → Engpass Activation. Erst das Leck stopfen, dann mehr Wasser einfüllen — Anfrage-Rate zu heben ist meist der stärkere Hebel als mehr Traffic.
- **Anfragen da, aber Kunden kommen nicht wieder** → Engpass Retention. (Kein Folgetermin-/Wartungs-Mechanismus.)
- **Stammkunden zufrieden, aber Wachstum stockt** → Engpass Referral/Revenue (clustern oft: Bewertungs-Motor + Preis-/Paket-Struktur).
- **Alles läuft im Kleinen** → Acquisition skalieren (Post-Fit-„mehr davon”).

**Reihenfolge der Darstellung:** im Plan immer A→A→R→R→R in Funnel-Reihenfolge zeigen (Leser-Erwartung), unabhängig von der Priorität. Priorität über die Executive Summary signalisieren, nicht über Umsortieren.

## (c) Ops-Stack-Mapping — Stage → Skills → MCP-Tools → ehrliche Lücke

Der Daten-Moat: Wir sagen nicht nur *was* zu tun ist, sondern *welcher* unserer Skills und *welche* echten MCP-Tools es bedienen. Nur Read-Tools (der Hub ist read-only). Alle Tools sind in `references/tool-map.md` als R verifiziert.

| Stage | Unsere Skills (Tiefe/Umsetzung) | MCP-Tool-Domänen (gemessen) | Ehrliche Lücke |
|---|---|---|---|
| **Acquisition** | `google-ads-audit`, `social-ads-audit`, `seo-audit`, `geo-audit`, `content-strategie`, `ad-creative` | Paid Search `ads_*` (`ads_campaign_performance`, `ads_impression_share`, `ads_search_terms`), Paid Social `meta_*`/`linkedin_*` (`meta_campaign_performance`, `linkedin_campaign_performance`), organische Suche `sc_*` (`sc_top_queries`, `sc_top_pages`, `sc_performance`), Markt/Wettbewerb `dfs_*` (`dfs_keyword_rankings`, `dfs_serp_google_organic`, `dfs_competitors_domain`), lokal `gbp_performance`/`gbp_search_keywords`/`gbp_local_rank`, `ga4_traffic_sources` | Keine — dichteste Abdeckung. Stärkste Beleg-Lage des ganzen Funnels. |
| **Activation** | `tracking-check` (misst, ob Anfragen ankommen), `seo-audit` (UX-/Landingpage-/CWV-Querschnitt) | `ga4_*` (`ga4_conversions`, `ga4_list_key_events`, `ga4_top_pages`, `ga4_report`), Verhalten `clarity_get_insights` (Rage Clicks, Scroll Depth, Abbruch-Stellen) | Messung stark, **Umsetzung** von Formular-/UX-/Anfrage-Fixes liegt beim Kunden bzw. bei `seo-audit`. Kein A/B-Test-Tool, kein CRO-Operator im Hub. Voraussetzung: sauberes Tracking — sonst „mit Tracking-Vorbehalt”. |
| **Retention** | Kein Skill mit Retention-Operator — Hub misst nur | **NUR Messung** via `ga4_*` (`ga4_report`/`ga4_traffic_sources` für wiederkehrende Besucher als Proxy) | **Kein E-Mail-/CRM-/Lifecycle-Anker.** Kein Tool für Newsletter, Wartungs-Reminder, Win-Back. Echte Kunden-Retention (Folgetermine, Wiederbestellung) passiert außerhalb der verbundenen Quellen. Umsetzung vollständig beim Kunden — im Plan **beratend** führen. |
| **Referral** | Kein dedizierter Referral-Skill; Bewertungs-Signale werden von `seo-audit`/`geo-audit` als lokale/Trust-Signale mitbewertet | `gbp_reviews` (Bewertungen + Schnitt), `gbp_get_review_link` (Bewertungs-Link zum Einsammeln), ergänzend `dfs_reviews` (Google/Trustpilot) | Nur Google-Bewertungen als Referral-Signal messbar. Kein Empfehlungs-/Affiliate-/Ambassador-Programm-Tool. Weiterempfehlung/Mundpropaganda offline nicht messbar. Aktives Einsammeln (Link verschicken) + Antworten = Kunden-Aktion, nicht Hub. |
| **Revenue** | `google-ads-audit`/`social-ads-audit` (Conversion-Wert), `tracking-check` (Wert-Tracking prüfen) | `ads_conversion_performance` (Conversion-Wert pro Aktion), `ga4_conversions` (Events mit Value) — Beleg-Stufe **mit Tracking-Vorbehalt** (CPA/ROAS nur so gut wie das Tracking) | Pricing/Packaging/Angebots-Annahmequote = **rein beratend, kein Tool-Anker**. Kein Warenkorb-/Kassen-/Rechnungs-Tool. Tatsächlicher Auftragswert liegt bei KMU oft im CRM/Kassensystem außerhalb der Quellen. |

**Merksatz zur Anker-Dichte:** Acquisition und Revenue-*Messung* sind gemessen; Activation und Revenue-Wert stehen unter Tracking-Vorbehalt; Retention und Referral sind tool-arm — dort ist Ehrlichkeit Pflicht (siehe d).

## (d) Der Punkt: Mapping = Daten-Vorteil, Ehrlichkeit = Qualitätsmaßstab

Dieses Mapping ist der Unterschied zu reinen Wissens-/Checklisten-Plänen: Jede Empfehlung hängt an einem realen, verbundenen Tool oder wird ausdrücklich als beratend gekennzeichnet — kein „man sollte mal”.

- **Empfehlung mit Tool-Anker** → als *gemessen* (bzw. *mit Tracking-Vorbehalt*) führen, mit der konkreten Datenquelle.
- **Empfehlung ohne Tool-Anker** (Retention-Lifecycle, Pricing, Empfehlungsprogramm) → offen als *beratend* kennzeichnen und die Umsetzung explizit beim Kunden verorten. Eine tool-arme Stage nicht schönreden — die Lücke benennen ist die ehrlichere und nützlichere Aussage.

Ein Plan, dessen Retention-/Referral-/Pricing-Empfehlungen so tun, als kämen sie aus den Daten, verspielt genau den Vertrauensvorsprung, den das Mapping schafft.
