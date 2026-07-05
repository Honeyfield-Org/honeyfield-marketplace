# Gerichte-Map — welcher Parameter für welches Gericht

## `ris_judikatur`: `gerichtsbarkeit`-Werte

| Wert | Deckt ab | Hinweise |
| --- | --- | --- |
| `Justiz` | OGH, OLG, LG, BG (Zivil + Straf) | Default. `gericht="OGH"` für nur-Höchstgericht; `rechtsgebiet` Zivilrecht/Strafrecht; `fachgebiet` (OGH-Sachgebiete, greift nur bei Entscheidungstexten) |
| `Vfgh` | Verfassungsgerichtshof | `sammlungsnummer` = VfSlg; `entscheidungsart` Erkenntnis/Beschluss |
| `Vwgh` | Verwaltungsgerichtshof | `sammlungsnummer` = VwSlg |
| `Bvwg` | Bundesverwaltungsgericht (ab 2014) | Asyl, Sozialrecht, Regulierungsbehörden u.a. |
| `Lvwg` | Landesverwaltungsgerichte (ab 2014) | auch `entscheidungsart="Bescheid"` |
| `Dsk` | Datenschutzbehörde (DSB; historisch: Datenschutzkommission) | der Wert heißt weiterhin `Dsk` |
| `AsylGH` | Asylgerichtshof (2008–2013) | Altbestand |
| `Gbk` / `Pvak` / `Dok` / `Normenliste` | Gleichbehandlungskommission / Personalvertretungsaufsicht / Disziplinarkommissionen / Normenprüfungs-Liste | Spezialbestände |
| `Verg`, `Uvs`, `Ubas`, `Umse`, `Bks` | 2014 aufgelöste Senate | nur Altbestand, still searchable |

## Kennungen

- **OGH-Geschäftszahl:** `5 Ob 234/20b` — Senat, Gattungszeichen, laufende Nummer/Jahr + Prüfzeichen. In `geschaeftszahl=` ohne Leerzeichen tolerant: `"5Ob234/20b"`.
- **Sammlungsnummern:** VfSlg (nur bei `Vfgh`), VwSlg (nur bei `Vwgh`) über `sammlungsnummer=`.
- **ECLI Österreich:** `ECLI:AT:OGH0002:2020:0050OB00234.20B.0525.000` — für Zitate reicht die Kurzform Gericht + Datum + Gz.
- **Rechtssatz vs. Entscheidungstext:** ein Rechtssatz kann auf mehreren Entscheidungen beruhen (Rechtssatzkette = Indiz für ständige Rechtsprechung); der Entscheidungstext trägt die Begründung.

## EuGH über EUR-Lex

- `eurlex_search` mit `resource_type`: `JUDG` (Urteil) · `ORDER` (Beschluss) · `OPIN_AG` (Schlussanträge des Generalanwalts — **keine Urteile**, aber oft der beste Einstieg in die Argumentation).
- **Titel-Suche:** EuGH-Sachen über **Parteinamen** suchen („Schrems”, „Meta Platforms”, „Google Spain”) — nicht über abstrakte Begriffe.
- **CELEX Sektor 6:** `6` + Jahr (der Rechtssache) + `CJ` (Urteil) / `CC` (Schlussanträge) / `CO` (Beschluss) + Nummer → `62018CJ0311` = Urteil in C-311/18 (Schrems II).
- **ECLI EU:** `ECLI:EU:C:2020:559`.
- **Rechtsprechung zu einem EU-Akt:** `eurlex_citations` (CELEX des Akts, `direction="cited_by"`) und die Treffer nach Urteilen filtern.
- **Zuständigkeit:** Der EuGH legt EU-Recht aus (v.a. Vorabentscheidungen, Art 267 AEUV) — die Anwendung im konkreten Fall bleibt bei den österreichischen Gerichten. Bei EU-rechtlich geprägten Normen beide Ebenen prüfen: EuGH-Linie + AT-Folgejudikatur (`norm=` in `ris_judikatur`).

## Rezepte

1. **„Rechtsprechung zu § 1319a ABGB?”** → `ris_judikatur` (`norm="1319a ABGB"`, `dokumenttyp="beide"`) → Rechtssatzketten gruppieren → tragende Aussagen aus Entscheidungstexten belegen.
2. **„Entscheidung 5 Ob 234/20b?”** → `ris_judikatur` (`geschaeftszahl="5Ob234/20b"`) → `ris_dokument`.
3. **„Was hat der EuGH zu Schrems entschieden?”** → `eurlex_search` (`query="Schrems"`, `resource_type="JUDG"`) → `eurlex_fetch` → ECLI + Kernaussagen; AT-Folgewirkung über `ris_judikatur` (`suchworte="Schrems"`).
4. **„Neueste OGH-Entscheidungen im Mietrecht?”** → `ris_judikatur` (`gerichtsbarkeit="Justiz"`, `gericht="OGH"`, `fachgebiet="Bestandrecht"`, `sortierung="datum_ab"`).
