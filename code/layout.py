"""
Store layout generation strategies.
 
Three strategies arrange the 15 aisles on the 4x4 store grid ([0][0] is the entrance/exit/checkout):
 
- random_layout: aisles placed in random order (Knuth shuffle)
- close_layout: aisles frequently bought together are placed near each other
- far_layout:   aisles frequently bought together are placed far apart
"""

import random
from config import N_AISLES, STORE_SIZE, AISLE_NAMES, AISLE_PRODUCTS

def init_store():
    """Return an empty STORE_SIZE x STORE_SIZE grid (-1 = empty cell)."""
    return [STORE_SIZE * [-1] for _ in range(STORE_SIZE)]

def aisle_transition_matrix(purchase_probability_df):
    """
    Return an N_AISLES x N_AISLES matrix where cell [i][j] is the average
    probability of buying something in aisle j given something was bought
    in aisle i.
    """
    matrix = [N_AISLES * [0] for _ in range(N_AISLES)]
    for i in range(N_AISLES):
        for j in range(N_AISLES):
            aisle_i = AISLE_NAMES[i]
            aisle_j = AISLE_NAMES[j]
            for product_i in AISLE_PRODUCTS[aisle_i]:
                for product_j in AISLE_PRODUCTS[aisle_j]:
                    matrix[i][j] += purchase_probability_df.loc[product_i, product_j]
            matrix[i][j] /= len(AISLE_PRODUCTS[aisle_i]) * len(AISLE_PRODUCTS[aisle_j])
    return [[round(float(x), 2) for x in row] for row in matrix]


def aisle_weights(shopping_list_probability_df):
    """Return, for each aisle, the summed probability of its products appearing on a shopping list."""
    weights = [0] * N_AISLES
    for i in range(N_AISLES):
        for product in AISLE_PRODUCTS[AISLE_NAMES[i]]:
            weights[i] += shopping_list_probability_df.loc[product, "Probabilité_liste_courses_%"]
    return [int(w) for w in weights]



def argmax(values):
    """Return the index of the largest value in the list."""
    best = 0
    for i in range(1, len(values)):
        if values[i] > values[best]:
            best = i
    return best


def clear_column(matrix, col):
    """Mark a column as unavailable (-1) in every row of the matrix, in place."""
    for row in matrix:
        row[col] = -1


### LAYOUTS

def random_layout():
    """Place the N_AISLES aisles on the grid in random order (Knuth shuffle)."""
    order = list(range(N_AISLES))
    for i in range(N_AISLES):
        k = random.randint(0, i)
        order[k], order[i] = order[i], order[k]
    store = init_store()
    for i in range(1, N_AISLES + 1):
        row = i // STORE_SIZE
        col = i % STORE_SIZE
        store[row][col] = order[i - 1]
    return store


def close_layout(purchase_probability_df, shopping_list_probability_df):
    """
    Place aisles so that aisles frequently bought together end up close to
    each other on the grid, starting from the corner opposed to the entrance 
    corner and expanding.
    """
    store = init_store()
    top_aisle = argmax(aisle_weights(shopping_list_probability_df))
    transition_matrix = aisle_transition_matrix(purchase_probability_df)
    store[-1][-1] = top_aisle
    clear_column(transition_matrix, top_aisle)
 
    to_fill = [(STORE_SIZE - 1, STORE_SIZE - 2), (STORE_SIZE - 2, STORE_SIZE - 1)]
    while to_fill != []:
        i, j = to_fill.pop(0)
        if i == STORE_SIZE - 1:
            ind = argmax(transition_matrix[store[i][j + 1]])
            clear_column(transition_matrix, ind)
            store[i][j] = ind
            if j > 0:
                to_fill.append((i, j - 1))
        elif j == STORE_SIZE - 1:
            ind = argmax(transition_matrix[store[i + 1][j]])
            clear_column(transition_matrix, ind)
            store[i][j] = ind
            to_fill.append((i, j - 1))
            if i != 0:
                to_fill.append((i - 1, j))
        else:
            combined = [
                transition_matrix[store[i][j + 1]][k] + transition_matrix[store[i + 1][j]][k]
                for k in range(N_AISLES)
            ]
            ind = argmax(combined)
            clear_column(transition_matrix, ind)
            store[i][j] = ind
            if j > 0 and not (i == 0 and j == 1):
                to_fill.append((i, j - 1))
    return store


def available_indices(store, i, j):
    """Return the empty cells sharing row i or column j with (i, j)."""
    indices = []
    for k in range(STORE_SIZE):
        if i != 0 and store[i][k] == -1:
            indices.append((i, k))
        if i == 0 and k != 0 and store[i][k] == -1:
            indices.append((i, k))
        if j != 0 and store[k][j] == -1:
            indices.append((k, j))
        if j == 0 and k != 0 and store[k][j] == -1:
            indices.append((k, j))
    return indices


def manhattan_distance(i, j, k, l):
    return abs(i - k) + abs(j - l)


def farthest_available_indices(store, i, j):
    """Among empty cells available from (i, j), return those farthest away."""
    candidates = available_indices(store, i, j)
    result = []
    if candidates != []:
        p, q = candidates[0]
        max_dist = manhattan_distance(i, j, p, q)
        for k, l in candidates:
            d = manhattan_distance(i, j, k, l)
            if d > max_dist:
                result = [(k, l)]
                max_dist = d
            elif d == max_dist:
                result.append((k, l))
    return result


def far_layout(purchase_probability_df, shopping_list_probability_df):
    """Place aisles so that aisles frequently bought together end up far from each other,
    starting from the corner opposed to the entrance corner and expanding."""
    store = init_store()
    top_aisle = argmax(aisle_weights(shopping_list_probability_df))
    transition_matrix = aisle_transition_matrix(purchase_probability_df)
    store[-1][-1] = top_aisle
    clear_column(transition_matrix, top_aisle)
 
    to_fill = farthest_available_indices(store, STORE_SIZE - 1, STORE_SIZE - 1)
    for p, q in to_fill:
        ind = argmax(transition_matrix[store[-1][-1]])
        clear_column(transition_matrix, ind)
        store[p][q] = ind
    while to_fill != []:
        i, j = to_fill.pop(0)
        candidates = farthest_available_indices(store, i, j)
        for p, q in candidates:
            ind = argmax(transition_matrix[store[i][j]])
            clear_column(transition_matrix, ind)
            store[p][q] = ind
            to_fill.append((p, q))
    return store
