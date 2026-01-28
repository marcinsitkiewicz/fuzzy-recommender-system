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
    score = engine.evaluate(
        budget=user_preferences["budget"],
        quality=user_preferences["quality"],
        usage=user_preferences["usage"]
    )
    results.append((product["name"], round(score, 2)))

results.sort(key=lambda x: x[1], reverse=True)

print("Ranking rekomendowanych produktów:\n")
for name, score in results:
    print(f"{name}: {score}%")