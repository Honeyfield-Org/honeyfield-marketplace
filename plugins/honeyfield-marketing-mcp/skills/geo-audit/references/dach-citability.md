# DACH-Citability — Drittplattformen, Methodik, AI-Referrer

Phase 5 (Off-site-Citability) + Operator (Zielliste). Das SOTA-Material aus generischen Marketing-Skills ist US-zentrisch — diese DACH-Liste ist der Value-Add. Selbst-Citation ist unmöglich, also sind Drittquellen die einzige Adresse für Citations.

## Mess-Loop (Weg B Default, manueller Fallback — Phase 5/7)

Default: `dfs_llm_mentions`/`dfs_llm_top_domains` (Weg B, s. `llm-mentions-adapter.md`) liefert das automatisiert, pay-as-you-go über das normale DataForSEO-Guthaben. Schlägt der Zugriff fehl (`subscription_required`, z. B. Guthaben aufgebraucht), monatlich manuell ChatGPT/Claude/Perplexity fragen: „Was sind die besten [Kategorie]-Tools/-Anbieter?" und protokollieren, wo die Marke auftaucht (Weg A). Das ist der direkte Citability-Check. Details/Protokoll: `llm-mentions-adapter.md`.

## Priorität A — Entity-Baseline (kategorie-unabhängig, global, DACH-tauglich)

Speist die Trainings-/Knowledge-Korpora der Modelle direkt. **Immer** als Ziel, egal welche Branche:
- **Wikidata** + **Wikipedia-DE** (sofern Relevanzkriterien erfüllt) — härtester Hebel für deutschsprachige Entity-Erkennung.
- **LinkedIn** Company Page (gepflegt).
- **Crunchbase**.
- **Dun & Bradstreet** (Business-Credibility, feeds AI-Korpora).
- Verknüpfen über `sameAs` in der Organization-Schema (siehe `schema-templates.md`).

## Priorität B — Review-Sites / Verzeichnisse (höchste Zitathäufigkeit bei „beste X"-Queries)

KI-Engines ziehen bei „bestes [Kategorie]"-Fragen stark aus High-DR-Verzeichnissen.

**Global (in DACH genutzt):** G2, Capterra, AlternativeTo (als Alternative zu den Top-Konkurrenten listen), SaaSHub, Software Advice, TrustRadius. **Schwelle: ~10 Reviews** — darunter sind Profile wirkungslos.

**DACH-Pendants (das SOTA-Material kennt sie NICHT — hier ergänzen):**
- **OMR Reviews** — das DACH-G2-Äquivalent, für deutschsprachige B2B-Queries oft wichtiger.
- **ProvenExpert** — Bewertungs-Aggregator, stark in DE.
- **Trusted Shops** — E-Commerce-Trust (Shop-Kunden).
- **Capterra.de / GetApp.de** — deutsche Varianten.
- **WLW (Visable) / „Wer liefert was"** — B2B-Industrie/Beschaffung DACH.
- **Cylex (cylex.de), Das Örtliche, Gelbe Seiten** — lokale Verzeichnisse.
- **OpenPR (openpr.de), Tupalo, EU-Business** — europäisch/deutsch.

Für DACH **abwerten/skippen:** US-Local-Directories (Manta, MerchantCircle, iBegin, 2FindLocal), reine US-PR-Wire-Sites.

## Priorität C — „Best of"-Listicles via Outreach

Oft wertvoller als Verzeichnisse: dofollow-Link + redaktioneller Trust + In-Market-Traffic + **AI-Citation-Gewicht**. Such-Patterns zum Auffinden der Quellen, die die KI zitiert (eingedeutscht):
- `"beste [Kategorie] Tools 2026"`
- `"[Kategorie] Anbieter Vergleich"`
- `"[Kategorie] Software Test"`
- `"beste [Konkurrent] Alternative"`

Gefundene Seiten → Outreach (eigene, distinkte Lead-Sentence pro Plattform; KI-Engines down-weighten Duplicate-Beschreibungen).

## Priorität D — MCP / Agent-Registries (nur bei AI-nativem Produkt)

Für Tools wie Honeyfield selbst relevant — LLMs ziehen daraus bei MCP-/Agent-Fragen: **Glama** (A/B/C/F-Grade optimieren), **mcpmarket.com**, **PulseMCP**, **Smithery**, **mcpservers.org**, **mcp.so**, **cursor.directory** + GitHub-Repo mit MCP-Topics und `awesome-mcp-servers`-PR. Achtung: einzelne Infra-Connector-Server zu listen reicht nicht — das **Flagship-Produkt** selbst muss gelistet sein.

**Verifikation (Pflicht):** Drittpräsenz IMMER per **WebFetch der Zielseite** prüfen, NIE aus dem WebSearch-Antworttext übernehmen (LLM-synthetisiert, erfindet Profile/Listings — im Live-Test real passiert). Bei mehrdeutigem Markennamen (z.B. Honeyfield ≠ HoneyBook/Honey/Honeyfield Communities) per Domain/Standort/Rechtsform ankern. WebSearch ist zudem US-lastig → für DACH-Review-Sites WebFetch direkt auf deren Suchseite.

## Earn-Mechaniken (verdiente Drittnennungen, nach Hebel)

1. **Original-Research / Daten-Story** (höchster Hebel): „Wir haben 10.000 X analysiert und Y gefunden" wird zur **Primärquelle** für alle, die über das Thema schreiben. Sprachneutral, voll DACH-tauglich.
2. **Reddit / Hacker News** (Claude/Perplexity indexieren stark) — eher für EN-Visibility; DACH-Pendant: Fachforen, LinkedIn-DE, t3n-/Heise-Kommentarräume.
3. **Inbound Press-Requests:** Connectively (ex-HARO), Qwoted, Help A B2B Writer (EN/US). DACH: themenrelevante LinkedIn-Calls, dpa-Anfragen.
4. **DACH-Fachpresse für Erwähnungen:** t3n, Heise, Golem, Gründerszene, OMR, **The Decoder** (deutsches AI-Outlet).

Pitch-Qualität: <150 Wörter, klarer News-Hook, keine Buzzwords („revolutionär/disruptiv").

## Competitor-Citation-Methodik (DataForSEO, im Stack)

Zwei Wege zur datengetriebenen Drittplattform-Zielliste, kombinierbar:

**Direkt (bei DataForSEO-Zugang):** `dfs_llm_top_domains(keywords=Category-Queries)` → liefert die Domains, die LLMs für das Thema tatsächlich zitieren (`{domain, citations}`, max. 10 Keywords/Call), ohne Umweg über Backlink-Inferenz. Bei `subscription_required` auf den Backlink-Weg unten degradieren.

**Backlink-Inferenz (Fallback, immer verfügbar):**
1. Aus der KI-/SERP-Antwort der Category-Query die genannten Marken/Domains extrahieren.
2. `dfs_backlink_competitors` (eigene Domain) → wer ein ähnliches/stärkeres Profil hat = Citation-Konkurrenz.
3. `dfs_backlinks_list(target=Konkurrenz-Domain, mode="all")` → deren konkrete Referring-URLs = genau die Drittquellen, über die sie zitiert werden = deine Zielliste (granularer als `dfs_backlink_summary`'s Aggregat — für eine reine Zählung reicht Letzteres).
4. Lücke = Drittquellen, auf denen die Konkurrenz steht und die Marke fehlt. Honesty-Regel für eigene Vergleichsseiten: KI-Engines cross-referenzieren Feature-Claims und de-ranken Seiten, die lügen.

## AI-Referrer-Domainliste (Phase 6 — GA4)

`ga4_traffic_sources` (`days=90`) ziehen → **nach `sessionSource` aggregieren** (GA4 splittet eine Quelle über mehrere `sessionMedium`-Zeilen, z.B. `(not set)` UND `referral` — ein Medium-Filter verliert >50 %) und gegen diese Liste matchen:
- `chatgpt.com`, `chat.openai.com`
- `perplexity.ai`
- `gemini.google.com`, `bard.google.com`
- `copilot.microsoft.com`, `copilot.com`, `bing.com/chat`
- `claude.ai`
- `you.com`, `poe.com`

Tool-/Intern-Referrer aus dem Gesamt-Nenner rausrechnen: `tagassistant.google.com`, `ads.google.com`, `*.lightning.force.com`, `*.officeapps.live.com`, `(not set)`, `(data not available)`.

Persistieren (optional, damit der Traffic dauerhaft segmentierbar ist): Custom Dimension `ai_source` ist via `ga4_create_custom_dimension` anlegbar (Schreib-Aktion → erst Preview, dann Bestätigung, s. Schreib-Guardrails des Plugins); die GA4-Channel-Group „AI Referral" (UTM-Konvention) ist per Tool NICHT anlegbar — nur im GA4-UI, als Empfehlung ausgeben. In GA4 DebugView verifizieren. **Caveat:** GA4-Referrer ist Näherung, kein Fetch-Beweis (Crawler-Fetches erzeugen oft keine Session).
