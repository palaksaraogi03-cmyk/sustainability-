import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from utils import preprocess

def show(df):
    st.title("🧠 Customer Segmentation")
    st.caption("Identifying distinct customer groups using K-Means clustering")

    st.markdown(" ")

    try:
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
        # KMeans
        # -----------------------------
        kmeans = KMeans(n_clusters=4, random_state=42)
        clusters = kmeans.fit_predict(X)

        df['Cluster'] = clusters

        # -----------------------------
        # Cluster Distribution
        # -----------------------------
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
        st.markdown("### 🔍 Cluster Visualization")

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
        # Insights
        # -----------------------------
        st.markdown("### 👤 Customer Segments")

        st.markdown("""
**Cluster 0 – Eco Enthusiasts 🌱**  
High awareness, low price sensitivity → premium users  

**Cluster 1 – Price-Conscious Greens 💸**  
High concern, high price sensitivity → discounts needed  

**Cluster 2 – Unaware Users 🤷**  
Low awareness → education needed  

**Cluster 3 – Occasional Buyers 🛍️**  
Moderate behavior → nudges & retargeting  
""")

        st.markdown("---")

        st.success("""
Biggest opportunity: Convert **price-sensitive eco-conscious users** using targeted offers.
""")

    except Exception as e:
        st.error("Error in clustering page")
        st.write(e)
