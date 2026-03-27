import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def show(df):
    st.title("🔗 Association Rules")
    st.caption("Discovering patterns in customer behavior")

    st.markdown(" ")

    try:
        # -----------------------------
        # Prepare Data (One-hot encoding)
        # -----------------------------
        df_rules = df.copy()

        df_rules = df_rules[[
            'Preferred_Category',
            'Purchase_Frequency',
            'Income'
        ]]

        df_encoded = pd.get_dummies(df_rules)

        # -----------------------------
        # Apply Apriori
        # -----------------------------
        freq_items = apriori(
            df_encoded,
            min_support=0.1,
            use_colnames=True
        )

        rules = association_rules(
            freq_items,
            metric="confidence",
            min_threshold=0.5
        )

        # Sort rules
        rules = rules.sort_values(by="lift", ascending=False)

        st.markdown("### 📊 Top Association Rules")

        # Clean display
        display_rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].copy()

        # Convert frozenset to string
        display_rules['antecedents'] = display_rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        display_rules['consequents'] = display_rules['consequents'].apply(lambda x: ', '.join(list(x)))

        st.dataframe(display_rules.head(10), use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # Key Insights
        # -----------------------------
        st.markdown("### 🔍 Key Insights")

        if not display_rules.empty:
            top_rule = display_rules.iloc[0]

            st.markdown(f"""
- Customers who show **{top_rule['antecedents']}** are likely to also show **{top_rule['consequents']}**
- High lift ({top_rule['lift']:.2f}) indicates a strong relationship
- These patterns can be used for targeted marketing
""")
        else:
            st.info("No strong association rules found. Try adjusting thresholds.")

        st.markdown("---")

        # -----------------------------
        # Business Recommendations
        # -----------------------------
        st.markdown("### 🚀 Business Applications")

        st.success("""
Use association rules to:

• Recommend related products  
• Personalize marketing campaigns  
• Bundle products effectively  
• Improve cross-selling strategies  

👉 Helps increase conversion and basket size
""")

    except Exception as e:
        st.error("Error in association rules page")
        st.write(e)
