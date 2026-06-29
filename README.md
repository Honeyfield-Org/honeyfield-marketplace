# Honeyfield Marketplace

Öffentlicher Claude-Code-Plugin-Marketplace der Honeyfield GmbH. Bündelt die
Honeyfield-MCP-Server als einzeln installierbare Plugins über das Gateway
`mcp.honeyfield.at`. (Interne Plugins liegen separat im privaten
`honeyfield-internal-marketplace`.)

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
| `honeyfield-marketing-mcp` | Marketing-Ops — Google Ads, GA4, Search Console, Google Business Profile, GTM, Clarity, DataForSEO **+ Audit-Skills** | `https://mcp.ads.honeyfield.at/mcp` |
| `honeyfield-eurlex-mcp` | EUR-Lex — EU-Rechtsdatenbank (Suche, Volltext, Zitate, Konsolidierungen) | `https://mcp.honeyfield.at/eurlex/mcp` |
| `honeyfield-ris-mcp` | RIS — österreichisches Rechtsinformationssystem (Bundes-/Landesrecht, Judikatur, Verordnungen) | `https://mcp.honeyfield.at/ris/mcp` |

Jeder MCP ist ein eigenes Plugin — so installiert man nur, was man braucht.
`honeyfield-marketing-mcp` bündelt die Marketing-Tools **und** die dazu passenden
Audit-Skills in einem Plugin — ein Install, alles dabei.

## Skills (honeyfield-marketing-mcp)

| Skill | Zweck |
|---|---|
| `seo-audit` | Datengetriebener, DACH-kalibrierter SEO-Audit (DE/AT/CH) — zieht echte Daten aus Search Console, DataForSEO, GA4, Clarity und Google Business Profile, priorisiert Befunde nach Wirkung und kann behebbare Punkte direkt umsetzen. |

Trigger z.B.: „mach einen SEO-Audit für example.at". Weitere Skills folgen.

## Updates

```
/plugin marketplace update honeyfield-marketplace
```

## Beitragen

1. Branch + PR gegen `main`; die CI validiert alle Plugins (`claude plugin validate`).
2. Neue Plugins: Ordner unter `plugins/<name>/` mit `.claude-plugin/plugin.json`
   anlegen und in `.claude-plugin/marketplace.json` registrieren.
3. Versionsnummer im jeweiligen `plugin.json` und im Katalog-Eintrag erhöhen.

## Troubleshooting

| Problem | Lösung |
|---|---|
| `marketplace add` schlägt fehl | GitHub-Auth prüfen (`gh auth status` / SSH-Key) |
| MCP-Tools fehlen nach Install | Claude Code neu starten; `/mcp` zeigt den Verbindungsstatus |
| Gateway nicht erreichbar | `curl -I https://mcp.honeyfield.at/eurlex/mcp` bzw. `https://mcp.ads.honeyfield.at/mcp` prüfen |
| Plugin-Update kommt nicht an | `/plugin marketplace update honeyfield-marketplace`, danach neu starten |
