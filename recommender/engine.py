import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyRecommenderEngine:
    def __init__(self):
        # Preferencje użytkownika
        self.user_budget = ctrl.Antecedent(np.arange(0, 11, 1), "user_budget")
        self.user_quality = ctrl.Antecedent(np.arange(0, 11, 1), "user_quality")
        self.user_usage = ctrl.Antecedent(np.arange(0, 11, 1), "user_usage")

        # Cecha produktu (pojedynczy agregat dopasowania)
        self.product_match = ctrl.Consequent(np.arange(0, 101, 1), "product_match")

        self._define_membership_functions()
        self._define_rules()

        system = ctrl.ControlSystem(self.rules)
        self.simulator = ctrl.ControlSystemSimulation(system)

    def _define_membership_functions(self):
        # Budżet / cena
        self.user_budget["low"] = fuzz.trimf(self.user_budget.universe, [0, 0, 5])
        self.user_budget["medium"] = fuzz.trimf(self.user_budget.universe, [3, 5, 7])
        self.user_budget["high"] = fuzz.trimf(self.user_budget.universe, [5, 10, 10])

        # Jakość
        self.user_quality["low"] = fuzz.trimf(self.user_quality.universe, [0, 0, 5])
        self.user_quality["medium"] = fuzz.trimf(self.user_quality.universe, [3, 5, 7])
        self.user_quality["high"] = fuzz.trimf(self.user_quality.universe, [5, 10, 10])

        # Użytkowanie
        self.user_usage["light"] = fuzz.trimf(self.user_usage.universe, [0, 0, 5])
        self.user_usage["regular"] = fuzz.trimf(self.user_usage.universe, [3, 5, 7])
        self.user_usage["intensive"] = fuzz.trimf(self.user_usage.universe, [5, 10, 10])

        # Wynik
        self.product_match["poor"] = fuzz.trapmf(self.product_match.universe, [0, 0, 30, 45])
        self.product_match["average"] = fuzz.trimf(self.product_match.universe, [40, 55, 70])
        self.product_match["good"] = fuzz.trimf(self.product_match.universe, [65, 75, 85])
        self.product_match["excellent"] = fuzz.trapmf(self.product_match.universe, [80, 90, 100, 100])

    def _define_rules(self):
        self.rules = [
            ctrl.Rule(
                self.user_budget["high"] & self.user_quality["high"],
                self.product_match["excellent"]
            ),
            ctrl.Rule(
                self.user_budget["medium"] & self.user_quality["medium"],
                self.product_match["good"]
            ),
            ctrl.Rule(
                self.user_budget["low"] & self.user_quality["high"],
                self.product_match["average"]
            ),
            ctrl.Rule(
                self.user_usage["intensive"] & self.user_quality["low"],
                self.product_match["poor"]
            ),
            ctrl.Rule(
                self.user_usage["regular"] & self.user_budget["medium"],
                self.product_match["good"]
            )
        ]

    def evaluate(self, user_prefs: dict, product: dict) -> float:
        self.simulator.reset()
        
        price_match = 10 - abs(user_prefs["budget"] - product["price"])
        quality_match = 10 - abs(user_prefs["quality"] - product["quality"])
        usage_match = 10 - abs(user_prefs["usage"] - product["usage"])

        # zabezpieczenie zakresu 0–10
        price_match = max(0, price_match)
        quality_match = max(0, quality_match)
        usage_match = max(0, usage_match)

        self.simulator.input["user_budget"] = price_match
        self.simulator.input["user_quality"] = quality_match
        self.simulator.input["user_usage"] = usage_match

        self.simulator.compute()

        if "product_match" not in self.simulator.output:
            return 0.0

        return float(self.simulator.output["product_match"])