import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from utils import preprocess

def show(df):
    st.title("🎯 New Customer Scorer")
    st.caption("Predict customer behavior and recommend strategies")

    st.markdown(" ")

    # -----------------------------
    # Sample File Download
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
    # Manual Input Option
    # -----------------------------
    st.markdown("### ✍️ Enter Single Customer")

    col1, col2 = st.columns(2)

    with col1:
        awareness = st.slider("Awareness", 1, 5, 3)
        price = st.slider("Price Sensitivity", 1, 5, 3)
        env = st.slider("Environmental Concern", 1, 5, 3)

    with col2:
        health = st.slider("Health Concern", 1, 5, 3)
        income = st.selectbox("Income", ["Low", "Medium", "High"])
        category = st.selectbox("Preferred Category", ["Fashion", "Home Products", "Food", "Personal Care"])

    if st.button("Predict Single Customer"):

        input_df = pd.DataFrame([{
            'Age': 25,
            'Gender': 'Male',
            'Income': income,
            'Occupation': 'Student',
            'Awareness': awareness,
            'Purchase_Frequency': 'Occasionally',
            'Environmental_Concern': env,
            'Health_Concern': health,
            'Social_Influence': 3,
            'Price_Sensitivity': price,
            'Availability_Issue': 2,
            'Preferred_Category': category,
            'Certification_Importance': 3,
            'Reviews_Importance': 3,
            'Brand_Story_Importance': 2,
            'UI_Expectation': 4,
            'Delivery_Expectation': 3
        }])

        combined = pd.concat([df, input_df], ignore_index=True)
        processed, _ = preprocess(combined)

        train = processed.iloc[:len(df)]
        test = processed.iloc[len(df):]

        X = train.drop('Purchase_Intent', axis=1)
        y = (train['Purchase_Intent'] > 3).astype(int)

        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)

        prob = model.predict_proba(test)[0][1]

        st.success(f"Purchase Probability: {prob:.2f}")

    st.markdown("---")

    # -----------------------------
    # Upload CSV
    # -----------------------------
    st.markdown("### 📤 Upload CSV for Bulk Prediction")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:

        new_df = pd.read_csv(uploaded_file)

        st.dataframe(new_df.head(), use_container_width=True)

        combined_df = pd.concat([df, new_df], ignore_index=True)
        processed_df, _ = preprocess(combined_df)

        train_df = processed_df.iloc[:len(df)]
        new_processed = processed_df.iloc[len(df):]

        X = train_df.drop('Purchase_Intent', axis=1)
        y = (train_df['Purchase_Intent'] > 3).astype(int)

        model = RandomForestClassifier(random_state=42)
        model.fit(X, y)

        preds = model.predict_proba(new_processed)[:, 1]
        new_df['Purchase_Probability'] = preds.round(2)

        st.markdown("### 📊 Results")
        st.dataframe(new_df, use_container_width=True)

        csv = new_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download Results",
            data=csv,
            file_name='predictions.csv',
            mime='text/csv'
        )

    else:
        st.info("Upload a CSV file or use manual input above")

    st.markdown("---")

    st.success("""
This tool enables:

• Real-time prediction  
• Customer segmentation  
• Personalized marketing  

👉 A complete decision-support system
""")
