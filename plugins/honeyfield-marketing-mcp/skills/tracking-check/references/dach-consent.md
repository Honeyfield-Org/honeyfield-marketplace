# DACH-Consent-Referenz

Referenz für `tracking-check`. Detailkörper zum Consent-Layer-Querschnitt in SKILL.md — on-demand laden. **Keine Rechtsberatung** — rein Prüf-/Hinweischarakter.

---

## A — Prüfbar vs. Nicht prüfbar (Beleg-Stufen)

| Was | Stufe | Tool | Hinweis |
|---|---|---|---|
| Consent-/CMP-Tag im GTM vorhanden | **Nur konfiguriert** | `gtm_list_tags`, `gtm_get_tag` | Prüft Existenz + Tag-Typ; beweist nicht, dass der Banner vor anderen Tags feuert |
| Tag-Level-Consent-Settings (Consent-Checks im Tag) | **Nur konfiguriert** | `gtm_get_tag` → Feld `consent_settings` | Feld vorhanden ≠ korrekt verdrahtet |
| Consent Mode v2 **korrekt** greift (Default denied → Update on grant) | **Nicht prüfbar** | — | Requires GTM-Preview / Tag-Assistant; kein API-Signal |
| `ad_user_data` / `ad_personalization` korrekt gesetzt | **Nicht prüfbar** | — | Nur im Browser-Kontext sichtbar |
| Tag feuert **vor** Consent (Dark Pattern) | **Nicht prüfbar** | — | Nur via Browser-Netzwerk-Tab oder Tag-Assistant |
| sGTM-Endpoint hinterlegt | **Nur konfiguriert** | `gtm_get_tag` (GA4-Config-Tag) → `transport_url` / `server_container_url` | Nur Konfigurationspräsenz; Live-Gesundheit des Servers nicht bestätigbar |

**Grundsatz:** Consent-Compliance ist per MCP-Tools höchstens als „konfiguriert vorhanden" belegbar — nie als „korrekt greifend". Für Compliance-Aussagen GTM-Preview / Tag-Assistant / Browser-Inspektion erforderlich.

---

## B — Google Consent Mode v2

### Die vier Signale

| Signal | Bedeutung | Pflicht ab 2024 |
|---|---|---|
| `ad_storage` | Werbe-Cookies und Identifier schreiben/lesen | Ja (war v1) |
| `analytics_storage` | GA4-Cookies (Session-Stitching) | Ja (war v1) |
| `ad_user_data` | First-Party-Daten an Google Ads senden | **Neu v2** — Pflicht für Conversion-Tracking |
| `ad_personalization` | Remarketing / Personalisierung | **Neu v2** — Pflicht für Remarketing-Listen |

**Enforcement:** Ab März 2024 verlangt Google alle vier Signale für EEA/UK-Traffic, um Remarketing, Personalisierung und modellierte Conversions zu ermöglichen. Ohne korrekte v2-Implementierung: keine neuen Einträge in Remarketing-Audiences, kein Conversion-Modelling.

### Basic vs. Advanced

| Modus | Verhalten bei Consent-Ablehnung | Modelling |
|---|---|---|
| **Basic** | Google-Tags werden komplett geblockt — kein cookieless Ping | Kein Modelling möglich |
| **Advanced** | Cookieless Ping wird trotzdem gesendet | Conversion- und Audience-Modelling aktiv |

Empfehlung DACH: Advanced = mehr Daten + Modelling, aber technisch anspruchsvoller und muss Banner-Logik korrekt implementieren (Default denied, kein Pre-Consent-Firing).

### Juni 2026 — Update (Stand/Datum vor Kundennutzung verifizieren)

Nach Google-Ankündigung ist ab 15. Juni 2026 `ad_storage` der einzige Kontrollhebel für Ads-Daten. Google Signals wird auf Analytics-interne Zwecke (GA4-Nutzerberichte) eingeschränkt — nicht mehr für Ads-Daten. **Praktische Konsequenz:** CMP-Konfiguration ist der alleinige Datenschutz-Hebel für Google-Ads-Signale; fehlerhafte CMP-Konfiguration hat direkten Ads-Impact.

---

## C — DACH-Recht (Prüf-/Hinweischarakter, keine Rechtsberatung)

### Deutschland — §25 TDDDG + DSGVO

Das frühere TTDSG heißt seit **Mai 2024 TDDDG** (Telekommunikation-Digitale-Dienste-Datenschutzgesetz). §25 ist inhaltlich unverändert.

- **§25 Abs. 1 TDDDG**: Einwilligung erforderlich vor Speicherung/Zugriff auf Endgerät (Cookies, Pixel, LocalStorage) — außer technisch notwendig.
- **Ausnahme §25 Abs. 2**: Technisch zwingend notwendige Cookies ohne Einwilligung erlaubt (Session, Warenkorb).
- **DSGVO Art. 6 Abs. 1 lit. a**: Rechtsbasis für Verarbeitung personenbezogener Daten — Einwilligung muss frei, informiert, granular und widerrufbar sein; kein Opt-out, kein Pre-checked.
- **Bußgeld**: §28 Abs. 1 TDDDG bis 300.000 EUR (Rahmen gegen aktuelle Fassung prüfen); DSGVO bis 4 % des weltweiten Jahresumsatzes oder 20 Mio. EUR.
- **Dark Pattern**: Erste Banner-Ebene muss gleichwertige Ablehnen-Option zeigen — kein „Okay"-Button ohne „Ablehnen".
- **PIMS** (Personal Information Management Services): Das TDDDG sieht anerkannte Einwilligungsverwaltungsdienste vor, die Cookie-Banner mittelfristig für zertifizierte Nutzer ersetzen können — Anerkennungsverordnung/Aufbau noch im Gange; konkreten Stand (Paragraf, Inkrafttreten) vor Kundennutzung verifizieren.

**DACH-spezifisch DE (Stand 2025):** Ob alleiniges Laden von GTM vor Consent (ohne Tag-Feuern) bereits einwilligungspflichtig ist, wird gerichtlich diskutiert und ist umstritten. Sicherere Praxis: CMP zuerst laden, GTM erst nach Consent-Signal injizieren.

### Österreich — §165 TKG 2021 + DSG + DSGVO

- **§165 Abs. 3 TKG 2021**: Cookie-Einwilligungspflicht analog §25 TDDDG (DE) — technisch notwendige Cookies ausgenommen.
- **DSG** (Datenschutzgesetz AT): Ergänzt DSGVO auf nationaler Ebene; keine signifikante Abweichung bei Cookie-Consent.
- **DSB-Leitlinien 2024**: verschärfte Anforderungen an Schaltflächen-Gleichwertigkeit auf erster Banner-Ebene + granulare Kategorien.
- Pay-or-OK-Modelle unter Beobachtung (DSB hat noch keine abschließende Positionierung).

### Schweiz — nDSG (revDSG)

- **nDSG** (in Kraft seit 1. September 2023): Kein gesetzlicher Cookie-Banner-Zwang aus dem Schweizer Recht — das nDSG folgt nicht der EU-Cookie-Richtlinie.
- **Ausnahme**: Marketing-/Tracking-Cookies, die Personendaten verarbeiten, können dennoch DSGVO-Pflichten auslösen, wenn der Betreiber EU-Bezug hat (Art. 3 DSGVO).
- **Google EU-UCP für CH**: Seit **31. Juli 2024** gilt Googles EU User Consent Policy auch für Schweizer Traffic — wer Google-Produkte (GA4, Google Ads) nutzt und CH-User trackt, muss Consent Mode implementieren oder riskiert eingeschränkte Datenerhebung.
- **Praktisches Ergebnis**: Für DACH-übergreifende Setups immer mit Banner abdecken — rein-CH-Setups ohne EU-Targeting haben theoretisch mehr Spielraum, aber faktisch kaum.

---

## D — CMP-Landschaft DACH

Zertifizierte CMPs mit nativem Consent Mode v2 Support und GTM-Template:

| CMP | Besonderheit DACH | GTM-Integration |
|---|---|---|
| **Usercentrics** | Marktführer DACH; Cookiebot = Usercentrics-Marke seit Übernahme 2021; starke DE-rechtliche Dokumentation | GTM-Template (Template Gallery) + direkte gtag-Integration; v2 nativ |
| **Cookiebot (by Usercentrics)** | Technisch ident mit Usercentrics v3 unter der Haube; Cookiebot-Branding für ältere Installationen noch verbreitet | GTM-Template; automatisches Consent-Update-Signal |
| **Consentmanager** | DE-basierter Anbieter (Köln); starke DACH-Localization; auch AT/CH-Sprach- und Rechtsvarianten | GTM-Template; Consent Mode v2 via API-Callback |

**Integrationsmuster (GTM):**
1. CMP-Script (via GTM-Template oder direkt im `<head>`) lädt **vor** allen anderen Tags.
2. CMP schreibt `gtag('consent', 'default', { ... denied })` — alle Signale standardmäßig denied.
3. Nach Nutzer-Interaktion: CMP ruft `gtag('consent', 'update', { ... granted })` für gewählte Kategorien.
4. Google-Tags (GA4, Ads) reagieren auf die Updates — im Advanced Mode haben sie bereits cookieless Pings gesendet.

**Prüfbar via Tools:** `gtm_list_tags` prüft, ob CMP-Template-Tag vorhanden + in welcher Priorität (sollte höchste Priorität / Sequencing haben). Feuert-Reihenfolge selbst nicht verifizierbar via API.

---

## E — Server-Side-Tagging (sGTM)

### Zweck

sGTM verschiebt Tag-Ausführung vom Browser auf einen Server-Container (Cloud Run, GCP, etc.). Vorteile: bessere Datenvollständigkeit (weniger Ad-Blocker-Impact), IP-Anonymisierung serverseitig, First-Party-Cookie-Verlängerung auf 7+ Tage (Safari ITP-Umgehung).

### Erkennungssignal via Tools

`gtm_get_tag` auf dem GA4-Konfiguration-Tag → Feld `transport_url` (oder `server_container_url`): zeigt auf eigene Domain (z. B. `collect.beispiel.de`) statt `analytics.google.com`.

**Prüfbar:** sGTM-Endpoint im Tag hinterlegt — ja/nein.
**Nicht prüfbar:** Live-Gesundheit des sGTM-Servers, ob Hits ankommen, ob Consent-Logik auf sGTM korrekt repliziert ist.

### sGTM und Consent Mode

Consent Mode v2 muss im **Browser-Container** (Client-Side GTM) implementiert bleiben — sGTM löst das Consent-Problem nicht. Häufiger Fehler: sGTM als Consent-Bypass missverstanden (ist es nicht — personenbezogene Daten dürfen auch serverseitig nur mit Rechtsgrundlage verarbeitet werden).

---

## F — compliance-Flag-Verknüpfung

Flags aus `projekt-kontext` (Frontmatter `compliance:`) sind harte Leitplanken:

| Flag | Implikation für Consent-Layer |
|---|---|
| `dsgvo: strict` | Kein Tracking vor expliziter Einwilligung; keine Pay-or-OK-Empfehlung; Erwähnung TDDDG §25 zwingend |
| `ttdsg: true` / `tdddg: true` | §25 TDDDG-Hinweis obligatorisch; GTM-Pre-Consent-Laderisiko benennen |
| `ch_only: true` | nDSG-Hinweis: kein gesetzlicher Banner-Zwang, aber Google EU-UCP für CH-Traffic seit 31.07.2024 beachten |
| `at: true` | §165 TKG AT + DSB-Leitlinien 2024 benennen |
| `no_remarketing: true` | `ad_personalization` = denied hardcoded empfehlen; Remarketing-Audiences deaktivieren |

Fehlt `compliance`-Block im `projekt-kontext`: Default = DSGVO-konservativ behandeln (DACH = DE-Standard).
