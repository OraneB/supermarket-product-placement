"""
Simulates individual shopping trips: generating shopping lists, computing purchase probabilities for a given list, 
and walking a customer through the store to compute their total spend.
"""

import random
from config import STORE_SIZE, AISLE_NAMES, AISLE_PRODUCTS, PRODUCT_NAMES

def generate_shopping_lists(n_customers, shopping_list_probability_df):
    """Generate n_customers shopping lists (each a list of product names). Never returns an empty list."""
    lists = []
    probabilities = shopping_list_probability_df["Probabilité_liste_courses_%"]
    for _ in range(n_customers):
        shopping_list = [product for product, p in probabilities.items() if random.randint(0, 99) < p]
        while shopping_list == []:  # avoid empty shopping lists
            shopping_list = [product for product, p in probabilities.items() if random.randint(0, 99) < p]
        lists.append(shopping_list)
    return lists


def generate_purchase_probabilities(shopping_list, purchase_probability_df):
    """
    For every product, return the probability (0-100) that a customer with
    this shopping_list buys it: 100 if it's on the list, otherwise the
    average co-purchase probability with the products that are on the list.
    Falls back to 0 for every product if the shopping list is empty.
    """
    probabilities = {}
    for product in PRODUCT_NAMES:
        if product in shopping_list:
            probabilities[product] = 100
        elif shopping_list == []:
            probabilities[product] = 0
        else:
            total = sum(
                int(purchase_probability_df.loc[product, listed_product])
                for listed_product in shopping_list
            )
            probabilities[product] = int(total / len(shopping_list))
    return probabilities



def find_aisle_position(store, aisle):
    """Return the (row, col) of the given aisle index in the store grid."""
    for i in range(len(store)):
        for j in range(len(store[0])):
            if store[i][j] == aisle:
                return i, j
    return None


def aisle_by_product():
    """Return a dict mapping each product name to its aisle index."""
    mapping = {}
    for aisle, products in AISLE_PRODUCTS.items():
        for product in products:
            mapping[product] = AISLE_NAMES.index(aisle)
    return mapping


def find_path(i, j, k, l):
    """Breadth-first search for the shortest path from (i, j) to (k, l) on the store grid."""
    visited = [[False] * STORE_SIZE for _ in range(STORE_SIZE)]
    queue = [(i, j, [(i, j)])]  # represents (x, y, path to reach (x,y)]
    visited[i][j] = True
    while queue != []:
        x, y, path = queue.pop(0)
        if (x, y) == (k, l): 
            return path
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < STORE_SIZE and 0 <= ny < STORE_SIZE and not visited[nx][ny]:
                visited[nx][ny] = True
                queue.append((nx, ny, path + [(nx, ny)]))
    return []


def simulate_shopping_trip(store, shopping_list, aisle_by_product_map, purchase_probability_df, average_price_df):
    """
    Walk a customer through the store to buy every item on their shopping
    list (plus impulse purchases along the way), then walk back to the exit.
    Returns the total amount spent.
    """
    spend = 0
    remaining = shopping_list[:]
    bought = []
    i, j = 0, 0  # every trip starts at the entrance
    purchase_probabilities = generate_purchase_probabilities(remaining, purchase_probability_df)
 
    while remaining != []:
        target_aisle = aisle_by_product_map.get(remaining.pop(0))
        target_i, target_j = find_aisle_position(store, target_aisle)
        path = find_path(i, j, target_i, target_j)
        for pi, pj in path:
            for product in AISLE_PRODUCTS[AISLE_NAMES[store[pi][pj]]]:
                if product not in bought:
                    if random.randint(0, 99) < purchase_probabilities.get(product):
                        spend += average_price_df.loc[product, "Prix_moyen_euros"]
                        bought.append(product)
                    else:
                        purchase_probabilities[product] *= 0.5 # divide the probability of buying the product by two (arbitrary) to simulate customer behaviour
                    if product in remaining:
                        remaining.remove(product) #the product was bought because its purchase probability was set to 100
        i, j = target_i, target_j  # customer is now in this aisle
 
    path_back = find_path(i, j, 0, 0)
    for pi, pj in path_back:
        for product in AISLE_PRODUCTS[AISLE_NAMES[store[pi][pj]]]:
            if product not in bought:
                if random.randint(0, 99) < purchase_probabilities.get(product):
                    spend += average_price_df.loc[product, "Prix_moyen_euros"]
 
    return round(float(spend), 2)
