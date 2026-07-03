# Schema-Templates — Entity-Klarheit via JSON-LD

Phase 4 (Entity-Klarheit) + Operator. Ziel: ein referenzierbarer **Entity-Graph**, kein Insel-Snippet pro Typ. KIs matchen die Entity gegen ihren Knowledge-Graph — ein klarer `@id`-Knoten + `sameAs` ist der Hebel.

## Kernpattern: ein `@graph` mit `@id`-Knoten

Statt isolierte Snippets auszugeben, alles in einem Graphen verknüpfen:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.at/#organization",
      "name": "Beispiel GmbH",
      "url": "https://example.at",
      "logo": "https://example.at/logo.png",
      "sameAs": [
        "https://www.wikidata.org/wiki/Q…",
        "https://de.wikipedia.org/wiki/…",
        "https://www.linkedin.com/company/…",
        "https://www.crunchbase.com/organization/…"
      ],
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer service",
        "email": "hallo@example.at",
        "areaServed": ["AT", "DE", "CH"]
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://example.at/#website",
      "url": "https://example.at",
      "publisher": { "@id": "https://example.at/#organization" }
    }
  ]
}
```

`sameAs` ist das wichtigste Entity-Reconciliation-Signal — **immer auf Wikidata/Wikipedia/LinkedIn/Crunchbase** zeigen, nicht nur auf Social-Profile.

## Kerntypen (je nach Seite)

- **Organization** — name, url, logo, sameAs, contactPoint, areaServed. Einmal site-weit, als `@id` referenziert.
- **Person** (Autoren) — name, url (→ Autor-Entity), jobTitle, sameAs. Verknüpft `author` in Article.
- **Product + Offer** — name, image, brand, sku, `offers` (price, priceCurrency, availability). Preis muss im sichtbaren Text stehen (Phase 2).
- **Article / BlogPosting** — headline, datePublished, dateModified, `author` (→ Person `@id`), `publisher` (→ Organization `@id`), `mainEntityOfPage`.
- **BreadcrumbList** — auf jeder Unterseite; positioniert sie im Entity-Hierarchie-Pfad. Gratis-Strukturkontext.

## FAQPage / QAPage — Nuance

**Nicht** als „bringt FAQ-Rich-Snippet” empfehlen (Rich Result tot, siehe `geo-mechanik.md`). Wert für GEO: maschinenlesbare **Frage→Antwort-Claim-Struktur**, die LLMs leicht extrahieren. Nur einsetzen, wenn echte Q&A-Inhalte auf der Seite sichtbar sind (Accuracy-Regel).

## Accuracy-Regeln (Pflicht)

- Schema muss **dem sichtbaren Content entsprechen** — keine Felder markieren, die auf der Seite nicht stehen (Halluzinations-/Spam-Risiko).
- ISO-8601-Daten (`2026-06-29`), voll qualifizierte URLs, exakte Schema.org-Enumerations (z. B. `https://schema.org/InStock`).
- **SSR/statisch ausliefern** — JS-injiziertes JSON-LD sehen nicht-rendernde Crawler nicht (Phase 2).

## Validierungs-Checkliste (Operator-Postprocessing)

- [ ] Gegen `validator.schema.org` und Google Rich Results Test geprüft.
- [ ] `@id`-Knoten konsistent referenziert (Organization/WebSite/Person verlinkt).
- [ ] `sameAs` zeigt auf existierende, gepflegte Profile.
- [ ] Im Roh-HTML vorhanden (nicht JS-injiziert) — mit `curl` gegengeprüft.
- [ ] Keine Felder ohne sichtbares Pendant auf der Seite.
