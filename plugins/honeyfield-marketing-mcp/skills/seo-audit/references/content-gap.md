# Content-Gap — Methodik-Referenz (Phase 5)

On-Demand-Tiefe für den `seo-audit`-Skill, Phase 5 (Content-Lücken). Nur laden, wenn Selbst-Gap/Markt-Gap tatsächlich analysiert wird.

## Competitor-Discovery-Kette (Markt-Gap)

Drei Schritte, immer in dieser Reihenfolge:

1. **Konkurrenten finden (nicht raten):** `dfs_competitors_domain` (eigene Domain, `location`/`language`!) → Domains mit den meisten gemeinsamen Rankings, sortiert nach Overlap. Gegenprobe: `dfs_serp_google_organic` für die 3-5 Ziel-Keywords → wer steht real auf Seite 1. **Deckung beider Listen = echte SEO-Konkurrenten** (2-3 Domains reichen). Der vom Kunden genannte „Hauptkonkurrent" ist oft NICHT der SEO-Konkurrent — das Ranking entscheidet, nicht die Branchen-Wahrnehmung.
2. **Gap direkt ziehen:** `dfs_domain_intersection(domain1=eigene Domain, domain2=Konkurrent, intersections=false)`, mit denselben `location`/`language`-Parametern wie beim Kunden → liefert die Keywords, für die der Konkurrent (`rank_domain2`) rankt und die eigene Domain (`rank_domain1`) nicht, direkt inkl. `search_volume`/`cpc_usd`. Ohne Kalibrierung vergleichst du DE-Rankings mit AT-Rankings — wertlos.
3. **Gegen eigene Rankings absichern:** die Gap-Liste gegen `sc_performance`/`dfs_keyword_rankings` der eigenen Domain halten und formatieren: „Keyword X · Volumen · CPC · Konkurrent Position N · wir: Position M / nicht in Top 100."

> `dfs_domain_intersection` im Gap-Modus (`intersections=false`) liefert den Diff jetzt direkt aus der API — keine eigene Schnittmengen-Rechnung aus zwei Ranking-Listen mehr nötig.

## Snapshot-Schema (Wiederholungs-Diffing)

`dfs_historical_rank_overview` (Domain) liefert jetzt monatliche Domain-Aggregate (`organic_keywords`, `organic_etv`, `top3`, `top10`) direkt — für „wächst/schrumpft die Sichtbarkeit der Domain/des Konkurrenten über Zeit" kein manuelles Diffing mehr nötig. Das Tool liefert aber **keine Einzel-Keyword-Historie** (kein „Keyword X rankte letzten Monat auf Position 8, jetzt auf 4") — dafür bleibt Snapshot-Diffing auf Keyword-Ebene nötig.

Gap-Analysen (Keyword-Ebene) sind Momentaufnahmen — ihr Wert vervielfacht sich beim zweiten Durchlauf. Darum Rohdaten datiert ablegen, nie überschreiben:

```
raw/<domain-slug>/<YYYY-MM-DD>/
  serp-<keyword-slug>.md        # Seite-1-Besetzung je Ziel-Keyword
  rankings-<konkurrent>.md      # dfs_keyword_rankings-Auszug je Konkurrent
  gap-liste.md                  # der berechnete Diff
```

- **Claude Code:** als Dateien im Arbeitsverzeichnis des Projekts.
- **Claude.ai:** als datierte Tabellen im Report festhalten (und ins Projektwissen übernehmen), damit der nächste Audit dagegen diffen kann.
- Beim Re-Audit: neuen Snapshot anlegen, gegen den letzten diffen → „Konkurrent hat 12 neue Top-10-Keywords im Cluster Y aufgebaut" ist ein stärkerer Befund als jede Momentaufnahme.

## Intent-Bucketing

Jede Lücke einem Intent zuordnen — Intent trennt „rankt nett" von „bringt Umsatz":

| Intent | Query-Muster (DACH) | Priorität |
|---|---|---|
| **Transactional** | „kaufen", „bestellen", „buchen", „anbieter", „kosten", „preis" | am wertvollsten, meist geringstes Volumen |
| **Commercial** | „vergleich", „test", „erfahrungen", „beste/r", „alternative zu" | Kaufnähe, mittleres Volumen |
| **Informational** | „was ist", „wie funktioniert", „warum", „anleitung" | Volumen-stark, konvertiert selten direkt — Pillar-/AEO-Futter |

CPC ist der Kommerz-Proxy: hoher CPC = Werbetreibende zahlen dafür = kommerzielle Absicht dahinter.

## Keyword-Difficulty (`dfs_keyword_overview`)

`dfs_keyword_overview` (Liste, max. 700 Keywords) liefert Difficulty, Haupt-Intent, Volumen und CPC in einem Call — eine echte, gemessene Difficulty-Zahl statt der früheren Heuristik.

- Difficulty direkt aus dem Tool zitieren, keine Werte aus fremden Tools (Ahrefs/SEMrush o.ä.) übernehmen — nicht vergleichbar.
- Ergänzend weiterhin sinnvoll: **SERP-Besetzung** via `dfs_serp_google_organic` — stehen auf Seite 1 nur große Marken/Portale/Wikipedia, ist das Keyword auch bei niedriger Difficulty-Zahl für einen kleinen Anbieter praktisch hart erreichbar; stehen dort Nischen-Seiten und Foren, bestätigt das eine niedrige Difficulty.

## Opportunity-Matrix (Netto-Neu-Themen)

Achsen: **Volumen × CPC-Wert × Pillar-Fit** (passt das Thema zu den Geschäftsfeldern aus dem Projekt-Kontext?).

| Bucket | Kriterien | Aktion |
|---|---|---|
| **High Opportunity** | ordentliches Volumen · kommerzieller Intent · Pillar-Fit · SERP erreichbar | zuerst angehen |
| **Quick Wins** | kleines-mittleres Volumen · schwache SERP-Besetzung · Pillar-Fit | nebenher produzieren |
| **Strategic** | hohes Volumen · hart umkämpfte SERP | langfristig, nur mit Autoritäts-Aufbau |
| **Skip** | kein Pillar-Fit oder reiner Traffic ohne Geschäftsbezug | begründet auslassen |

**Abgrenzung zur Striking-Distance (Phase 4):** Striking-Distance priorisiert *bestehende* Rankings (Position 5-15) mit hartem GSC-Beleg — das bleibt der stärkste Hebel. Die Matrix priorisiert *neue* Themen auf Schätzdaten: Volumen ist gemessen, die Priorisierung selbst ist beratend.

## Fragen-Mining (AEO-Brücke)

- `dfs_related_keywords` mit Frage-Seeds („wie [Thema]", „was kostet [Thema]", „warum [Thema]") → W-Fragen-Cluster als Input für Answer-First-Content.
- People-Also-Ask: `dfs_serp_google_organic` liefert `people_also_ask` jetzt in jedem Call mit (gemessen, kein Fallback mehr nötig) — direkt als weiteren Frage-Cluster nutzen.
- Zweck hier: Content-*Themen* finden. Die KI-Sichtbarkeits-*Diagnose* (wird die Antwort zitiert?) gehört zu `geo-audit` — nicht hier hineinziehen.
