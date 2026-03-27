import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from utils import preprocess

def show(df):
    st.title("🎯 New Customer Scorer")
    st.caption("Predict customer behavior and recommend strategies")

    st.markdown(" ")

    try:
        # -----------------------------
        # Upload Section
        # -----------------------------
        uploaded_file = st.file_uploader("📤 Upload New Customer Data (CSV)", type=["csv"])

        if uploaded_file is not None:

            new_df = pd.read_csv(uploaded_file)

            st.markdown("### 📄 Uploaded Data")
            st.dataframe(new_df.head(), use_container_width=True)

            st.markdown("---")

            # -----------------------------
            # Combine for preprocessing
            # -----------------------------
            combined_df = pd.concat([df, new_df], ignore_index=True)

            processed_df, _ = preprocess(combined_df)

            # Split back
            train_df = processed_df.iloc[:len(df)]
            new_processed = processed_df.iloc[len(df):]

            # -----------------------------
            # Train Model
            # -----------------------------
            X = train_df.drop('Purchase_Intent', axis=1)
            y = (train_df['Purchase_Intent'] > 3).astype(int)

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            # -----------------------------
            # Predict
            # -----------------------------
            predictions = model.predict_proba(new_processed)[:, 1]

            new_df['Purchase_Probability'] = predictions.round(2)

            # -----------------------------
            # Segment Assignment
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
                    return "Show premium sustainable products"
                elif segment == "Price-Conscious Green":
                    return "Offer discounts and bundles"
                elif segment == "Unaware User":
                    return "Show educational content"
                else:
                    return "Use retargeting ads"

            new_df['Recommendation'] = new_df['Segment'].apply(recommend)

            # -----------------------------
            # Output
            # -----------------------------
            st.markdown("### 📊 Predictions & Recommendations")

            st.dataframe(new_df, use_container_width=True)

            st.markdown("---")

            # -----------------------------
            # Download Option
            # -----------------------------
            csv = new_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Download Results",
                data=csv,
                file_name='customer_predictions.csv',
                mime='text/csv'
            )

            st.markdown("---")

            # -----------------------------
            # Insight
            # -----------------------------
            st.success("""
This system enables real-time decision making:

• Identify high-value customers  
• Personalize marketing strategies  
• Improve conversion rates  

👉 Transforms raw data into actionable intelligence
""")

        else:
            st.info("Upload a CSV file to start predictions")

    except Exception as e:
        st.error("Error in scorer page")
        st.write(e)
