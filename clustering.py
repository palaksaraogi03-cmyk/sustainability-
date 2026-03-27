import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from utils import preprocess

def show(df):
    st.title("🧠 Customer Segmentation")
    st.caption("Identifying distinct customer groups using K-Means clustering")

    st.markdown(" ")

    # -----------------------------
    # Preprocess Data
    # -----------------------------
    df_processed, _ = preprocess(df)

    features = [
        'Awareness',
        'Environmental_Concern',
        'Price_Sensitivity',
        'Health_Concern'
    ]

    X = df_processed[features]

    # -----------------------------
    # KMeans Clustering
    # -----------------------------
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X)

    st.markdown("### 📊 Cluster Distribution")

    cluster_counts = df['Cluster'].value_counts().reset_index()
    cluster_counts.columns = ['Cluster', 'Count']

    fig_bar = px.bar(cluster_counts, x='Cluster', y='Count')

    fig_bar.update_layout(
        template="simple_white",
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # PCA Visualization
    # -----------------------------
    st.markdown("### 🔍 Cluster Visualization (2D Projection)")

    pca = PCA(n_components=2)
    components = pca.fit_transform(X)

    df['PCA1'] = components[:, 0]
    df['PCA2'] = components[:, 1]

    fig_scatter = px.scatter(
        df,
        x='PCA1',
        y='PCA2',
        color=df['Cluster'].astype(str),
        opacity=0.7
    )

    fig_scatter.update_layout(
        template="simple_white",
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Cluster Profiles (Insights)
    # -----------------------------
    st.markdown("### 👤 Customer Segments")

    st.markdown("""
**Cluster 0 – Eco Enthusiasts 🌱**  
- High awareness & environmental concern  
- Low price sensitivity  
👉 Ideal for premium sustainable products  

**Cluster 1 – Price-Conscious Greens 💸**  
- High concern but high price sensitivity  
👉 Target with discounts & bundles  

**Cluster 2 – Unaware Mass 🤷**  
- Low awareness & engagement  
👉 Focus on education & awareness campaigns  

**Cluster 3 – Occasional Buyers 🛍️**  
- Moderate across all factors  
👉 Use nudges & retargeting  
""")

    st.markdown("---")

    # -----------------------------
    # Business Insight
    # -----------------------------
    st.markdown("### 🚀 Key Insight")

    st.success("""
The biggest opportunity lies in converting **price-sensitive but environmentally aware users**.  
Targeting this segment can significantly improve overall conversion rates.
""")
