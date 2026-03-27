import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from utils import preprocess

def show(df):
    st.title("🎯 New Customer Scorer")
    st.caption("Predict behavior and generate smart recommendations")

    st.markdown(" ")

    try:
        # -----------------------------
        # Upload Section
        # -----------------------------
        st.markdown("### 📤 Upload Customer Data")

        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

        if uploaded_file is not None:

            new_df = pd.read_csv(uploaded_file)

            st.markdown("### 📄 Uploaded Preview")
            st.dataframe(new_df.head(), use_container_width=True)

            st.markdown("---")

            # -----------------------------
            # Preprocess
            # -----------------------------
            combined_df = pd.concat([df, new_df], ignore_index=True)
            processed_df, _ = preprocess(combined_df)

            train_df = processed_df.iloc[:len(df)]
            new_processed = processed_df.iloc[len(df):]

            X = train_df.drop('Purchase_Intent', axis=1)
            y = (train_df['Purchase_Intent'] > 3).astype(int)

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            # Fix column alignment
            new_processed = new_processed[X.columns]

            preds = model.predict_proba(new_processed)[:, 1]
            new_df['Purchase_Probability'] = preds.round(2)

            # -----------------------------
            # Segment + Recommendation
            # -----------------------------
            def assign_segment(row):
                if row['Awareness'] >= 4 and row['Price_Sensitivity'] <= 2:
                    return "Eco Enthusiast"
                elif row['Awareness'] >= 4 and row['Price_Sensitivity'] >= 4:
                    return "Price-Conscious Green"
                elif row['Awareness'] <= 2:
                    return "Unaware User"
                else:
                    return "Occasional Buyer"

            def recommend(segment):
                if segment == "Eco Enthusiast":
                    return "Promote premium products"
                elif segment == "Price-Conscious Green":
                    return "Offer discounts"
                elif segment == "Unaware User":
                    return "Educate user"
                else:
                    return "Retarget user"

            new_df['Segment'] = new_df.apply(assign_segment, axis=1)
            new_df['Recommendation'] = new_df['Segment'].apply(recommend)

            # -----------------------------
            # 🎯 EXECUTIVE SUMMARY (LIKE MUSE)
            # -----------------------------
            st.markdown("### 🧠 Summary")

            avg_prob = new_df['Purchase_Probability'].mean()
            high_users = (new_df['Purchase_Probability'] > 0.7).sum()

            st.markdown(f"""
- Average purchase likelihood: **{avg_prob:.2f}**  
- High intent users: **{high_users} users**  
- Majority segment: **{new_df['Segment'].mode()[0]}**
""")

            st.markdown("---")

            # -----------------------------
            # 🌟 TOP USERS
            # -----------------------------
            st.markdown("### 🌟 High-Value Customers")

            top = new_df.sort_values(by="Purchase_Probability", ascending=False).head(3)

            for i, row in top.iterrows():
                st.info(f"""
**User {i+1}**
- Probability: {row['Purchase_Probability']}
- Segment: {row['Segment']}
- Strategy: {row['Recommendation']}
""")

            st.markdown("---")

            # -----------------------------
            # 📈 VISUAL (CLEAN)
            # -----------------------------
            st.markdown("### 📊 Distribution")

            fig = px.histogram(new_df, x="Purchase_Probability")

            fig.update_layout(template="simple_white")

            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # -----------------------------
            # 📋 OPTIONAL TABLE
            # -----------------------------
            with st.expander("View Full Data"):
                st.dataframe(new_df, use_container_width=True)

            # -----------------------------
            # Download
            # -----------------------------
            csv = new_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Download Results",
                data=csv,
                file_name="predictions.csv",
                mime="text/csv"
            )

            st.markdown("---")

            # -----------------------------
            # FINAL INSIGHT
            # -----------------------------
            st.success("""
Focus on **high probability + price-sensitive users**  
→ They give highest conversion uplift with offers
""")

        else:
            st.info("Upload a CSV file to begin")

    except Exception as e:
        st.error("Error in scorer page")
        st.write(e)
