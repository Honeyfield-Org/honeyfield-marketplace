# Plattform-Specs & Bild-Optimierung

Zieldimensionen je Plattform, Format-Wahl, Web-Optimierung, OG-Images, Alt-Text. Neue Bilder entstehen von Anfang an optimiert — der Audit bestehender Seiten gehört zu `seo-audit`.

## Dimensionen je Plattform

| Plattform | Format | Pixel | KI: `--aspect-ratio` / `--resolution` | Code-Gen: `data-size` |
|---|---|---|---|---|
| LinkedIn | Feed | 1200×627 | `16:9` / `1K` | `linkedin-feed` |
| LinkedIn | Carousel-Slide | 1080×1080 | `1:1` / `1K` | `linkedin-carousel` |
| Instagram | Feed/Carousel | 1080×1350 | `4:5` / `1K` | `ig-portrait` |
| Instagram | Story / Reel-Cover | 1080×1920 | `9:16` / `1K` | `ig-story` |
| Facebook | Feed/Link | 1200×630 | `16:9` / `1K` | `blog-featured` |
| Twitter/X | Landscape | 1200×675 | `16:9` / `1K` | `twitter-landscape` |
| Twitter/X | Square | 1080×1080 | `1:1` / `1K` | `twitter-square` |
| Blog | Hero / OG | 1200×630 | `16:9` / `2K` | `blog-featured` |
| Blog | Inline | variabel | `3:2` / `1K` | — |
| Meta Ads | Feed quadratisch | 1080×1080 | `1:1` / `1K` | `twitter-square` |
| Meta Ads | Feed/Link | 1200×628 | `16:9` / `1K` | `blog-featured` |

Hinweise: Blog-Hero in `2K` (Primär-Visual), Social reicht `1K`. Meta-Ad-Bilder: max. **8 MB** (`meta_upload_ad_image` — Größe vor dem Upload prüfen). Krumme Plattform-Ratios (1.91:1) werden mit `16:9` generiert und beim Export/Zuschnitt exakt gesetzt (Code-Gen trifft die Pixel exakt via `data-size`).

## Format-Guide

| Format | Wofür | Merken |
|---|---|---|
| **PNG** | Code-Gen-Export, Screenshots, Transparenz | verlustfrei; Standard-Export dieses Skills |
| **WebP** | Web-Auslieferung (Fotos + Grafiken) | Default fürs CMS; 75–85 % Qualität |
| **AVIF** | höchste Kompression | wenn CDN/CMS es ausliefert |
| **JPEG** | Fallback ältere Browser | nur als Fallback |
| **SVG** | Logos, Icons | nicht Output dieses Skills (kein Logo-Design) |

## Optimierungs-Checkliste (jedes Bild, das ins Web geht)

- [ ] Auf Anzeigegröße skalieren (keine 4000px-Bilder in 800px-Containern)
- [ ] WebP erzeugen (Fallback JPEG/PNG) — oder CDN-Auto-Format des CMS nutzen
- [ ] Qualität 75–85 % (Fotos) / nahezu verlustfrei (Grafiken mit Text)
- [ ] Ziel: Hero <200 KB
- [ ] `loading="lazy"` unterhalb des Folds; `width`/`height` gegen Layout-Shift (CLS)
- [ ] Alt-Text mitliefern (unten)

Kommandos (Verfügbarkeit prüfen, sonst benennen statt still überspringen):

```bash
cwebp -q 80 bild.png -o bild.webp          # einzelnes Bild
mogrify -format webp -quality 80 *.png     # Batch (ImageMagick)
```

## OG-Images (Social-Preview)

1200×630, unter 200 KB. Meta-Tags, die die Seite braucht:

```html
<meta property="og:image" content="https://domain.tld/og/seite.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://domain.tld/og/seite.png" />
```

Das OG-Bild ist meist identisch mit dem Blog-Hero (`blog-featured`). Ob die Tags gesetzt sind, prüft `seo-audit`/`geo-audit` — dieser Skill liefert das Bild.

## Alt-Text-Regeln (Pflicht-Output pro Bild)

- Ein beschreibender Satz: was ist zu sehen, in natürlicher Sprache der Zielgruppe.
- Relevantes Keyword natürlich einbauen — **kein** Keyword-Stuffing.
- Rein dekorative Bilder: leerer Alt-Text (`alt=""`) ist die richtige Empfehlung.
- Zahlen-Grafiken: Kernaussage in den Alt-Text („Balkendiagramm: X wächst von … auf …").
- CH-Markt: kein ß auch im Alt-Text.
