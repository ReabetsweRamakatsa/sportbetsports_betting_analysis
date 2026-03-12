# SPORTS BETTING ANALYSIS - SOUTH AFRICA MARKET

import pandas as pd

# LOAD DATA

file_path = "South_Africa_Sports_Betting_Dataset.xlsx"

users = pd.read_excel(file_path, sheet_name="users")
events = pd.read_excel(file_path, sheet_name="events")
bets = pd.read_excel(file_path, sheet_name="bets")

# MERGE TABLES

bets_events = bets.merge(events, on="event_id", how="left")
full_df = bets_events.merge(users, on="user_id", how="left")

# 1. KYC COMPLETION RATE

kyc_completion = users["kyc_status"].mean() * 100
print(f"KYC Completion Rate: {kyc_completion:.2f}%")

# 2. AVERAGE DEPOSITS BY KYC STATUS

avg_deposits = users.groupby("kyc_status")["total_deposits"].mean()
print("Average Deposits by KYC Status")
print(avg_deposits)

# 3. CUSTOMER LIFETIME BETTING VALUE

lifetime_value = (
    bets.groupby("user_id")["stake_amount"]
    .sum()
    .reset_index()
    .merge(users[["user_id", "username"]], on="user_id")
    .sort_values("stake_amount", ascending=False)
)

print("Top 10 Customers by Lifetime Betting Value")
print(lifetime_value.head(10))

# 4. GROSS GAMING REVENUE (GGR)

total_stakes = bets["stake_amount"].sum()
total_payouts = bets["payout_amount"].sum()
ggr = total_stakes - total_payouts

print(f"Total Stakes: {total_stakes:.2f}")
print(f"Total Payouts: {total_payouts:.2f}")
print(f"GGR: {ggr:.2f}")

# 5. REVENUE BY SPORT TYPE

revenue_by_sport = (
    bets_events.groupby("sport_type")
    .agg(
        total_stakes=("stake_amount", "sum"),
        total_payouts=("payout_amount", "sum")
    )
)

revenue_by_sport["ggr"] = (
    revenue_by_sport["total_stakes"] - revenue_by_sport["total_payouts"]
)

print("Revenue by Sport")
print(revenue_by_sport.sort_values("ggr", ascending=False))

# 6. PROFITABILITY BY BET TYPE

profit_by_bet_type = (
    bets.groupby("bet_type")
    .agg(
        total_stakes=("stake_amount", "sum"),
        total_payouts=("payout_amount", "sum")
    )
)

profit_by_bet_type["profitability"] = (
    profit_by_bet_type["total_stakes"] - profit_by_bet_type["total_payouts"]
)

print("Profitability by Bet Type")
print(profit_by_bet_type.sort_values("profitability", ascending=False))

import matplotlib.pyplot as plt

# VISUAL 1: KYC COMPLETION RATE

kyc_counts = users["kyc_status"].value_counts()

plt.figure()
kyc_counts.plot(kind="bar")
plt.title("KYC Verification Status Distribution")
plt.xlabel("KYC Status")
plt.ylabel("Number of Users")
plt.tight_layout()
plt.savefig("outputs/charts/kyc_status_distribution.png")
plt.close()


# VISUAL 2: GGR BY SPORT TYPE

revenue_by_sport["ggr"].sort_values(ascending=False).plot(kind="bar")
plt.title("Gross Gaming Revenue (GGR) by Sport")
plt.xlabel("Sport Type")
plt.ylabel("GGR (ZAR)")
plt.tight_layout()
plt.savefig("outputs/charts/ggr_by_sport.png")
plt.close()


# VISUAL 3: BET TYPE PROFITABILITY

profit_by_bet_type["profitability"].sort_values(ascending=False).plot(kind="bar")
plt.title("Profitability by Bet Type")
plt.xlabel("Bet Type")
plt.ylabel("Profit (ZAR)")
plt.tight_layout()
plt.savefig("outputs/charts/profitability_by_bet_type.png")
plt.close()


print("Charts generated and saved in outputs/charts/")


# Ensure output folders exist
import os
os.makedirs("outputs/tables", exist_ok=True)

# 1. Revenue by sport
revenue_by_sport.to_csv(
    "outputs/tables/revenue_by_sport.csv",
    index=True
)

# 2. Customer lifetime betting value
lifetime_value.to_csv(
    "outputs/tables/customer_lifetime_value.csv",
    index=False
)

# 3. Profitability by bet type
profit_by_bet_type.to_csv(
    "outputs/tables/profitability_by_bet_type.csv",
    index=True
)

print("Tables saved in outputs/tables/")


