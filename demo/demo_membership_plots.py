import matplotlib.pyplot as plt
from recommender.engine import FuzzyRecommenderEngine

engine = FuzzyRecommenderEngine()

engine.user_budget.view()
engine.user_quality.view()
engine.user_usage.view()
engine.product_match.view()

plt.show()