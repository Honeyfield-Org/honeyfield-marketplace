# Tool-Map — rent2b MCP

156 Tools, Präfix `rent2b_`, generiert aus der rent2b-API (`mcp.honeyfield.at/rent2b/mcp`). Jeder Nutzer sieht/verwaltet ausschließlich die eigene Organisation (OAuth-Login mit dem rent2b-Konto). R = read, W = write/destruktiv (nie ohne Bestätigung ausführen).

**Caveat:** Die 4 `rent2b_duration_discounts_*`-Tools (Staffelpreise/Langzeitrabatte) sind neu und gehen mit dem nächsten rent2b-api-Deploy live. Antworten sie mit 404, direkt so sagen ("Feature ist noch nicht ausgerollt") statt erneut zu probieren.

---

## Buchungen (Bookings)

| Tool | Was | R/W |
|---|---|---|
| `rent2b_bookings_create` | Neue Buchung für Raum(e) oder Artikel anlegen | W |
| `rent2b_bookings_list` | Alle Buchungen der Organisation (Vermieter-Sicht), filter-/sortierbar | R |
| `rent2b_bookings_my_list` | Buchungen, bei denen der eingeloggte User Mieter ist | R |
| `rent2b_bookings_get` | Details einer Buchung | R |
| `rent2b_bookings_update` | Buchung aktualisieren (Termine, Status, Preis-Override, …) | W |
| `rent2b_bookings_cancel` | Buchung stornieren + Rückerstattung anstoßen | W |
| `rent2b_bookings_confirm` | Ausstehende Buchung bestätigen | W |
| `rent2b_bookings_reject` | Ausstehende Buchung ablehnen (optional mit Grund) | W |
| `rent2b_available_resources` | Alle verfügbaren Räume/Artikel der Organisation für einen Zeitraum | R |
| `rent2b_availability_check` | Verfügbarkeit + Preis für Raum/Artikel in einem Zeitraum prüfen | R |

### Anfragen (off-platform Reservierungen)

| Tool | Was | R/W |
|---|---|---|
| `rent2b_bookings_reservations_pending_list` | Offene/reservierte Reservierungen (noch nicht abgelaufen) — Kalender-Ansicht | R |
| `rent2b_bookings_reservations_pending_requests_list` | Off-platform-Reservierungen mit Status pending/reserved, die auf Freigabe warten — Admin-„Anfragen"-Sektion | R |
| `rent2b_bookings_reservations_confirm_create` | Off-platform-Reservierung bestätigen (nur Org-Owner) | W |
| `rent2b_bookings_reservations_reject_create` | Off-platform-Reservierung ablehnen/stornieren (nur Org-Owner) | W |

### Checklisten

| Tool | Was | R/W |
|---|---|---|
| `rent2b_bookings_checklists_create` | Checkliste für eine Buchung anlegen (Phase check_in/check_out) | W |
| `rent2b_checklists_list` | Alle Checklisten einer Buchung | R |
| `rent2b_checklists_get` | Einzelne Checkliste abrufen | R |
| `rent2b_bookings_checklists_items_update` | Checklisten-Punkt abhaken/Notiz setzen | W |
| `rent2b_bookings_checklists_complete_update` | Checkliste als abgeschlossen markieren | W |

### Schäden (Damages)

| Tool | Was | R/W |
|---|---|---|
| `rent2b_bookings_damages_create` | Schaden für eine Buchung melden (Titel, Typ, Schweregrad, Betrag) | W |
| `rent2b_bookings_damages_list` | Alle Schadensmeldungen einer Buchung | R |
| `rent2b_bookings_damages_list_2` | Einzelne Schadensmeldung abrufen | R |
| `rent2b_bookings_damages_update` | Schadensmeldung ändern (Status, Betrag, Beschreibung, …) | W |
| `rent2b_bookings_damages_delete` | Schadensmeldung löschen | W |
| `rent2b_bookings_damages_images_create` | Bilder zu einer Schadensmeldung hochladen | W |
| `rent2b_bookings_damages_images_list` | Bilder einer Schadensmeldung auflisten | R |
| `rent2b_bookings_damages_images_delete` | Schadensbild löschen | W |

### Reviews

| Tool | Was | R/W |
|---|---|---|
| `rent2b_bookings_reviews_create` | Bewertung für eine abgeschlossene Buchung anlegen | W |
| `rent2b_items_reviews_list` | Bewertungen zu einem Artikel abrufen | R |

---

## Verfügbarkeit & Kalender

| Tool | Was | R/W |
|---|---|---|
| `rent2b_rooms_availability` | Verfügbarkeitskalender eines Raums | R |
| `rent2b_bookings_rooms_availability_bulk_create` | Verfügbarkeit für mehrere Räume auf einmal | R |
| `rent2b_items_availability` | Verfügbarkeitskalender eines Artikels | R |
| `rent2b_bookings_items_availability_bulk_create` | Tagesgenaue Verfügbarkeit für mehrere Artikel auf einmal | R |
| `rent2b_locations_items_availability_list` | Verfügbarkeitskalender eines Artikels an einem Standort | R |
| `rent2b_locations_items_availability_generate_create` | Verfügbarkeit für einen Zeitraum generieren | W |
| `rent2b_locations_items_availability_pricing_update` | Preis für einen Zeitraum überschreiben | W |
| `rent2b_locations_items_availability_block_create` | Bestimmte Tage sperren (Kalender-Blockierung) | W |
| `rent2b_locations_items_availability_unblock_create` | Sperrung bestimmter Tage aufheben | W |

### Time-Slots (stundenweise Vermietung)

| Tool | Was | R/W |
|---|---|---|
| `rent2b_timeslots_create` | Zeitfenster für einen Standort anlegen | W |
| `rent2b_timeslots_list` | Zeitfenster eines Standorts auflisten | R |
| `rent2b_time_slots_day_list` | Alle Zeitfenster eines Wochentags | R |
| `rent2b_time_slots_list` | Einzelnes Zeitfenster abrufen | R |
| `rent2b_timeslots_update` | Zeitfenster ändern | W |
| `rent2b_timeslots_delete` | Zeitfenster löschen | W |
| `rent2b_timeslots_create_weekly` | Komplettes Wochenschema für einen Standort anlegen | W |

---

## Preise (Pricing) — inkl. Staffelpreise

| Tool | Was | R/W |
|---|---|---|
| `rent2b_pricing_organization_rules_create` | Org-weite Preisregel anlegen (Datum/Wochentag/Zeitraum) | W |
| `rent2b_pricing_organization_rules_list` | Org-weite Preisregeln auflisten | R |
| `rent2b_pricing_organization_rules_list_2` | Einzelne Org-Preisregel abrufen | R |
| `rent2b_pricing_organization_rules_update` | Org-Preisregel ändern | W |
| `rent2b_pricing_organization_rules_delete` | Org-Preisregel löschen | W |
| `rent2b_pricing_organization_rules_list_3` | Alle Preisregeln der Organisation (Räume + Artikel) gemeinsam auflisten | R |
| `rent2b_pricing_rooms_rules_create` | Preisregel für einen Raum anlegen | W |
| `rent2b_pricing_rooms_rules_list` | Preisregeln eines Raums auflisten | R |
| `rent2b_pricing_rooms_rules_list_2` | Einzelne Raum-Preisregel abrufen | R |
| `rent2b_pricing_rooms_rules_update` | Raum-Preisregel ändern | W |
| `rent2b_pricing_rooms_rules_delete` | Raum-Preisregel löschen | W |
| `rent2b_pricing_items_rules_create` | Preisregel für einen Artikel anlegen (auch time_of_day) | W |
| `rent2b_pricing_items_rules_list` | Preisregeln eines Artikels auflisten | R |
| `rent2b_pricing_items_rules_list_2` | Einzelne Artikel-Preisregel abrufen | R |
| `rent2b_pricing_items_rules_update` | Artikel-Preisregel ändern | W |
| `rent2b_pricing_items_rules_delete` | Artikel-Preisregel löschen | W |
| `rent2b_rooms_pricing_rules_list` | Verfügbare Preisregel-Vorlagen einer Organisation | R |

### Staffelpreise / Langzeitrabatte (NEU — 404 bis zum nächsten Deploy live)

| Tool | Was | R/W |
|---|---|---|
| `rent2b_duration_discounts_list` | Rabattstufen auflisten; mit `item_id`/`room_id` zusätzlich `effective_tiers` (die tatsächlich greifenden Stufen: eigene aktive Stufen oder Org-Fallback) | R |
| `rent2b_duration_discounts_create` | Neue Rabattstufe anlegen (`min_duration`, `discount_percent`, optional `item_id`/`room_id`; beides leer = org-weit) | W |
| `rent2b_duration_discounts_update` | Rabattstufe ändern | W |
| `rent2b_duration_discounts_delete` | Rabattstufe löschen | W |

---

## Artikel & Räume

### Räume (Rooms)

| Tool | Was | R/W |
|---|---|---|
| `rent2b_rooms_create` | Neuen Raum anlegen | W |
| `rent2b_rooms_list` | Räume der Organisation auflisten (paginiert, Suche) | R |
| `rent2b_rooms_organization_list` | Räume einer Organisation (mit Paginierung/Suche) | R |
| `rent2b_rooms_location_list` | Räume eines Standorts | R |
| `rent2b_rooms_get` | Raumdetails abrufen | R |
| `rent2b_rooms_update` | Raum aktualisieren | W |
| `rent2b_rooms_delete` | Raum löschen | W |
| `rent2b_rooms_images_list` | Bilder eines Raums auflisten | R |
| `rent2b_rooms_images_delete` | Raumbild löschen | W |
| `rent2b_rooms_images_primary_update` | Primärbild eines Raums setzen | W |
| `rent2b_rooms_buffer_times_list` | Pufferzeiten (Vor-/Nachbereitung) eines Raums abrufen | R |
| `rent2b_rooms_buffer_times_update` | Pufferzeiten eines Raums konfigurieren | W |
| `rent2b_rooms_test_list` | Datenbankverbindung testen | R |

### Artikel (Items)

| Tool | Was | R/W |
|---|---|---|
| `rent2b_items_create` | Neuen Artikel anlegen | W |
| `rent2b_items_list` | Artikel der Organisation auflisten (Suche, Kategorie, Standort, Umkreis) | R |
| `rent2b_items_organization_list` | Artikel einer Organisation (Paginierung/Suche/Umkreis) | R |
| `rent2b_items_location_list` | Artikel eines Standorts | R |
| `rent2b_items_get` | Artikeldetails abrufen | R |
| `rent2b_items_update` | Artikel aktualisieren | W |
| `rent2b_items_delete` | Artikel löschen | W |
| `rent2b_items_quantity_update` | Verfügbare Menge eines Artikels ändern | W |
| `rent2b_items_images_create` | Bilder für einen Artikel hochladen | W |
| `rent2b_items_images_list` | Bilder eines Artikels auflisten | R |
| `rent2b_items_images_delete` | Artikelbild löschen | W |
| `rent2b_items_images_primary_update` | Primärbild eines Artikels setzen | W |
| `rent2b_items_debug_images_list` | Debug-Endpunkt für Bild-Abruf | R |
| `rent2b_items_buffer_times_list` | Pufferzeiten eines Artikels abrufen | R |
| `rent2b_items_buffer_times_update` | Pufferzeiten eines Artikels konfigurieren | W |
| `rent2b_items_analyze_image_create` | KI-Bildanalyse: liefert 3 Artikel-Vorschläge (Name, Beschreibung, Kategorie, Attribute, Preis) | W |
| `rent2b_items_favorites_create` | Favoritenstatus für einen Artikel umschalten | W |
| `rent2b_items_favorites_delete` | Artikel aus Favoriten entfernen | W |
| `rent2b_items_favorite_status_list` | Favoritenstatus eines Artikels für den aktuellen User prüfen | R |

### Kategorien & Attribute

| Tool | Was | R/W |
|---|---|---|
| `rent2b_categories_create` | Neue Kategorie anlegen (Admin) | W |
| `rent2b_categories_list` | Alle Artikel-Kategorien auflisten | R |
| `rent2b_categories_get` | Einzelne Kategorie abrufen | R |
| `rent2b_categories_update` | Kategorie ändern (Admin) | W |
| `rent2b_categories_delete` | Kategorie löschen (Admin) | W |
| `rent2b_categories_attributes_create` | Attribut für eine Kategorie anlegen (Admin) | W |
| `rent2b_categories_attributes_list` | Attribute einer Kategorie auflisten | R |
| `rent2b_categories_attributes_update` | Attribut ändern (Admin) | W |
| `rent2b_categories_attributes_delete` | Attribut löschen (Admin) | W |
| `rent2b_categories_items_attributes_list` | Attribute eines Artikels abrufen | R |
| `rent2b_categories_items_attributes_create` | Attribute für einen Artikel setzen | W |
| `rent2b_categories_items_attributes_update` | Einzelnes Artikel-Attribut ändern | W |
| `rent2b_categories_items_attributes_delete` | Einzelnes Artikel-Attribut löschen | W |

---

## Gäste (Guests)

| Tool | Was | R/W |
|---|---|---|
| `rent2b_guests_create` | Neuen Gast anlegen | W |
| `rent2b_guests_list` | Gäste auflisten (Suche, Paginierung) | R |
| `rent2b_guests_get` | Gast abrufen | R |
| `rent2b_guests_update` | Gastdaten ändern | W |
| `rent2b_guests_delete` | Gast löschen | W |

---

## Statistiken

| Tool | Was | R/W |
|---|---|---|
| `rent2b_statistics_overview` | Vollständige Org-Statistik: Buchungen, Umsatz, Auslastung | R |
| `rent2b_statistics_summary` | Kurze Zusammenfassung der Org-Statistik | R |
| `rent2b_statistics_revenue` | Detaillierte Umsatzstatistik | R |
| `rent2b_statistics_utilization` | Auslastungsstatistik | R |
| `rent2b_statistics_location_list` | Detaillierte Analytics für einen Standort (Buchungen, Umsatz, Auslastung, Trends) | R |
| `rent2b_statistics_location_summary_list` | Kennzahlen-Übersicht eines Standorts (Dashboard) | R |
| `rent2b_statistics_location_revenue_list` | Umsatzaufschlüsselung + Trends eines Standorts | R |
| `rent2b_statistics_location_utilization_list` | Auslastungsraten + Buchungsmuster eines Standorts | R |

---

## Standorte (Locations)

| Tool | Was | R/W |
|---|---|---|
| `rent2b_locations_address_search_create` | Adresssuche (Google Places Autocomplete) | R |
| `rent2b_locations_place_details_create` | Ortsdetails inkl. Koordinaten abrufen | R |
| `rent2b_locations_create` | Neuen Standort anlegen | W |
| `rent2b_locations_list` | Standorte der Organisation auflisten | R |
| `rent2b_locations_organization_list` | Alle Standorte einer Organisation | R |
| `rent2b_locations_get` | Standortdetails abrufen | R |
| `rent2b_locations_update` | Standort aktualisieren | W |
| `rent2b_locations_delete` | Standort löschen | W |
| `rent2b_locations_set_main_update` | Standort als Haupt-/Standardstandort setzen | W |

---

## Kampagnen-Links

| Tool | Was | R/W |
|---|---|---|
| `rent2b_campaign_links_list` | Tracking-Links für die Buchungsseite auflisten | R |
| `rent2b_campaign_links_create` | Kampagnen-Tracking-Link anlegen (filtered/item/room) | W |
| `rent2b_campaign_links_get` | Kampagnen-Link abrufen | R |
| `rent2b_campaign_links_update` | Kampagnen-Link ändern | W |
| `rent2b_campaign_links_delete` | Kampagnen-Link löschen | W |
| `rent2b_campaign_links_analytics` | Klicks/Conversions eines Kampagnen-Links abrufen | R |

---

## Branding & Website-Content

| Tool | Was | R/W |
|---|---|---|
| `rent2b_branding_get` | Branding (Farben, Texte) abrufen | R |
| `rent2b_branding_update` | Branding aktualisieren | W |
| `rent2b_branding_logo_delete` | Logo entfernen | W |
| `rent2b_branding_background_delete` | Hero-Hintergrundbild entfernen | W |
| `rent2b_website_content_get` | Öffentliche Buchungsseiten-Inhalte (Über uns, Impressum, Datenschutz, AGB, …) abrufen | R |
| `rent2b_website_content_update` | Öffentliche Buchungsseiten-Inhalte aktualisieren | W |

---

## Einstellungen / Profil / Abo

| Tool | Was | R/W |
|---|---|---|
| `rent2b_settings_get` | Organisations- und Nutzereinstellungen abrufen | R |
| `rent2b_settings_organization_update` | Organisationseinstellungen aktualisieren (Name, Vermietungsmodus, Homepage-Konfiguration, …) | W |
| `rent2b_settings_user_update` | Nutzereinstellungen aktualisieren | W |
| `rent2b_profile_get` | Eigentümer-Profil abrufen | R |
| `rent2b_profile_update` | Eigentümer-Profil aktualisieren | W |
| `rent2b_profile_image_delete` | Profilbild löschen | W |
| `rent2b_profile_referred_by_create` | Empfehlungscode setzen (nur einmalig möglich) | W |
| `rent2b_settings_subscription_list` | Aktuellen Abo-Plan/Status abrufen | R |
| `rent2b_settings_subscription_checkout_create` | Stripe-Checkout-Session für Plan-Upgrade erstellen | W |
| `rent2b_settings_subscription_cancel_create` | Abo zum Ende der Laufzeit kündigen | W |
| `rent2b_settings_subscription_history_list` | Abo-Zahlungsverlauf abrufen | R |
