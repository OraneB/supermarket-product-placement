"""
Entry point: compares total customer spend across the three store layouts (random, close, far) over repeated simulated shopping trips.
"""
from config import purchase_probability_df, shopping_list_probability_df, average_price_df
from store_layout import random_layout, close_layout, far_layout
from shopping_simulation import generate_shopping_lists, aisle_by_product, simulate_shopping_trip

def compare_layouts(n_trials, random_store, close_store, far_store):
    """Simulate n_trials customers on each of the three layouts and print the average spend."""
    shopping_lists = generate_shopping_lists(n_trials, shopping_list_probability_df)
    total_random = total_close = total_far = 0
    product_to_aisle = aisle_by_product()
 
    for shopping_list in shopping_lists:
        total_random += simulate_shopping_trip(random_store, shopping_list, product_to_aisle, purchase_probability_df, average_price_df)
        total_close += simulate_shopping_trip(close_store, shopping_list, product_to_aisle, purchase_probability_df, average_price_df)
        total_far += simulate_shopping_trip(far_store, shopping_list, product_to_aisle, purchase_probability_df, average_price_df)
 
    print(
        f"Random: {round(total_random / n_trials, 2)}, "
        f"Close: {round(total_close / n_trials, 2)}, "
        f"Far: {round(total_far / n_trials, 2)}"
    )


if __name__ == "__main__":
    for _ in range(10):
        store_random = random_layout()
        print(store_random)
        compare_layouts(
            100,
            store_random,
            close_layout(purchase_probability_df, shopping_list_probability_df),
            far_layout(purchase_probability_df, shopping_list_probability_df),
        )
        print()
