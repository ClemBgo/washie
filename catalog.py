# -*- coding: utf-8 -*-
"""Catalogue Washie – couches lavables hybrides.
Architecture de gamme inspirée des couches hybrides du marché (type Hamac) :
couche à poche étanche intégrée (Classic), culotte + poche étanche détachable
(Switch), absorbants lavables jour / nuit / coton, boosters, absorbants
jetables pour les déplacements, voiles, kits, bain, apprentissage, entretien.
Noms, textes et visuels propres à Washie.
"""

BRAND = "Washie"

COLORS = {
    "Sable": ("#E3D3B8", "#CDB894"),
    "Sauge": ("#9DB59A", "#7E9A7B"),
    "Terracotta": ("#D98B6A", "#C0714F"),
    "Ciel": ("#9CC0DD", "#7BA6C9"),
    "Moutarde": ("#E0B24F", "#C79A39"),
    "Rose poudré": ("#E8B7B0", "#D79C94"),
    "Nuit": ("#3F4A68", "#2E3752"),
    "Écru": ("#F3EEE3", "#DCD3C2"),
    "Blanc": ("#F7F5F0", "#E2DDD2"),
}

# Guide des tailles Washie
SIZE_GUIDE = [
    ("XS", "2–4 kg", "Naissance / prématuré"),
    ("S", "4–8 kg", "≈ 0 à 6 mois"),
    ("M", "6–12 kg", "≈ 4 à 15 mois"),
    ("L", "9–17 kg", "≈ 12 mois à la propreté"),
    ("XL", "14–21 kg", "Grands gabarits et nuit"),
]
SIZE_W = {s: w for s, w, _ in SIZE_GUIDE}
ABS_SIZE = {"T1": "pour couches XS et S", "T2": "pour couches M et L", "T3": "pour couches XL"}

PRODUCTS = [
    {
        "id": "WS-CLASSIC", "slug": "couche-lavable-hybride-washie-classic",
        "name": "Couche lavable hybride Washie Classic",
        "range": "Couches", "type": "Couche hybride", "shape": "classic",
        "product_type": "Couches lavables > Couches hybrides > Classic",
        "gcat": "Baby & Toddler > Diapering > Diapers",
        "price": 32.00,
        "sizes": ["XS", "S", "M", "L", "XL"], "size_kind": "kg",
        "size": "XS 2–4 kg · S 4–8 kg · M 6–12 kg · L 9–17 kg · XL 14–21 kg",
        "age_group": "infant", "material": "Microfibre polyamide / polyuréthane",
        "colors": ["Sable", "Sauge", "Terracotta", "Ciel"],
        "short": "La couche lavable aussi simple qu'une jetable : une culotte douce avec poche étanche intégrée, on glisse l'absorbant, on ferme, c'est prêt.",
        "description": (
            "Washie Classic est une couche hybride : une culotte en microfibre douce et respirante, doublée d'une poche "
            "étanche en polyuréthane qui retient l'humidité et les selles. On glisse un absorbant Washie (lavable) ou un "
            "absorbant compostable (en déplacement), on pose un voile, on ferme les rabats : c'est prêt. Au change, on retire "
            "l'absorbant ; si la poche n'est pas souillée, on peut remettre un absorbant propre et réutiliser la couche. "
            "Coupe fine en 5 tailles pour un ajustement parfait à chaque étape, sans effet « grosses fesses » sous les "
            "vêtements. Absorbant vendu séparément."
        ),
        "attrs": {
            "Système": "Hybride – culotte + poche étanche intégrée + absorbant",
            "Tailles": "XS 2–4 kg · S 4–8 kg · M 6–12 kg · L 9–17 kg · XL 14–21 kg",
            "Fermeture": "Rabats auto-agrippants doux",
            "Extérieur": "Microfibre polyamide respirante",
            "Poche": "Polyuréthane respirant et imperméable",
            "Absorbant": "Non inclus – absorbants Washie T1, T2 ou T3",
            "Usage": "Jour et nuit selon absorbant",
            "Lavage": "40 °C, rabats fermés, séchage à l'air libre",
        },
        "highlights": ["Aussi simple qu'une jetable", "Poche étanche anti-fuites", "Coupe fine en 5 tailles", "Absorbant lavable ou compostable"],
        "labels": ["bestseller", "marge-moyenne", "jour-nuit"],
        "faq": [
            ("Combien de couches Washie Classic prévoir ?", "Pour un lavage tous les 2 jours : 6 à 7 couches et 12 à 14 absorbants T1 en tailles XS ou S, 5 à 6 couches et 10 à 12 absorbants T2 en M, 4 à 5 couches et 10 à 12 absorbants T2 en L."),
            ("Quelle taille choisir ?", "Fiez-vous au poids : XS 2–4 kg, S 4–8 kg, M 6–12 kg, L 9–17 kg, XL 14–21 kg. Entre deux tailles, prenez la plus grande : votre enfant la portera plus longtemps."),
        ],
    },
    {
        "id": "WS-SWITCH", "slug": "culotte-lavable-washie-switch",
        "name": "Culotte lavable Washie Switch",
        "range": "Couches", "type": "Culotte Switch", "shape": "switch",
        "product_type": "Couches lavables > Système Switch > Culotte",
        "gcat": "Baby & Toddler > Diapering > Diapers",
        "price": 18.00,
        "sizes": ["S", "M", "L", "XL"], "size_kind": "kg",
        "size": "S 4–8 kg · M 6–12 kg · L 9–17 kg · XL 14–21 kg",
        "age_group": "infant", "material": "Microfibre polyamide",
        "colors": ["Sable", "Sauge", "Moutarde"],
        "short": "Une culotte pour 2 à 3 changes : seule la poche étanche détachable se remplace. Moins de linge, séchage express.",
        "description": (
            "Le système Washie Switch sépare le propre du sale en un geste. La culotte reçoit une poche étanche détachable, "
            "fixée par deux languettes glissées dans des passants. À chaque change, on retire uniquement la poche souillée et "
            "on clipse une poche propre : la culotte reste en place pour 2 à 3 changes. Résultat : moins de culottes à "
            "acheter, moins de linge et un séchage très rapide. Poches étanches et absorbants vendus séparément."
        ),
        "attrs": {
            "Système": "Culotte + poche étanche détachable + absorbant",
            "Tailles": "S 4–8 kg · M 6–12 kg · L 9–17 kg · XL 14–21 kg",
            "Fermeture": "Rabats auto-agrippants doux",
            "Matière": "Microfibre polyamide respirante",
            "Compatibilité": "Poches étanches Washie Switch de même taille",
            "Équipement conseillé": "S : 3–4 culottes, 6–7 poches · M/L : 2–3 culottes, 4–6 poches",
            "Lavage": "40 °C, séchage à l'air libre",
        },
        "highlights": ["1 culotte pour 2 à 3 changes", "Poche détachable en un geste", "Moins de linge à laver"],
        "labels": ["coeur-de-gamme", "marge-haute", "jour"],
        "faq": [
            ("Comment retirer la poche Switch ?", "Soulevez délicatement chaque languette hors de son passant, d'un côté puis de l'autre, sans tirer sur la poche. Sur les tailles M à XL, placez le côté le plus large de la poche à l'arrière."),
        ],
    },
    {
        "id": "WS-POCHE", "slug": "poches-etanches-washie-switch-lot-de-2",
        "name": "Poches étanches Washie Switch – lot de 2",
        "range": "Couches", "type": "Poche Switch", "shape": "pocket",
        "product_type": "Couches lavables > Système Switch > Poches étanches",
        "gcat": "Baby & Toddler > Diapering > Diapers",
        "price": 30.00,
        "sizes": ["S", "M", "L", "XL"], "size_kind": "kg",
        "size": "S 4–8 kg · M 6–12 kg · L 9–17 kg · XL 14–21 kg",
        "age_group": "infant", "material": "Polyuréthane",
        "colors": ["Blanc"],
        "short": "Les poches étanches détachables à clipser dans la culotte Switch. On remplace la poche, on garde la culotte.",
        "description": (
            "Poches étanches en polyuréthane respirant, avec collerettes élastiquées qui bloquent les fuites de selles et "
            "deux languettes de fixation pour la culotte Washie Switch. On y glisse l'absorbant et un voile. Sur les tailles "
            "M, L et XL, la poche est asymétrique pour mieux couvrir l'arrière. Vendues par 2."
        ),
        "attrs": {
            "Type": "Poche étanche détachable",
            "Contenu": "Lot de 2",
            "Tailles": "S · M · L · XL (identique à la culotte)",
            "Matière": "Polyuréthane respirant et imperméable",
            "Particularité": "Collerettes anti-fuites, forme asymétrique en M–XL",
            "Lavage": "40 °C",
        },
        "highlights": ["Collerettes anti-fuites", "Se clipse en 2 secondes", "Lot de 2"],
        "labels": ["coeur-de-gamme", "marge-haute", "jour"],
        "faq": [],
    },
    {
        "id": "WS-ABS-JOUR", "slug": "absorbants-lavables-jour-microfibre-lot-de-2",
        "name": "Absorbants lavables Jour microfibre – lot de 2",
        "range": "Absorbants", "type": "Absorbant jour", "shape": "insert",
        "product_type": "Absorbants > Absorbants lavables > Jour",
        "gcat": "Baby & Toddler > Diapering > Diaper Liners",
        "price": 14.50,
        "sizes": ["T1", "T2", "T3"], "size_kind": "abs",
        "size": "T1 (couches XS–S) · T2 (M–L) · T3 (XL)",
        "age_group": "infant", "material": "Microfibre",
        "colors": ["Sable"],
        "short": "L'absorbant du quotidien : 3 épaisseurs de microfibre qui captent vite, sèchent vite. Pour 3 à 4 h de journée.",
        "description": (
            "Absorbant lavable en microfibre 3 épaisseurs, avec une face douce côté peau. Il capte rapidement le liquide et "
            "sèche très vite entre deux lavages. Format profilé qui se glisse sans surépaisseur dans la poche des couches "
            "Washie Classic et Switch. Taille T1 pour les couches XS et S, T2 pour les M et L, T3 pour les XL. Lot de 2."
        ),
        "attrs": {
            "Type": "Absorbant lavable jour",
            "Matière": "Microfibre, 3 épaisseurs",
            "Tailles": "T1 (XS–S) · T2 (M–L) · T3 (XL)",
            "Contenu": "Lot de 2",
            "Autonomie": "3 à 4 h",
            "Lavage": "60 °C, sèche-linge basse température possible",
        },
        "highlights": ["Séchage très rapide", "Sans surépaisseur", "3 à 4 h d'autonomie"],
        "labels": ["consommable", "marge-haute", "jour"],
        "faq": [],
    },
    {
        "id": "WS-ABS-NUIT", "slug": "absorbant-lavable-nuit-sieste",
        "name": "Absorbant lavable Nuit & sieste",
        "range": "Absorbants", "type": "Absorbant nuit", "shape": "insert_night",
        "product_type": "Absorbants > Absorbants lavables > Nuit",
        "gcat": "Baby & Toddler > Diapering > Diaper Liners",
        "price": 10.90,
        "sizes": ["T1", "T2", "T3"], "size_kind": "abs",
        "size": "T1 (couches XS–S) · T2 (M–L) · T3 (XL)",
        "age_group": "infant", "material": "Microfibre",
        "colors": ["Nuit"],
        "short": "4 épaisseurs pour les longues siestes et la nuit : 6 à 12 h d'absorption selon les bébés.",
        "description": (
            "Une épaisseur de plus que l'absorbant Jour pour tenir la nuit et les longues siestes : 6 à 12 heures "
            "d'absorption selon les bébés. Pliez-le en deux dans la largeur, puis encore en deux, avant de le glisser dans "
            "la poche, face douce côté peau. Sa forme évite les bourrelets sur les bords de la poche. Ajoutez un booster pour "
            "les gros dormeurs. Vendu à l'unité."
        ),
        "attrs": {
            "Type": "Absorbant lavable nuit",
            "Matière": "Microfibre, 4 épaisseurs",
            "Tailles": "T1 (XS–S) · T2 (M–L) · T3 (XL)",
            "Contenu": "1 absorbant",
            "Autonomie": "6 à 12 h",
            "Lavage": "60 °C",
        },
        "highlights": ["6 à 12 h d'absorption", "Forme anti-bourrelets", "Compatible booster"],
        "labels": ["nouveaute", "marge-haute", "nuit"],
        "faq": [],
    },
    {
        "id": "WS-ABS-COTON", "slug": "absorbants-lavables-coton-bio-lot-de-2",
        "name": "Absorbants lavables coton bio – lot de 2",
        "range": "Absorbants", "type": "Absorbant coton", "shape": "insert",
        "product_type": "Absorbants > Absorbants lavables > Coton bio",
        "gcat": "Baby & Toddler > Diapering > Diaper Liners",
        "price": 16.90,
        "sizes": ["T1", "T2", "T3"], "size_kind": "abs",
        "size": "T1 (couches XS–S) · T2 (M–L) · T3 (XL)",
        "age_group": "infant", "material": "Coton biologique",
        "colors": ["Écru"],
        "short": "Version fibre naturelle : coton biologique non blanchi, doux pour les peaux sensibles.",
        "description": (
            "Pour les parents qui préfèrent une fibre naturelle au contact de la peau : absorbants en coton biologique non "
            "blanchi, 4 épaisseurs. Le coton absorbe un peu plus lentement que la microfibre mais ne relargue pas "
            "l'humidité sous la pression. Prélavez 3 fois avant la première utilisation. Lot de 2."
        ),
        "attrs": {
            "Type": "Absorbant lavable",
            "Matière": "Coton biologique non blanchi, 4 épaisseurs",
            "Tailles": "T1 (XS–S) · T2 (M–L) · T3 (XL)",
            "Contenu": "Lot de 2",
            "Autonomie": "3 à 4 h",
            "Lavage": "60 °C – 3 prélavages",
        },
        "highlights": ["Coton bio non blanchi", "Peaux sensibles", "Ne relargue pas l'humidité"],
        "labels": ["premium", "marge-moyenne", "jour"],
        "faq": [],
    },
    {
        "id": "WS-BOOSTER", "slug": "boosters-microfibre-duo",
        "name": "Boosters 2 épaisseurs – duo",
        "range": "Absorbants", "type": "Booster", "shape": "insert_thin",
        "product_type": "Absorbants > Boosters",
        "gcat": "Baby & Toddler > Diapering > Diaper Liners",
        "price": 8.90,
        "sizes": [], "size": "Universel (28 × 10 cm)",
        "age_group": "infant", "material": "Microfibre",
        "colors": ["Sable"],
        "short": "Un supplément fin à glisser sous l'absorbant pour gagner 1 à 2 h, la nuit ou chez la nounou.",
        "description": (
            "Booster fin en microfibre 2 épaisseurs, à placer sous l'absorbant principal pour gagner 1 à 2 heures "
            "d'autonomie. Idéal pour la nuit, les longs trajets ou les journées chez l'assistante maternelle. Compatible "
            "toutes tailles. Lot de 2."
        ),
        "attrs": {"Type": "Booster", "Matière": "Microfibre, 2 épaisseurs", "Dimensions": "28 × 10 cm", "Contenu": "Lot de 2", "Lavage": "60 °C"},
        "highlights": ["+1 à 2 h d'autonomie", "Fin et discret"],
        "labels": ["accessoire", "marge-haute", "nuit"],
        "faq": [],
    },
    {
        "id": "WS-JETABLE-20", "slug": "absorbants-jetables-compostables-x20",
        "name": "Absorbants jetables compostables – recharge de 20",
        "range": "Absorbants", "type": "Absorbant jetable", "shape": "disposable",
        "product_type": "Absorbants > Absorbants jetables",
        "gcat": "Baby & Toddler > Diapering > Diaper Liners",
        "price": 9.90,
        "sizes": ["T1", "T2"], "size_kind": "abs",
        "size": "T1 (couches XS–S) · T2 (M–L–XL)",
        "age_group": "infant", "material": "Pâte de cellulose",
        "colors": ["Blanc"],
        "short": "Le mode voyage des couches hybrides : un absorbant jetable dans la poche Washie, rien à rapporter à la maison.",
        "description": (
            "Les couches Washie sont hybrides : en vacances, à la crèche ou en déplacement, remplacez l'absorbant lavable par "
            "un absorbant jetable. Il se glisse dans la poche étanche comme un absorbant classique et se jette après usage. "
            "Fabriqué à base de pâte de cellulose, sans parfum ni lotion. Recharge de 20."
        ),
        "attrs": {"Type": "Absorbant jetable", "Matière": "Pâte de cellulose, sans parfum ni lotion", "Tailles": "T1 (XS–S) · T2 (M–XL)", "Contenu": "20 absorbants", "Fin de vie": "Compostage domestique hors selles"},
        "highlights": ["Idéal voyage et crèche", "Sans parfum ni lotion"],
        "labels": ["consommable", "marge-haute", "voyage"],
        "faq": [],
    },
    {
        "id": "WS-VOILES-100", "slug": "voiles-de-protection-jetables-rouleau-100",
        "name": "Voiles de protection jetables – rouleau de 100",
        "range": "Accessoires", "type": "Voiles", "shape": "roll",
        "product_type": "Accessoires > Voiles de protection",
        "gcat": "Baby & Toddler > Diapering > Diaper Liners",
        "price": 8.90,
        "sizes": [], "size": "100 voiles 30 × 20 cm",
        "age_group": "infant", "material": "Viscose",
        "colors": ["Écru"],
        "short": "Posé sur l'absorbant, le voile retient les selles : on le jette, la couche reste propre.",
        "description": (
            "Le voile se pose sur l'absorbant, à l'intérieur de la poche. Il laisse passer les liquides et retient les selles : "
            "au change, on le retire et on le jette. En viscose, sans chlore. Rouleau de 100 voiles de 30 × 20 cm, compatible "
            "avec toutes les couches lavables."
        ),
        "attrs": {"Type": "Voile de protection jetable", "Contenu": "Rouleau de 100", "Dimensions": "30 × 20 cm", "Matière": "Viscose, sans chlore"},
        "highlights": ["Change plus propre", "Compatible toutes couches"],
        "labels": ["consommable", "marge-haute", "jour-nuit"],
        "faq": [],
    },
    {
        "id": "WS-KIT-CLASSIC", "slug": "kit-essai-couche-lavable-washie-classic",
        "name": "Kit d'essai Washie Classic",
        "range": "Kits", "type": "Kit d'essai", "shape": "kit_small",
        "product_type": "Kits > Kit d'essai",
        "gcat": "Baby & Toddler > Diapering > Diaper Kits",
        "price": 49.00, "sale_price": 39.00,
        "sizes": ["S", "M", "L"], "size_kind": "kg",
        "size": "S 4–8 kg · M 6–12 kg · L 9–17 kg",
        "age_group": "infant", "material": "Microfibre polyamide / polyuréthane",
        "colors": ["Sable"],
        "short": "Tout pour tester la couche lavable hybride : 1 couche Classic, 2 absorbants Jour, 1 absorbant jetable et 10 voiles.",
        "description": (
            "Le meilleur moyen de se lancer sans investir : 1 couche Washie Classic, 2 absorbants lavables Jour, "
            "1 absorbant jetable pour tester le mode voyage et 10 voiles de protection. Choisissez la taille selon le poids "
            "de votre bébé (S 4–8 kg, M 6–12 kg, L 9–17 kg). Une fois convaincu·e, complétez avec un pack d'équipement."
        ),
        "attrs": {"Type": "Kit d'essai", "Contenu": "1 couche Classic, 2 absorbants Jour, 1 absorbant jetable, 10 voiles", "Tailles": "S · M · L", "Valeur des articles": "≈ 48 € achetés séparément"},
        "highlights": ["Tester avant d'investir", "Lavable et mode voyage inclus"],
        "labels": ["kit", "marge-moyenne", "acquisition"],
        "faq": [],
    },
    {
        "id": "WS-KIT-SWITCH", "slug": "kit-essai-washie-switch",
        "name": "Kit d'essai Washie Switch",
        "range": "Kits", "type": "Kit d'essai", "shape": "kit_switch",
        "product_type": "Kits > Kit d'essai",
        "gcat": "Baby & Toddler > Diapering > Diaper Kits",
        "price": 59.00, "sale_price": 49.00,
        "sizes": ["S", "M", "L"], "size_kind": "kg",
        "size": "S 4–8 kg · M 6–12 kg · L 9–17 kg",
        "age_group": "infant", "material": "Microfibre polyamide / polyuréthane",
        "colors": ["Sauge"],
        "short": "Découvrez le système à poche détachable : 1 culotte Switch, 2 poches étanches, 2 absorbants Jour et 10 voiles.",
        "description": (
            "Le kit pour tester le système Switch : 1 culotte, 2 poches étanches détachables, 2 absorbants lavables Jour et "
            "10 voiles. Vous verrez qu'une seule culotte suffit pour plusieurs changes : il suffit de remplacer la poche."
        ),
        "attrs": {"Type": "Kit d'essai", "Contenu": "1 culotte Switch, 2 poches étanches, 2 absorbants Jour, 10 voiles", "Tailles": "S · M · L", "Valeur des articles": "≈ 64 € achetés séparément"},
        "highlights": ["1 culotte, plusieurs changes", "Kit complet prêt à l'emploi"],
        "labels": ["kit", "marge-moyenne", "acquisition"],
        "faq": [],
    },
    {
        "id": "WS-PACK-CLASSIC", "slug": "pack-equipement-couches-lavables-washie-classic",
        "name": "Pack équipement Washie Classic – 6 couches",
        "range": "Kits", "type": "Pack équipement", "shape": "kit_big",
        "product_type": "Kits > Pack équipement",
        "gcat": "Baby & Toddler > Diapering > Diaper Kits",
        "price": 299.00, "sale_price": 259.00,
        "sizes": ["S", "M", "L"], "size_kind": "kg",
        "size": "S 4–8 kg · M 6–12 kg · L 9–17 kg",
        "age_group": "infant", "material": "Microfibre polyamide / polyuréthane",
        "colors": ["Sable"],
        "short": "Le temps plein en une commande : 6 couches Classic, 12 absorbants, 2 absorbants nuit, 100 voiles et un sac imperméable.",
        "description": (
            "Tout l'équipement d'une taille pour passer au lavable à temps plein avec un lavage tous les 2 jours : "
            "6 couches Washie Classic (couleurs assorties), 12 absorbants lavables Jour, 2 absorbants Nuit & sieste, "
            "1 rouleau de 100 voiles et 1 sac imperméable. Livraison offerte."
        ),
        "attrs": {"Type": "Pack équipement temps plein", "Contenu": "6 couches Classic, 12 absorbants Jour, 2 absorbants Nuit, 100 voiles, 1 sac imperméable", "Tailles": "S · M · L", "Valeur des articles": "≈ 330 € achetés séparément"},
        "highlights": ["Temps plein, lavage tous les 2 jours", "Livraison offerte", "Jour et nuit inclus"],
        "labels": ["kit", "marge-haute", "acquisition"],
        "faq": [],
    },
    {
        "id": "WS-BAIN", "slug": "maillot-couche-de-bain-lavable",
        "name": "Maillot-couche de bain lavable",
        "range": "Accessoires", "type": "Couche de bain", "shape": "swim",
        "product_type": "Couches lavables > Couches de bain",
        "gcat": "Baby & Toddler > Diapering > Diapers",
        "price": 19.00,
        "sizes": ["S", "M", "L"], "size_kind": "kg",
        "size": "S 4–9 kg · M 8–13 kg · L 12–17 kg",
        "age_group": "infant", "material": "Polyester recyclé",
        "colors": ["Ciel", "Terracotta"],
        "short": "Maillot-couche réutilisable pour la piscine et la plage, qui retient les selles sans gonfler dans l'eau.",
        "description": (
            "Maillot de bain et couche à la fois : élastiques serrés aux cuisses et à la taille pour retenir les selles dans "
            "l'eau, sans absorbant qui gonflerait. Tissu de maillot extérieur, maille douce intérieure, pressions latérales "
            "pour le retirer facilement même mouillé. Remplace les couches de bain jetables."
        ),
        "attrs": {"Type": "Couche de bain réutilisable", "Tailles": "S 4–9 kg · M 8–13 kg · L 12–17 kg", "Fermeture": "Pressions latérales", "Matière": "Polyester recyclé / élasthanne", "Lavage": "40 °C"},
        "highlights": ["Ne gonfle pas dans l'eau", "Pressions latérales"],
        "labels": ["saisonnier", "marge-haute", "bain"],
        "faq": [],
    },
    {
        "id": "WS-APPR", "slug": "culotte-apprentissage-proprete-lavable",
        "name": "Culotte d'apprentissage de la propreté",
        "range": "Accessoires", "type": "Culotte d'apprentissage", "shape": "training",
        "product_type": "Couches lavables > Culottes d'apprentissage",
        "gcat": "Baby & Toddler > Diapering > Diapers",
        "price": 19.00,
        "sizes": ["2-3 ans", "3-4 ans"], "size_kind": "age",
        "size": "2–3 ans (12–16 kg) · 3–4 ans (15–19 kg)",
        "age_group": "toddler", "material": "Coton biologique",
        "colors": ["Moutarde", "Sauge", "Rose poudré"],
        "short": "Une vraie culotte que l'enfant enfile seul, avec une zone absorbante pour les petits accidents.",
        "description": (
            "Pensée pour la transition vers la propreté, elle s'enfile et se retire comme une culotte, ce qui rend l'enfant "
            "autonome aux toilettes. Une zone absorbante en coton (3 couches) et une couche imperméable cachée retiennent "
            "les petits accidents ; l'enfant sent qu'il est mouillé, ce qui l'aide à prendre conscience de ses besoins."
        ),
        "attrs": {"Type": "Culotte d'apprentissage", "Tailles": "2–3 ans · 3–4 ans", "Matière": "Coton bio, zone absorbante 3 couches, couche imperméable cachée", "Lavage": "60 °C"},
        "highlights": ["Autonomie de l'enfant", "Retient les petits accidents"],
        "labels": ["coeur-de-gamme", "marge-moyenne", "proprete"],
        "faq": [],
    },
    {
        "id": "WS-SAC", "slug": "sac-impermeable-couches-lavables",
        "name": "Sac imperméable à couches",
        "range": "Accessoires", "type": "Sac", "shape": "bag",
        "product_type": "Accessoires > Sacs à couches",
        "gcat": "Baby & Toddler > Diapering > Diaper Wet Bags",
        "price": 16.00,
        "sizes": [], "size": "30 × 40 cm",
        "age_group": "infant", "material": "Polyester enduit",
        "colors": ["Sauge", "Terracotta", "Ciel"],
        "short": "Sac étanche à 2 compartiments propre / sale pour la crèche et les sorties.",
        "description": (
            "Une poche imperméable zippée pour les couches sales, une poche avant pour les propres. Contient 4 à 5 couches. "
            "Anse à pression pour l'accrocher à la poussette ou au portemanteau de la crèche. Lavable avec les couches."
        ),
        "attrs": {"Type": "Sac imperméable", "Dimensions": "30 × 40 cm", "Capacité": "4 à 5 couches", "Lavage": "40 °C"},
        "highlights": ["2 compartiments propre / sale", "Anse poussette"],
        "labels": ["accessoire", "marge-haute", "sortie"],
        "faq": [],
    },
    {
        "id": "WS-LINGETTES", "slug": "lingettes-lavables-lot-de-10",
        "name": "Lingettes lavables – lot de 10",
        "range": "Accessoires", "type": "Lingettes", "shape": "wipes",
        "product_type": "Accessoires > Lingettes lavables",
        "gcat": "Baby & Toddler > Diapering > Baby Wipes",
        "price": 12.90,
        "sizes": [], "size": "20 × 20 cm",
        "age_group": "infant", "material": "Coton",
        "colors": ["Écru"],
        "short": "Lingettes douces éponge / velours, lavées avec les couches.",
        "description": "Éponge d'un côté, velours de l'autre, 20 × 20 cm. À utiliser avec de l'eau tiède ou du liniment, elles vont dans le même bac et la même machine que les couches. Lot de 10.",
        "attrs": {"Type": "Lingettes lavables", "Dimensions": "20 × 20 cm", "Matière": "Coton éponge / velours", "Contenu": "Lot de 10", "Lavage": "60 °C"},
        "highlights": ["Se lavent avec les couches", "Zéro déchet"],
        "labels": ["accessoire", "marge-haute", "change"],
        "faq": [],
    },
    {
        "id": "WS-LESSIVE", "slug": "lessive-speciale-couches-lavables",
        "name": "Lessive spéciale couches lavables – 1 L",
        "range": "Entretien", "type": "Lessive", "shape": "bottle",
        "product_type": "Entretien > Lessive",
        "gcat": "Home & Garden > Household Supplies > Laundry Supplies > Laundry Detergent",
        "price": 13.90,
        "sizes": [], "size": "1 L (≈ 40 lavages)",
        "age_group": "", "material": "",
        "colors": [],
        "short": "Sans agent de blanchiment, azurant optique ni adoucissant : préserve l'étanchéité des poches et l'absorption.",
        "description": (
            "Les agents de blanchiment, azurants optiques, adoucissants et parfums en excès abîment le polyuréthane des poches "
            "étanches et encrassent les absorbants. Cette lessive liquide en est exempte et reste efficace dès 40 °C. "
            "Bidon de 1 L pour environ 40 lavages."
        ),
        "attrs": {"Type": "Lessive liquide", "Contenance": "1 L (≈ 40 lavages)", "Sans": "Agent de blanchiment, azurant optique, adoucissant, huile essentielle", "Efficacité": "Dès 40 °C"},
        "highlights": ["Préserve l'étanchéité", "Efficace dès 40 °C"],
        "labels": ["consommable", "marge-moyenne", "entretien"],
        "faq": [],
    },
]
