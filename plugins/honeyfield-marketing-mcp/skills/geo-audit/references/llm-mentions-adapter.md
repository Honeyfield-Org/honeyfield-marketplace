# Cross-Engine-Messung — LLM-Mentions-Adapter (Weg B, Default) + Manuelle Capture (Weg A, Fallback)

Phase 7. Cross-Engine-Citations (wird die Marke in ChatGPT/Claude/Gemini/Perplexity genannt/zitiert?) laufen per Default über die DataForSEO-LLM-Mentions-Tools (Weg B, pay-as-you-go über das normale DataForSEO-Guthaben). Schlägt der Zugriff fehl (`subscription_required`, z. B. Guthaben aufgebraucht), auf manuelle Capture (Weg A) degradieren. Niemals aus einer Einzelabfrage einen „Score” ableiten — die Antworten variieren stark (Personalisierung, Session, Modellversion). Belastbar wird es nur über **wiederholtes Sampling / aggregierte Daten**. Jeder Befund trägt den Stempel: **welcher Weg + welche Konfidenz**.

## Weg B — LLM-Mentions-Adapter (Default, automatisiert)

DataForSEOs **AI Optimization API** misst Marken-Sichtbarkeit über einen aggregierten Index von ~200 Mio KI-Antworten — löst das Varianz-Problem durch große Stichprobe und unterscheidet **Citation (URL verlinkt) vs. Mention (genannt ohne URL)**. Vier Tools, alle read-only. `dfs_llm_mentions`/`_mentions_metrics`/`_top_domains` nehmen `keywords` entgegen — hartes API-Limit **max. 10 Keywords pro Call**:

- **`dfs_llm_mentions(keywords, limit=20)`** — Mentions/Citations zu Keyword/Brand, pro Zeile `{prompt/topic, model/engine, type, url, domain, snippet}`. `type: "citation"` = URL verlinkt (zählt direkt für Off-site-Citability, Phase 5); `type: "mention"` = genannt ohne Link.
- **`dfs_llm_mentions_metrics(keywords)`** — `{mentions_total, mentions_by_engine, citations_total, share_of_voice_by_engine, top_source_domains: [{domain, mentions}]}`: Citations nur als Gesamtsumme (nicht per Engine), Share-of-Voice pro Engine client-seitig aus den Per-Engine-Mentions berechnet. `top_source_domains` liefert zusätzlich meistgenannte Quell-Domains — ergänzt `dfs_llm_top_domains` für die Off-site-Zielliste (Phase 5).
- **`dfs_llm_top_domains(keywords, limit=20)`** — meistzitierte Domains zum Thema, `{domain, citations}` (kein separates `mentions`-Feld — die Domain-Aggregation ist bereits die Citation-Menge) — speist direkt die Off-site-Zielliste (Phase 5, s. `references/dach-citability.md`).
- **`dfs_llm_responses(prompt, model)`** — rohe LLM-Antwort + Zitate für einen einzelnen Prompt (`model` ∈ chatgpt/claude/gemini/perplexity): `{model, prompt, answer_text, citations: [{url, domain, title?}]}`. Ist eine Einzel-Stichprobe wie eine Capture — nie allein als Befund verkaufen, gegen `dfs_llm_mentions_metrics` gegenprüfen.

**Status / Kosten:** Kein separates Abo mehr nötig — DataForSEO hat die eigene AI-Optimization-Subscription aufgehoben, die API ist pay-as-you-go über das normale DataForSEO-Guthaben (kein Mindest-Top-up, keine Dashboard-Aktivierung). Kosten unverändert: ~$0,10/Request + ~$0,001/Zeile.

**Schlägt der Zugriff fehl** (`{"error": "subscription_required", "status_code": 40204, "hint": "DataForSEO verweigert Zugriff auf die AI-Optimization-API (40204) — Guthaben/Zugang im DataForSEO-Dashboard prüfen; Fallback: manuelles Capture-Protokoll (Weg A)"}`) — der Error-Key bleibt aus Kompatibilitätsgründen `subscription_required`, bedeutet aber jetzt ein Zugriffsproblem (z. B. Guthaben aufgebraucht), nicht mehr eine fehlende Subscription —, sofort auf Weg A umschalten und den Befund entsprechend kennzeichnen (Konfidenz: Weg A statt Weg B).

**Index-Lag:** Index ist nicht tagesaktuell; die genaue Lag-Dauer ist nicht über die DataForSEO-Docs API-verifiziert — bei frisch veröffentlichtem Content und Stichtag-nahen Vergleichen entsprechend vorsichtig einordnen.

**Kosten-Disziplin:** Weg B ist Default — kein Aktivierungsschritt mehr nötig, läuft automatisch über jeden DataForSEO-Zugang. Bei größeren Keyword-Sets/häufigen Wiederholungen die Call-Kosten (~$0,10/Request) im Blick behalten. Weg A bleibt nur noch Fallback bei `subscription_required` oder ganz ohne DataForSEO-Zugang.

## Weg A — Manuelle Capture (Fallback bei `subscription_required` / ohne DataForSEO-Zugang, höchste Treue pro Sample)

Der Mensch fährt die echten Prompts in der echten Web-App. Das ist die einzige echte Consumer-UI-Ground-Truth — nutzen, wenn Weg B `subscription_required` liefert oder kein DataForSEO-Zugang besteht.

**Protokoll:**
1. 15–20 reale Käufer-Prompts definieren (branded + Category, z. B. „Wer ist [Marke]?”, „beste [Kategorie] Tools in Österreich”, „[Marke] vs [Konkurrent]”).
2. Jeden Prompt über ChatGPT, Claude, Perplexity, Gemini laufen lassen — in **frischer/Incognito-Session** (Personalisierung minimieren).
3. Pro Antwort protokollieren: **genannt / zitiert (mit Link) / abwesend**, welche **Konkurrenz** stattdessen, **Ton** (positiv/neutral/negativ), zitierte **Quell-Domains**.
4. Monatlich wiederholen → Month-over-Month-Trend. Spreadsheet genügt.
5. Optional: Chrome-Extension „ChatGPT Search Capture” (RESONEO) / Console-Script exportiert `result_source`/`turn_use_case`/Citations als JSON → der Skill liest das JSON ein und wertet es strukturiert aus.

Die zitierten Quell-Domains aus Schritt 3 fließen direkt in Phase 5 (Off-site-Zielliste) — dieselbe Rolle wie `dfs_llm_top_domains` bei Weg B.

## Adapter-Prinzip

Die Sammlung ist austauschbar: Phase 1–6 brauchen keinen der beiden Wege. Phase 7 läuft per Default über Weg B und degradiert automatisch auf Weg A bei `subscription_required` (z. B. Guthaben aufgebraucht). Jeder Cross-Engine-Befund trägt den Stempel: **welcher Weg + welche Konfidenz**.
