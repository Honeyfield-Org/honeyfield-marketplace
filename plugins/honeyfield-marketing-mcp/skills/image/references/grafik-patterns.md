# Grafik-Patterns — Diagramm-Typen & HTML/CSS-Referenz

Welcher Diagramm-Typ für welchen Zweck, mit HTML/CSS-Umsetzungsmustern. Technische Referenz für den `image`-Skill — on-demand laden, hält SKILL.md schlank.

---

## Vorbereitung: Base-Template

Alle code-generierten Grafiken entstehen in **HTML/CSS/JS** (nicht Python/matplotlib). Playwright MCP übernimmt Browser-Rendering, visuelle Prüfung und PNG-Export.

Basis: `assets/base-template.html` im Skill-Verzeichnis — ins Arbeitsverzeichnis kopieren, CSS-Variablen aus `visual-style.md` setzen. Das Template liefert Struktur, Google Fonts (`var(--font-heading)` / `var(--font-body)` / `var(--font-annotation)` — konkrete Font-Familien aus `visual-style.md`), CSS-Variablen und Textur-Layer.

---

## Diagramm-Auswahl

| Ziel | Diagramm-Typ | CSS-Ansatz |
|------|-------------|-----------|
| Prozess oder Workflow | Flowchart | Flexbox + `.flow-arrow-h`-Komponenten |
| Beziehungen zwischen Konzepten | Mindmap / Netzwerk | CSS Grid + SVG-Konnektoren |
| Vergleich von Optionen | Vergleich (Split) | `.split`-Grid + `.divider` + `.vs-badge` |
| Daten über Zeit | Zeitachse (Timeline) | Flexbox horizontal + Marker-Elemente |
| Verteilung von Werten | Balkendiagramm | CSS-Grid-Zeilen mit Prozent-Breiten |
| Vorher/Nachher-Kontraste | Zweispalten-Vergleich | `.split` + farbcodierte Spalten |
| Systemarchitektur | Architektur-Diagramm | CSS Grid + SVG-Pfeile |
| Sequenzielle Schritte | Step-Diagramm / Pipeline | `.flow-vertical` oder `.flow-horizontal` |
| Einzelne beeindruckende Kennzahl | Hero-Number | `.hero-number` + Kontext-Text |
| Zitat-Grafik | Quote-Grafik | Zentriertes Layout + `.annotation`-Font |

---

## Design-Prinzipien

### Tiefe & Elevation

Jede Grafik braucht visuelle Tiefe. Flache Designs wirken generisch.

- **Box-Shadows** auf allen interaktiven/wichtigen Elementen: `box-shadow: 0 2px 8px rgba(0,0,0,0.06)`
- **Hero-Elemente elevated** mit stärkeren, farbigen Schatten: `box-shadow: 0 3px 12px rgba(26,115,232,0.15), 0 1px 3px rgba(26,115,232,0.08)`
- **Success-/Abschluss-Elemente** bekommen ein Glow: `box-shadow: 0 3px 16px rgba(24,128,56,0.3)`
- Tiefen-Hierarchie: neutral < aktiv/Hero < Erfolg/Abschluss

Diese Schatten-Farbwerte (RGBA) sind Beispielwerte, passend zum Default-Theme des Base-Templates (`--accent`/`--good`/`--bad`). RGBA-Kanäle können keine `var(--…)`-Referenz aufnehmen — bei anderer Mandanten-Palette die RGB-Werte manuell aus `visual-style.md` übertragen.

Nie eine Box flach ohne Schatten lassen. Base-Template-Klassen nutzen:
- `.box` — Basis-Schatten
- `.box--elevated` — Hero-Elemente mit stärkerem, farbigem Schatten
- `.box--solid-good` / `.box--solid-bad` — gefüllt mit Glow-Effekt

### Textur & Tiefe

Grid- und Noise-Textur sind der Default des Base-Templates gegen einen Flat-Look:

- **Graph-Paper-Grid**: `::before`-Pseudo-Element mit Gitterlinien bei Opazität 0.45
- **Noise-Grain-Overlay**: `::after`-Pseudo-Element mit SVG-`feTurbulence` bei Opazität 0.03
- Beide sind im Base-Template enthalten

Ob eine Grid-Optik zum Mandanten passt, entscheidet `visual-style.md` (`stil`/`verbote`) — bei Bedarf deaktivieren. Noise-Grain fast immer behalten (trägt kaum stilabhängig zur Wiedererkennung bei, sorgt aber für Tiefe).

### Visuelle Hierarchie

- **Hero-Element** muss das visuell prominenteste sein (größte, gesättigste, am stärksten elevated)
- **Vorwärts-Pfeile** zwischen Schritten: gedämpft (`--fg`, Opazität 0.3)
- **Farbige Pfeile** nur für aktive/wichtige Pfade (`--accent` zwischen Loops, `--good` Richtung Erfolg)
- **Progressive Opazität** bei wiederholten Elementen (z. B. Feedback-Bögen: 0.35, 0.45, 0.55)
- **Durchgestrichen + reduzierte Opazität** (0.7) für Anti-Pattern-Items (`.sketch-strikethrough`); `.sketch-underline` für Hervorhebung
- **Einfach und fokussiert halten** — ein Konzept pro Grafik
- **Keine Gradients, keine 3D-Effekte, keine Stock-Foto-Elemente**

### Typografie-Regeln

- `var(--font-heading)` (Font-Familie aus `visual-style.md`): Headings, Labels, Code, Taglines
- `var(--font-body)` (Font-Familie aus `visual-style.md`): Fließtext, Beschreibungen, Detail-Items
- `var(--font-annotation)` (Font-Familie aus `visual-style.md`): Annotations, prägnante Take-away-Zeilen, handschriftliches Gefühl
- **Minimum 14px** für allen Text (Lesbarkeit auf Mobile bei 1080px Breite)
- Schlüsselwort in der Tagline mit `var(--accent)` hervorheben, `.highlight`-Span

### Content-Zentrierung

Immer `justify-content: center` auf dem Haupt-Content-Wrapper nutzen, um Inhalt vertikal im Canvas zu zentrieren. Nie `flex: 1` auf Kind-Grids oder `margin-top: auto` verwenden, um Elemente nach unten zu schieben — das erzeugt hässliche Whitespace-Lücken.

```css
.content {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 32px 48px 20px;
  justify-content: center;
}
```

---

## Common Patterns

### Vergleich (Split)

Für: Vorher/Nachher, Good/Bad, Mit/Ohne, Option A vs. B.

```html
<div class="visual-canvas" data-size="twitter-landscape">
  <div style="display: flex; flex-direction: column; height: 100%; padding: 32px 48px 20px; justify-content: center;">
    <!-- Header -->
    <div style="text-align: center; margin-bottom: 12px;">
      <div class="title">VERGLEICHS-TITEL</div>
      <div class="subtitle">Kontext-Subtitle für Standalone-Nutzung</div>
    </div>

    <!-- Split content -->
    <div class="split">
      <div class="divider"></div>
      <div class="vs-badge">VS</div>

      <div class="split-left">
        <div class="box box--bad box--header" style="width: 100%;">LINKER HEADER</div>
        <!-- Left content items -->
      </div>
      <div class="split-right">
        <div class="box box--good box--header" style="width: 100%;">RECHTER HEADER</div>
        <!-- Right content items -->
      </div>
    </div>

    <!-- Tagline -->
    <div style="text-align: center; padding-top: 10px;">
      <div class="tagline">Prägnantes Fazit mit <span class="highlight">Schlüsselwort</span>.</div>
    </div>
  </div>

  <span class="signature" style="position: absolute; bottom: 10px; right: 20px;"><!-- Signatur aus visual-style.md (signatur-Key); ohne Key: Element weglassen --></span>
</div>
```

Farb-Konventionen:
- Linke Spalte: `--bad`-Akzent (Anti-Pattern, Bad, Vorher)
- Rechte Spalte: `--good`-Akzent (Best Practice, Good, Nachher)
- `.sketch-strikethrough` auf linksseitigen Failure-Items
- `opacity: 0.7` auf durchgestrichenem Text zur visuellen Abschwächung

### Horizontaler Flow (Pipeline)

Für: Links-nach-rechts-Prozesse, Build-Pipelines, Datenflüsse mit Feedback-Loops.

```html
<div style="display: flex; align-items: flex-start; gap: 0;">
  <!-- Wrap each step in a step-col for bracket alignment -->
  <div style="display: flex; flex-direction: column; align-items: center;">
    <div class="box box--fg">Code</div>
  </div>

  <div style="display: flex; align-items: center; height: 58px;">
    <div class="flow-arrow-h"></div>
  </div>

  <div style="display: flex; flex-direction: column; align-items: center;">
    <div class="box box--accent box--elevated">Loop-Schritt</div>
    <!-- Optional bracket label -->
    <div style="margin-top: 6px; text-align: center;">
      <div style="width: 70%; height: 10px; border: 1.5px solid var(--accent); border-top: none; border-radius: 0 0 6px 6px; opacity: 0.35; margin: 0 auto;"></div>
      <span class="annotation" style="font-size: 17px; color: var(--accent); opacity: 0.8;">Loop 1</span>
    </div>
  </div>

  <!-- ... weitere Schritte ... -->

  <div style="display: flex; flex-direction: column; align-items: center;">
    <div class="box box--solid-good">FERTIG &#10003;</div>
  </div>
</div>
```

Pfeil-Farb-Konventionen:
- Neutral/`--fg`-Pfeile: Standard-Vorwärtsfluss (gedämpft, Opazität 0.3)
- `--accent`-Pfeile: zwischen aktiven/Loop-Stufen
- `--good`-Pfeile: Richtung Erfolg/Gate/Fertig

### Dynamische SVG-Feedback-Pfeile

Für gekrümmte Feedback-Pfeile, die zurückschleifen (z. B. Fehler → Retry), per JavaScript dynamisch anhand der tatsächlichen Box-Positionen zeichnen. Das verhindert Fehlausrichtung bei Layout-Änderungen.

```html
<!-- SVG-Overlay innerhalb von .visual-canvas -->
<svg id="feedback-svg" style="position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 2;">
  <defs>
    <marker id="arrow-bad" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#D93025" />
    </marker>
  </defs>
</svg>

<script>
window.addEventListener('load', () => {
  const canvas = document.querySelector('.visual-canvas');
  const cr = canvas.getBoundingClientRect();
  const svg = document.getElementById('feedback-svg');

  function pos(id) {
    const el = document.getElementById(id);
    const r = el.getBoundingClientRect();
    return {
      cx: r.left - cr.left + r.width / 2,
      bottom: r.bottom - cr.top + 3,
    };
  }

  const target = pos('box-code');
  const sources = [
    { box: pos('box-compile'), depth: 38 },
    { box: pos('box-test'),    depth: 62 },
    { box: pos('box-lint'),    depth: 86 },
  ];

  sources.forEach(({ box, depth }, i) => {
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    const cpY = Math.max(box.bottom, target.bottom) + depth;
    path.setAttribute('d',
      `M ${box.cx} ${box.bottom} C ${box.cx} ${cpY}, ${target.cx} ${cpY}, ${target.cx} ${target.bottom}`
    );
    path.setAttribute('stroke', '#D93025');
    path.setAttribute('stroke-width', '2');
    path.setAttribute('stroke-dasharray', '6 4');
    path.setAttribute('fill', 'none');
    path.setAttribute('marker-end', 'url(#arrow-bad)');
    path.setAttribute('opacity', String(0.35 + i * 0.1)); // progressive opacity
    svg.appendChild(path);
  });
});
</script>
```

Hex-Werte in SVG-Attributen/JS (`fill="#D93025"`, `stroke: '#D93025'`) sind Beispielwerte für `--bad` — CSS-Variablen lassen sich in SVG-Attributen/`setAttribute`-Aufrufen nicht direkt nutzen. Mandanten-Palette aus `visual-style.md` übertragen.

Mit einer Feedback-Pill für die textliche Erklärung kombinieren:
```html
<span class="feedback-pill feedback-pill--bad">&#8635; Fehler? Agent korrigiert automatisch und versucht erneut</span>
```

### Hero-Number (Einzelwert)

Für: eine beeindruckende Zahl oder Kennzahl, die Betonung braucht.

```html
<div style="text-align: center;">
  <div class="hero-number" style="font-size: 72px; color: var(--accent);">42%</div>
  <div style="font-family: var(--font-body); font-size: 14px; color: var(--muted); margin-top: 4px; font-weight: 500;">
    SCHNELLER MIT FEEDBACK-LOOPS
  </div>
</div>
```

Für Vergleichs-Hero-Numbers (nebeneinander):
```html
<!-- Links: schlechter Wert (bad) -->
<div style="text-align: center;">
  <div class="hero-number" style="font-size: 72px; color: var(--bad);">40</div>
  <div style="font-family: var(--font-body); font-size: 14px; color: var(--muted);">Minuten verschwendet</div>
</div>

<!-- Rechts: guter Wert (good) -->
<div style="text-align: center;">
  <div class="hero-number" style="font-size: 72px; color: var(--good);">25</div>
  <div style="font-family: var(--font-body); font-size: 14px; color: var(--muted);">Minuten bis zum Erfolg</div>
</div>
```

### Quote-Grafik

Für: herausragende Zitate zum Teilen auf Social Media.

```html
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; padding: 60px;">
  <div class="annotation" style="font-size: 48px; text-align: center; color: var(--fg); line-height: 1.3; max-width: 900px;">
    "Zitat-Text hier einsetzen."
  </div>
  <div class="label" style="margin-top: 32px; color: var(--muted);">
    -- Name, Rolle/Quelle
  </div>
</div>
```

### Vertikaler Flow (Pipeline)

Für: Workflows, Schritt-für-Schritt-Prozesse, Content-Pipelines.

```html
<div class="flow-vertical">
  <div class="box box--fg">Schritt 1: Input</div>
  <div class="flow-arrow flow-arrow--accent"></div>
  <div class="box box--accent box--elevated">Schritt 2: Verarbeiten</div>
  <div class="flow-arrow flow-arrow--accent"></div>
  <div class="box box--accent box--elevated">Schritt 3: Validieren</div>
  <div class="flow-arrow flow-arrow--good"></div>
  <div class="box box--solid-good">Schritt 4: Fertig</div>
</div>
```

### Zeitachse (Timeline)

Für: chronologische Ereignisse, Projekt-Meilensteine.

```html
<div style="display: flex; align-items: center; gap: 0; padding: 0 40px;">
  <!-- Meilenstein -->
  <div style="text-align: center; flex: 1;">
    <div class="label" style="color: var(--accent);">Q1</div>
    <div style="width: 16px; height: 16px; background: var(--accent); border-radius: 50%; margin: 8px auto; box-shadow: 0 2px 6px rgba(26,115,232,0.3);"></div>
    <div style="font-family: var(--font-body); font-size: 14px; color: var(--muted);">Recherche</div>
  </div>
  <!-- Connector -->
  <div style="flex: 2; height: 2px; background: var(--grid);"></div>
  <!-- Nächster Meilenstein... -->
</div>
```

---

## Playwright-Validierungs-Workflow

### Lokalen Server starten

```bash
# Server im Projekt-Root starten (einmal pro Session)
python3 -m http.server 8847 &
```

Playwright blockiert `file://`-URLs. Immer über HTTP servieren.

### Vorschau & Validierung

1. **Navigieren**: `browser_navigate` zu `http://localhost:8847/pfad/zur/datei.html`
2. **Screenshot**: `browser_take_screenshot` mit `type: "png"` zur Prüfung
3. **Iterieren**: HTML editieren, erneut navigieren (erzwingt Reload), erneut screenshotten, bis zufriedenstellend

### Finalen PNG-Export bei exakten Canvas-Maßen

`browser_run_code` nutzen, um genau das `.visual-canvas`-Element zu erfassen:

```javascript
async (page) => {
  await page.waitForLoadState('networkidle');
  await page.locator('.visual-canvas').screenshot({
    path: '/absoluter/pfad/zu/output.png',
    type: 'png',
    scale: 'css'
  });
  return 'Exportiert';
}
```

Immer `scale: 'css'` nutzen, um Pixel-Maße passend zum CSS zu bekommen (z. B. 1200x675), nicht skaliert durch Device-Pixel-Ratio. Immer einen absoluten Pfad für die Ausgabedatei verwenden. HTML-Quelle immer neben dem exportierten PNG speichern (Nachvollziehbarkeit, spätere Iteration).

### Kritisch: Feedback-Loop schließen

NIE ohne Screenshot-Review liefern. Der ganze Sinn von Playwright ist visuelle Validierung. Jede Grafik muss vor der Auslieferung gesehen werden.

---

## Canvas-Größen

`data-size` auf `.visual-canvas` setzen, um die Maße zu steuern:

| data-size | Maße | Für |
|-----------|-----------|-----|
| `twitter-landscape` | 1200x675 | Twitter/X-Posts, Blog-Featured (Default) |
| `twitter-square` | 1080x1080 | Twitter/X, LinkedIn-Carousel |
| `linkedin-feed` | 1200x627 | LinkedIn-Feed-Posts |
| `linkedin-carousel` | 1080x1080 | LinkedIn-Carousel-Slides |
| `blog-featured` | 1200x630 | Blog-Header-Bilder |
| `ig-portrait` | 1080x1350 | Instagram-Feed (Portrait), Carousel-Slides |
| `ig-story` | 1080x1920 | Instagram-Stories |

---

## Häufige Pitfalls & Fixes

### Whitespace-Lücken zwischen Content und unteren Elementen

**Problem**: `margin-top: auto` auf Ergebnis-Badges oder Outcome-Elementen schiebt sie ganz nach unten — große Lücke entsteht.

**Fix**: Explizites `margin-top: 16px` oder `20px` statt `auto` nutzen. `justify-content: center` auf dem Parent übernimmt die Gesamt-Zentrierung.

### Flex-Expansion erzeugt Leerraum

**Problem**: `flex: 1` auf einem `.split`-Grid füllt den gesamten verbleibenden vertikalen Raum, drückt Content auseinander.

**Fix**: `flex: 1` aus dem Split entfernen. `justify-content: center` auf dem `.content`-Wrapper stattdessen setzen.

### SVG-Pfeile nach Layout-Änderungen fehlausgerichtet

**Problem**: Hardcodierte SVG-Koordinaten brechen, wenn sich Box-Größen oder -Positionen ändern.

**Fix**: JavaScript nutzen, um SVG-Pfeile dynamisch anhand tatsächlicher Element-Positionen zu zeichnen (siehe Pattern „Dynamische SVG-Feedback-Pfeile” oben).

### Klammern nicht auf Höhe ihrer Loop-Boxen

**Problem**: Loop-Labels (Loop 1, Loop 2, Loop 3) landen unter der falschen Box.

**Fix**: Jede Box + Klammer in einen `.step-col`-Flex-Column-Container wrappen, damit sie zusammenbleiben:

```html
<div class="step-col">
  <div class="step-box loop" id="box-compile">
    <span class="step-name">COMPILE</span>
    <span class="step-label">Build-Loop</span>
  </div>
  <div class="bracket">
    <div class="bracket-line"></div>
    <span class="bracket-label">Loop 1</span>
  </div>
</div>
```

---

## Quality-Gate-Checkliste

Vor jedem Export einer Grafik ALLE Punkte prüfen:

- [ ] Alle Texte mindestens 14px (lesbar auf Mobile)
- [ ] Hero-Element ist das visuell prominenteste Element
- [ ] Maximal 3 Akzentfarben verwendet
- [ ] Textur gemäß `visual-style.md` vorhanden
- [ ] Noise-Grain-Overlay vorhanden (Opazität 0.03)
- [ ] Box-Shadows auf allen wichtigen Elementen (nicht flach)
- [ ] Annotations nutzen `var(--font-annotation)`
- [ ] Anti-Patterns nutzen Strikethrough + `--bad`-Akzente
- [ ] Kontext-Subtitle für Standalone-Social-Media-Nutzung vorhanden
- [ ] Signatur gemäß `visual-style.md` gesetzt (falls definiert)
- [ ] Kontrastverhältnis besteht 4.5:1 für allen Text
- [ ] Kein verschwendeter Whitespace — Content füllt den Canvas
- [ ] Content ist vertikal zentriert (keine großen Lücken)
