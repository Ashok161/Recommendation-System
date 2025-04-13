import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

class RecommendationEngine:
    def __init__(self, products_path='products.csv', users_path='users.csv'):
        self.products = pd.read_csv(products_path)
        self.users = pd.read_csv(users_path)
    
    def get_initial_recommendations(self, top_n=5):
        """
        Generate diverse cold-start recommendations by combining:
        1. Diversity: Pick the highest-scored product from each category.
        2. Global Trending: Include some of the overall most popular products.
        Then merge these lists to create a hybrid set.
        """
        # 1. Diversity-based recommendation: get one top product per category
        grouped = self.products.groupby('category', as_index=False).apply(
            lambda df: df.sort_values("popularity_score", ascending=False).iloc[0]
        ).reset_index(drop=True)
        diverse = grouped.sort_values("popularity_score", ascending=False)
        
        diverse_recs = diverse.head(top_n)
        
        trending = self.products.sort_values("popularity_score", ascending=False).head(top_n)
        
        hybrid = pd.concat([diverse_recs, trending]).drop_duplicates(subset="product_id").reset_index(drop=True)
        
        final_recs = hybrid.head(top_n)
        return final_recs



    def update_user_profile(self, selected_product_ids):
        profile = defaultdict(lambda: Counter())
        for pid in selected_product_ids:
            prod_rows = self.products[self.products['product_id'] == pid]
            if prod_rows.empty:
                print(f"Warning: Product ID {pid} not found.")
                continue
            prod = prod_rows.iloc[0]
            profile['category'][prod['category']] += 1
            tags = [tag.strip() for tag in prod['tags'].split(',')]
            for tag in tags:
                profile['tags'][tag] += 1
        return profile

    def get_personalized_recommendations(self, user_profile, top_n=5):
        if user_profile['category']:
            pref_category = user_profile['category'].most_common(1)[0][0]
        else:
            pref_category = None

        if user_profile['tags']:
            pref_tags = [tag for tag, _ in user_profile['tags'].most_common(3)]
        else:
            pref_tags = []

        personalized = self.products.copy()
        if pref_category:
            personalized = personalized[personalized['category'] == pref_category]

        def score_product(row):
            score = row['popularity_score']
            product_tags = [tag.strip() for tag in row['tags'].split(',')]
            score += 5 * sum(1 for tag in pref_tags if tag in product_tags)
            return score

        personalized = personalized.copy()
        personalized['final_score'] = personalized.apply(score_product, axis=1)
        personalized_sorted = personalized.sort_values(by='final_score', ascending=False)

        trending = self.products.sort_values(by='popularity_score', ascending=False).head(3)
        combined = pd.concat([personalized_sorted.head(top_n), trending]).drop_duplicates(subset='product_id')
        return combined.head(top_n).reset_index(drop=True)

    @staticmethod
    def visualize_user_profile(user_profile, user_id="User"):
        categories = list(user_profile['category'].keys())
        counts = list(user_profile['category'].values())
        plt.figure(figsize=(6, 4))
        plt.bar(categories, counts, color='skyblue')
        plt.xlabel('Categories')
        plt.ylabel('Click Counts')
        plt.title(f'{user_id} - Preferred Categories')
        plt.show()

    def add_user_interactions(self, user_id, selected_product_ids):
        new_interactions = pd.DataFrame({
            'user_id': [user_id] * len(selected_product_ids),
            'product_id': selected_product_ids,
            'interaction': ['click'] * len(selected_product_ids)
        })
        self.users = pd.concat([self.users, new_interactions], ignore_index=True)
        return self.users

def simulate_user_interaction(engine, user_id):
    print(f"\n\n=== Simulating session for {user_id} ===")
    initial_recs = engine.get_initial_recommendations()
    print("\n--- Initial Recommendations ---")
    print(initial_recs[['product_id', 'title', 'popularity_score']])
    selection = input(f"\n{user_id}, enter product IDs you like (comma separated, e.g., P1,P4): ")
    selected_ids = [pid.strip() for pid in selection.split(',') if pid.strip()]
    print(f"{user_id} selected: {selected_ids}\n")
    user_profile = engine.update_user_profile(selected_ids)
    print(f"--- {user_id} Updated Profile ---")
    print("Preferred Categories:", dict(user_profile['category']))
    print("Tag Frequencies:", dict(user_profile['tags']))
    engine.visualize_user_profile(user_profile, user_id=user_id)
    personalized = engine.get_personalized_recommendations(user_profile)
    print(f"--- Personalized Recommendations for {user_id} ---")
    print(personalized[['product_id', 'title', 'popularity_score', 'tags', 'category']])
    engine.add_user_interactions(user_id, selected_ids)

def main():
    engine = RecommendationEngine()
    simulate_user_interaction(engine, "U4")
    simulate_user_interaction(engine, "U5")
    print("\n--- Updated Overall User Interactions ---")
    print(engine.users.head(10))

if __name__ == '__main__':
    main()
