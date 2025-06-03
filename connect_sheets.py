import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import json

# Authenticate & Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# Open Google Sheet
sheet = client.open("Personal Savings Tracker").sheet1

def add_transaction(date, transaction_type, category, amount, description):
    """Add a money transaction (Income or Expense) to Google Sheets."""
    sheet.append_row([date, transaction_type, category, amount, description])
    print(f"✅ Transaction added: {transaction_type} {amount} UGX for {category}")

def get_balance():
    """Calculate current savings balance from Google Sheets."""
    data = sheet.get_all_records()
    
    # Calculate total income and total expenses
    total_income = sum(entry["Amount(UGX)"] for entry in data if entry["Type"] == "In")
    total_expense = sum(entry["Amount(UGX)"] for entry in data if entry["Type"] == "Out")
    
    # Compute balance
    balance = total_income - total_expense

    # Display results
    print(f"💰 Total Income: {total_income} UGX")
    print(f"💸 Total Expenses: {total_expense} UGX")
    print(f"✅ Current Balance: {balance} UGX")
    
    return balance

def spending_pie_chart():
    """Create an enhanced pie chart for expense distribution."""
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Filter only expenses
    expenses = df[df["Type"] == "Out"].groupby("Category")["Amount(UGX)"].sum()

    # Create pie chart
    plt.figure(figsize=(8, 8))
    colors = sns.color_palette("pastel")  # Use soft pastel colors for better visuals
    expenses.plot(
        kind="pie",
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        wedgeprops={"edgecolor": "black", "linewidth": 1}
    )

    plt.title("📊 Expense Distribution", fontsize=14, fontweight="bold")
    plt.ylabel("")  # Remove y-axis label for cleaner look

    plt.savefig("expense_distribution.png")
    plt.show()
    print("✅ Enhanced expense distribution pie chart generated!")

def income_pie_chart():
    """Create a pie chart for income sources."""
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Filter only income
    income = df[df["Type"] == "In"].groupby("Category")["Amount(UGX)"].sum()

    # Create pie chart
    plt.figure(figsize=(8, 8))
    colors = sns.color_palette("bright")  # Use bright colors for income visualization
    income.plot(
        kind="pie",
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        wedgeprops={"edgecolor": "black", "linewidth": 1}
    )

    plt.title("💰 Income Sources Distribution", fontsize=14, fontweight="bold")
    plt.ylabel("")  # Remove y-axis label for cleaner look

    plt.savefig("income_distribution.png")
    plt.show()
    print("✅ Income sources pie chart generated!")

from sklearn.linear_model import LinearRegression
import numpy as np

def predict_savings_growth():
    """Predict future savings trends using AI."""
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Prepare data for forecasting
    df["Date"] = pd.to_datetime(df["Date"])
    df["Days"] = (df["Date"] - df["Date"].min()).dt.days
    df["Balance"] = df["Amount(UGX)"].cumsum()

    # Train the AI model
    X = df[["Days"]]
    y = df["Balance"]
    model = LinearRegression()
    model.fit(X, y)

    # Predict next 30 days
    future_days = np.array(range(df["Days"].max() + 1, df["Days"].max() + 31)).reshape(-1, 1)
    future_balance = model.predict(future_days)

    # Plot predictions
    plt.figure(figsize=(8, 5))
    plt.plot(df["Days"], df["Balance"], label="Actual Savings")
    plt.plot(future_days, future_balance, linestyle="dashed", label="Projected Growth", color="red")
    plt.legend()
    plt.title("📈 Savings Growth Prediction")
    plt.xlabel("Days")
    plt.ylabel("UGX Balance")

    plt.savefig("financial_trend.png")
    plt.show()
    print("✅ Savings prediction graph generated!")
