---
name: projekt-kontext
description: "Erstellt und pflegt den Projekt-Kontext eines Kunden — das Fundament-Dokument, das alle anderen Marketing-Skills (seo-audit, google-ads-audit, geo-audit, …) zuerst lesen, damit sie Markt, Marke, Ziele und rechtlichen Rahmen kennen, ohne erneut zu fragen. Nutze diesen Skill am Anfang eines neuen Kunden-Projekts und bei: „Projekt-Kontext anlegen/aufsetzen”, „Kunden-Kontext”, „Kontext erstellen/updaten”, „neues Kunden-Onboarding”, „Kunde einrichten”, „festhalten wer der Kunde ist / was die Firma macht”, „Marke/Branche/Zielmarkt/Compliance hinterlegen”. Befüllt eine Erstversion automatisch aus verbundenen Quellen (Website/Impressum, Google Business Profile, Search Console, GA4) und verfeinert sie im Interview. Speichert das Ergebnis als `projekt-kontext.md` (Claude Code) bzw. zur Ablage im Projektwissen (Claude.ai). Kalibriert auf den DACH-Markt (DE/AT/CH). Für Audits/Reports selbst den jeweiligen Skill nutzen — hier entsteht nur das Fundament."
metadata:
  version: 0.3.0
---

# Projekt-Kontext

Lege den Projekt-Kontext eines Kunden an und pflege ihn — das **Fundament-Dokument**, das alle anderen Marketing-Skills (`seo-audit`, `google-ads-audit`, `geo-audit`, `tracking-check`, `ad-creative`, `wochenreport`) **zuerst lesen**, damit sie Markt, Marke, Ziele und rechtlichen Rahmen kennen, ohne den Nutzer erneut auszufragen.

Zwei Prinzipien:
- **Echte Daten statt Erfindung.** Befülle eine Erstversion aus dem, was schon da ist (Website, Google Business Profile, Search Console, GA4) — der Nutzer korrigiert, statt bei null anzufangen. Markenbegriffe und Kundensprache **wörtlich** erfassen.
- **DACH-kalibriert.** DE/AT/CH unterscheiden sich (Sprache, Recht, Währung). **Compliance ist Policy, nicht Deko**: gesetzte Flags steuern später, was Audit-/Creation-Skills dürfen.

## Schritt 1 — Existenz prüfen (immer zuerst)
Liegt für dieses Projekt schon ein Kontext vor?
- **Claude.ai:** im **Projektwissen** dieses Projekts (oft schon im Kontext sichtbar).
- **Claude Code:** Datei `projekt-kontext.md` im Arbeitsverzeichnis.

Wenn ja → **updaten, nicht neu**: gezielt Felder ergänzen/korrigieren, `stand`-Datum aktualisieren. Wenn nein → Schritt 2.

## Schritt 2 — Daten sammeln (Auto-Draft bevorzugt)
**Weg A — Auto-Draft (empfohlen).** Zieh eine Erstversion aus verbundenen Quellen, dann gemeinsam korrigieren. Quellen → Felder:

| Quelle (Tool) | füllt vor |
|---|---|
| `list_workspaces` | Domain(s), verbundene Datenquellen, `workspace:`-Slug (+ ggf. `dfs_workspace:`) |
| `dfs_onpage_instant` (Homepage) | Title/Meta/H1 → Firmenname, grobe Branche/Positionierung — mehr (Fließtext) liefert das Tool nicht |
| Impressum/„Über uns”-Volltext via Web-Fetch der Plattform (Claude.ai: eingebautes Browsing; Claude Code: `curl`/WebFetch) | Rechtsform, Leistungen, Standort/Markt, Sie/Du-Ansprache |
| `gbp_get_profile` / `gbp_location_info` | lokales Geschäft?, Kategorie → Branche, Standort → Markt; bei lokalen Geschäften `gbp_search_keywords` → reale lokale Suchbegriffe |
| `sc_top_queries` / `ga4_top_pages` | reale Money-Keywords, Schlüsselseiten, Brand-Queries → Brand-Begriffe |
| `dfs_keyword_rankings` (braucht nur die Domain) | Money-Keywords / Kern-Themen, wenn SC/GA4 (noch) nicht verbunden |
| `dfs_competitors_domain` (primär) + `dfs_serp_google_organic` / `dfs_backlink_competitors` (Ergänzung) | Konkurrenz-Domains |

Keine Fetch-Möglichkeit für Impressum/„Über uns”? → diese Felder im Interview (Weg B) erfragen, nicht still leer lassen.

**Beleg-Stufen — jedes auto-befüllte Feld markieren:** `# Quelle: <tool>` (belegt, direkt aus einem Tool) · `# vermutet` (abgeleitet, z.B. aus Title/H1) · `# offen` (unbekannt). So sehen nachgelagerte Skills, ob ein Wert belegt oder geraten ist.

Markt auf `dfs_*`-Calls kalibrieren (DE→`Germany`/`de`, AT→`Austria`/`de`, CH→`Switzerland`/`de`; Default AT/de). Zeig den Entwurf und frag **pro Sektion** „stimmt das / was fehlt?”.

**Weg B — Interview.** Sektion für Sektion, **eine Frage nach der anderen** (nicht alle auf einmal). **Pflichtkern zuerst**, optionaler Teil danach und **überspringbar** („reicht dir der Kern, oder willst du auch Zielgruppe/Voice für Content erfassen?”).

## Schritt 3 — Dokument schreiben
Nach dem Template unten: YAML-Frontmatter (greppbare Stable Keys) + Prosa-Sektionen. Optionalen Teil weglassen, wenn übersprungen. Nichts erfinden — leere Felder leer lassen oder als `# offen` markieren; auto-befüllte Felder tragen ihre Beleg-Stufe (`# Quelle: <tool>` / `# vermutet`). `# vermutet` wird erst nach expliziter Nutzer-Bestätigung zur unmarkierten Angabe — unbestätigte Markierungen bleiben im gespeicherten Dokument stehen.

## Schritt 4 — Speichern / Handoff (plattformabhängig)
- **Claude Code** (Dateizugriff vorhanden): schreibe das Dokument nach `projekt-kontext.md` ins Arbeitsverzeichnis (oder den vom Nutzer genannten Pfad). Liegt es im Repo, lesen alle Audits es automatisch.
- **Claude.ai** (kein Dateizugriff): gib das fertige Dokument vollständig aus und weise an: **„Füge dieses Dokument dem Projektwissen dieses Claude-Projekts hinzu (Projekteinstellungen → Wissen). Danach nutzen alle Audits es automatisch.”** Sei ehrlich: der Skill kann es hier **nicht selbst** speichern.

Bestätige am Ende, welche Felder gesichert sind und welche noch zu prüfen sind.

## Template
```markdown
---
kunde:                # Firmenname
workspace:            # Workspace-Slug aus `list_workspaces` — Konsumenten-Skills routen darüber, statt neu zu fragen
dfs_workspace:        # optional: Schwester-Workspace mit dataforseo:true (Credential-Träger für dfs_*)
domains: []           # [beispiel.de, beispiel.at]
sprachen: []          # de-DE, de-AT, de-CH
maerkte: []           # DE, AT, CH
lokal:                # true | false (lokales/regionales Geschäft?)
branche:              # z.B. Zahnarztpraxis, SaaS, E-Commerce Möbel
geschaeftsmodell:     # B2B | B2C | beides
ansprache:            # Sie | Du
brand_begriffe: []    # Marke, Produktnamen, Slogans (+ Varianten/Tippfehler)
konkurrenten: []      # Konkurrenz-Domains
geschaeftsziel:       # Lead | Kauf | Anruf | Awareness
ziel_kpi:             # z.B. "CPA < 40 €", "ROAS > 4"
compliance: []        # HWG, UWG, DSGVO, TTDSG, PAngV, … (s. references/dach-compliance.md)
stand:                # YYYY-MM-DD
---

# Projekt-Kontext: [Kunde]

## 1 — Geschäftsüberblick
**One-Liner:**
**Was / für wen:**
**Geschäftsmodell & Angebot:**

## 2 — Markt & Region
**Märkte (DE/AT/CH) + Unterschiede:**
**Reichweite:** lokal/regional vs. national
**Währung:** EUR / CHF

## 3 — Marke & Begriffe
**Markenname (+ Varianten/Tippfehler):**   <!-- für Brand/Non-Brand-Split & GEO-Citations -->
**Produktnamen / Slogans:**

## 4 — Wettbewerb
**Konkurrenz-Domains:**
**Positionierung ggü. ihnen (kurz):**

## 5 — Ziele & KPIs
**Primäres Geschäftsziel / Conversion:**
**Ziel-KPI (CPA/ROAS/…):**
**Saisonalität:**

## 6 — Such- & Themen-Fokus
**Money-Keywords / Kern-Themen (3–5):**
**Schlüsselseiten / Landingpages:**

## 7 — Compliance & rechtlicher Rahmen
**Flags:** [siehe Frontmatter] — Audit-/Creation-Skills behandeln diese als harte Leitplanke
**Hinweise:** z.B. HWG → keine Heil-/Wirkversprechen; DSGVO/TTDSG → Tracking nur mit Consent
*(Keine Rechtsberatung — nur den Rahmen markieren; im Zweifel Fachanwalt.)*

## 8 — Ansprache & Ton
**Sie/Du:**
**Ton / Tonalität (kurz):**

<!-- Optionaler Teil (für Content-/Creation-Skills; überspringbar) -->
## 9 — Zielgruppe / ICP (optional)
## 10 — Probleme & Pain Points (optional — verbatim Kundensprache)
## 11 — Positionierung & Differenzierung (optional)
## 12 — Brand-Voice (optional)
## 13 — Kundensprache (optional — Wörter to use / to avoid, Glossar DE↔EN)
## 14 — Proof Points (optional — Metriken, Testimonials, Logos)
```

## Compliance als Policy
Setze in `compliance:` die zutreffenden Flags anhand der Branche — Mapping + „worauf achten” in `references/dach-compliance.md`. Audit- und Creation-Skills lesen diese Flags und behandeln sie als **harte Leitplanke** (z.B. `HWG` → keine Heil-/Wirkversprechen in Anzeigen; `DSGVO`/`TTDSG` → Conversion-Tracking nur mit gültigem Consent als valide werten). Keine Rechtsberatung — nur den Rahmen markieren.

## Grenzen (ehrlich)
- Auto-Draft ist ein **Entwurf** — immer vom Nutzer bestätigen lassen; nichts als gesichert ausgeben, was nur geraten ist.
- In **Claude.ai** kein Auto-Save ins Projektwissen — manueller Schritt.
- Compliance-Flags ≠ Rechtsprüfung.

## Verwandte Skills
`seo-audit` · `google-ads-audit` · `geo-audit` · `tracking-check` · `wochenreport` (lesen diesen Kontext zuerst) · `ad-creative` (Haupt-Konsument des optionalen Teils 9–14 und der `compliance`-Flags)

## Referenzen
- `references/dach-compliance.md` — Branche → regulatorischer Rahmen (HWG/UWG/DSGVO/TTDSG/PAngV/…), Länderunterschiede DE/AT/CH, worauf Audits/Ads/Content achten müssen.
