import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv"
df = pd.read_csv(url)

# Keep chart style consistent across figures
sns.set_theme(style="whitegrid", context="talk")

# --- GRAPHIC 1: Comparison of Incidents (1985-1999 vs 2000-2014) ---
# We'll look at the top 10 largest airlines (by available seat km)
top_10 = df.nlargest(10, "avail_seat_km_per_week").copy()
top_10["airline"] = top_10["airline"].str.replace("*", "", regex=False).str.strip()

# Prepare data for plotting
melted_df = top_10.melt(
    id_vars="airline",
    value_vars=["incidents_85_99", "incidents_00_14"],
    var_name="Era",
    value_name="Incidents",
)
melted_df["Era"] = melted_df["Era"].replace(
    {"incidents_85_99": "1985-1999", "incidents_00_14": "2000-2014"}
)

plt.figure(figsize=(12, 6))
sns.barplot(data=melted_df, x="airline", y="Incidents", hue="Era", palette="viridis")
plt.title(
    "Improvement in Airline Safety: Incidents by Era (Top 10 Largest Airlines)",
    fontsize=14,
)
plt.xlabel("Airline", fontsize=12)
plt.ylabel("Total Incidents", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.legend(title="Time Period")
plt.tight_layout()
plt.savefig("safety_comparison.png", dpi=160)
plt.close()

# --- GRAPHIC 2: Scatter Plot of Flight Volume vs. Fatalities ---
plt.figure(figsize=(10, 6))
sns.regplot(
    data=df,
    x="avail_seat_km_per_week",
    y="fatalities_85_99",
    color="red",
    scatter_kws={"alpha": 0.7, "s": 70},
    line_kws={"linewidth": 2},
    label="1985-1999",
)
sns.regplot(
    data=df,
    x="avail_seat_km_per_week",
    y="fatalities_00_14",
    color="blue",
    scatter_kws={"alpha": 0.7, "s": 70},
    line_kws={"linewidth": 2},
    label="2000-2014",
)
plt.title("Relationship Between Flight Volume and Fatalities", fontsize=14)
plt.xlabel("Available Seat Kilometers Per Week (Scale of Airline)", fontsize=12)
plt.ylabel("Total Fatalities", fontsize=12)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("volume_vs_fatalities.png", dpi=160)
plt.close()

print("Charts generated: safety_comparison.png, volume_vs_fatalities.png")
