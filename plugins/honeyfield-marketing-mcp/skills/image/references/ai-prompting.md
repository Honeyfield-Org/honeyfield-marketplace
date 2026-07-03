# KI-Bild-Prompting (fal.ai)

Story-first-Handwerk, Prompt-Aufbau, Anti-Patterns und Modell-Wahl für Modus B. Stil-Templates kommen **immer** aus dem `visual-style.md` des Mandanten — hier steht das stilunabhängige Handwerk.

## Story-first: die wichtigste Regel

**Nie das Topic illustrieren, immer den Kontrast der Story.**

- Falsch gedacht: „Der Artikel handelt von Feedback-Loops → zeichne ein Loop-Diagramm.”
- Richtig gedacht: „Der Artikel kontrastiert Chaos (ohne Loops) mit System (mit Loops) → zeichne Slot-Machine vs. sauberen Kreislauf.”

### Story-Analyse (vor JEDEM Prompt)
1. Kern-Spannung/Kontrast des Contents? (Chaos vs. System, alt vs. neu, falsch vs. richtig)
2. Dominante Metapher? (aus dem Content übernehmen, nicht erfinden)
3. Welche Emotion soll das Bild auslösen? (Neugier, Wiedererkennen, Überraschung)
4. Ein Hero-Image erzählt den Konflikt der Story — nicht die Illustration der Lösung.

## Prompt-Aufbau

Grundmuster: **Stil-Template (aus `visual-style.md`) + Motiv (3–5 Sätze) + Komposition + Whitespace-Anforderung.**

- **Split-Kompositionen** für Problem→Lösung-Bögen: Schlechtes links, Gutes rechts, gestrichelte Linie dazwischen.
- **Kurz und luftig:** Jedes Prompt-Detail versucht das Modell zu rendern. Weniger Wörter = klareres Bild. Motiv-Teil max. 3–5 Sätze.
- **Whitespace explizit anfordern:** „lots of whitespace, minimal, airy composition, no clutter” in jeden Prompt.
- **Kein Text im Bild anfordern.** Labels höchstens 1–2 Wörter — alles darüber gehört in Modus A (Code-Gen).

## Anti-Patterns (vermeiden)

- Dichte Annotations-Wünsche („hand-written notes around the edges”) → Clutter.
- Lange Erklär-Sätze, was Elemente bedeuten → werden als Text ins Bild gerendert.
- Konkrete Text-Inhalte/Slogans anfordern → KI-Text-Rendering ist unzuverlässig.
- Detail UND Whitespace gleichzeitig → immer Whitespace wählen.
- Generische Topic-Illustration ohne Story-Spannung → langweilig, austauschbar.
- Reale Personen, fremde Marken/Logos/Produkte → Rechte-Leitplanke (SKILL.md, Ehrlichkeits-Modell 5) — blocken.

## Modelle & Preise (fal.ai)

| Modell | ID | Preis/Bild | Wofür |
|---|---|---|---|
| NanoBanana | `fal-ai/nano-banana` | ~$0.039 | Drafts, Varianten-Exploration |
| NanoBanana Pro | `fal-ai/nano-banana-pro` | ~$0.15 | Produktions-Qualität (Default) |

Preise Stand 2026-07 — Kosten-Wahrheit gilt: vor jedem Call Anzahl × Modell × Preis nennen. Weitere Modelle (FLUX etc.) über `--model`; Doku: https://fal.ai/docs/documentation

## Aspect-Ratio & Auflösung

`--aspect-ratio`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `4:5`, `5:4`, `21:9` · `--resolution`: `1K` (Social), `2K` (Blog-Hero/Primär-Visual). Plattform-Mapping: `platform-specs.md`.

## Generierungs-Kommando

```bash
python3 <skill-verzeichnis>/scripts/generate_image.py \
  --prompt "voller Prompt" \
  --aspect-ratio "16:9" --resolution "2K" \
  --output "pfad/beschreibender-name.png"
```

`FAL_KEY` muss in der Umgebung gesetzt sein — global via Shell-Config (`export FAL_KEY="<key-id>:<key-secret>"`) oder pro Projekt via `.claude/settings.local.json` (`env`-Block). Das Script gibt neben dem lokalen Pfad die **fal.ai-Result-URL** aus — sie ist öffentlich und direkt für `meta_upload_ad_image` verwendbar (Operator).

## Workflow-Regeln

- Kosten VOR dem Call nennen und bestätigen lassen; >3 Bilder = Batch mit Gesamtsumme.
- Nach der Generierung: Bild ansehen (Read) und gegen `visual-style.md` prüfen.
- Max. **eine** Nachbesserungs-Iteration ohne erneute Kosten-Rückfrage.
- Fehler/Timeout: **ein** Retry, dann ehrlich abbrechen und die Diagnose zeigen.
- Dateinamen beschreibend (`chaos-vs-system-hero.png`), nie generisch.
