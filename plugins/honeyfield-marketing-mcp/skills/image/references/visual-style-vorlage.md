# visual-style.md — Vorlage & Interview-Leitfaden (Modus S)

Das Stil-Fundament pro Mandant. Modus A liest daraus die CSS-Variablen fürs Base-Template, Modus B die Prompt-Templates. Speicherung: Claude Code → `visual-style.md` ins Arbeitsverzeichnis; Claude.ai → zur Ablage im Projektwissen übergeben. Existiert die Datei: **updaten statt neu anlegen.**

## Erst-Befüllung (vor dem Interview)

1. **Website des Mandanten ansehen** (WebFetch/curl): dominante Farben (CSS/Logo), Schriften, vorhandene Bildsprache (Foto? Illustration? abstrakt?).
2. **`projekt-kontext` lesen:** Marke, Zielgruppe, Tonalität, `compliance`-Flags (gelten auch für Bildsprache).
3. Optional `gbp_get_profile` (falls `google_business` verbunden): Logo/Fotos als weitere Stil-Signale.

## Interview (nur was noch fehlt — knapp)

1. **Stil-Richtung:** fotorealistisch / flat-illustrativ / sketch / 3D-clean? (eine wählen — Stile nie mischen)
2. **Farben bestätigen:** die von der Website gezogene Palette zeigen, korrigieren lassen. Semantik klären: Akzent, Positiv/Negativ (für Vergleichs-Grafiken), Hintergrund.
3. **Fonts:** Marken-Font vorhanden (Google-Fonts-Name)? Sonst Vorschlag aus der Website ableiten.
4. **Signatur/Branding auf Grafiken:** Handle/Logo/Claim in der Ecke — ja/nein, welcher Text?
5. **No-Gos:** Stock-Optik? Emojis? Bestimmte Farben/Motive (Compliance, Marke)?

## Datei-Format

```markdown
---
projekt: <kunde-slug>
palette:
  fg: "#..."          # Text/Primär → --fg
  accent: "#..."      # Marken-Akzent → --accent
  bad: "#..."         # Negativ/Anti-Pattern → --bad
  good: "#..."        # Positiv/Erfolg → --good
  bg: "#..."          # Hintergrund → --bg
  muted: "#..."       # Sekundär-Text → --muted
  grid: "#..."        # Grid-/Rahmenlinien → --grid
  # -soft-Tönungen (--accent-soft/--bad-soft/--good-soft) nicht als Keys — je Grundfarbe als helle Tönung ableiten (ca. 8–12 % Deckung auf bg)
fonts:
  heading: "<Google-Font-Name>"     # → --font-heading
  body: "<Google-Font-Name>"        # → --font-body
  annotation: "<Google-Font-Name>"  # → --font-annotation (handschriftlich o. ä.)
stil: "<fotorealistisch | flat-illustrativ | sketch | 3d-clean>"
signatur: "<Text/Handle für die Grafik-Ecke — oder leer>"
verbote: ["<No-Go 1>", "<No-Go 2>"]
---

## Bildsprache

<2–4 Sätze: wie fühlen sich Bilder dieser Marke an, ein Wiedererkennungs-Element,
was es nie sein darf.>

## KI-Prompt-Templates (Modus B)

### Basis
```
<Stil-Beschreibung in 3–5 Zeilen: Technik, Farbwelt (Hex nennen), Stimmung,
"no photorealistic elements" o. Ä. je nach stil-Key>
[MOTIV]
```

### Konzept-Illustration
```
<wie Basis, plus: ein Fokus-Objekt, viel Whitespace>
[MOTIV]
```

### Kontrast/Split
```
<wie Basis, plus: split composition, links [SCHLECHT] in <bad-Farbe>,
rechts [GUT] in <good-Farbe>, dashed line between>
[MOTIV]
```

## Do / Don't

- Do: <3–5 Punkte>
- Don't: <3–5 Punkte, inkl. verbote von oben>
```

## Durchgespieltes Beispiel (fiktiver Mandant — NICHT als Default verwenden)

So sieht ein ausgefülltes `visual-style.md` aus, Stil „sketch”:

```markdown
---
projekt: beispiel-engineering-blog
palette:
  fg: "#2D2D2D"
  accent: "#1A73E8"
  bad: "#D93025"
  good: "#188038"
  bg: "#F8F5F0"
  muted: "#6B6B6B"
  grid: "#E0DCD4"
fonts:
  heading: "JetBrains Mono"
  body: "Inter"
  annotation: "Caveat"
stil: "sketch"
signatur: "@beispielfirma"
verbote: ["Stock-Fotos", "Gradients", "3D-Effekte", "mehr als 3 Farben pro Bild"]
---

## Bildsprache

Wie ein Ingenieurs-Notizbuch: Millimeterpapier-Grund, handgezeichnete Diagramme,
technische Annotationen. Sauber, aber nicht steril. Wiedererkennung: Grid-Textur +
Handschrift-Annotationen. Nie: Fotorealismus, Hochglanz.

## KI-Prompt-Templates (Modus B)

### Basis
```
Technical sketchbook style illustration on cream paper with subtle grid lines.
Ink-style drawing with blue (#1A73E8) accents. Clean, minimal, professional.
No photorealistic elements. Lots of whitespace.
[MOTIV]
```

### Konzept-Illustration
```
Minimalist concept illustration in technical sketchbook style.
Cream paper background with faint grid. One focal subject in charcoal ink
with blue accent details. Airy composition, lots of whitespace.
[MOTIV]
```

### Kontrast/Split
```
Technical sketchbook illustration, split composition: wrong approach left
with red (#D93025) crossed-out elements, right approach right with green
(#188038) checkmarks, dashed line between. Graph paper background.
[MOTIV]
```

## Do / Don't

- Do: Grid-Textur, eine Metapher pro Bild, Handschrift-Annotationen sparsam
- Don't: Stock-Fotos, Gradients, 3D, mehr als 3 Farben, Text-Blöcke im KI-Bild
```
