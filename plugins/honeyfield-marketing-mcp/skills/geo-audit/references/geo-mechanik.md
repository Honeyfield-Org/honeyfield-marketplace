# GEO-Mechanik — wie KI-Engines Quellen wählen

Grundlage für die Audit-Phasen. Kurzfassung steht im SKILL.md; hier die Details + Belege.

## fetched ≠ cited ≠ mentioned

Aus dem Reverse-Engineering von ChatGPTs Netzwerk-Traffic (Suganthan Mohanadasan, 2026) + Ahrefs-Studie über 1,4 Mio Prompts:
- **Fetched:** Seite wird in den Kontext gezogen, für den Nutzer unsichtbar.
- **Cited:** Quelle per Fußnote an einen *konkreten Satz* gebunden.
- **Mentioned:** Markenname steht in der Antwort, ist aber nicht Quelle des Claims.

Konsequenzen für den Audit:
- **Citations binden an Sätze, nicht an die ganze Antwort** → es zählt, ob eine *Passage* eine präzise Aussage stützt (siehe Extractability).
- **Domain-Dedup:** 20 dünne Seiten kollabieren zu 1 → eine starke Seite pro Claim schlägt viele dünne.
- **Selbst-Citation ist unmöglich:** das Modell zitiert für Aussagen über eine Marke Drittquellen. Marken werden ~**6,5× häufiger über Drittquellen** zitiert als über die eigene Domain. → Phase 5 ist das Herzstück.
- **Reddit-Muster:** massiv gefetcht (278×), kaum zitiert (11×); Ahrefs: Reddit-Citation-Rate 1,93 %, YouTube 0,51 %. Fetched ≠ Einfluss-Credit.

## Index-Backend pro Engine (zentrale Lücke vieler Audits)

„In AI sichtbar werden” ist pro Engine eine andere Crawl-/Index-Baustelle:

| Engine | Such-Backend | Konsequenz |
|---|---|---|
| ChatGPT, Copilot | **Bing** | Bing Webmaster Tools + **IndexNow** nutzen — viele DACH-Sites reichen nur bei der GSC ein und fehlen in Bing |
| Claude | **Brave Search** | Sichtbarkeit auf `search.brave.com` prüfen — nicht Google/Bing |
| Perplexity | eigener Crawler + Google | Standard-SEO + eigener Index |
| Google AI Overviews | Google-Index | klassisches SEO trägt direkt |

Prüf-Schritt: Steht die Site in **Bing**? `dfs_serp_bing_organic(keyword="site:domain.at")` ist der saubere, deterministische Check (kein Captcha-Risiko). Ohne DataForSEO-Zugang: `curl "https://www.bing.com/search?q=site:domain.at"` ist meist Captcha-geblockt → scriptbarer Fallback `curl "https://html.duckduckgo.com/html/?q=site:domain.at"` (Bing-backed) oder manueller Bing-Check. Wenn nur GSC eingereicht wurde → High-Impact-Fix für ChatGPT/Copilot-Sichtbarkeit.

## KI-Bot-Liste + robots.txt-Nuancen

Relevante User-Agents: `GPTBot`, `ChatGPT-User`, `OAI-SearchBot`, `OAI-AdsBot` (OpenAI), `ClaudeBot`, `Claude-SearchBot`, `Claude-User`, `Claude-Agent`, `anthropic-ai` (Anthropic), `PerplexityBot`, `Perplexity-User`, `Google-Extended` (Gemini-Training-Opt-out), `Bingbot`. Belege: https://developers.openai.com/docs/gptbot · https://support.claude.com/en/articles/8896518 · https://docs.perplexity.ai/docs/resources/perplexity-crawlers

**Abdeckung `site_crawler_check`** (16 Bots): Googlebot, Bingbot, Applebot · OAI-SearchBot, PerplexityBot, Claude-SearchBot · ChatGPT-User, Claude-User, Perplexity-User · GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot, Bytespider, Meta-ExternalAgent. **Nicht abgedeckt:** `OAI-AdsBot`, `Claude-Agent`, `anthropic-ai`, AIPREF → manuell prüfen (robots.txt lesen, z. B. `curl <domain>/robots.txt` bzw. WebFetch).

- **GPTBot** = Training UND Search zugleich, nicht trennbar → Blocken kostet Citations.
- **OAI-SearchBot / ChatGPT-User** = Live-/Search-Fetch → niemals blocken, wenn man zitiert werden will.
- **`OAI-AdsBot`** = Ad-Review für OpenAI-Anzeigen → relevant, wenn der Kunde `openai_ads_*` nutzt; nicht blocken.
- **`Claude-Agent`** = von Anthropic gehosteter Browser (Agent im Nutzerauftrag); **`Claude-SearchBot`** = Anthropics Such-Crawler → für Citations in Claude offen lassen.
- **`Perplexity-User`** = Abruf im Nutzerauftrag; ignoriert robots.txt laut Perplexity meist („generally ignores robots.txt rules”) → eine robots.txt-Sperre nur dafür ist keine wirksame Sperre.
- **CCBot** (Common Crawl) = nur Training, **keine** Citations → kann gefahrlos geblockt werden (die einzige sichere „Content-Diebstahl”-Antwort).
- **Google-Extended** blockt nur Gemini-Training, nicht die Google-Suche/AIO.
- **AIO/AI-Mode-Opt-out = Snippet-Steuerung:** `nosnippet`, `max-snippet`, `data-nosnippet` und `noindex` sind laut Google die Controls für die Nutzung in AI Overviews/AI Mode (https://developers.google.com/search/docs/appearance/ai-features). Ungewollt gesetzt → kritischer Blocker; `site_crawler_check` liefert Meta-Robots (`robots`/`googlebot`) und X-Robots-Tag nur der Startseite, `data-nosnippet` steht nur im Roh-HTML.
- **AIPREF (ab Anfang 2027):** Google will das AIPREF-Signal `user-agent: __usage_ai-training` als Trainings-Opt-out unterstützen (https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers). `site_crawler_check` wertet es nicht aus (nur Content Signals) → bei Bedarf robots.txt manuell lesen.

Bot-Status-Test: `site_crawler_check` mit `check_live=true` (Startseite, beide Plattformen). In Claude Code für weitere URLs je Bot-UA abrufen, z. B.
`curl -sIL -A "OAI-SearchBot/1.0 (+https://openai.com/searchbot)" <url>` → 200 (gut) vs. 403/Cloudflare-Block vs. Soft-404 (Status 200 auf leerer Seite). UA ist spoofbar, und Cloudflare & Co. verifizieren echte Bots über IP-Bereiche: ein 403 auf unseren Testabruf beweist keine Sperre des echten Bots (nur Indiz, robots.txt ist verlässlich); für die Auswertung fremder Server-Logs müsste man die Source-IP gegen die publizierten Ranges der Anbieter prüfen. Anthropic veröffentlicht seine IPs unter `claude.com/crawling/bots.json` und empfiehlt trotzdem robots.txt statt IP-Blocking (https://support.claude.com/en/articles/8896518); Perplexity veröffentlicht IP-JSONs je Bot.

## Princeton-GEO-Hebel (Fix-Priorisierung)

Quantifizierter Sichtbarkeits-Boost (Princeton/„GEO”, KDD 2024) — als Sortierlogik der Fix-Liste:

| Methode | Boost |
|---|---|
| Quellen zitieren | +40 % |
| Statistiken einbauen | +37 % |
| Experten-Zitate | +30 % |
| Autoritativer Ton | +25 % |
| Klarheit / Lesbarkeit | +20 % |
| Fachbegriffe / Vokabular | +15–18 % |
| **Keyword-Stuffing** | **−10 % (schadet aktiv)** |

Beste Kombi: **Fluency + Statistics**. Niedrig rankende Sites profitieren überproportional (Methode „Cite Sources”: +115 % für Rang 5, −30 % für Rang 1).

*Fußnote:* Benchmark-Werte aus dem Paper (https://arxiv.org/html/2311.09735v3), keine Garantie im Einzelfall. Auf Perplexity fiel der Effekt kleiner aus (Quotation Addition ca. +22 %). → Bei der Fix-Empfehlung „Statistik mit Quelle ergänzen” über „Ton verbessern” stellen.

## Content-Answer-Fit & Freshness

- **Content-Answer-Fit:** Wie gut Stil/Struktur dem Antwortformat der Engine gleicht, korreliert laut ZipTie (~400k Seiten) stark mit Citation-Wahrscheinlichkeit — deutlich stärker als Domain-Authority. Heuristik: „Schreib so, wie die KI die Frage beantworten würde.”
- **Freshness:** Content mit sichtbarem Update <30 Tage wird bei ChatGPT ~3,2× häufiger zitiert. Sichtbares „Zuletzt aktualisiert”-Datum, Quartals-Refresh kompetitiver Seiten. **Leitplanke:** Das Datum nur bei substanzieller inhaltlicher Änderung ändern. Datum hochsetzen ohne Änderung ist laut Google kein Qualitätssignal und kann schaden (https://developers.google.com/search/docs/fundamentals/creating-helpful-content).

## Extractability-Detailcheck (Phase 3)

Pass/Fail pro Schlüsselseite — kann eine Passage als Antwort herausgelöst werden?
- [ ] Definition / direkte Antwort im **ersten Absatz** (answer-first, nicht vergraben).
- [ ] **Self-contained Antwortblöcke**, 40–60 Wörter, ohne Kontext verständlich.
- [ ] Statistiken **mit Quelle**.
- [ ] **Tabellen** für „X vs Y”-Vergleiche (statt Prosa).
- [ ] FAQ in natürlicher Frage-Sprache (als Claim-Struktur, nicht für Rich Results).
- [ ] Heading-Struktur matcht typische Query-Muster.
- [ ] Autoren-Attribution mit Credentials (E-E-A-T-Proxy).

## Mythen & Anti-Patterns (nicht als Befund/Fix verkaufen)

- **FAQ-/HowTo-Schema für Rich Results** → tot (FAQ ab 08/2023 nur noch Behörden/Health, seit 07.05.2026 für alle Sites abgeschaltet; HowTo 09/2023 entfernt; der Typ `FAQPage` bleibt gültig). Für GEO behält strukturiertes Q&A Rest-Wert als **maschinenlesbare Claim-Struktur** (LLMs extrahieren Frage→Antwort leichter) — so framen, nicht als Snippet-Taktik.
- **Separater „AI-Content”** → fällt unter „scaled content abuse” (Spam-Policy).
- **Content-Chunking** → Google explizit: „Don't break your content into tiny pieces for AI.”
- **Mass-Generation / dünne programmatische Seiten** → ignoriert.
- **Gefakte/gespammte Mentions** → Cross-Reference, De-Ranking.
- **AI-Bots pauschal blocken** → schneidet Citations ab (Ausnahme CCBot).
- **JS-only Rendering** → unsichtbar für nicht-rendernde Crawler.
- **Keyword-Stuffing** → −10 %.

**Google-vs-Multi-Platform-Dualität:** Google sagt offiziell, es brauche keine Spezial-Files/kein AI-Markup. Inhaltliche Struktur (answer-first, Tabellen, Q&A) erleichtert allen Engines die Extraktion. Die Wirkung von **Schema/strukturierten Daten** auf KI-Zitate ist dagegen **unbelegt** — nicht „Mythos”, nicht „der Hebel”: Ahrefs findet keine klare Richtung (30-Tage-Fenster, gepoolte Schema-Typen, Störfaktoren; https://ahrefs.com/blog/schema-ai-citations/). Schema bleibt sinnvoll für Rich Results und Klarheit über die Entität. Sicherer Default, der beide Lager bedient: **„write for people, organize for clarity.”** Strukturelle Hacks nicht überversprechen.

## llms.txt / OKF — nüchterne Einordnung

`llms.txt` bringt keine Sichtbarkeit in der Suche oder AI-Search (kein Such-/Antwort-System nutzt es nachweislich). Ausnahme: Dev-Docs für Coding-Agents (die rufen sie tatsächlich ab). Für SEO/GEO nicht empfehlen; bei SaaS mit Entwickler-Doku optional. Beleg: https://ahrefs.com/blog/llmstxt-study/

## Google AI Overview via DataForSEO

`dfs_serp_google_organic` liefert den `ai_overview`-Block jetzt direkt mit: `{present: bool, sources: [{title, url, domain}]}`. Intern läuft der Call mit `load_async_ai_overview: true` — ohne dieses Flag fehlen asynchron nachgeladene Overviews (false „nicht präsent”); das Tool setzt es bereits, kein separater Folge-Call durch den Skill nötig. `present: false` heißt: keine AI Overview für diese Query in diesem Markt/Moment — vor dem Befund Query-Formulierung und Markt (`location`/`language`) gegenprüfen, nicht vorschnell als „Site fehlt” werten. ~$0,0035/Call (advanced-Endpoint), keine Zusatz-Subscription nötig.
