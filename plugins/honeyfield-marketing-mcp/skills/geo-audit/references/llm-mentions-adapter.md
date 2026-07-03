# Cross-Engine-Messung — LLM-Mentions-Adapter (Weg B, Default) + Manuelle Capture (Weg A, Fallback)

Phase 7. Cross-Engine-Citations (wird die Marke in ChatGPT/Claude/Gemini/Perplexity genannt/zitiert?) laufen per Default über die DataForSEO-LLM-Mentions-Tools (Weg B). Ohne aktives Abo (`subscription_required`) auf manuelle Capture (Weg A) degradieren. Niemals aus einer Einzelabfrage einen „Score" ableiten — die Antworten variieren stark (Personalisierung, Session, Modellversion). Belastbar wird es nur über **wiederholtes Sampling / aggregierte Daten**. Jeder Befund trägt den Stempel: **welcher Weg + welche Konfidenz**.

## Weg B — LLM-Mentions-Adapter (Default, automatisiert)

DataForSEOs **AI Optimization API** misst Marken-Sichtbarkeit über einen aggregierten Index von ~200 Mio KI-Antworten — löst das Varianz-Problem durch große Stichprobe und unterscheidet **Citation (URL verlinkt) vs. Mention (genannt ohne URL)**. Vier Tools, alle read-only:

- **`dfs_llm_mentions(keywords, limit=20)`** — Mentions/Citations zu Keyword/Brand, pro Zeile `{prompt/topic, model/engine, type, url, domain, snippet}`. `type: "citation"` = URL verlinkt (zählt direkt für Off-site-Citability, Phase 5); `type: "mention"` = genannt ohne Link.
- **`dfs_llm_mentions_metrics(keywords)`** — aggregierte Mentions-/Citation-Zählwerte + Share-of-Voice pro Engine.
- **`dfs_llm_top_domains(keywords, limit=20)`** — meistzitierte Domains zum Thema, `{domain, citations, mentions}` — speist direkt die Off-site-Zielliste (Phase 5, s. `references/dach-citability.md`).
- **`dfs_llm_responses(prompt, model)`** — rohe LLM-Antwort + Zitate für einen einzelnen Prompt (`model` ∈ chatgpt/claude/gemini/perplexity): `{model, prompt, answer_text, citations: [{url, domain, title?}]}`. Ist eine Einzel-Stichprobe wie eine Capture — nie allein als Befund verkaufen, gegen `dfs_llm_mentions_metrics` gegenprüfen.

**Status / Aktivierung:** Eigenes Abo nötig — **nicht** Teil des Standard-DataForSEO-Zugangs. Mindest-Top-up **~$100/Monat**, der als Guthaben auf JEDER DataForSEO-API ausgebbar bleibt (kein reiner Access-Fee; ungenutzt bleibt es liegen). Pro Request ~$0,10 + ~$0,001/Zeile. Aktivierung: DataForSEO-Dashboard → Plans & Subscriptions.

**Ohne aktives Abo** liefern alle vier Tools ein strukturiertes Degradations-Signal (`{"error": "subscription_required", "status_code": 40204, ...}`) statt eines harten API-Fehlers — sofort auf Weg A umschalten und den Befund entsprechend kennzeichnen (Konfidenz: Weg A statt Weg B).

**Index-Lag:** 2–7 Tage — Befunde sind nie tagesaktuell; bei frisch veröffentlichtem Content entsprechend einordnen.

**Wann aktivieren:** Wenn der laufende DataForSEO-Monatsverbrauch über alle Workspaces ohnehin Richtung $100 geht (dann ist der Top-up großteils vorgezogener Spend), oder für ein Flagship-Mandat, das echtes Cross-Engine-Tracking braucht. Für Einmal-Audits ohne aktives Abo reicht Weg A.

## Weg A — Manuelle Capture (Degradationspfad ohne Abo, höchste Treue pro Sample)

Der Mensch fährt die echten Prompts in der echten Web-App. Das ist die einzige echte Consumer-UI-Ground-Truth — nutzen, wenn Weg B `subscription_required` liefert oder kein DataForSEO-Zugang besteht.

**Protokoll:**
1. 15–20 reale Käufer-Prompts definieren (branded + Category, z. B. „Wer ist [Marke]?", „beste [Kategorie] Tools in Österreich", „[Marke] vs [Konkurrent]").
2. Jeden Prompt über ChatGPT, Claude, Perplexity, Gemini laufen lassen — in **frischer/Incognito-Session** (Personalisierung minimieren).
3. Pro Antwort protokollieren: **genannt / zitiert (mit Link) / abwesend**, welche **Konkurrenz** stattdessen, **Ton** (positiv/neutral/negativ), zitierte **Quell-Domains**.
4. Monatlich wiederholen → Month-over-Month-Trend. Spreadsheet genügt.
5. Optional: Chrome-Extension „ChatGPT Search Capture" (RESONEO) / Console-Script exportiert `result_source`/`turn_use_case`/Citations als JSON → der Skill liest das JSON ein und wertet es strukturiert aus.

Die zitierten Quell-Domains aus Schritt 3 fließen direkt in Phase 5 (Off-site-Zielliste) — dieselbe Rolle wie `dfs_llm_top_domains` bei Weg B.

## Adapter-Prinzip

Die Sammlung ist austauschbar: Phase 1–6 brauchen keinen der beiden Wege. Phase 7 läuft per Default über Weg B (sobald das Abo aktiv ist) und degradiert automatisch auf Weg A bei `subscription_required`. Jeder Cross-Engine-Befund trägt den Stempel: **welcher Weg + welche Konfidenz**.
