import streamlit as st
import plotly.express as px

# -----------------------------
# HEADER
# -----------------------------
def header():
    col1, col2 = st.columns([1, 6])

    with col1:
        st.image("logo.png", width=60)

    with col2:
        st.markdown("## EcoSense AI")


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def show(df):

    header()
    st.markdown("---")

    st.title("📊 Descriptive Analysis")
    st.caption("Understanding customer demographics and behavior")

    # -----------------------------
    # AGE DISTRIBUTION
    # -----------------------------
    st.markdown("### 👥 Age Distribution")

    fig_age = px.histogram(
        df,
        x="Age",
        nbins=20,
        color_discrete_sequence=["#74c69d"]
    )

    fig_age.update_layout(
        template="simple_white",
        paper_bgcolor="#f7fcf9",
        plot_bgcolor="#f7fcf9",
        font=dict(color="#1b4332")
    )

    st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # GENDER DISTRIBUTION
    # -----------------------------
    st.markdown("### 👤 Gender Distribution")

    fig_gender = px.pie(
        df,
        names="Gender",
        color_discrete_sequence=[
            "#52b788",
            "#74c69d",
            "#95d5b2"
        ]
    )

    fig_gender.update_traces(textinfo="percent+label")

    fig_gender.update_layout(
        template="simple_white",
        paper_bgcolor="#f7fcf9",
        font=dict(color="#1b4332")
    )

    st.plotly_chart(fig_gender, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # INCOME DISTRIBUTION (FIXED 🔥)
    # -----------------------------
    st.markdown("### 💰 Income Distribution")

    income_counts = df["Income"].value_counts().reset_index()
    income_counts.columns = ["Income Level", "Count"]

    fig_income = px.bar(
        income_counts,
        x="Income Level",
        y="Count",
        color_discrete_sequence=["#74c69d"]
    )

    fig_income.update_layout(
        template="simple_white",
        paper_bgcolor="#f7fcf9",
        plot_bgcolor="#f7fcf9",
        font=dict(color="#1b4332")
    )

    st.plotly_chart(fig_income, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # PURCHASE FREQUENCY (FIXED 🔥)
    # -----------------------------
    st.markdown("### 🛒 Purchase Frequency")

    freq_counts = df["Purchase_Frequency"].value_counts().reset_index()
    freq_counts.columns = ["Frequency", "Count"]

    fig_freq = px.bar(
        freq_counts,
        x="Frequency",
        y="Count",
        color_discrete_sequence=["#74c69d"]
    )

    fig_freq.update_layout(
        template="simple_white",
        paper_bgcolor="#f7fcf9",
        plot_bgcolor="#f7fcf9",
        font=dict(color="#1b4332")
    )

    st.plotly_chart(fig_freq, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # AWARENESS LEVEL
    # -----------------------------
    st.markdown("### 📱 Awareness Levels")

    fig_awareness = px.histogram(
        df,
        x="Awareness",
        color_discrete_sequence=["#74c69d"]
    )

    fig_awareness.update_layout(
        template="simple_white",
        paper_bgcolor="#f7fcf9",
        plot_bgcolor="#f7fcf9",
        font=dict(color="#1b4332")
    )

    st.plotly_chart(fig_awareness, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # INSIGHTS
    # -----------------------------
    st.markdown("### 🔍 Key Insights")

    st.markdown("""
- Majority users are young adults  
- Balanced gender distribution  
- Medium income group dominates  
- Most users purchase occasionally  
- Awareness is moderate but growing  

👉 Opportunity: Educate users to increase adoption
""")
