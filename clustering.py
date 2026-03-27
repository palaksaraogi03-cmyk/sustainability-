import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
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
        # KMeans Clustering
        # -----------------------------
        kmeans = KMeans(n_clusters=4, random_state=42)
        df['Cluster'] = kmeans.fit_predict(X)

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
        # PCA Transformation
        # -----------------------------
        pca = PCA(n_components=2)
        components = pca.fit_transform(X)

        df['PCA1'] = components[:, 0]
        df['PCA2'] = components[:, 1]

        # -----------------------------
        # PREMIUM SCATTER PLOT
        # -----------------------------
        st.markdown("### 🔍 Customer Segments Visualization")

        fig = go.Figure()

        colors = ["#6366F1", "#10B981", "#F59E0B", "#EF4444"]

        for i in range(4):
            cluster_data = df[df['Cluster'] == i]

            fig.add_trace(go.Scatter(
                x=cluster_data['PCA1'],
                y=cluster_data['PCA2'],
                mode='markers',
                name=f"Cluster {i}",
                marker=dict(
                    size=8,
                    color=colors[i],
                    opacity=0.7
                )
            ))

        # -----------------------------
        # Add Cluster Centers (🔥 KEY)
        # -----------------------------
        centers = []
        for i in range(4):
            cluster_data = df[df['Cluster'] == i]
            centers.append([
                cluster_data['PCA1'].mean(),
                cluster_data['PCA2'].mean()
            ])

        centers = np.array(centers)

        fig.add_trace(go.Scatter(
            x=centers[:, 0],
            y=centers[:, 1],
            mode='markers+text',
            name="Centers",
            marker=dict(
                size=18,
                color="black",
                symbol="x"
            ),
            text=[f"C{i}" for i in range(4)],
            textposition="top center"
        ))

        fig.update_layout(
            template="simple_white",
            title="Customer Segments (PCA Projection)",
            margin=dict(l=10, r=10, t=40, b=10),
            legend_title="Clusters"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # Segment Profiles
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

        # -----------------------------
        # Key Business Insight
        # -----------------------------
        st.markdown("### 🚀 Key Insight")

        st.success("""
Biggest opportunity lies in converting **price-sensitive eco-conscious users**  
through targeted pricing and awareness strategies.
""")

    except Exception as e:
        st.error("Error in clustering page")
        st.write(e)
