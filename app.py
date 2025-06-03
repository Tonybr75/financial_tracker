from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import connect_sheets  # Import your financial tracking system

app = Flask(__name__)

@app.route("/")
def home():
    """Dashboard homepage showing balance and expense trends."""
    data = connect_sheets.sheet.get_all_records()
    df = pd.DataFrame(data)

    # Calculate current balance
    total_income = df[df["Type"] == "In"]["Amount(UGX)"].sum()
    total_expense = df[df["Type"] == "Out"]["Amount(UGX)"].sum()
    balance = total_income - total_expense

    return render_template("dashboard.html", balance=balance)

@app.route("/expense_chart")
def expense_chart():
    """Generate and serve the expense distribution chart."""
    data = connect_sheets.sheet.get_all_records()
    df = pd.DataFrame(data)

    expenses = df[df["Type"] == "Out"].groupby("Category")["Amount(UGX)"].sum()

    # Create chart
    plt.figure(figsize=(8, 8))
    colors = sns.color_palette("pastel")
    expenses.plot(kind="pie", autopct="%1.1f%%", colors=colors, startangle=140)

    plt.title("📊 Expense Distribution", fontsize=14, fontweight="bold")
    plt.ylabel("")

    plt.savefig("expense_chart.png")
    return send_file("expense_chart.png", mimetype="image/png")

@app.route("/category_spending")
def category_spending():
    """Show spending by category in a table."""
    data = connect_sheets.sheet.get_all_records()
    df = pd.DataFrame(data)

    expenses = df[df["Type"] == "Out"].groupby("Category")["Amount(UGX)"].sum()
    return render_template("categories.html", categories=expenses.to_dict())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

@app.route("/category_spending")
def category_spending():
    """Show spending by category in a table."""
    data = connect_sheets.sheet.get_all_records()
    df = pd.DataFrame(data)

    expenses = df[df["Type"] == "Out"].groupby("Category")["Amount(UGX)"].sum()
    return render_template("categories.html", categories=expenses.to_dict())
