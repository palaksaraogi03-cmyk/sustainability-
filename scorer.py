import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from utils import preprocess

def show(df):
    st.title("🎯 New Customer Scorer")
    st.caption("Predict customer behavior and recommend strategies")

    st.markdown(" ")

    try:
        # -----------------------------
        # SAMPLE DOWNLOAD
        # -----------------------------
        st.markdown("### 📥 Download Sample Template")

        sample = df.drop(columns=['Purchase_Intent']).head(5)
        csv_sample = sample.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download Sample CSV",
            data=csv_sample,
            file_name="sample_input.csv",
            mime="text/csv"
        )

        st.markdown("---")

        # -----------------------------
        # FILE UPLOAD
        # -----------------------------
        st.markdown("### 📤 Upload CSV")

        uploaded_file = st.file_uploader("Upload New Customer Data", type=["csv"])

        if uploaded_file is not None:

            new_df = pd.read_csv(uploaded_file)

            st.markdown("### 📄 Uploaded Data")
            st.dataframe(new_df, use_container_width=True)

            st.markdown("---")

            # -----------------------------
            # Combine for preprocessing
            # -----------------------------
            combined_df = pd.concat([df, new_df], ignore_index=True)

            processed_df, _ = preprocess(combined_df)

            train_df = processed_df.iloc[:len(df)]
            new_processed = processed_df.iloc[len(df):]

            # -----------------------------
            # Train model
            # -----------------------------
            X = train_df.drop('Purchase_Intent', axis=1)
            y = (train_df['Purchase_Intent'] > 3).astype(int)

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            # -----------------------------
            # FIX: Align columns
            # -----------------------------
            new_processed = new_processed[X.columns]

            # -----------------------------
            # Predict
            # -----------------------------
            st.info("Running predictions...")

            preds = model.predict_proba(new_processed)[:, 1]
            new_df['Purchase_Probability'] = preds.round(2)

            # -----------------------------
            # Segment Logic
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

            new_df['Segment'] = new_df.apply(assign_segment, axis=1)

            # -----------------------------
            # Recommendation Engine
            # -----------------------------
            def recommend(segment):
                if segment == "Eco Enthusiast":
                    return "Promote premium sustainable products"
                elif segment == "Price-Conscious Green":
                    return "Offer discounts and bundles"
                elif segment == "Unaware User":
                    return "Show educational content"
                else:
                    return "Use retargeting and reminders"

            new_df['Recommendation'] = new_df['Segment'].apply(recommend)

            # -----------------------------
            # 🎯 PREMIUM OUTPUT STARTS HERE
            # -----------------------------
            st.markdown("### 📊 Prediction Summary")

            # KPI Cards
            avg_prob = new_df['Purchase_Probability'].mean()
            high_intent = (new_df['Purchase_Probability'] > 0.7).sum()

            col1, col2 = st.columns(2)

            col1.metric("Avg Purchase Probability", f"{avg_prob:.2f}")
            col2.metric("High Intent Users", high_intent)

            st.markdown("---")

            # Top Users
            st.markdown("### 🌟 Top High-Intent Customers")

            top_users = new_df.sort_values(
                by="Purchase_Probability",
                ascending=False
            ).head(5)

            st.dataframe(
                top_users.style.highlight_max(
                    axis=0,
                    subset=['Purchase_Probability']
                ),
                use_container_width=True
            )

            st.markdown("---")

            # Distribution Chart
            st.markdown("### 📈 Probability Distribution")

            fig = px.histogram(
                new_df,
                x="Purchase_Probability",
                nbins=10
            )

            fig.update_layout(
                template="simple_white",
                margin=dict(l=10, r=10, t=30, b=10)
            )

            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # Clean Table
            st.markdown("### 📋 All Customers")

            st.dataframe(
                new_df.sort_values(
                    by="Purchase_Probability",
                    ascending=False
                ),
                use_container_width=True
            )

            st.markdown("---")

            # Download Results
            csv = new_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Download Results",
                data=csv,
                file_name="customer_predictions.csv",
                mime="text/csv"
            )

            st.markdown("---")

            # Final Insight
            st.success("""
This system enables:

• Identification of high-value customers  
• Personalized marketing strategies  
• Improved conversion rates  

👉 Transforms raw data into actionable business decisions
""")

        else:
            st.info("Upload a CSV file to start predictions")

    except Exception as e:
        st.error("Error in scorer page")
        st.write(e)
