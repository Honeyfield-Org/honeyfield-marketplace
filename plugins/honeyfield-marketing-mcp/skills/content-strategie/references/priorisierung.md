# Themen-Priorisierung & Buyer-Stage

Für die Themen-Findung und Priorisierung. Jedes Thema fußt auf gemessenen bzw. geschätzten Daten (GSC/DFS), die Gewichtung ist beratend. On-demand laden. Priorisierungs-Score nach Corey Haines' `marketingskills`, eingedeutscht.

## 40/30/20/10-Score

Jedes Thema auf vier Faktoren bewerten (1–10), gewichtet:

### 1. Customer Impact (40 %)
- Wie oft kam das Thema in der Recherche/den Kundengesprächen vor?
- Welcher Anteil der Zielgruppe hat dieses Problem?
- Wie emotional aufgeladen ist der Schmerzpunkt?
- Welcher LTV steckt hinter Kunden mit diesem Bedarf?

### 2. Content-Market-Fit (30 %)
- Passt es zu den Problemen, die das Produkt/die Leistung löst?
- Gibt es einzigartige Insights aus eigener Erfahrung/Kunden-Research?
- Gibt es Kunden-Stories, die es stützen?
- Führt es natürlich zum Angebot?

### 3. Search Potential (20 %)
- Monatliches Suchvolumen (`dfs_keyword_volume`, gemessen)?
- Keyword-Difficulty (`dfs_keyword_overview`, gemessene Zahl — SERP-Besetzung via `dfs_serp_google_organic` bleibt ergänzendes qualitatives Signal)?
- Long-Tail-Chancen drumherum (`dfs_keyword_suggestions`)?
- Interesse steigend oder fallend (`dfs_keyword_trends`, max. 5 Keywords/Call — für die Shortlist, nicht jedes Thema)?

### 4. Resources (10 %)
- Ist die Expertise da, um autoritativ zu schreiben?
- Welche zusätzliche Recherche/Assets braucht es?

### Scoring-Template

| Thema | Customer Impact (40 %) | Content-Market-Fit (30 %) | Search Potential (20 %) | Resources (10 %) | Total |
|---|---|---|---|---|---|
| Thema A | 8 | 9 | 7 | 6 | 8,0 |
| Thema B | 6 | 7 | 9 | 8 | 7,1 |

Total = gewichteter Schnitt. Hoch nach unten sortieren, Empfehlung aussprechen was zuerst.

## Buyer-Stage-Keyword-Modifier (DACH)

Themen der Buyer-Journey zuordnen. `dfs_keyword_overview.main_intent` liefert den Intent jetzt als Messwert (informational/commercial/transactional/navigational) — der Modifier unten übersetzt das in die vier Buyer-Stages und den passenden Content-Typ, und dient als Plausibilisierung, wenn Query-Muster und gemessener Intent auseinanderlaufen:

| Stage | DE-Modifier (Beispiele) | Content-Typ |
|---|---|---|
| **Awareness** | „was ist”, „wie funktioniert”, „grundlagen”, „einführung” | Ratgeber, Erklärstück, Glossar |
| **Consideration** | „beste”, „vergleich”, „vs”, „alternative”, „test”, „top” | Vergleichsseite, Alternatives-Liste, Kaufberatung |
| **Decision** | „preis”, „kosten”, „erfahrungen”, „bewertung”, „demo”, „testen” | Pricing-/Produktseite, Case Study, Review-Seite |
| **Implementation** | „vorlage”, „anleitung”, „tutorial”, „beispiel”, „checkliste”, „so geht” | Template, Schritt-für-Schritt, How-to |

**DACH-Hinweis:** Komposita UND Phrase abdecken („[Thema]-Vergleich” und „[Thema] vergleichen”). Consideration-/Decision-Modifier mit kommerziellem Intent haben oft höheren CPC — CPC als Kommerz-Proxy nutzen (gemessen), nicht als Erfolgsgarantie (beratend).

## Verzahnung mit dem `seo-audit`-Gap-Input

Kommt eine Content-Lücken-Liste aus `seo-audit` Phase 5, ist die Diagnose schon erledigt — **nicht neu diagnostizieren**. Der Gap enthält Selbst-Gap (eigene Domain: hohes Volumen, kein/schlechtes Ranking) und Competitor-Gap (wo Konkurrenten ranken, der Kunde nicht). Vorgehen:
1. Jedes Gap-Thema um die für die Erstellung fehlenden Felder ergänzen: Volumen/CPC (`dfs_keyword_volume`), Difficulty/Intent (`dfs_keyword_overview`), Buyer-Stage (Modifier oben), Pillar-Fit.
2. Striking-Distance-Gaps (bestehende Rankings Position 5–15 mit GSC-Beleg) sind der stärkste Hebel — vor Netto-Neu-Themen priorisieren.
3. Score anwenden, Content-Typ je Buyer-Stage festlegen, in die Roadmap.

## Headline- & CTA-Formeln (eingedeutscht)

Für Arbeitstitel-/H1-Vorschläge und CTA-Hinweise im Content-Brief. Nach Corey Haines' `copywriting`.

**Headline-Formeln:**
- „[Ergebnis erreichen] ohne [Schmerzpunkt]” — „Sauberes Reporting ohne Excel-Chaos”
- „Das/Die [Kategorie] für [Zielgruppe]” — „Die Terminverwaltung für Handwerksbetriebe”
- „Nie wieder [unangenehmes Ereignis]” — „Nie wieder verpasste Fristen”
- „[Frage, die den Hauptschmerz trifft]” — „Warum bleiben halbe Angebote liegen?”

Regel: spezifisch > generisch. Wichtiges Keyword nach vorn (Pixel-/SEO-Logik). Klarheit vor Cleverness.

**CTA-Formel:** [Aktionsverb] + [was der Leser bekommt] (+ Qualifier).
- Schwach: „Absenden”, „Anmelden”, „Mehr erfahren”, „Hier klicken”.
- Stark: „Kostenlos testen”, „Checkliste herunterladen”, „Preise für mein Team ansehen”, „Erstberatung buchen”.

Belegpflicht beachten: Superlative/Zahlen in Headlines nur mit Beleg (UWG) — `references/copy-qa.md` im Plugin, Sweep 4.
