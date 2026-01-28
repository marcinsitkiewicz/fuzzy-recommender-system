from expert.engine import LaptopPurchaseExpertSystem

system = LaptopPurchaseExpertSystem()

price = 7      # cena względem budżetu (0–10)
quality = 6    # jakość sprzętu
usage = 6      # intensywność użytkowania

result = system.evaluate(price, quality, usage)

print("Ocena opłacalności zakupu:\n")
print(f"Wynik: {result['score']}%")
print(f"Rekomendacja: {result['label']}")