import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

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

    st.title("🔍 Customer Segmentation")
    st.caption("Grouping customers based on behavior")

    try:
        # -----------------------------
        # SELECT FEATURES
        # -----------------------------
        features = [
            "Awareness",
            "Price_Sensitivity",
            "Environmental_Concern",
            "Health_Concern",
            "Social_Influence"
        ]

        X = df[features]

        # -----------------------------
        # SCALE
        # -----------------------------
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # -----------------------------
        # KMEANS
        # -----------------------------
        kmeans = KMeans(n_clusters=4, random_state=42)
        df['Cluster'] = kmeans.fit_predict(X_scaled)

        # -----------------------------
        # PCA (for visualization)
        # -----------------------------
        pca = PCA(n_components=2)
        components = pca.fit_transform(X_scaled)

        df['PC1'] = components[:, 0]
        df['PC2'] = components[:, 1]

        # -----------------------------
        # CLEAN SCATTER (PASTEL 🌿)
        # -----------------------------
        st.markdown("### 📊 Customer Segments")

        fig = px.scatter(
            df,
            x="PC1",
            y="PC2",
            color=df["Cluster"].astype(str),
            color_discrete_sequence=[
                "#52b788",
                "#74c69d",
                "#95d5b2",
                "#b7e4c7"
            ],
            opacity=0.7
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
        # SEGMENT PROFILES
        # -----------------------------
        st.markdown("### 📋 Segment Profiles")

        cluster_summary = df.groupby("Cluster")[features].mean().round(2)

        st.dataframe(
            cluster_summary.style.set_properties(**{
                'background-color': '#ffffff',
                'color': '#1b4332'
            }),
            use_container_width=True
        )

        st.markdown("---")

        # -----------------------------
        # SEGMENT INTERPRETATION
        # -----------------------------
        st.markdown("### 🧠 Segment Insights")

        st.markdown("""
**Cluster 0 – Premium Eco Users**
- High awareness  
- Low price sensitivity  
👉 Target with premium products  

**Cluster 1 – Price-Sensitive Greens**
- High awareness  
- High price sensitivity  
👉 Offer discounts  

**Cluster 2 – Unaware Users**
- Low awareness  
👉 Focus on education  

**Cluster 3 – Casual Buyers**
- Moderate behavior  
👉 Use retargeting strategies  
""")

        st.markdown("---")

        # -----------------------------
        # BUSINESS STRATEGY
        # -----------------------------
        st.markdown("### 🚀 Business Application")

        st.success("""
Customer segmentation enables:

• Personalized marketing  
• Better targeting  
• Improved conversion  

👉 Focus on Cluster 1 for highest growth potential
""")

    except Exception as e:
        st.error("Error in clustering page")
        st.write(e)
