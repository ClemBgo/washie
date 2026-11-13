# -*- coding: utf-8 -*-
"""Réglages du site Washie. Modifiez ici puis relancez `python3 build.py`."""

# URL publique du site (sans / final). GitHub Pages : https://<compte>.github.io/<depot>
SITE_URL = "https://clembgo.github.io/washie"

# Google Analytics 4 : identifiant de mesure (ex. "G-ABC123XYZ"). Vide = balise non chargée.
GA4_ID = ""
# Google Ads (optionnel) : identifiant de conversion (ex. "AW-123456789") pour le remarketing / conversions.
GOOGLE_ADS_ID = ""

# Formulaire de liste d'attente / newsletter (optionnel) : URL d'un service type Formspree, Brevo, Tally…
# Vide = les formulaires e-mail ne sont pas affichés.
LEAD_FORM_ENDPOINT = ""

# Les commandes en ligne sont-elles ouvertes ? False = le bouton « Commander » affiche un message de pré-lancement.
ORDERS_OPEN = False
# Date d'ouverture prévue des commandes (utilisée dans le flux pour les produits en précommande)
LAUNCH_DATE = "2027-01-15"

FREE_SHIPPING_FROM = 49.0
SHIPPING_PRICE = 4.90

# Mentions légales (obligatoires en France pour un site public)
LEGAL = {
    "company": "[Raison sociale à compléter]",
    "address": "[Adresse du siège à compléter]",
    "siren": "[SIREN à compléter]",
    "vat": "[N° TVA intracommunautaire à compléter]",
    "director": "[Directeur·rice de la publication à compléter]",
    "email": "[e-mail de contact à compléter]",
    "host": "GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis",
}
