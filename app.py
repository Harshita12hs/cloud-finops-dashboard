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
score = 100 - int((compute_cost / total_cost) * 50)

st.metric("Cloud Efficiency Score", f"{score}/100")

percentage = (compute_cost / total_cost) * 100

st.info(f"💡 {round(percentage,2)}% of your cost is from EC2 → possible over-provisioning")

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

    if "ec2" in question:
        return "EC2 cost is high. Consider Reserved Instances or reduce usage during off-hours."

    elif "s3" in question:
        return "Move infrequent data to Glacier to save up to 60%."

    elif "rds" in question:
        return "Use Reserved DB instances to reduce long-term cost."

    elif "save" in question:
        return f"You can save approximately ₹{int(total_savings)} monthly."

    else:
        return "Analyze high-cost services like EC2 and optimize usage."

if user_question:
    response = chatbot_response(user_question)
    st.success(f"🤖 {response}")