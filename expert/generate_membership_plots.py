# Uruchamianie - 'python -m expert.generate_membership_plots'
import matplotlib.pyplot as plt
from expert.engine import LaptopPurchaseExpertSystem


def plot_membership_functions():
    system = LaptopPurchaseExpertSystem()

    plots = [
        (system.price, "Cena względem budżetu"),
        (system.quality, "Jakość laptopa"),
        (system.usage, "Intensywność użytkowania"),
        (system.value, "Opłacalność zakupu"),
    ]

    for variable, title in plots:
        plt.figure(figsize=(8, 4))

        for term_name, term in variable.terms.items():
            plt.plot(
                variable.universe,
                term.mf,
                label=term_name
            )

        plt.title(title)
        plt.xlabel("Wartość")
        plt.ylabel("Stopień przynależności")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        filename = f"plots/{variable.label}_membership.png"
        plt.savefig(filename)
        plt.close()

        print(f"Zapisano wykres: {filename}")


if __name__ == "__main__":
    plot_membership_functions()