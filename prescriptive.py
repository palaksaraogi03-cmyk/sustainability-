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
        df = df.copy()

        # -----------------------------
        # SAFE FEATURE SELECTION
        # -----------------------------
        cluster_features = [
            "Awareness",
            "Price_Sensitivity",
            "Environmental_Concern",
            "Health_Concern"
        ]

        cluster_features = [c for c in cluster_features if c in df.columns]

        X = df[cluster_features].apply(pd.to_numeric, errors='coerce')
        X = X.fillna(X.mean())

        # -----------------------------
        # CLUSTERING
        # -----------------------------
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=4, random_state=42)
        df["Cluster"] = kmeans.fit_predict(X_scaled)

        # -----------------------------
        # TARGET CREATION
        # -----------------------------
        if "Purchase_Intent" not in df.columns:
            st.error("Purchase_Intent column missing")
            return

        df["Target"] = (df["Purchase_Intent"] > 3).astype(int)

        # -----------------------------
        # MODEL FEATURES
        # -----------------------------
        model_features = [
            "Age",
            "Awareness",
            "Environmental_Concern",
            "Health_Concern",
            "Price_Sensitivity"
        ]

        model_features = [c for c in model_features if c in df.columns]

        X_model = df[model_features].apply(pd.to_numeric, errors='coerce')
        X_model = X_model.fillna(X_model.mean())

        y = df["Target"]

        # -----------------------------
        # TRAIN MODEL
        # -----------------------------
        X_train, X_test, y_train, y_test = train_test_split(
            X_model, y, test_size=0.2, random_state=42
        )

        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        df["Adoption_Probability"] = model.predict_proba(X_model)[:, 1]

        # -----------------------------
        # CLUSTER VISUAL
        # -----------------------------
        st.markdown("### 👥 Customer Segments")

        cluster_counts = df["Cluster"].value_counts().reset_index()
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
            plot_bgcolor="#f7fcf9"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # HIGH VALUE USERS
        # -----------------------------
        st.markdown("### 💎 High Value Customers")

        high_value = df[df["Adoption_Probability"] > 0.7]

        st.metric("High Value Users", len(high_value))

        # -----------------------------
        # STRATEGY
        # -----------------------------
        st.markdown("### 🎯 Strategy Recommendations")

        st.success("""
1. Target high-probability users for conversion  
2. Offer discounts to price-sensitive segments  
3. Promote certifications & reviews  
4. Educate low-awareness users  

👉 Maximizes ROI and conversion
""")

    except Exception as e:
        st.error("Error in prescriptive page")
        st.write(e)
