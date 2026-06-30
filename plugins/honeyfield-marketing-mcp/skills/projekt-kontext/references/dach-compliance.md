# DACH-Compliance — Branche → Rahmen (für `compliance:`-Flags)

Zweck: Aus der Branche die richtigen `compliance:`-Flags ableiten und im Projekt-Kontext festhalten, **damit Audit-/Ads-/Content-Skills wissen, worauf sie achten müssen**.

**Keine Rechtsberatung** — nur den regulatorischen Rahmen markieren; im Zweifel an Fachanwalt/Kammer verweisen. Die Rechtslage ändert sich; Flags sind Orientierung, kein Rechtsrat. Länderunterschiede DE/AT/CH beachten.

## Gilt (fast) immer
| Flag | Was | Worauf achten |
|---|---|---|
| `DSGVO` | EU-Datenschutz (CH: revDSG) | Tracking-/Conversion-Pixel nur mit gültigem Consent; Auftragsverarbeitung sauber |
| `TTDSG` | Cookie-/Endgeräte-Zugriff — DE: TDDDG (früher TTDSG) · AT: TKG §165 · CH: revDSG | Consent vor nicht-essentiellen Cookies; **Conversion-Tracking ohne Consent ist unvollständig** — erklärt oft „fehlende” Conversions; relevant für `tracking-check` + Ads-Conversion-Bewertung |
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
- **google-ads-audit / Ads-Creation:** riskante/verbotene Formulierungen in Headlines/Descriptions/Sitelinks meiden; bei `HWG`/`HealthClaims` besonders streng.
- **tracking-check / Conversion-Bewertung:** bei `DSGVO`/`TTDSG` Conversions nur mit gültigem Consent als valide werten; Consent-Mode/fehlender Consent erklärt oft scheinbar „verlorene” Conversions.
- **seo-audit:** `Impressum`/`PAngV` als Trust-/Pflicht-Check auf Landingpages.

*Im Zweifel keine Aussage zur Rechtmäßigkeit treffen — Flag setzen, Hinweis geben, an Fachanwalt verweisen.*
