import streamlit as st
import pandas as pd
import plotly.express as px
from mlxtend.frequent_patterns import apriori, association_rules

def show(df):
    st.title("🔗 Association Rules")
    st.caption("Discovering patterns in customer behavior")

    st.markdown(" ")

    try:
        # -----------------------------
        # Prepare Data
        # -----------------------------
        df_rules = df[['Preferred_Category', 'Purchase_Frequency', 'Income']]
        df_encoded = pd.get_dummies(df_rules)

        # -----------------------------
        # Apriori
        # -----------------------------
        freq_items = apriori(df_encoded, min_support=0.1, use_colnames=True)

        rules = association_rules(freq_items, metric="confidence", min_threshold=0.5)

        if rules.empty:
            st.warning("No strong association rules found.")
            return

        rules = rules.sort_values(by="lift", ascending=False)

        # Clean columns
        rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

        st.markdown("### 🎯 Top Rule Insight")

        top_rule = rules.iloc[0]

        st.success(f"""
**If a user shows:** {top_rule['antecedents']}  
👉 They are likely to also show: **{top_rule['consequents']}**

Lift: {top_rule['lift']:.2f} | Confidence: {top_rule['confidence']:.2f}
""")

        st.markdown("---")

        # -----------------------------
        # VISUAL: Lift Chart
        # -----------------------------
        st.markdown("### 📊 Strongest Associations (by Lift)")

        top_rules = rules.head(8).copy()
        top_rules['rule'] = top_rules['antecedents'] + " → " + top_rules['consequents']

        fig = px.bar(
            top_rules,
            x='lift',
            y='rule',
            orientation='h'
        )

        fig.update_layout(
            template="simple_white",
            margin=dict(l=10, r=10, t=30, b=10),
            yaxis_title="Rule",
            xaxis_title="Lift"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # Table (clean)
        # -----------------------------
        st.markdown("### 📋 Rule Details")

        display_cols = ['antecedents', 'consequents', 'support', 'confidence', 'lift']

        st.dataframe(
            rules[display_cols].head(10),
            use_container_width=True
        )

        st.markdown("---")

        # -----------------------------
        # Insights
        # -----------------------------
        st.markdown("### 🔍 Key Insights")

        st.markdown("""
- High lift values indicate **strong relationships between behaviors**
- Certain customer groups tend to exhibit **predictable patterns**
- These insights help in **personalization and targeting**
""")

        st.markdown("---")

        # -----------------------------
        # Business Use
        # -----------------------------
        st.markdown("### 🚀 Business Applications")

        st.success("""
Use these rules to:

• Recommend related products  
• Create smart bundles  
• Personalize user journeys  
• Improve cross-selling  

👉 This directly increases conversion and revenue
""")

    except Exception as e:
        st.error("Error in association rules page")
        st.write(e)
