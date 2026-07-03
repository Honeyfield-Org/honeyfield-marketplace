# Content-Gap — Methodik-Referenz (Phase 5)

On-Demand-Tiefe für den `seo-audit`-Skill, Phase 5 (Content-Lücken). Nur laden, wenn Selbst-Gap/Markt-Gap tatsächlich analysiert wird.

## Competitor-Discovery-Kette (Markt-Gap)

Drei Schritte, immer in dieser Reihenfolge:

1. **Konkurrenten finden (nicht raten):** `dfs_serp_google_organic` für die 3-5 Ziel-Keywords (`location`/`language`!) → wer steht real auf Seite 1. Parallel `dfs_backlink_competitors` (eigene Domain) → wer hat ein ähnliches Linkprofil. **Schnittmenge beider Listen = echte SEO-Konkurrenten** (2-3 Domains reichen). Der vom Kunden genannte „Hauptkonkurrent" ist oft NICHT der SEO-Konkurrent — das Ranking entscheidet, nicht die Branchen-Wahrnehmung.
2. **Konkurrenz-Rankings ziehen:** `dfs_keyword_rankings` je Konkurrenz-Domain, mit denselben `location`/`language`-Parametern wie beim Kunden. Ohne Kalibrierung vergleichst du DE-Rankings mit AT-Rankings — wertlos.
3. **Diff bilden:** Konkurrenz-Rankings gegen die eigenen GSC-Rankings (`sc_performance`) und `dfs_keyword_rankings` halten. Gap = Keyword, für das ein Konkurrent in den Top 20 steht und die eigene Domain nicht (oder weit dahinter). Format je Fund: „Keyword X · Volumen · CPC · Konkurrent Position N · wir: Position M / nicht in Top 100."

> Es gibt **kein direktes Domain-Intersection-Tool** — der Diff wird aus den zwei Ranking-Listen selbst gebildet. Das ist okay, aber sag nicht „Tool-Ergebnis", wenn es deine eigene Schnittmengen-Rechnung ist.

## Snapshot-Schema (Wiederholungs-Diffing)

Gap-Analysen sind Momentaufnahmen — ihr Wert vervielfacht sich beim zweiten Durchlauf. Darum Rohdaten datiert ablegen, nie überschreiben:

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

## Difficulty-Substitution (Tool-Reality)

**Wir haben keine Keyword-Difficulty.** `dfs_keyword_volume` / `dfs_related_keywords` / `dfs_keyword_ideas_for_domain` liefern Volumen + CPC — keinen Schwierigkeitswert. Deshalb:

- **Nie eine Difficulty-Zahl behaupten** oder aus anderen Tools „erinnern".
- Ersatz-Heuristik (beratend kennzeichnen): **CPC** (Konkurrenzdruck der Werbetreibenden) + **SERP-Besetzung** via `dfs_serp_google_organic` — stehen auf Seite 1 nur große Marken/Portale/Wikipedia, ist das Keyword für einen kleinen Anbieter hart; stehen dort Nischen-Seiten und Foren, ist es erreichbar.

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
- People-Also-Ask: nur auswerten, wenn `dfs_serp_google_organic` SERP-Features tatsächlich zurückliefert — sonst Fragen-Empfehlungen als **beratend** kennzeichnen.
- Zweck hier: Content-*Themen* finden. Die KI-Sichtbarkeits-*Diagnose* (wird die Antwort zitiert?) gehört zu `geo-audit` — nicht hier hineinziehen.
