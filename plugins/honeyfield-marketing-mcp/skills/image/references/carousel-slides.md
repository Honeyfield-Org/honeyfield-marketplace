# Carousel-Slides — Instagram-Slide-Typen

Referenz für Instagram-Carousel-Slides. Fünf Slide-Typen, 1080x1350px (4:5 Portrait, `data-size="ig-portrait"`), als eigenständige HTML-Dateien gebaut, validiert und exportiert via Playwright. Technische Referenz für den `image`-Skill — on-demand laden, hält SKILL.md schlank.

---

## Vorbereitung: Base-Template & Slide-Klassen

Basis ist `assets/base-template.html` (im Skill-Verzeichnis — ins Arbeitsverzeichnis kopieren, CSS-Variablen aus `visual-style.md` setzen) mit `data-size="ig-portrait"`. Die Slide-spezifischen Klassen ergänzen das Base-Template über folgenden Style-Block (in jede Slide-HTML-Datei einbetten):

```html
<style>
  .slide {
    position: relative; width: 100%; height: 100%;
    display: flex; flex-direction: column; justify-content: center;
    padding: 64px 72px; font-family: var(--font-heading);
  }
  .slide--hook .hook-headline { font-size: 64px; font-weight: 700; line-height: 1.15; color: var(--fg); }
  .hook-headline .accent { color: var(--bad); }
  .hook-headline .accent-blue { color: var(--accent); }
  .hook-headline .accent-green { color: var(--good); }
  .hook-subtext { font-family: var(--font-body); font-size: 24px; color: var(--muted); margin-top: 20px; }
  .swipe-indicator { font-family: var(--font-annotation); font-size: 26px; color: var(--accent); margin-top: 48px; }
  .swipe-indicator::after { content: ' \2192'; }
  .content-number { position: absolute; top: 48px; right: 64px; font-size: 120px; font-weight: 700; color: var(--accent); opacity: 0.15; }
  .content-headline { font-size: 48px; font-weight: 700; color: var(--fg); }
  .content-body { font-family: var(--font-body); font-size: 26px; line-height: 1.5; color: var(--fg); margin-top: 20px; }
  .content-annotation { font-family: var(--font-annotation); font-size: 26px; color: var(--muted); margin-top: 24px; }
  .slide--problem { text-align: center; align-items: center; }
  .problem-headline { font-size: 46px; font-weight: 700; line-height: 1.2; color: var(--fg); }
  .problem-body { font-family: var(--font-body); font-size: 26px; line-height: 1.55; color: var(--muted); max-width: 80%; }
  .divider-line { width: 96px; height: 3px; background: var(--accent); margin: 28px auto; border-radius: 2px; }
  .timeline-title { font-size: 40px; font-weight: 700; color: var(--fg); margin-bottom: 40px; }
  .timeline-track { border-left: 3px solid var(--grid); padding-left: 32px; display: flex; flex-direction: column; gap: 36px; }
  .timeline-item { position: relative; }
  .timeline-item::before { content: ''; position: absolute; left: -41px; top: 6px; width: 15px; height: 15px; border-radius: 50%; background: var(--accent); }
  .timeline-item:last-child::before { background: var(--good); }
  .timeline-label { font-size: 20px; font-weight: 700; color: var(--accent); text-transform: uppercase; }
  .timeline-item:last-child .timeline-label { color: var(--good); }
  .timeline-text { font-family: var(--font-body); font-size: 24px; color: var(--fg); margin-top: 6px; }
  .slide--cta { text-align: center; align-items: center; }
  .cta-save-icon svg { width: 72px; height: 72px; stroke: var(--accent); fill: none; stroke-width: 2; }
  .cta-headline { font-size: 44px; font-weight: 700; color: var(--fg); margin-top: 28px; }
  .cta-subtext { font-family: var(--font-body); font-size: 24px; color: var(--muted); margin-top: 16px; }
  .cta-handle { font-size: 26px; font-weight: 600; color: var(--accent); margin-top: 32px; }
  .progress-dots { position: absolute; bottom: 36px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; }
  .progress-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--fg); opacity: 0.15; }
  .progress-dot--active { background: var(--accent); opacity: 0.7; }
  .slide-handle { position: absolute; bottom: 32px; right: 40px; font-size: 16px; color: var(--muted); opacity: 0.4; }
</style>
```

---

## Slide-Typ-Übersicht

| Slide-Rolle | CSS-Klasse | Wann nutzen |
|------------|-----------|-------------|
| Hook/Titel (Slide 1) | `slide--hook` | Immer die erste Slide |
| Problem/Setup | `slide--problem` | Pain Point oder Kontext etablieren |
| Nummerierter Content | `slide--content` | Eine Idee mit Nummern-Präfix vermitteln |
| Zeitachse (Timeline) | `slide--timeline` | Fortschritt über Zeit zeigen |
| CTA (letzte Slide) | `slide--cta` | Immer die letzte Slide |

---

## 1. Hook-Slide (`slide--hook`)

Die erste Slide. Stoppt den Scroll. Fette Headline, optionaler Subtext, Swipe-Indikator.

```html
<div class="slide slide--hook">
  <div class="hook-headline">
    Warum dein Ergebnis <span class="accent">einbricht</span> nach Schritt 3
  </div>
  <div class="hook-subtext">
    Und die 3 Fixes, die die meisten überspringen
  </div>
  <div class="swipe-indicator">Zum Weiterlesen wischen</div>
</div>
```

**Regeln:**
- Headline: 3-7 Wörter, fett, aufmerksamkeitsstark
- `.accent` (bad), `.accent-blue` (accent) oder `.accent-green` (good) für ein Schlüsselwort nutzen
- Subtext: eine Zeile, die den Nutzen verspricht
- Swipe-Indikator nutzt `var(--font-annotation)`, hängt automatisch einen Pfeil an
- Keine Progress-Dots auf dieser Slide
- Keine Slide-Nummer

---

## 2. Content-Slide (`slide--content`)

Der Arbeitspferd-Typ. Vermittelt eine Idee pro Slide. Große Hintergrund-Nummer + Headline + Body-Text.

```html
<div class="slide slide--content">
  <div class="content-number">01</div>
  <div class="content-headline">Übe unter Belastung</div>
  <div class="content-body">
    Nicht einfach nur üben. Übe NACH der anstrengenden Phase. Genau da entscheidet sich später der Ernstfall.
  </div>
  <div class="content-annotation">nach der Belastung, nicht davor</div>
</div>
```

**Regeln:**
- `.content-number`: Groß (120px), `--accent`, 15% Opazität Hintergrund-Element. „01”, „02”, „03” usw. nutzen
- `.content-headline`: 3-7 Wörter, fett
- `.content-body`: 15-30 Wörter unterstützender Text. Nur eine Idee.
- `.content-annotation` (optional): `var(--font-annotation)`, bringt Persönlichkeit
- Progress-Dots auf diesen Slides immer ergänzen

---

## 3. Problem-Slide (`slide--problem`)

Baut Kontext auf. Zentriert den Content. Beschreibt Pain Point oder Situation.

```html
<div class="slide slide--problem">
  <div class="problem-headline">
    Du übst hart. Der Ernstfall erzählt eine andere Geschichte.
  </div>
  <div class="divider-line"></div>
  <div class="problem-body">
    Das Ergebnis bricht an bestimmten Stellen ein. Übergänge kosten Zeit.
    Du schiebst es auf die Grundlagen. Aber die Grundlagen sind nicht das Problem.
  </div>
</div>
```

**Regeln:**
- Zentriertes Layout, textfokussiert
- Headline: benennt das Problem direkt
- Body: 2-3 Sätze, die den Pain Point ausführen
- Optionale `.divider-line` zwischen Headline und Body
- Gut für Slide 2 (nach dem Hook), um das Problem vor den Fixes zu etablieren

---

## 4. Timeline-Slide (`slide--timeline`)

Zeigt Fortschritt über Zeit. Vertikale Zeitachse mit beschrifteten Meilensteinen.

```html
<div class="slide slide--timeline">
  <div class="timeline-title">Was sich verändert, wenn smart trainiert wird</div>
  <div class="timeline-track">
    <div class="timeline-item">
      <div class="timeline-label">Woche 2-3</div>
      <div class="timeline-text">Sauberere Grundlagen, bessere Bewegung an den kritischen Stellen</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-label">Woche 4-6</div>
      <div class="timeline-text">Stabilere Ergebnisse, stärkere Leistung in den Kernübungen</div>
    </div>
    <div class="timeline-item">
      <div class="timeline-label">Woche 8+</div>
      <div class="timeline-text">Flüssigerer Ablauf, weniger Einbrüche, bessere Abschlüsse</div>
    </div>
  </div>
</div>
```

**Regeln:**
- Titel oben beschreibt die Transformation
- 3-5 Meilensteine (3 ist ideal)
- Labels sind kurz (Zeiträume, Phasen)
- Text ist eine Zeile pro Meilenstein
- Erste Items: `--accent`-Dot; letztes Item: `--good`-Dot (Progression)
- Linke Randlinie verbindet die Meilensteine

---

## 5. CTA-Slide (`slide--cta`)

Die letzte Slide. Fordert zu Save/Share/Follow auf. Sauber und minimal.

```html
<div class="slide slide--cta">
  <div class="cta-save-icon">
    <svg viewBox="0 0 24 24">
      <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
    </svg>
  </div>
  <div class="cta-headline">Speichere das für später</div>
  <div class="cta-subtext">Mehr dazu: [Link/Quelle]</div>
  <div class="cta-handle"><!-- Signatur/Handle aus visual-style.md (signatur-Key); ohne Key: Element weglassen --></div>
</div>
```

**Regeln:**
- Bookmark-Icon als visueller Anker
- Headline: direkter CTA (speichern, teilen, markieren)
- Subtext: optionaler Kontext oder Quelle
- Handle: `--accent`, verlinkt zum Account (falls in `visual-style.md` gesetzt, sonst Element weglassen)
- Minimal halten — keine weiteren Elemente ergänzen
- Progress-Dots ergänzen (letzter Dot aktiv)

---

## Progress-Dots

Bei allen Slides außer Slide 1 (Hook) ergänzen. Position absolut, unten zentriert.

```html
<div class="progress-dots">
  <div class="progress-dot"></div>
  <div class="progress-dot"></div>
  <div class="progress-dot progress-dot--active"></div>  <!-- aktuelle Slide -->
  <div class="progress-dot"></div>
  <div class="progress-dot"></div>
</div>
```

- Ein Dot pro Gesamt-Slide-Anzahl
- Aktiver Dot (aktuelle Slide) bekommt `.progress-dot--active`
- Dots: 10px, `--fg` bei 15% Opazität; aktiv: `--accent` bei 70% Opazität
- Slide 1 (Hook): keine Dots
- Letzte Slide (CTA): letzter Dot aktiv

---

## Handle-Branding

In jede Slide unten rechts einfügen:

```html
<div class="slide-handle"><!-- Signatur/Handle aus visual-style.md (signatur-Key); ohne Key: Element weglassen --></div>
```

- Subtil: 16px, `--muted`, 40% Opazität
- Absolut positioniert, stört den Slide-Content nicht

---

## Slide-Design-Regeln (alle Slides)

- Canvas: **1080x1350px** (4:5 Portrait, `data-size="ig-portrait"`)
- Textur (Grid + Noise-Grain): siehe `grafik-patterns.md` → „Textur & Tiefe” (Default des Base-Templates; Grid-Nutzung abhängig von `visual-style.md`)
- Handle-Branding unten rechts (subtil, gemäß `visual-style.md`)
- Minimum 14px Schriftgröße für allen Text
- Box-Shadows auf allen geboxten Elementen (nie flach)
- Padding: 72px horizontal, 64px vertikal (in der `.slide`-Klasse eingebaut)
- Maximal 10 Slides pro Carousel (Instagram-Limit)

---

## Playwright-Pipeline

### Build

1. Slide-Inhalte und -Reihenfolge aus der Vorgabe (Content-Plan, Briefing o. Ä.) ableiten
2. Für jede Slide eine eigenständige HTML-Datei aus `assets/base-template.html` (`data-size="ig-portrait"` + Slide-Style-Block, siehe oben) erstellen
3. Progress-Dots (außer Slide 1), Handle-Branding und Slide-spezifischen Content ergänzen
4. Als `slide-01.html`, `slide-02.html` usw. im Arbeitsverzeichnis speichern

### Validate

1. HTTP-Server starten: `python3 -m http.server 8847 &`
2. Für jede Slide: `browser_navigate` → `browser_take_screenshot` → prüfen
3. Prüfen: Textlesbarkeit, visuelle Hierarchie, Progress-Dots korrekt, Textur vorhanden, kein Overflow/Clipping
4. Probleme fixen und erneut validieren

### Export

```javascript
async (page) => {
  await page.waitForLoadState('networkidle');
  await page.locator('.visual-canvas').screenshot({
    path: '/absoluter/pfad/zu/slide-01.png',
    type: 'png',
    scale: 'css'
  });
  return 'Slide 01 exportiert';
}
```

Immer `scale: 'css'` für exakte 1080x1350-Maße nutzen. Immer absolute Pfade verwenden.

### Final Review

Alle exportierten PNGs in Reihenfolge screenshotten, um zu prüfen:
- Konsistenter Grafik-Stil über alle Slides
- Korrekte Slide-Reihenfolge
- Visueller Flow vom Hook zum CTA
- Alle Progress-Dots stimmen über die Slides hinweg überein

---

## Häufige Pitfalls

### Whitespace-Lücken
Nie `margin-top: auto` nutzen. Explizite Margins verwenden. `justify-content: center` auf dem `.slide`-Parent übernimmt die vertikale Zentrierung.

### Flex-Expansion
Nie `flex: 1` auf Kind-Elementen nutzen. Die `.slide`-Klasse übernimmt Zentrierung bereits via Flexbox.

### Font-Loading
Immer `waitForLoadState('networkidle')` vor dem Export nutzen. Google Fonts müssen vollständig geladen sein, sonst rendert Text im Fallback-Font.

### Inkonsistente Slides
Alle Slides müssen dasselbe Padding, denselben Hintergrund und dieselben Brand-Elemente teilen. Nie Canvas-Maße oder Hintergrund-Layer pro Slide ändern.

---

## Customization

Das Template liefert die Basis. Pro Slide anpassen, wie nötig:

- **Icons/Emojis:** Inline-SVG oder Emoji-Zeichen innerhalb der Content-Bereiche ergänzen
- **Boxen:** `.box`, `.box--accent`, `.box--bad`, `.box--good` für hervorgehobene Elemente nutzen
- **Farb-Akzente im Text:** Schlüsselwörter in `<span class="accent">`, `.accent-blue`, `.accent-green` wrappen
- **Zusätzliche Elemente:** Eigenes CSS in einem `<style>`-Block in der HTML ergänzen, falls eine Slide einzigartige visuelle Elemente braucht (z. B. Vergleichs-Grid, Icon-Reihe)
