# Google-Ads-Benchmarks & Deutungs-Regeln

Schwellwerte und Interpretationshilfen für den Audit. **Wichtigster Grundsatz: keine erfundenen CTR-/CPC-/Conversion-Rate-„Benchmarks”.** Diese variieren extrem nach Branche, Markt, Marke vs. Non-Brand und Saison. Beurteile gegen den **eigenen Trend des Kontos** und gegen **Impression Share**, nicht gegen ausgedachte Industriewerte. Wenn ein Industriewert genannt wird, als grobe Orientierung kennzeichnen, nie als Soll.

## Conversion-Tracking-Mechanik (Phase 1)

### Primär vs. sekundär
Seit 2021 zählt die **„Conversions”-Spalte nur primäre Conversion-Actions**. Sekundäre Actions sind rein beobachtend („alle Conv.”-Spalte) und beeinflussen Smart Bidding **nicht**.
- Falsch als sekundär eingestuft → die Action steuert das Bidding nicht, obwohl sie soll.
- Falsch als primär (z. B. „Newsletter” als primär neben „Kauf”) → CPA/ROAS verwässert, Smart Bidding optimiert aufs falsche Ziel.

### Zählung „Jede” vs. „Eine”
- **„Eine” (One):** max. eine Conversion pro Klick → richtig für **Lead-Gen** (ein Lead pro Anfrage zählt, nicht 3 abgeschickte Formulare).
- **„Jede” (Every):** jede Conversion zählt → richtig für **E-Commerce** (3 Käufe = 3 Conversions).
- Vertauscht → Lead-Konten überzählen, E-Commerce unterzählt.

### Attributionsmodell & -fenster
- Datengetrieben (DDA) ist heute Default; Last-Click ist alt. Modellwechsel verschiebt Conversion-Zuordnung über Kampagnen — bei Vergleichen über die Zeit beachten.
- **Conversion-Fenster** (z. B. 30/90 Tage): längeres Fenster → mehr Conversions, aber späteres „Eintreffen”.

### GA4-Cross-Check
GA4-Key-Events und Ads-Conversions weichen normal ab: andere Attribution, Zeitzone, Bot-Filter; seit 06/2023 ist bei neuer Verknüpfung „Google Paid Channels” der Attributions-Default in GA4; Cross-Device-Conversions sieht GA4 nur mit Google Signals (Beleg: https://support.google.com/analytics/answer/10632359). **Faktor 2+** oder „Ads zählt, GA4 zählt fast nichts” (oder umgekehrt) = echtes Tracking-Problem:
- Doppelzählung (native Tags **und** GA4-Import beide aktiv).
- Auto-Tagging/GCLID aus → Import-Brücke kaputt.
- Conversion-Tag feuert mehrfach / auf falscher Seite.

### Consent-Mode-Modellierung (Tracking-Vorbehalt)
- Auch **Basic** modelliert: Google modelliert Conversions ohne Pings mit einem allgemeinen Modell.
- **Advanced** nutzt Pings vor der Einwilligung für ein eigenes Modell, braucht aber eine Mindest-Datenmenge („data collection threshold”). Kleine DACH-Konten mit niedriger Einwilligungsrate erreichen sie oft nicht.
- Folge: Conversions systematisch untererfasst → Tracking-Vorbehalt, kein Performance-Befund. Tiefe Prüfung (Consent-Setup, Rechtsfrage) via `tracking-check` — Advanced sendet Pings ohne Einwilligung, § 25 TDDDG ist relevant.
- Beleg: https://developers.google.com/tag-platform/security/concepts/consent-mode

## Attributions-Lag (Beurteilungsfenster)
Frische Conversions tröpfeln nach. Beurteile CPA/ROAS auf einem **abgeschlossenen** Fenster (z. B. Tag −37 bis −7), die jüngsten ~7 Tage separat als „läuft noch nach”. Längeres Conversion-Fenster (B2B, hohe Preise) → längeren Puffer wählen.

## Smart-Bidding-Conversion-Schwellen (Google-Werte)
Smart Bidding braucht Datenvolumen, um stabil zu lernen. Google nennt eigene Werte:
- **Bewertungszeitraum:** Performance nur in Zeiträumen mit mind. **30 Conversions** bewerten (tCPA / Maximize Conversions), mind. **50** bei tROAS. Volumen je Kampagne via `ads_conversion_performance` prüfen; reicht der Monat nicht, längeres Fenster wählen.
- **Vor Value-Based Bidding** (tROAS / Maximize Conversion Value): Conversion-Werte seit „4 Wochen oder 3 Conversion-Zyklen (der längere Zeitraum)” erfassen. Werte erst seit Kurzem im Konto → noch kein tROAS.
- Darunter: Smart Bidding rät eher → Optionen: Conversions zusammenlegen (Portfolio-Strategie über Kampagnen), eine höhere Conversion-Action in der Funnel-Stufe wählen (z. B. „Warenkorb” statt „Kauf”, wenn Käufe zu selten), oder einfacher steuern (Maximize Clicks / Manual mit Beobachtung), bis Volumen da ist.
- Belege: https://support.google.com/google-ads/answer/7065882 · https://support.google.com/google-ads/answer/6268633

### Lernphase
- Status „Learning” lösen **nur** aus: neue oder reaktivierte Gebotsstrategie, Einstellungsänderung der Strategie, Änderung der Zusammensetzung (Kampagnen/Ad Groups/Keywords hinzufügen oder entfernen) und eine signifikante Änderung der Conversion-Ziele (z. B. Action primär ↔ sekundär umgestuft).
- Budget-, Zielwert- (tCPA/tROAS) und Targeting-Änderungen lösen laut Google **nie** „Learning” aus. Große Budget-Sprünge können trotzdem kurz Volatilität bringen — das ist kein „Learning”.
- Der Status dauert **höchstens 7 Tage**. Danach bleibt nur Schwankung durch Conversion-Lag (s. Attributions-Lag) als Vorbehalt.
- Im Audit: via `ads_change_history` prüfen, ob jüngst ein echter Auslöser lag; in der Learning-Zeit nicht hart beurteilen.
- Beleg: https://support.google.com/google-ads/answer/13020501

## Impression-Share-Diagnose-Matrix (Phase 5)
IS beantwortet „warum werde ich (nicht) ausgespielt”. Die drei Kernwerte:

| Wert | Bedeutung | Wenn hoch → Hebel |
|---|---|---|
| **Search Lost IS (Budget)** | Anteil verpasster Impressionen, weil Budget aus | Budget erhöhen — **aber nur wenn CPA/ROAS gut** (sonst erst Effizienz) |
| **Search Lost IS (Rank)** | Anteil verpasst wegen Ad Rank (Gebot × Qualität) | QS-Komponenten + Gebot/tCPA-Ziel, **nicht** Budget |
| **Search (Abs) Top IS** | Anteil der Impressionen ganz oben | niedrig + wichtige Keywords → Gebot/Qualität für Top-Position |

Schnell-Logik:
- **Lost IS (Budget) hoch, CPA gut** → klassischer „lass Geld liegen”-Fall → Budget rauf.
- **Lost IS (Rank) hoch** → Relevanz-/Gebotsproblem → Ad-Relevanz, LP, ggf. tCPA-Ziel anheben.
- **Beides niedrig, trotzdem wenig Traffic** → echtes Nachfrage-/Keyword-Volumen-Limit, nicht Konto-Setup.
- IS-Werte sind **Schätzungen** und werden unterhalb einer Schwelle redigiert (`< 10 %` / `--`) — als Richtung lesen.

## Quality Score richtig deuten (Phase 4)
QS (1–10) ist eine **nachlaufende Diagnose**, kein Hebel. Es zählen die drei Komponenten, jeweils „über/​durchschnittlich/​unterdurchschnittlich”:

| Komponente | „Unterdurchschnittlich” heißt | Fix |
|---|---|---|
| **Erwartete CTR** | Anzeige wird zu selten geklickt | Anzeigentext/Headlines, Extensions, Angebot |
| **Anzeigenrelevanz** | Anzeige passt schlecht zum Keyword | Keyword in die Anzeige, engere thematische Ad Group |
| **Landingpage-Erfahrung** | LP irrelevant/langsam/dünn | Landingpage (Tiefe/Speed via `seo-audit`) |

Niedriger QS → höherer CPC für dieselbe Position. **Aber:** QS nie als „Score hochschrauben”-Ziel formulieren — immer den Komponenten-Befund in eine konkrete Maßnahme übersetzen.

## Ad Strength & Optimization Score (Realität)
- **Ad Strength** (Poor → Excellent) bewertet Asset-Vielfalt/-Menge der RSA (genug Headlines, Diversität, wenig Pinning). Sie bleibt Diagnose, nicht Geschäftsziel — aber:
  - Für **ungepinnte** Anzeigen gilt: höhere Ad Strength = bessere Ergebnisse → „Excellent” anstreben (https://adalysis.com/blog/google-ads-data-study-does-a-higher-ad-strength-improve-your-performance/).
  - Der Conversion-Vorteil schwächer bewerteter Anzeigen kommt vor allem vom **Pinning** (Beobachtungsdaten). Gegenbefund Optmyzr: Mit Pinning sinkt die Conversion-Rate; Pinning ist eine Kreativ-/Marken-Entscheidung (https://www.optmyzr.com/blog/google-ad-strength-study/).
  - Google empfiehlt mind. **2 RSAs mit Ad Strength „Good” oder „Excellent” pro Ad Group** (https://support.google.com/google-ads/answer/7684791).
  - **Tool-Grenze:** `ads_list_ads` liefert keine RSA-Ad-Strength (nur PMax-Asset-Gruppen via `ads_list_asset_groups`). Wert im Ads-UI prüfen; Befund-Stufe: beratend.
- **Optimization Score** (0–100 %) ist Googles **Hebel-Liste**, kein Konto-Qualitäts-Maß. Viele Empfehlungen sind Google-günstig (Budget rauf, Broad Match, Auto-Apply). 100 % „Optimierung” ≠ besseres Konto. Jede Empfehlung gegen die Audit-Befunde spiegeln (Phase 7).
