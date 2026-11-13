# Washie – site e-commerce de couches lavables hybrides

Site statique généré par `build.py` à partir du catalogue (`catalog.py`) et des réglages (`config.py`).
Le site publié est dans `docs/` (servi par GitHub Pages).

## Mettre à jour le site
```bash
pip install --break-system-packages playwright  # facultatif, pour les tests
python3 build.py            # régénère docs/ (images incluses)
python3 build.py --skip-images   # plus rapide si seules les pages changent
git add -A && git commit -m "maj" && git push
```
Pré-requis images : `rsvg-convert` (librsvg).

## Réglages (`config.py`)
| Clé | Rôle |
|---|---|
| `SITE_URL` | URL publique (canonicals, flux, sitemap) |
| `GA4_ID` | Identifiant de mesure GA4 `G-XXXXXXX` |
| `GOOGLE_ADS_ID` | `AW-XXXXXXX` (optionnel) |
| `LEAD_FORM_ENDPOINT` | URL Formspree/Brevo/Tally… pour la liste d'attente (formulaires masqués si vide) |
| `ORDERS_OPEN` | `False` = pré-lancement : « Commander » affiche un message, flux en `preorder` |
| `LAUNCH_DATE` | Date d'ouverture (flux `availability_date`) |
| `LEGAL` | Mentions légales (obligatoires) |

## Flux produits
- `docs/feeds/google-merchant.xml` – RSS 2.0 Google Merchant Center
- `docs/feeds/products.csv` – Merchant Center / Meta Catalog
- `docs/feeds/products.json`

Une ligne par variante (couleur × taille), regroupées par `item_group_id`.
`custom_label_0..4` : gamme, tranche de prix, statut (bestseller, nouveauté, kit…), marge, usage.

## Plan de marquage GA4

### Consentement
Consent Mode v2, tout refusé par défaut, bannière Accepter / Refuser (lien « Gérer les cookies » en pied de page).
Sans consentement, GA4 envoie des pings sans cookie (modélisation).

### Attribution (paramètres envoyés sur chaque événement)
| Paramètre | Valeurs |
|---|---|
| `traffic_type` | `paid`, `organic_search`, `ai_assistant`, `organic_social`, `email`, `referral`, `direct` |
| `traffic_source` | google, bing, meta, chatgpt.com, perplexity.ai, google.fr… |
| `landing_page` | page d'entrée de la session |
| `page_type` / `content_group` | home, plp, pdp, guide, faq, cart, about, info |
| user property `first_traffic_type`, `first_traffic_source` | premier contact (persistant) |

Règles : présence de `gclid/gbraid/wbraid/msclkid/fbclid+utm_medium/ttclid…` ou `utm_medium` cpc/ppc/paid*/display/shopping/pmax ⇒ **paid** ;
référent ou `utm_source` d'assistant IA (chatgpt.com, perplexity.ai, claude.ai, gemini, copilot, mistral…) ⇒ **ai_assistant** ;
référent moteur de recherche sans UTM ⇒ **organic_search**.

### Événements
| Événement | Déclencheur |
|---|---|
| `page_view` | automatique |
| `view_item_list` / `select_item` | listes produits (accueil, boutique, recommandations) |
| `view_item` | fiche produit |
| `select_variant` | choix couleur / taille |
| `size_guide_open` | ouverture du guide des tailles sur fiche |
| `view_product_image` | clic vignette |
| `add_to_cart` / `remove_from_cart` / `view_cart` | panier |
| `begin_checkout` | clic « Commander » |
| `prelaunch_notice` | message de pré-lancement affiché (demande d'achat réelle) |
| `generate_lead` | inscription liste d'attente / newsletter |
| `filter_products` | filtre boutique |
| `cta_click` | boutons marqués `data-cta` |
| `faq_open` | ouverture d'une question |
| `guide_read` | lecture des guides à 25/50/75/100 % |
| `consent_choice` | choix cookies |

### À faire dans GA4 (Admin)
1. Créer la propriété + flux Web, copier `G-…` dans `config.py`, rebuild, push.
2. Définitions personnalisées → Dimensions (portée Événement) : `traffic_type`, `traffic_source`, `landing_page`, `page_type`, `cta_name`, `question`, `filter_value`, `variant_type`, `percent_scrolled`.
   Dimensions (portée Utilisateur) : `first_traffic_type`, `first_traffic_source`.
3. Événements clés : `add_to_cart`, `begin_checkout`, `prelaunch_notice`, `generate_lead`.
4. Associer Google Ads + Search Console ; activer le marquage automatique (gclid) dans Google Ads.
5. Explorations : entonnoir `view_item → add_to_cart → view_cart → begin_checkout` ventilé par `traffic_type`.

Tester : ajouter `?debug=1` à l'URL puis GA4 → Admin → DebugView.
