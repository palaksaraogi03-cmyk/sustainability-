import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.cluster import KMeans
from utils import preprocess

def show(df):
    st.title("🧠 Customer Segmentation")
    st.caption("Understanding different customer groups")

    st.markdown(" ")

    try:
        # -----------------------------
        # Preprocess
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
        df['Cluster'] = kmeans.fit_predict(X)

        # -----------------------------
        # Cluster Size
        # -----------------------------
        st.markdown("### 📊 Cluster Distribution")

        cluster_counts = df['Cluster'].value_counts().reset_index()
        cluster_counts.columns = ['Cluster', 'Count']

        fig_bar = px.bar(cluster_counts, x='Cluster', y='Count')

        fig_bar.update_layout(template="simple_white")
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # CLUSTER PROFILE (🔥 BEST VISUAL)
        # -----------------------------
        st.markdown("### 📈 Cluster Characteristics")

        cluster_profile = df.groupby('Cluster')[features].mean().reset_index()

        fig_profile = px.bar(
            cluster_profile.melt(id_vars="Cluster"),
            x="variable",
            y="value",
            color="Cluster",
            barmode="group"
        )

        fig_profile.update_layout(
            template="simple_white",
            xaxis_title="Features",
            yaxis_title="Average Score"
        )

        st.plotly_chart(fig_profile, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # SIMPLE SCATTER (OPTIONAL CLEAN)
        # -----------------------------
        st.markdown("### 🔍 Simplified View")

        fig_scatter = px.scatter(
            df,
            x="Awareness",
            y="Price_Sensitivity",
            color=df['Cluster'].astype(str),
            opacity=0.6
        )

        fig_scatter.update_layout(template="simple_white")

        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # SEGMENT EXPLANATION
        # -----------------------------
        st.markdown("### 👤 Customer Segments")

        st.markdown("""
**Cluster 0 – Eco Enthusiasts 🌱**  
High awareness, low price sensitivity → premium segment  

**Cluster 1 – Price-Conscious Greens 💸**  
High concern but price sensitive → discount-focused  

**Cluster 2 – Unaware Users 🤷**  
Low awareness → education needed  

**Cluster 3 – Occasional Buyers 🛍️**  
Moderate behavior → retargeting  
""")

        st.markdown("---")

        # -----------------------------
        # BUSINESS INSIGHT
        # -----------------------------
        st.markdown("### 🚀 Key Insight")

        st.success("""
Focus on **price-sensitive eco-conscious users** —  
this segment has the highest potential for conversion improvement.
""")

    except Exception as e:
        st.error("Error in clustering page")
        st.write(e)
