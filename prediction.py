import streamlit as st
import pandas as pd
import plotly.express as px
from mlxtend.frequent_patterns import apriori, association_rules

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

    st.title("🔗 Association Rules")
    st.caption("Understanding relationships between customer preferences")

    try:
        # -----------------------------
        # SELECT FEATURES
        # -----------------------------
        selected = df[[
            "Awareness",
            "Environmental_Concern",
            "Health_Concern",
            "Price_Sensitivity",
            "Certification_Importance",
            "Reviews_Importance"
        ]]

        # -----------------------------
        # BINARIZE
        # -----------------------------
        binary = selected.applymap(lambda x: 1 if x >= 4 else 0)

        # -----------------------------
        # APRIORI
        # -----------------------------
        frequent = apriori(binary, min_support=0.2, use_colnames=True)

        rules = association_rules(frequent, metric="confidence", min_threshold=0.6)

        # -----------------------------
        # HANDLE EMPTY RULES 🔥
        # -----------------------------
        if rules.empty:
            st.warning("No strong association rules found. Try adjusting thresholds.")
            return

        # -----------------------------
        # CLEAN RULE FORMAT
        # -----------------------------
        rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

        # Ensure numeric
        rules['confidence'] = rules['confidence'].astype(float)
        rules['lift'] = rules['lift'].astype(float)
        rules['support'] = rules['support'].astype(float)

        # -----------------------------
        # TOP RULES
        # -----------------------------
        st.markdown("### 🔥 Top Rules")

        top_rules = rules.sort_values(by="confidence", ascending=False).head(5)

        for _, row in top_rules.iterrows():
            st.info(f"""
**IF:** {row['antecedents']}  
**THEN:** {row['consequents']}  

Confidence: {row['confidence']:.2f}  
Lift: {row['lift']:.2f}
""")

        st.markdown("---")

        # -----------------------------
        # BAR CHART (CONFIDENCE)
        # -----------------------------
        st.markdown("### 📊 Rule Strength (Confidence)")

        fig = px.bar(
            top_rules,
            x="confidence",
            y="antecedents",
            orientation='h',
            color_discrete_sequence=["#74c69d"]
        )

        fig.update_layout(
            template="simple_white",
            paper_bgcolor="#f7fcf9",
            plot_bgcolor="#f7fcf9",
            font=dict(color="#1b4332")
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # LIFT SCATTER (FIXED 🔥)
        # -----------------------------
        st.markdown("### 📈 Lift Analysis")

        fig2 = px.scatter(
            rules,
            x="support",
            y="lift",
            color="confidence",  # better visual encoding
            color_continuous_scale=["#d8f3dc", "#52b788"],
            opacity=0.7
        )

        fig2.update_layout(
            template="simple_white",
            paper_bgcolor="#f7fcf9",
            plot_bgcolor="#f7fcf9",
            font=dict(color="#1b4332")
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # INSIGHTS
        # -----------------------------
        st.markdown("### 🧠 Key Insights")

        st.markdown("""
- High awareness users prefer certifications  
- Health-conscious users rely on reviews  
- Strong relationships exist between trust signals  

👉 Combining features improves conversions
""")

        st.markdown("---")

        # -----------------------------
        # BUSINESS USE
        # -----------------------------
        st.markdown("### 🚀 Business Application")

        st.success("""
Use association rules to:

• Bundle product features  
• Recommend combinations  
• Improve cross-selling  

👉 Example: Show certifications + reviews together
""")

    except Exception as e:
        st.error("Error in association page")
        st.write(e)
