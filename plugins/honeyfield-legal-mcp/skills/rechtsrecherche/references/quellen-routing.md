# Quellen-Routing — Tool-Map RIS + EUR-Lex

Alle Tools sind read-only. Diese Map beantwortet: welches Tool für welche Frage, mit welchen Schlüssel-Parametern — und wo die Fallstricke liegen.

## RIS — Österreich

### `ris_bundesrecht` — Bundesgesetze und -verordnungen, konsolidiert
- `titel=` für Gesetzesnamen/Abkürzungen („ABGB”, „Strafgesetzbuch”), `suchworte=` für Volltext, `paragraph=` für die konkrete Stelle.
- `abschnitt_typ`: `"Paragraph"` (Default) · `"Artikel"` (Artikel-Gesetze wie B-VG, StGG) · `"Anlage"`. **Fallstrick:** Art 7 B-VG ohne `abschnitt_typ="Artikel"` → kein Treffer.
- `fassung_vom=YYYY-MM-DD`: Rechtsstand zu einem Stichtag (historische Fassung).
- `applikation`: `"BrKons"` (konsolidiert, Default) · `"Begut"` (Begutachtungsentwürfe) · `"BgblAuth"` (Kundmachungen) · `"Erv"` (englische Übersetzungen — unverbindlich, kein `fassung_vom`).

### `ris_landesrecht` — Landesgesetze, konsolidiert
- `bundesland=` (Wien, Niederoesterreich, Oberoesterreich, Salzburg, Tirol, Vorarlberg, Kaernten, Steiermark, Burgenland), `titel=`/`suchworte=`/`paragraph=`, `fassung_vom=`, `gesetzesnummer=` für den Direktzugriff.

### `ris_gemeinden` — Gemeinderecht
- `applikation="Gr"` (Gemeinderecht, Default; `fassung_vom`, `index=` Sachgebiete) · `"GrA"` (Amtsblätter; `bezirk=`, `kundmachungsdatum_von/bis`). `gemeinde=` z.B. „Graz”.

### `ris_bezirke` — Kundmachungen der Bezirksverwaltungsbehörden
- Nur Niederösterreich, Oberösterreich, Tirol, Vorarlberg, Burgenland, Steiermark veröffentlichen hier.

### `ris_verordnungen` — Verordnungsblätter der Länder
- **Nur Tirol, erst seit 2022-01-01.** Andere Länder publizieren (noch) nicht in RIS — als Lücke benennen, nicht raten.

### `ris_bundesgesetzblatt` — BGBl
- `applikation`: `"BgblAuth"` (authentisch, ab 2004, Default) · `"BgblAlt"` (1945–2003) · `"BgblPdf"`.
- `bgblnummer=`/`jahrgang=`/`teil=` (`"1"` Gesetze · `"2"` Verordnungen · `"3"` Staatsverträge).

### `ris_landesgesetzblatt` — LGBl
- `applikation`: `"LgblAuth"` (Default) · `"Lgbl"` · `"LgblNO"`; plus `bundesland=`, `lgblnummer=`, `jahrgang=`.

### `ris_regierungsvorlagen` — Gesetzesmaterialien
- Regierungsvorlagen ans Parlament: Absicht des Gesetzgebers, EU-Bezüge. `einbringende_stelle=` (Ministerium), `beschlussdatum_von/bis`, `suchworte=`.

### `ris_history` — Änderungshistorie
- `applikation=` ist Pflicht (u.a. `Bundesnormen`, `Landesnormen`, `BgblAuth`, `Justiz`, `Vfgh`, `Vwgh`, `Erlaesse`); `aenderungen_von/bis` — was im Zeitraum neu/geändert/gelöscht wurde. Werkzeug für den Rechtsstand-Check.

### `ris_sonstige` — Spezialsammlungen
- `applikation=` Pflicht: `"Erlaesse"` (Ministerien, mit `fassung_vom`) · `"Mrp"` (Ministerratsprotokolle) · `"Avsv"` (Sozialversicherung) · `"PruefGewO"` · `"Spg"` · `"Avn"` · `"KmGer"` · `"Upts"`.

### `ris_dokument` — Volltext
- `dokumentnummer=` (z.B. „NOR40052761”) oder `url=` aus dem Suchergebnis. **Lange Dokumente können gekürzt sein** — dann gezielter suchen und die Kürzung ausweisen.

### `ris_judikatur` — Rechtsprechung
- Gehört zum Skill `judikatur`. Hier nur relevant: `norm="1295 ABGB"` zeigt, welche Entscheidungen eine Norm zitieren — nützlich als Querverweis am Ende einer Norm-Recherche.

## EUR-Lex — EU

### `eurlex_search` — Suche nach Titel
- **SPARQL-Titelsuche, kein Volltext-Index.** „Kommt Begriff X im Text vor” geht nicht — Aktennamen verwenden oder auf `eurlex_by_eurovoc` ausweichen.
- `resource_type`: `REG` (Verordnung) · `DIR` (Richtlinie) · `DEC` (Beschluss) · `JUDG`/`ORDER`/`OPIN_AG` (Rechtsprechung) · `RECO`, jeweils auch `_IMPL`/`_DEL`. `language` DEU/ENG/FRA, `date_from/to`, `limit` ≤ 50.

### `eurlex_by_eurovoc` — thematische Suche
- EuroVoc-Konzept als Label („data protection”) oder URI. Der Weg für Themenfragen ohne bekannten Aktennamen.

### `eurlex_fetch` — Volltext per CELEX
- `format` plain/xhtml, `max_chars` ≤ **50.000 (Truncation!)**. Liefert die **Stammfassung** — nicht zwingend den geltenden Text.

### `eurlex_consolidated` — geltende konsolidierte Fassung
- Via ELI: `doc_type` (`reg`/`dir`/`dec`) + `year` + `number` — z.B. reg/2016/679 für die DSGVO. Erste Wahl für „was gilt heute”.

### `eurlex_metadata` — Metadaten per CELEX
- Daten (Annahme, Inkrafttreten), Autoren, EuroVoc-Deskriptoren, Directory-Codes.

### `eurlex_citations` — Zitierbeziehungen
- `direction`: `cites` (was zitiert dieser Akt: Rechtsgrundlagen) · `cited_by` (wer zitiert ihn: Änderungsakte, Durchführungsrecht, Urteile) · `both`.

## CELEX-Anatomie (Kurz)

- **Sektor 3** = Sekundärrecht: `3` + Jahr + Typ (`R` VO / `L` RL / `D` Beschluss) + Nummer → `32016R0679` = VO (EU) 2016/679.
- **Sektor 6** = Rechtsprechung: `6` + Jahr + `CJ` (EuGH-Urteil) / `CC` (Schlussanträge) / `CO` (Beschluss) + Nummer.
- **Sektor 0** = konsolidierte Fassungen (`02016R0679-…`).

## Standard-Rezepte

1. **„Was sagt § X?”** → `ris_bundesrecht` (`titel`, `paragraph`) → `ris_dokument` → zitieren mit Fassung.
2. **„Geltender Text der VO 2016/679?”** → `eurlex_consolidated` (reg, 2016, 679).
3. **„Was ist neu im MRG seit 2024?”** → `ris_history` (Bundesnormen, ab 2024-01-01) + `ris_bundesgesetzblatt` → Novellen mit Kundmachung + Inkrafttreten.
4. **„RL (EU) 2019/1937 in Österreich?”** → `eurlex_metadata`/`eurlex_citations` (32019L1937) → `ris_bundesrecht` (`suchworte="2019/1937"`) → BGBl-Text auf den Umsetzungshinweis prüfen.
