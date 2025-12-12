import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(path):
    windplants   = pd.read_excel(path, "windplants")
    wind_lf      = pd.read_excel(path, "wind_loadfactors")
    solarplants  = pd.read_excel(path, "solarplants")
    solar_lf     = pd.read_excel(path, "solar_loadfactors")
    gasplants    = pd.read_excel(path, "gasplants")
    gas_prices   = pd.read_excel(path, "gas_prices")
    demand       = pd.read_excel(path, "demand")

    # Ensure time series are sorted
    for df in [wind_lf, solar_lf, gas_prices, demand]:
        df.sort_values("hour", inplace=True)

    return windplants, wind_lf, solarplants, solar_lf, gasplants, gas_prices, demand


def process_renewables(plants, loadfactors, tech):
    lf = loadfactors.melt(id_vars="hour", var_name="name", value_name="load_factor")
    df = lf.merge(plants, on="name")
    df["available_mw"] = df["capacity"] * df["load_factor"]
    df["marginal_cost"] = 0.0
    df["tech"] = tech
    return df



def process_gas(gasplants, gas_prices):
    g = gasplants.assign(key=1).merge(gas_prices.assign(key=1), on="key").drop("key", axis=1)
    g["available_mw"] = g["capacity"]
    g["marginal_cost"] = (g["price"] * 34.121) / g["efficiency"]
    g["tech"] = "Gas"
    return g


def dispatch_hourly(generators, demand):
    records = []

    for h in demand["hour"]:
        need = demand.loc[demand["hour"] == h, "demand"].iat[0]
        stack = generators[generators["hour"] == h].sort_values("marginal_cost")

        sent = 0
        for _, row in stack.iterrows():
            if sent >= need:
                break

            take = min(row["available_mw"], need - sent)
            sent += take

            records.append({
                "hour": h,
                "name": row["name"],
                "tech": row["tech"],
                "dispatched_mw": take,
                "marginal_cost": row["marginal_cost"]
            })

    return pd.DataFrame(records)


def summarize_hourly(dispatch_df, demand):
    table = dispatch_df.groupby(["hour", "tech"])["dispatched_mw"].sum().unstack(fill_value=0)
    table["dispatched"] = table.sum(axis=1)

    table = table.merge(demand, on="hour")
    table["shortage"] = table["dispatched"] < table["demand"] - 1e-2
    table["mismatch"] = table["dispatched"] - table["demand"]
    table["price"] = dispatch_df.groupby("hour")["marginal_cost"].max().values

    for t in ["Wind", "Solar", "Gas"]:
        table[t] = table.get(t, 0)
        table[f"{t.lower()}_pct"] = table[t] / table["dispatched"]

    return table.reset_index()



def apply_prorata(generators, demand):
    records = []

    for h in demand["hour"]:
        need = demand.loc[demand["hour"] == h, "demand"].iloc[0]

        stack = generators[generators["hour"] == h]
        re_stack = stack[stack["marginal_cost"] == 0]
        gas_stack = stack[stack["marginal_cost"] > 0].sort_values("marginal_cost")

        total_re = re_stack["available_mw"].sum()

        # Oversupply → pro-rata
        if total_re >= need:
            for _, row in re_stack.iterrows():
                share = row["available_mw"] / total_re
                records.append({
                    "hour": h,
                    "name": row["name"],
                    "tech": row["tech"],
                    "dispatched_mw": need * share,
                    "marginal_cost": 0.0
                })

        # Undersupply → full renewables + gas by merit order
        else:
            for _, row in re_stack.iterrows():
                records.append({
                    "hour": h,
                    "name": row["name"],
                    "tech": row["tech"],
                    "dispatched_mw": row["available_mw"],
                    "marginal_cost": 0.0
                })

            remaining = need - total_re
            for _, row in gas_stack.iterrows():
                if remaining <= 0:
                    break
                take = min(row["available_mw"], remaining)
                remaining -= take
                records.append({
                    "hour": h,
                    "name": row["name"],
                    "tech": row["tech"],
                    "dispatched_mw": take,
                    "marginal_cost": row["marginal_cost"]
                })

    return pd.DataFrame(records)


def plot_dispatch(hourly, filename):
    fig, ax1 = plt.subplots(figsize=(14, 6))

    ax1.stackplot(
        hourly["hour"],
        hourly["Wind"], hourly["Solar"], hourly["Gas"],
        labels=["Wind", "Solar", "Gas"],
        alpha=0.85
    )

    ax1.plot(hourly["hour"], hourly["demand"], "--", color="red", lw=1.4)

    for h in hourly[hourly["shortage"]]["hour"]:
        ax1.axvline(h, color="black", ls=":", alpha=0.4)

    ax1.set_xlabel("Hour")
    ax1.set_ylabel("Dispatch (MW)")
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()
    ax2.plot(hourly["hour"], hourly["price"], color="purple", lw=1.5)
    ax2.set_ylabel("Price (£/MWh)")

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


def plot_mismatch(hourly, filename):
    plt.figure(figsize=(14, 4))

    plt.plot(hourly["hour"], hourly["mismatch"], color="black", linewidth=1.4)
    plt.axhline(0, color="red", ls="--", linewidth=1.2)

    for h in hourly[hourly["shortage"]]["hour"]:
        plt.axvline(h, color="grey", linestyle=":", alpha=0.5)

    plt.xlabel("Hour")
    plt.ylabel("MW")
    plt.title("Dispatch Mismatch and Shortage Hours")
    plt.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


def main():
    path = "data 2.xlsx"

    windplants, wind_lf, solarplants, solar_lf, gasplants, gas_prices, demand = load_data(path)

    wind = process_renewables(windplants, wind_lf, "Wind")
    solar = process_renewables(solarplants, solar_lf, "Solar")
    gas = process_gas(gasplants, gas_prices)

    generators = pd.concat([wind, solar, gas], ignore_index=True)

    # Merit order dispatch
    dispatch = dispatch_hourly(generators, demand)
    hourly = summarize_hourly(dispatch, demand)

    dispatch.to_csv("dispatch_results.csv", index=False)
    hourly.to_csv("dispatch_hourly_summary.csv", index=False)

    plot_dispatch(hourly, "dispatch_plot.png")
    plot_mismatch(hourly, "mismatch_plot.png")

    # Pro-rata dispatch
    dispatch_pr = apply_prorata(generators, demand)
    hourly_pr = summarize_hourly(dispatch_pr, demand)

    dispatch_pr.to_csv("dispatch_prorata.csv", index=False)
    hourly_pr.to_csv("dispatch_hourly_prorata.csv", index=False)

    plot_dispatch(hourly_pr, "dispatch_prorata_plot.png")

    print("Finished. CSVs and plots saved.")


if __name__ == "__main__":
    main()


