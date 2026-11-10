# DACH-Compliance — Branche → Rahmen (für `compliance:`-Flags)

Zweck: Aus der Branche die richtigen `compliance:`-Flags ableiten und im Projekt-Kontext festhalten, **damit Audit-/Ads-/Content-Skills wissen, worauf sie achten müssen**.

**Keine Rechtsberatung** — nur den regulatorischen Rahmen markieren; im Zweifel an Fachanwalt/Kammer verweisen. Die Rechtslage ändert sich; Flags sind Orientierung, kein Rechtsrat. Länderunterschiede DE/AT/CH beachten.

## Kanonisches Flag-Vokabular (verbindlich für alle Konsumenten)
`compliance:` ist eine **flache YAML-Liste**. Gültig sind **exakt** die Flags aus den Tabellen dieser Datei — Schreibweise wie dort, Konsumenten-Skills matchen wörtlich (Exact-Match): `DSGVO`, `TTDSG`, `Impressum`, `PAngV`, `HWG`, `BRAO`, `RAO`, `StBerG`, `WpHG`, `Verbraucherkredit`, `GlüStV`, `GSpG`, `Jugendschutz`, `HealthClaims`, `UWG` + Zusatz-Flags unten. Keine eigenen Flag-Namen erfinden. **Länder-Unterscheidung läuft über den Stable Key `maerkte:`** (DE/AT/CH), nicht über eigene Flags.

### Zusatz-Flags (optional, kundenspezifisch)
| Flag | Was | Worauf achten |
|---|---|---|
| `no_remarketing` | Kunde untersagt Remarketing/Personalisierung | `ad_personalization` = denied empfehlen; keine Remarketing-Audiences anlegen |

## Gilt (fast) immer
| Flag | Was | Worauf achten |
|---|---|---|
| `DSGVO` | EU-Datenschutz (CH: revDSG) | Tracking-/Conversion-Pixel nur mit gültigem Consent. **Rolle je Dienst klären:** Für Google-Ads-/GA4-Messung gelten grundsätzlich die Controller-Controller-Bedingungen; Google ist Auftragsverarbeiter (AVV/Data Processing Terms) nur bei Customer Match, Enhanced Conversions (inkl. für Leads) und Store-Sales-Uploads ([Google-Liste](https://business.safety.google/adsservices/)). Die Google EU User Consent Policy ist Vertragspflicht — auch für Kunden-Properties, die eine Agentur betreut ([Policy](https://www.google.com/about/company/user-consent-policy/)). Im Zweifel Fachanwalt |
| `TTDSG` | Cookie-/Endgeräte-Zugriff — DE: § 25 Abs. 1 TDDDG (früher TTDSG; der Flag-Name `TTDSG` bleibt, Konsumenten matchen ihn wörtlich) · AT: TKG §165 · CH: revDSG | Consent vor nicht-essentiellen Cookies — Einwilligung ist Gesetz, nicht nur Google-Vorgabe; **Conversion-Tracking ohne Consent ist unvollständig** — erklärt oft „fehlende” Conversions; relevant für die Ads-Conversion-Bewertung, den Consent-Check macht `tracking-check` |
| `Impressum` | Anbieterkennzeichnung — DE: DDG (früher TMG) · AT: §5 ECG / §25 MedienG · CH: Art. 3 UWG (Fernabsatz) | Impressum vorhanden + ≤1 Klick erreichbar; auf beworbenen Landingpages Pflicht |
| `PAngV` | Preisangaben | Endpreise inkl. USt., ggf. Grundpreis je Einheit; relevant für E-Commerce-Ads + LP |

## Branchen-spezifisch
| Branche | Flags | Worauf achten (Ads / Content / Audit) |
|---|---|---|
| Heilberufe / Arzt / Zahnarzt / Klinik / Pharma / Medizinprodukte | `HWG` (DE Heilmittelwerbegesetz; AT AMG + Ärztegesetz-Werbeschranken; CH HMG/AWV) | Keine Heil-/Wirkversprechen, keine Vorher-Nachher-Bilder, keine irreführenden Erfolgsaussagen; berufsrechtliche Werbeschranken (Ärztekammer). Ads: Superlative/Versprechen in Headlines vermeiden |
| Rechtsanwälte | `BRAO` (DE BRAO/BORA) · `RAO` (AT) | Sachliche, berufsbezogene Werbung; keine reißerische Erfolgs-/Mandantenwerbung |
| Steuerberater / Wirtschaftsprüfer | `StBerG` (DE) | Berufsrechtliche Werbebeschränkung, Sachlichkeit |
| Finanz / Kredit / Versicherung / Anlage | `WpHG` (AT: WAG) · `Verbraucherkredit` | Pflicht-Risikohinweise; Effektivzins/Pflichtangaben bei Krediten; keine irreführenden Renditeversprechen |
| Glücksspiel / Wetten | `GlüStV` (DE) · `GSpG` (AT) | Stark reglementiert/teils verboten; Lizenz-/Werbeauflagen, Jugendschutz |
| Alkohol / Tabak | `Jugendschutz` | Werbebeschränkungen; kein Targeting Minderjähriger |
| Lebensmittel / Supplements / „gesundheitsbezogen” | `HealthClaims` (EU-VO 1924/2006) | Nur zugelassene Health Claims; keine krankheitsbezogenen Aussagen |
| Gewinnspiele / Rabattaktionen | `UWG` | Transparente Teilnahmebedingungen; keine Irreführung |

## Wie Skills die Flags nutzen
- **`google-ads-audit` / `ad-creative`:** riskante/verbotene Formulierungen in Headlines/Descriptions/Sitelinks meiden; bei `HWG`/`HealthClaims` besonders streng.
- **tracking-check / Conversion-Bewertung:** bei `DSGVO`/`TTDSG` Conversions nur mit gültigem Consent als valide werten; Consent-Mode/fehlender Consent erklärt oft scheinbar „verlorene” Conversions.
- **seo-audit:** `Impressum`/`PAngV` als Trust-/Pflicht-Check auf Landingpages.

*Im Zweifel keine Aussage zur Rechtmäßigkeit treffen — Flag setzen, Hinweis geben, an Fachanwalt verweisen.*
