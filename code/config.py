"""
Configuration constants and data loading for the supermarket simulation.
"""

from pathlib import Path
import pandas as pd
 
DATA_DIR = Path(__file__).parent / "data"
 
# Products grouped by aisle
AISLE_PRODUCTS = {
    "Fruits et Légumes": ["Pommes", "Salade verte", "Tomates", "Pommes de terre", "Carottes", "Oignons", "Concombres"],
    "Crèmerie": ["Lait", "Oeufs", "Farine", "Sucre"],
    "Produits laitiers": ["Yaourts", "Fromage rapé", "Fromage", "Crème fraiche", "Beurre"],
    "Boulangerie": ["Pain", "Viennoiseries"],
    "Boucherie": ["Poulet", "Jambon", "Steak Haché", "Saucisses"],
    "Epicerie": ["Pâtes", "Riz", "Lentilles"],
    "Condiment": ["Huile d'olive", "Sel"],
    "Boisson": ["Eau", "Jus de fruits"],
    "Petit-déjeuner": ["Café", "Céréales", "Thé"],
    "Conserves": ["Thon", "Légumes en conserve"],
    "Produits d'hygiène": ["Papier toilette", "Savon", "Dentifrice"],
    "Produits ménagers": ["Lessive", "Liquide vaisselle"],
    "Epicerie sucré": ["Biscuits", "Chocolat"],
    "Biscuits salés": ["Chips"],
    "Surgelés": ["Pizzas", "Légumes congelés"],
}
 
AISLE_NAMES = list(AISLE_PRODUCTS.keys())
PRODUCT_NAMES = [product for products in AISLE_PRODUCTS.values() for product in products]
 
N_AISLES = len(AISLE_NAMES)      # 15
N_PRODUCTS = len(PRODUCT_NAMES)  # 44
STORE_SIZE = 4                   # the store is a 4x4 grid; [0][0] is the entrance/exit/checkout
 
# Purchase co-occurrence probabilities, shopping-list probability per product, and average price per product.
purchase_probability_df = pd.read_csv(DATA_DIR / "probabilites_achats_supermarche.csv", sep=",", index_col=0)
shopping_list_probability_df = pd.read_csv(DATA_DIR / "probabilites_produits.csv", sep=",", index_col=0)
average_price_df = pd.read_csv(DATA_DIR / "prix_moyens_produits.csv", sep=",", index_col=0)
