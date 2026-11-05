
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SmartMoney AI",
    page_icon="💰",
    layout="wide"
)

st.title("💰 SmartMoney AI")
st.subheader("Personal Financial Planning Assistant")
st.write("Manage your monthly income, expenses, budget, savings and financial goals.")

# 1. Monthly Income
st.header("1. Monthly Income")

income = st.number_input(
    "Enter Monthly Income (₹)",
    min_value=0,
    value=30000,
    step=1000
)

# 2. Expense Categories
st.header("2. Expense Category Analysis")

categories = {
    "Rent": 7000,
    "Food": 5000,
    "Transport": 2000,
    "Shopping": 2000,
    "Other": 3000,
    "Healthcare": 700,
    "Education": 1000,
    "Mobile": 800
}

expenses = {}
col1, col2 = st.columns(2)

for index, (category, amount) in enumerate(categories.items()):
    with col1 if index % 2 == 0 else col2:
        expenses[category] = st.number_input(
            f"{category} Expenses (₹)",
            min_value=0,
            value=amount,
            step=100,
            key="expense_" + category
        )

total_expenses = sum(expenses.values())
savings = income - total_expenses
savings_rate = savings / income * 100 if income > 0 else 0

# 3. Financial Summary
st.header("3. Financial Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{income:,.0f}")
col2.metric("Total Expenses", f"₹{total_expenses:,.0f}")
col3.metric("Monthly Savings", f"₹{savings:,.0f}")

st.metric("Savings Rate", f"{savings_rate:.2f}%")

# 4. Expense Breakdown
st.header("4. Expense Breakdown")

expense_data = pd.DataFrame({
    "Category": list(expenses.keys()),
    "Amount": list(expenses.values())
})

st.bar_chart(expense_data, x="Category", y="Amount")
st.dataframe(expense_data, use_container_width=True)

# 5. Monthly Budget Planner
st.header("5. Monthly Budget Planner")

planned_budgets = {
    "Rent": 7000,
    "Food": 4000,
    "Transport": 2500,
    "Shopping": 1500,
    "Other": 3000,
    "Healthcare": 1000,
    "Education": 1500,
    "Mobile": 1000
}

budget_rows = []
budget_col1, budget_col2 = st.columns(2)

for index, (category, default_budget) in enumerate(planned_budgets.items()):
    with budget_col1 if index % 2 == 0 else budget_col2:
        planned = st.number_input(
            f"{category} Budget (₹)",
            min_value=0,
            value=default_budget,
            step=100,
            key="budget_" + category
        )

    actual = expenses[category]
    remaining = planned - actual

    if actual > planned:
        status = "Over Budget"
    elif actual == planned:
        status = "Budget Used"
    else:
        status = "Within Budget"

    budget_rows.append({
        "Category": category,
        "Planned Budget": planned,
        "Actual Expenses": actual,
        "Remaining Budget": remaining,
        "Status": status
    })

budget_data = pd.DataFrame(budget_rows)

total_planned = budget_data["Planned Budget"].sum()
total_remaining = total_planned - total_expenses

col1, col2, col3 = st.columns(3)
col1.metric("Planned Budget", f"₹{total_planned:,.0f}")
col2.metric("Actual Expenses", f"₹{total_expenses:,.0f}")
col3.metric("Remaining Budget", f"₹{total_remaining:,.0f}")

st.dataframe(budget_data, use_container_width=True)

st.subheader("Planned vs Actual Expenses")

budget_chart = budget_data.set_index("Category")[
    ["Planned Budget", "Actual Expenses"]
]

st.bar_chart(budget_chart)

over_budget_count = sum(budget_data["Status"] == "Over Budget")

if over_budget_count > 0:
    st.warning(f"You are over budget in {over_budget_count} categories.")
else:
    st.success("You are within your planned budgets.")

# 6. Financial Goals Planner
st.header("6. Financial Goals and Savings Planner")

st.write("Set a savings target and track your progress.")

goal_name = st.text_input(
    "Enter Your Financial Goal",
    value="Emergency Fund"
)

goal_amount = st.number_input(
    "Your Savings Target (₹)",
    min_value=1,
    value=50000,
    step=1000
)

current_savings = st.number_input(
    "Amount Already Saved (₹)",
    min_value=0,
    value=10000,
    step=1000
)

monthly_contribution = st.number_input(
    "Monthly Contribution Towards Goal (₹)",
    min_value=0,
    value=5000,
    step=500
)

remaining_goal = max(goal_amount - current_savings, 0)

progress = min(current_savings / goal_amount, 1.0)

st.subheader("Your Goal Progress")
st.progress(progress)

st.write(f"Goal: {goal_name}")
st.write(f"Target Amount: ₹{goal_amount:,.0f}")
st.write(f"Already Saved: ₹{current_savings:,.0f}")
st.write(f"Remaining Amount: ₹{remaining_goal:,.0f}")
st.write(f"Progress: {progress * 100:.2f}%")

if remaining_goal == 0:
    st.success("Congratulations! You have achieved your savings goal.")
elif monthly_contribution > 0:
    months_needed = (
        remaining_goal + monthly_contribution - 1
    ) // monthly_contribution

    st.info(
        f"At ₹{monthly_contribution:,.0f} per month, "
        f"you may reach your goal in approximately {months_needed} months."
    )
else:
    st.warning("Enter a monthly contribution to estimate your goal timeline.")

# 7. Financial Recommendations
st.header("7. Financial Recommendations")

if savings < 0:
    st.error("Your expenses are higher than your income.")
elif savings_rate >= 20:
    st.success("Good savings! Continue your monthly savings.")
else:
    st.warning("Try to increase your monthly savings.")

highest_category = max(expenses, key=expenses.get)
st.info(f"Your highest expense category is {highest_category}.")

# 8. Download Reports
st.header("8. Download Your Reports")

st.download_button(
    "Download Expense Report",
    expense_data.to_csv(index=False),
    "SmartMoney_Expense_Report.csv",
    "text/csv"
)

st.download_button(
    "Download Budget Report",
    budget_data.to_csv(index=False),
    "SmartMoney_Budget_Report.csv",
    "text/csv"
)

st.caption("SmartMoney AI | Personal Finance Assistant")
