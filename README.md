# Honeyfield Marketplace

Öffentlicher Claude-Code-Plugin-Marketplace der Honeyfield GmbH. Bündelt die
Honeyfield-MCP-Server als einzeln installierbare Plugins über die
Honeyfield-Gateways (`mcp.honeyfield.at`, `mcp.ads.honeyfield.at`). (Interne
Plugins liegen separat im privaten `honeyfield-internal-marketplace`.)

## Installation

```
/plugin marketplace add Honeyfield-Org/honeyfield-marketplace
/plugin install honeyfield-marketing-mcp@honeyfield-marketplace
/plugin install honeyfield-eurlex-mcp@honeyfield-marketplace
/plugin install honeyfield-ris-mcp@honeyfield-marketplace
```

Nach der Installation Claude Code neu starten; `/mcp` zeigt den Verbindungsstatus.

## Plugins

| Plugin | MCP-Server | Endpoint |
|---|---|---|
| `honeyfield-marketing-mcp` | Marketing-Ops — Google Ads, GA4, Search Console, Google Business Profile, GTM, Clarity, DataForSEO, LinkedIn/Meta Ads, Strapi- & WordPress-CMS **+ Skills (Projekt-Kontext + Audits + Ad-Creation + Wochenreport)** | `https://mcp.ads.honeyfield.at/mcp` |
| `honeyfield-eurlex-mcp` | EUR-Lex — EU-Rechtsdatenbank (Suche, Volltext, Zitate, Konsolidierungen) | `https://mcp.honeyfield.at/eurlex/mcp` |
| `honeyfield-ris-mcp` | RIS — österreichisches Rechtsinformationssystem (Bundes-/Landesrecht, Judikatur, Verordnungen) | `https://mcp.honeyfield.at/ris/mcp` |

Jeder MCP ist ein eigenes Plugin — so installiert man nur, was man braucht.
`honeyfield-marketing-mcp` bündelt die Marketing-Tools **und** die dazu passenden
Skills (Projekt-Kontext-Fundament + Audits + Ad-Creation + Wochenreport) in einem
Plugin — ein Install, alles dabei.

## Skills (honeyfield-marketing-mcp)

| Skill | Zweck |
|---|---|
| `projekt-kontext` | Foundation-Skill — legt das Projekt-Kontext-Fundament eines Kunden (Markt, Marke, Ziele, rechtlicher Rahmen) an und pflegt es; alle anderen Skills lesen es zuerst, statt erneut zu fragen. Am Anfang eines Kunden-Projekts ausführen. |
| `seo-audit` | Datengetriebener, DACH-kalibrierter SEO-Audit (DE/AT/CH) — zieht echte Daten aus Search Console, DataForSEO, GA4, Clarity und Google Business Profile, priorisiert Befunde nach Wirkung und kann behebbare Punkte direkt umsetzen. |
| `geo-audit` | GEO-/AEO-Audit — prüft, ob KI-Assistenten (ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews) die Website lesen, fetchen und zitieren können (Crawlbarkeit, Rendering, Schema), DACH-kalibriert. |
| `google-ads-audit` | Google-Ads-Audit — Wasted Spend, verschwendete Suchbegriffe, Quality Score, Impression Share, Konto-Struktur; zieht echte Ads-Daten (+ GA4-Cross-Check) und kann nach Bestätigung direkt aufräumen. |
| `tracking-check` | Measurement-Audit — prüft die Integrität des Conversion-/Event-Trackings (GA4, GTM, Google Ads) end-to-end, stuft jeden Befund nach Beweiskraft (gemessen / nur konfiguriert / nicht prüfbar) und behebt Sicheres nach Bestätigung. DACH-Consent-Layer (Consent Mode v2, TDDDG). |
| `ad-creative` | Google-Ads-Copy-Generator — erstellt/iteriert Responsive Search Ads + Sitelinks daten-fundiert aus der Konto-Performance, hält die harten Zeichen-Limits gegen deutsche Komposita, prüft DACH-Werberecht (UWG/Preisangaben) und schreibt nach Bestätigung als pausierte Assets ins Konto. |
| `wochenreport` | Cross-Kanal-Report-Hub — zieht die Kern-KPIs aus allen verbundenen Kanälen (Google Ads, Meta/LinkedIn Ads, SEO, Local/GBP, GA4, AI-Sichtbarkeit) als Zeitraum-Vergleich (Woche-über-Woche / Monat-über-Monat); read-only, verweist bei Auffälligkeiten auf den passenden Audit. |

Trigger z.B.: „mach einen SEO-Audit für example.at", „GEO-Audit für …", „Google-Ads-Audit für …". Jeder Skill liest zuerst den `projekt-kontext`, falls vorhanden. Weitere Trigger: „stimmt mein Conversion-Tracking?" (`tracking-check`), „schreib neue Anzeigen für Kampagne X" (`ad-creative`), „Wochenreport für Kunde Y" (`wochenreport`).

## Updates

```
/plugin marketplace update honeyfield-marketplace
```

## Beitragen

1. Branch + PR gegen `main`. Die CI (`.github/workflows/validate.yml`, Check `validate`)
   prüft JSON-Manifeste, **Version-Sync** (`plugin.json` ↔ `marketplace.json`),
   **Skill-Frontmatter** (echter YAML-Parse, fängt den Anführungszeichen-Footgun) und
   `claude plugin validate`. Der Check ist als Required Status Check gesetzt: **rot = kein Merge**.
2. Neue Plugins: Ordner unter `plugins/<name>/` mit `.claude-plugin/plugin.json`
   anlegen und in `.claude-plugin/marketplace.json` registrieren.
3. **Bei jeder inhaltlichen Änderung die Version erhöhen** — sonst erkennt der
   Org-Marketplace-Sync das Update nicht. Drei Felder synchron halten:
   `plugin.json` → `version`, der Plugin-Eintrag in `marketplace.json`
   (`plugins[].version`, **muss = `plugin.json`**) und die Katalog-`metadata.version`.
4. Sichtbar wird ein Skill in Claude Web erst **nach dem Merge nach `main`** — der
   Sync zieht von `main`, nicht vom Feature-Branch.

## Troubleshooting

| Problem | Lösung |
|---|---|
| `marketplace add` schlägt fehl | GitHub-Auth prüfen (`gh auth status` / SSH-Key) |
| MCP-Tools fehlen nach Install | Claude Code neu starten; `/mcp` zeigt den Verbindungsstatus |
| Gateway nicht erreichbar | `curl -I https://mcp.honeyfield.at/eurlex/mcp` bzw. `https://mcp.ads.honeyfield.at/mcp` prüfen |
| Plugin-Update / neuer Skill kommt nicht an | Erstens: Version in `plugin.json` **und** `marketplace.json` (Plugin-Eintrag + `metadata.version`) erhöht? Zweitens: Änderung nach `main` gemerged? Der Sync (auch Org-Auto-Sync in Claude Web) zieht von `main`, nicht vom Feature-Branch. Dann `/plugin marketplace update honeyfield-marketplace` und neu starten. |
