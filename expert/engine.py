import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class LaptopPurchaseExpertSystem:
    def __init__(self):
        # Wejścia
        self.price = ctrl.Antecedent(np.arange(0, 11, 1), "price")
        self.quality = ctrl.Antecedent(np.arange(0, 11, 1), "quality")
        self.usage = ctrl.Antecedent(np.arange(0, 11, 1), "usage")

        # Wyjście
        self.value = ctrl.Consequent(np.arange(0, 101, 1), "value")

        self._define_membership_functions()
        self._define_rules()

        system = ctrl.ControlSystem(self.rules)
        self.simulator = ctrl.ControlSystemSimulation(system)

    def _define_membership_functions(self):
        # Cena
        self.price["low"] = fuzz.trimf(self.price.universe, [0, 0, 5])
        self.price["medium"] = fuzz.trimf(self.price.universe, [3, 5, 7])
        self.price["high"] = fuzz.trimf(self.price.universe, [5, 10, 10])

        # Jakość
        self.quality["low"] = fuzz.trimf(self.quality.universe, [0, 0, 5])
        self.quality["medium"] = fuzz.trimf(self.quality.universe, [3, 5, 7])
        self.quality["high"] = fuzz.trimf(self.quality.universe, [5, 10, 10])

        # Użytkowanie
        self.usage["light"] = fuzz.trimf(self.usage.universe, [0, 0, 5])
        self.usage["regular"] = fuzz.trimf(self.usage.universe, [3, 5, 7])
        self.usage["intensive"] = fuzz.trimf(self.usage.universe, [5, 10, 10])

        # Opłacalność
        self.value["poor"] = fuzz.trapmf(self.value.universe, [0, 0, 30, 45])
        self.value["average"] = fuzz.trimf(self.value.universe, [40, 55, 70])
        self.value["good"] = fuzz.trimf(self.value.universe, [65, 75, 85])
        self.value["excellent"] = fuzz.trapmf(self.value.universe, [85, 92, 100, 100])

    def _define_rules(self):
        self.rules = [
            ctrl.Rule(
                self.price["low"] & self.quality["high"],
                self.value["excellent"]
            ),
            ctrl.Rule(
                self.price["medium"] & self.quality["high"],
                self.value["good"]
            ),
            ctrl.Rule(
                self.price["medium"] & self.quality["medium"],
                self.value["good"]
            ),
            ctrl.Rule(
                self.price["high"] & self.quality["low"],
                self.value["poor"]
            ),
            ctrl.Rule(
                self.usage["intensive"] & self.quality["low"],
                self.value["poor"]
            )
        ]

    def evaluate(self, price: int, quality: int, usage: int) -> dict:
        self.simulator.reset()

        self.simulator.input["price"] = price
        self.simulator.input["quality"] = quality
        self.simulator.input["usage"] = usage

        self.simulator.compute()

        score = float(self.simulator.output["value"])
        label = self._linguistic_label(score)

        return {
            "score": round(score, 2),
            "label": label
        }

    def _linguistic_label(self, score: float) -> str:
        if score < 40:
            return "nieopłacalny zakup"
        elif score < 60:
            return "umiarkowanie opłacalny zakup"
        elif score < 80:
            return "opłacalny zakup"
        else:
            return "bardzo opłacalny zakup"