# Event-Soll-Library DACH

> **Nutzungshinweis:** Nur die geschäftstyp-relevante Sektion gegen den Kunden halten (aus `projekt-kontext`) — nicht die ganze Library.

Grundlage: Coreys Event-Library (US-SaaS), DACH-lokalisiert + erweitert um Lead-Gen / lokale Dienstleister. GA4 Enhanced E-Commerce Naming als Standard.

---

## Naming-Regeln

- **Schema:** Object-Action, `lowercase_underscore` — z. B. `form_submit`, `add_to_cart`, `video_play`
- **Kein Kontext im Event-Namen.** Kein `newsletter_form_submit_homepage` — stattdessen `form_submit` mit `form_name="newsletter"` und `form_location="homepage_hero"`
- **GA4-Standard-Events** (Enhanced E-Commerce) bevorzugen, wo sie existieren (`view_item`, `add_to_cart`, `purchase` etc.)
- **Währung immer `EUR`**, nie USD

---

## 1 — Marketing-Site / Lead-Gen (DACH-Fokus)

### Kern-Events

| Event | Beschreibung | Schlüssel-Properties |
|---|---|---|
| `page_view` | Seite geladen (enhanced) | `page_title`, `page_location`, `content_group` |
| `scroll_depth` | Scroll-Schwellwert erreicht | `depth` (25 / 50 / 75 / 100) |
| `cta_click` | CTA-Button geklickt | `button_text`, `cta_location`, `page` |
| `form_start` | Nutzer hat Formular begonnen | `form_name`, `form_location` |
| `form_submit` | Anfrageformular erfolgreich abgeschickt | `form_name`, `form_location`, `form_type` |
| `form_error` | Formular-Validierungsfehler | `form_name`, `error_type` |
| `phone_click` | `tel:`-Link geklickt | `phone_number`, `page`, `click_location` |
| `whatsapp_click` | WhatsApp-Link/-Button geklickt | `page`, `click_location` |
| `email_click` | `mailto:`-Link geklickt | `email_address`, `page` |
| `download` | Datei heruntergeladen (Angebot / PDF / Broschüre) | `file_name`, `file_type`, `page` |
| `outbound_link_click` | Klick auf externe Seite | `link_url`, `link_text` |
| `video_play` | Video gestartet | `video_title`, `video_id`, `duration` |
| `video_complete` | Video beendet | `video_title`, `video_id` |
| `appointment_booked` | Termin gebucht (Online-Buchungstool) | `service_type`, `booking_tool`, `source` |
| `directions_click` | Routenplaner-Link geklickt (Google Maps o. Ä.) | `page`, `click_location` |

### Funnel-Sequenz

1. `page_view`
2. `cta_click` oder `form_start`
3. `form_submit` / `phone_click` / `whatsapp_click` / `email_click`
4. (offline) Lead qualifiziert → GA4 Offline-Conversion-Import oder CRM-Sync

---

## 2 — E-Commerce

GA4 Enhanced E-Commerce Events — Naming = GA4-Standard.

### Kern-Events

| Event | Beschreibung | Schlüssel-Properties |
|---|---|---|
| `view_item_list` | Kategorie- / Listenansicht | `item_list_name`, `items[]` |
| `select_item` | Produkt aus Liste geklickt | `item_list_name`, `item_id`, `item_name` |
| `view_item` | Produkt-Detailseite aufgerufen | `item_id`, `item_name`, `item_category`, `price`, `currency` (EUR) |
| `add_to_cart` | Produkt in Warenkorb gelegt | `item_id`, `item_name`, `price`, `quantity`, `currency` (EUR) |
| `remove_from_cart` | Produkt aus Warenkorb entfernt | `item_id`, `quantity` |
| `view_cart` | Warenkorb angesehen | `value`, `currency` (EUR), `items[]` |
| `begin_checkout` | Checkout begonnen | `value`, `currency` (EUR), `items[]` |
| `add_shipping_info` | Lieferadresse eingegeben | `shipping_tier`, `value`, `currency` (EUR) |
| `add_payment_info` | Zahlungsdaten eingegeben | `payment_type`, `value`, `currency` (EUR) |
| `purchase` | Bestellung abgeschlossen | `transaction_id`, `value`, `tax`, `shipping`, `currency` (EUR), `items[]` |
| `refund` | Rückerstattung veranlasst | `transaction_id`, `value`, `currency` (EUR) |
| `select_promotion` | Promotion-Banner geklickt | `promotion_id`, `promotion_name`, `creative_slot` |

**Pflicht-Properties bei `purchase`:** `transaction_id` (eindeutig, kein Duplikat-Zählen), `value`, `currency: "EUR"`. Netto vs. Brutto: projektintern konsistent festlegen.

### Funnel-Sequenz

1. `view_item`
2. `add_to_cart`
3. `begin_checkout`
4. `add_shipping_info`
5. `add_payment_info`
6. `purchase`

---

## 3 — SaaS / Product

### Kern-Events

| Event | Beschreibung | Schlüssel-Properties |
|---|---|---|
| `page_view` | Marketing-Site-Seite geladen | `page_title`, `page_location` |
| `pricing_view` | Preis-Seite aufgerufen | `source`, `plan_highlighted` |
| `sign_up` | Account angelegt | `method` (email / google / sso), `source`, `plan` |
| `onboarding_start` | Onboarding begonnen | — |
| `onboarding_step_complete` | Onboarding-Schritt abgeschlossen | `step_number`, `step_name` |
| `onboarding_complete` | Onboarding vollständig | `steps_completed`, `time_to_complete_s` |
| `activation` | Erster Aha-Moment erreicht (produktspezifisch definieren) | `action_type` |
| `feature_used` | Feature-Interaktion | `feature_name`, `feature_category` |
| `trial_start` | Testphase begonnen | `plan`, `trial_days` |
| `trial_end` | Testphase abgelaufen | `plan`, `converted` (bool) |
| `subscribe` | Abo abgeschlossen / Plan aktiviert | `plan`, `billing_cycle` (monthly / yearly), `value`, `currency` (EUR) |
| `subscription_upgrade` | Plan hochgestuft | `from_plan`, `to_plan`, `value`, `currency` (EUR) |
| `subscription_downgrade` | Plan heruntergestuft | `from_plan`, `to_plan` |
| `subscription_cancel` | Kündigung | `plan`, `reason`, `tenure_days` |
| `invite_send` | Nutzer eingeladen | `invite_type`, `count` |
| `integration_connect` | Integration erfolgreich verbunden | `integration_name` |

### Funnel-Sequenz

1. `pricing_view`
2. `sign_up`
3. `onboarding_complete`
4. `activation`
5. `trial_start` (falls Trial-Flow vorhanden)
6. `subscribe`

---

## 4 — Lokaler Dienstleister (DACH)

Basis wie Sektion 1 (Marketing-Site / Lead-Gen) — alle dortigen Events gelten. Ergänzt um physischen Kontakt, Terminbuchung und Routing.

### Zusätzliche Kern-Events

| Event | Beschreibung | Schlüssel-Properties |
|---|---|---|
| `appointment_booked` | → Sektion 1 | — |
| `directions_click` | → Sektion 1 | — |
| `phone_click` | `tel:`-Link geklickt | `phone_number`, `page`, `click_location` |
| `whatsapp_click` | WhatsApp-Kontakt geklickt | `page`, `click_location` |
| `form_submit` | Anfrageformular abgeschickt | `form_name`, `form_type`, `form_location` |
| `email_click` | `mailto:`-Link geklickt | `page`, `click_location` |
| `download` | PDF / Angebot / Preisliste heruntergeladen | `file_name`, `file_type` |

**Call-Tracking-Hinweis:** Statische Rufnummer = alle `phone_click`-Ereignisse landen unter derselben Property; quellgenaue Attribution ohne Dynamic Number Insertion (DNI) nicht möglich. DNI-Tools (z. B. Matelso, Aircall, CallRail) ermöglichen `phone_click` pro Quelle — prüfen ob aktiv oder empfehlenswert.

**Out of scope:** GBP-Interaktionen (Anrufe / Routenplanung aus Google Maps direkt im GBP-Panel) — kein GA4-Event, gehört in `gbp_performance`-Check → `seo-audit`-Skill.

### Funnel-Sequenz

1. `page_view`
2. `cta_click` oder `form_start`
3. `form_submit` / `phone_click` / `whatsapp_click` / `appointment_booked` / `directions_click`
4. (offline) Auftrag erteilt → Offline-Conversion-Import in GA4 / Google Ads empfohlen

---

## Standard-Properties (DACH-Referenz)

```
# Nutzer-Kontext (erst nach Login setzen — DSGVO beachten)
user_id:    "usr_12345"
user_type:  "free" | "trial" | "paid"
account_id: "acct_99"

# Session
session_id:     "sess_abc"
session_number: 3

# Kampagnen (UTM)
source:   "google"
medium:   "cpc"
campaign: "fruehjahrsaktion-2024"
content:  "hero-cta"

# Produkt / E-Commerce
item_id:       "SKU-1234-DE"
item_name:     "Winterjacke Modell X"
item_category: "Bekleidung"
price:         89.95
quantity:      1
currency:      "EUR"          # Immer EUR — nie USD

# Transaktion
transaction_id: "ORD-2024-00123"
value:          89.95         # Netto oder Brutto — projektintern konsistent
tax:            14.36         # MwSt. (DE: 19 %, AT: 20 %, CH: 8.1 %)
shipping:       4.99
```
