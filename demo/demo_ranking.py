#Uruchamianie poprzez 'python -m demo.demo_ranking'
from recommender.engine import FuzzyRecommenderEngine
from recommender.products import PRODUCTS


engine = FuzzyRecommenderEngine()

# Preferencje użytkownika
user_preferences = {
    "budget": 3,
    "quality": 6,
    "usage": 6
}

results = []

for product in PRODUCTS:
    score = engine.evaluate(user_preferences, product)
    results.append((product["name"], round(score, 2)))

results.sort(key=lambda x: x[1], reverse=True)

print("Ranking rekomendowanych produktów:\n")
for name, score in results:
    label = engine.linguistic_label(score)
    print(f"{name}: {score}% - {label}")