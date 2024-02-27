import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import scipy


PATH_TO_PUMPS = Path("./data/OECD_Parts_Liquid-Pumps.csv")
PATH_TO_RICE_PRODUCTION = Path("./data/FAOSTAT_Rice_Production-Yield.csv")

YEAR_SPACE_PUMPS_RICE = (2000, 2019)


def main():
    df_rice = pd.read_csv(PATH_TO_RICE_PRODUCTION, sep=",")
    df_pumps = pd.read_csv(PATH_TO_PUMPS, sep=",")

    pump_data = np.array(
        [df_pumps[df_pumps["Year"] == year]["Trade Value"].to_numpy().sum() for year in range(YEAR_SPACE_PUMPS_RICE[0], YEAR_SPACE_PUMPS_RICE[1] + 1)]
    )

    rice_data = np.array(
        [df_rice[(df_rice["Year"] == year) & (df_rice["Element"] == "Production")]["Value"].astype(int).to_numpy().sum() for year in range(YEAR_SPACE_PUMPS_RICE[0], YEAR_SPACE_PUMPS_RICE[1] + 1)]
    )

    plt.scatter(pump_data, rice_data, color="black", marker="+")

    result = scipy.stats.linregress(pump_data, rice_data)
    y = pump_data * result.slope + result.intercept

    plt.plot(pump_data, y, label=f"$\\alpha={result.slope}$, $\\beta={result.intercept}$")

    plt.ylabel("rice production [t]")
    plt.xlabel("liquid pump imports [trade value]")
    plt.legend()
    plt.savefig("pump_data.pdf", dpi=150)

    output_data = {
        "slope": [result.slope],
        "error on slope": [result.stderr],
        "intercept": [result.intercept],
        "error on intercept": [result.intercept_stderr],
        "r value": [result.rvalue],
        "p value": [result.pvalue],
    }

    output_df = pd.DataFrame(output_data)

    output_df.to_csv("regression_results_pumps.csv", sep=",")

    plt.show()


if __name__ == "__main__":
    main()
