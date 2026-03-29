import streamlit as st
import pandas as pd
st.markdown("### 🚀 Smart Cloud Cost Intelligence Dashboard")
st.caption("AI-driven insights to optimize your AWS spending")
# Title
st.title("💡 AI-Powered FinOps Cloud Optimization Advisor")

# Load Data
df = pd.read_csv("data.csv")

# Total Cost
total_cost = df["total_cost"].sum()
st.metric("Total Monthly Cloud Cost", f"₹{total_cost}")



# -----------------------------
# Recommendation Engine
# -----------------------------
def recommend(row):
    service = row["service"]
    usage = row["usage_hours"]
    cost = row["total_cost"]
    env = row["environment"]

    if service == "EC2" and usage > 100 and env == "dev":
        return f"Idle dev instances detected → Save ₹{int(cost*0.3)}"

    elif service == "EC2" and env == "prod" and cost > 1000:
        return f"Use Reserved Instances → Save ₹{int(cost*0.25)}"

    elif service == "S3" and usage > 500:
        return "Move to Glacier → Save ~60%"

    elif service == "RDS" and cost > 1000:
        return "Use Reserved DB → Save ~30%"

    else:
        return "Optimized"

df["Recommendation"] = df.apply(recommend, axis=1)

# -----------------------------
# Business Insight
# -----------------------------
compute_cost = df[df["service"] == "EC2"]["total_cost"].sum()
if total_cost > 0:
    score = 100 - int((compute_cost / total_cost) * 50)
else:
    score = 0

st.metric("Cloud Efficiency Score", f"{score}/100")

percentage = (compute_cost / total_cost) * 100

st.info(f"💡 {round(percentage,2)}% of your cost is from EC2 → possible over-provisioning")
if percentage > 60:
    st.warning("⚠️ High dependency on compute resources → Optimization needed urgently")
# -----------------------------
# Savings Calculation
# -----------------------------
total_savings = 0

for _, row in df.iterrows():
    if row["service"] == "EC2" and row["environment"] == "dev":
        total_savings += row["total_cost"] * 0.3

st.metric("Estimated Monthly Savings", f"₹{int(total_savings)}")
st.metric("Annual Savings Potential", f"₹{int(total_savings*12)}")

# -----------------------------
# Chart
# -----------------------------
st.subheader("Cost by Service")
st.bar_chart(df.groupby("service")["total_cost"].sum())

# -----------------------------
# Recommendations Table
# -----------------------------
st.subheader("Optimization Recommendations")
st.dataframe(df)

# -----------------------------
# Priority Alert
# -----------------------------
high_cost = df.sort_values(by="total_cost", ascending=False).iloc[0]
st.error(f"⚡ Highest cost: {high_cost['service']} → Optimize immediately")
st.subheader("What-if Simulator")

reduction = st.slider("Reduce EC2 usage (%)", 0, 50)

simulated_savings = compute_cost * (reduction / 100)

st.success(f"You can save ₹{int(simulated_savings)} monthly")

st.subheader("🤖 Ask Your Cloud Advisor")

user_question = st.text_input("Ask a question about your cloud cost:")

def chatbot_response(question):
    question = question.lower()

    if "cost" in question:
        return f"Your total monthly cloud cost is ₹{int(total_cost)}."

    elif "ec2" in question:
        return f"EC2 contributes {round(percentage,2)}% of total cost. Consider rightsizing or Reserved Instances."

    elif "savings" in question or "save" in question:
        return f"You can save approximately ₹{int(total_savings)} monthly and ₹{int(total_savings*12)} annually."

    elif "optimize" in question:
        return "Focus on EC2 rightsizing, S3 lifecycle policies, and Reserved Instances for long-term savings."

    elif "score" in question:
        return f"Your cloud efficiency score is {score}/100. Lower score indicates optimization opportunities."

    else:
        return "Try asking about cost, EC2, savings, or optimization."