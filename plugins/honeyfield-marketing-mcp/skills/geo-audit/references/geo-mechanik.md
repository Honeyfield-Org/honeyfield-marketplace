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

„In AI sichtbar werden" ist pro Engine eine andere Crawl-/Index-Baustelle:

| Engine | Such-Backend | Konsequenz |
|---|---|---|
| ChatGPT, Copilot | **Bing** | Bing Webmaster Tools + **IndexNow** nutzen — viele DACH-Sites reichen nur bei der GSC ein und fehlen in Bing |
| Claude | **Brave Search** | Sichtbarkeit auf `search.brave.com` prüfen — nicht Google/Bing |
| Perplexity | eigener Crawler + Google | Standard-SEO + eigener Index |
| Google AI Overviews | Google-Index | klassisches SEO trägt direkt |

Prüf-Schritt: Steht die Site in **Bing**? `curl "https://www.bing.com/search?q=site:domain.at"` ist meist Captcha-geblockt → scriptbarer Fallback `curl "https://html.duckduckgo.com/html/?q=site:domain.at"` (Bing-backed); Bing-direkt als manueller Check. Wenn nur GSC eingereicht wurde → High-Impact-Fix für ChatGPT/Copilot-Sichtbarkeit.

## KI-Bot-Liste + robots.txt-Nuancen

Relevante User-Agents: `GPTBot`, `ChatGPT-User`, `OAI-SearchBot` (OpenAI), `ClaudeBot`, `anthropic-ai`, `Claude-User` (Anthropic), `PerplexityBot`, `Perplexity-User`, `Google-Extended` (Gemini-Training-Opt-out), `Bingbot`.

- **GPTBot** = Training UND Search zugleich, nicht trennbar → Blocken kostet Citations.
- **OAI-SearchBot / ChatGPT-User** = Live-/Search-Fetch → niemals blocken, wenn man zitiert werden will.
- **CCBot** (Common Crawl) = nur Training, **keine** Citations → kann gefahrlos geblockt werden (die einzige sichere „Content-Diebstahl"-Antwort).
- **Google-Extended** blockt nur Gemini-Training, nicht die Google-Suche/AIO.

Bot-Status-Test: Schlüssel-URL je Bot-UA abrufen, z. B.
`curl -sIL -A "OAI-SearchBot/1.0 (+https://openai.com/searchbot)" <url>` → 200 (gut) vs. 403/Cloudflare-Block vs. Soft-404 (Status 200 auf leerer Seite). UA ist spoofbar — für die *Diagnose der eigenen Site* irrelevant; für die Auswertung fremder Server-Logs müsste man die Source-IP gegen die publizierten Ranges der Anbieter prüfen.

## Princeton-GEO-Hebel (Fix-Priorisierung)

Quantifizierter Sichtbarkeits-Boost (Princeton/„GEO", KDD 2024) — als Sortierlogik der Fix-Liste:

| Methode | Boost |
|---|---|
| Quellen zitieren | +40 % |
| Statistiken einbauen | +37 % |
| Experten-Zitate | +30 % |
| Autoritativer Ton | +25 % |
| Klarheit / Lesbarkeit | +20 % |
| Fachbegriffe / Vokabular | +15–18 % |
| **Keyword-Stuffing** | **−10 % (schadet aktiv)** |

Beste Kombi: **Fluency + Statistics**. Niedrig rankende Sites profitieren überproportional (bis +115 % mit Citations). → Bei der Fix-Empfehlung „Statistik mit Quelle ergänzen" über „Ton verbessern" stellen.

## Content-Answer-Fit & Freshness

- **Content-Answer-Fit:** Wie gut Stil/Struktur dem Antwortformat der Engine gleicht, korreliert laut ZipTie (~400k Seiten) stark mit Citation-Wahrscheinlichkeit — deutlich stärker als Domain-Authority. Heuristik: „Schreib so, wie die KI die Frage beantworten würde."
- **Freshness:** Content mit sichtbarem Update <30 Tage wird bei ChatGPT ~3,2× häufiger zitiert. Sichtbares „Zuletzt aktualisiert"-Datum, Quartals-Refresh kompetitiver Seiten.

## Extractability-Detailcheck (Phase 3)

Pass/Fail pro Schlüsselseite — kann eine Passage als Antwort herausgelöst werden?
- [ ] Definition / direkte Antwort im **ersten Absatz** (answer-first, nicht vergraben).
- [ ] **Self-contained Antwortblöcke**, 40–60 Wörter, ohne Kontext verständlich.
- [ ] Statistiken **mit Quelle**.
- [ ] **Tabellen** für „X vs Y"-Vergleiche (statt Prosa).
- [ ] FAQ in natürlicher Frage-Sprache (als Claim-Struktur, nicht für Rich Results).
- [ ] Heading-Struktur matcht typische Query-Muster.
- [ ] Autoren-Attribution mit Credentials (E-E-A-T-Proxy).

## Mythen & Anti-Patterns (nicht als Befund/Fix verkaufen)

- **FAQ-/HowTo-Schema für Rich Results** → tot (FAQ ~Aug 2023 nur noch Behörden/Health, HowTo ~Sep 2023 entfernt). Für GEO behält strukturiertes Q&A Rest-Wert als **maschinenlesbare Claim-Struktur** (LLMs extrahieren Frage→Antwort leichter) — so framen, nicht als Snippet-Taktik.
- **Separater „AI-Content"** → fällt unter „scaled content abuse" (Spam-Policy).
- **Content-Chunking** → Google explizit: „Don't break your content into tiny pieces for AI."
- **Mass-Generation / dünne programmatische Seiten** → ignoriert.
- **Gefakte/gespammte Mentions** → Cross-Reference, De-Ranking.
- **AI-Bots pauschal blocken** → schneidet Citations ab (Ausnahme CCBot).
- **JS-only Rendering** → unsichtbar für nicht-rendernde Crawler.
- **Keyword-Stuffing** → −10 %.

**Google-vs-Multi-Platform-Dualität:** Google sagt offiziell, es brauche keine Spezial-Files/kein AI-Markup. Non-Google-Engines belohnen Struktur aber sehr wohl. Sicherer Default, der beide Lager bedient: **„write for people, organize for clarity."** Strukturelle Hacks nicht überversprechen.

## llms.txt / OKF — nüchterne Einordnung

Aktuell crawlt kein Engine `llms.txt` aktiv für Citations. Höchstens als „Signpost"-Wette (vergleichbar mit früher Schema.org-Adoption), nicht als Hebel. **Skip**, wenn: <10 Seiten, Closed-Platform (Wix/Squarespace-Lock-in), keine laufende Schema-/Content-Pflege. Nicht als Pflicht-Fix empfehlen.

## Google AI Overview via DataForSEO

**Wichtig (im Live-Test verifiziert):** Der MCP-Wrapper `dfs_serp_google_organic` liefert NUR organische Treffer — **keinen `ai_overview`-Block** (kein `type`-Feld, kein `asynchronous_ai_overview`). AI-Overview-Prüfung erfordert die **Raw-DataForSEO-API direkt**:
`POST https://api.dataforseo.com/v3/serp/google/organic/live/advanced` mit `[{"keyword":"…","location_name":"Austria","language_name":"German"}]`. Im `items`-Array nach `type:"ai_overview"` suchen; Feld `asynchronous_ai_overview:true` → zitierte Quellen erst über einen Async-Folgecall. ~$0,0035/Call, kein AI-Optimization-Abo nötig. Solange der MCP-Wrapper das nicht exponiert: AI-Overview als Lücke benennen oder den Raw-Call nutzen.
