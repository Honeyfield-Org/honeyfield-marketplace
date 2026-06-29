# Cross-Engine-Messung — Manual Capture + LLM-Mentions-Adapter

Phase 7. Cross-Engine-Citations (wird die Marke in ChatGPT/Claude/Gemini/Perplexity genannt/zitiert?) sind mit dem Standard-Stack **nicht** automatisiert messbar. Zwei Wege, beide ehrlich gekennzeichnet. Niemals aus einer Einzelabfrage einen „Score" ableiten — die Antworten variieren stark (Personalisierung, Session, Modellversion). Belastbar wird es nur über **wiederholtes Sampling / aggregierte Daten**.

## Weg A — Manuelle Capture (höchste Treue, skaliert nicht)

Der Mensch fährt die echten Prompts in der echten Web-App. Das ist die einzige echte Consumer-UI-Ground-Truth.

**Protokoll:**
1. 15–20 reale Käufer-Prompts definieren (branded + Category, z. B. „Wer ist [Marke]?", „beste [Kategorie] Tools in Österreich", „[Marke] vs [Konkurrent]").
2. Jeden Prompt über ChatGPT, Claude, Perplexity, Gemini laufen lassen — in **frischer/Incognito-Session** (Personalisierung minimieren).
3. Pro Antwort protokollieren: **genannt / zitiert (mit Link) / abwesend**, welche **Konkurrenz** stattdessen, **Ton** (positiv/neutral/negativ), zitierte **Quell-Domains**.
4. Monatlich wiederholen → Month-over-Month-Trend. Spreadsheet genügt.
5. Optional: Chrome-Extension „ChatGPT Search Capture" (RESONEO) / Console-Script exportiert `result_source`/`turn_use_case`/Citations als JSON → der Skill liest das JSON ein und wertet es strukturiert aus.

Die zitierten Quell-Domains aus Schritt 3 fließen direkt in Phase 5 (Off-site-Zielliste).

## Weg B — DataForSEO LLM-Mentions-Adapter (automatisiert, abo-pflichtig)

DataForSEOs **AI Optimization API** misst Marken-Sichtbarkeit über einen aggregierten Index von ~200 Mio KI-Antworten — löst das Varianz-Problem durch große Stichprobe und unterscheidet **Citation (URL verlinkt) vs. Mention (genannt ohne URL)**.

**Status / Aktivierung:** Eigenes Abo nötig — **nicht** Teil des Standard-DataForSEO-Zugangs. Mindest-Top-up **~$100/Monat**, der als Guthaben auf JEDER DataForSEO-API ausgebbar bleibt (kein reiner Access-Fee; ungenutzt bleibt es liegen). Pro Request ~$0,10 + ~$0,001/Zeile. Aktivierung: DataForSEO-Dashboard → Plans & Subscriptions. Ohne Aktivierung liefert der Endpoint `40204 Access denied`.

**Auth:** HTTP Basic (`curl -u "login:password"`). Im Honeyfield-Setup liegen die Creds in der MCP-Server-Konfiguration; die klassischen `dfs_*`-MCP-Tools wrappen die `ai_optimization/*`-Endpoints (Stand jetzt) noch **nicht** → entweder den MCP erweitern oder DataForSEO direkt aufrufen.

**Endpoints (LLM Mentions, POST JSON-Array):**
- `…/v3/ai_optimization/llm_mentions/search/live` — Mentions/Citations zu Keyword/Brand suchen.
- `…/v3/ai_optimization/llm_mentions/aggregated_metrics/live` — Share-of-Voice/Metriken.
- `…/v3/ai_optimization/llm_mentions/top_domains/live` — welche Domains für ein Thema zitiert werden.
- `…/v3/ai_optimization/llm_mentions/top_pages/live`.

Beispiel-Payload: `[{"keyword":"Honeyfield","limit":10}]`. Index-Lag 2–7 Tage. Engines: ChatGPT/Claude/Gemini/Perplexity.

**Wann aktivieren:** Wenn der laufende DataForSEO-Monatsverbrauch über alle Workspaces ohnehin Richtung $100 geht (dann ist der Top-up großteils vorgezogener Spend), oder für ein Flagship-Mandat, das echtes Cross-Engine-Tracking braucht. Für Einmal-Audits reicht meist Weg A.

## Adapter-Prinzip

Die Sammlung ist austauschbar: Phase 1–6 brauchen keinen der beiden Wege. Phase 7 läuft per Default mit Weg A (manuell) und schaltet auf Weg B um, sobald das Abo aktiv ist. Jeder Cross-Engine-Befund trägt den Stempel: **welcher Weg + welche Konfidenz**.
