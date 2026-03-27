import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

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

    st.title("🚀 Prescriptive Analysis")
    st.caption("Turning insights into actionable strategies")

    try:
        # -----------------------------
        # CLUSTERING
        # -----------------------------
        features = [
            "Awareness",
            "Price_Sensitivity",
            "Environmental_Concern",
            "Health_Concern"
        ]

        X = df[features]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=4, random_state=42)
        df['Cluster'] = kmeans.fit_predict(X_scaled)

        # -----------------------------
        # PREDICTION MODEL
        # -----------------------------
        df_model = df.copy()
        df_model['Target'] = (df_model['Purchase_Intent'] > 3).astype(int)

        model_features = [
            "Age",
            "Awareness",
            "Environmental_Concern",
            "Health_Concern",
            "Price_Sensitivity"
        ]

        X_model = df_model[model_features].fillna(df_model.mean())
        y_model = df_model['Target']

        X_train, X_test, y_train, y_test = train_test_split(
            X_model, y_model, test_size=0.2, random_state=42
        )

        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        df['Adoption_Probability'] = model.predict_proba(X_model)[:, 1]

        # -----------------------------
        # CLUSTER DISTRIBUTION
        # -----------------------------
        st.markdown("### 👥 Customer Segments")

        cluster_counts = df['Cluster'].value_counts().reset_index()
        cluster_counts.columns = ["Cluster", "Count"]

        fig = px.bar(
            cluster_counts,
            x="Cluster",
            y="Count",
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
        # SEGMENT STRATEGY
        # -----------------------------
        st.markdown("### 🎯 Segment-wise Strategy")

        st.info("""
**Cluster 0 – Premium Users**
• Low price sensitivity  
• High awareness  
👉 Offer premium eco-products  

**Cluster 1 – Price Sensitive**
• High awareness + high price concern  
👉 Discounts & bundles  

**Cluster 2 – Low Awareness**
👉 Awareness campaigns + education  

**Cluster 3 – Casual Users**
👉 Retargeting & engagement  
""")

        st.markdown("---")

        # -----------------------------
        # HIGH VALUE USERS
        # -----------------------------
        st.markdown("### 💎 High Value Customers")

        high_value = df[df['Adoption_Probability'] > 0.7]

        st.metric("High Value Users", len(high_value))

        st.markdown("""
👉 These users are most likely to convert  
👉 Focus marketing spend here  
""")

        st.markdown("---")

        # -----------------------------
        # PRICING STRATEGY
        # -----------------------------
        st.markdown("### 💰 Pricing Strategy")

        avg_price_sensitivity = df['Price_Sensitivity'].mean()

        if avg_price_sensitivity > 3:
            st.warning("Users are price sensitive → Keep pricing competitive")
        else:
            st.success("Users are less price sensitive → Premium pricing possible")

        st.markdown("---")

        # -----------------------------
        # FEATURE STRATEGY
        # -----------------------------
        st.markdown("### 🧩 Feature Strategy")

        st.markdown("""
Top features to highlight:

• Certifications  
• Reviews  
• Health benefits  

👉 These drive trust and conversions
""")

        st.markdown("---")

        # -----------------------------
        # FINAL RECOMMENDATION
        # -----------------------------
        st.markdown("### 🚀 Final Recommendation")

        st.success("""
1. Target high-probability users  
2. Offer discounts to price-sensitive segments  
3. Highlight trust signals (reviews + certifications)  
4. Educate low-awareness users  

👉 This maximizes conversions and ROI
""")

    except Exception as e:
        st.error("Error in prescriptive page")
        st.write(e)
