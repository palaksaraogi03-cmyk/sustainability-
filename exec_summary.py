import streamlit as st
import plotly.express as px

def show(df):
    # -----------------------------
    # Header
    # -----------------------------
    st.title("🌱 Sustainable Marketplace")
    st.caption("Data-driven insights for eco-conscious commerce")

    st.markdown(" ")

    # -----------------------------
    # KPIs (Styled Cards)
    # -----------------------------
    high_intent = (df['Purchase_Intent'] > 3).mean() * 100
    avg_awareness = df['Awareness'].mean()
    avg_price_sensitivity = df['Price_Sensitivity'].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("High Purchase Intent", f"{high_intent:.1f}%")

    with col2:
        st.metric("Avg Awareness", f"{avg_awareness:.2f}")

    with col3:
        st.metric("Price Sensitivity", f"{avg_price_sensitivity:.2f}")

    st.markdown("---")

    # -----------------------------
    # Category Distribution
    # -----------------------------
    st.markdown("### 🛍️ Product Preferences")

    fig = px.pie(df, names="Preferred_Category")

    fig.update_layout(
        template="simple_white",
        showlegend=True,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Awareness vs Purchase Intent
    # -----------------------------
    st.markdown("### 📈 Awareness vs Purchase Intent")

    fig2 = px.scatter(
        df,
        x="Awareness",
        y="Purchase_Intent",
        opacity=0.5
    )

    fig2.update_layout(
        template="simple_white",
        margin=dict(l=10, r=10, t=40, b=10)
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Insights
    # -----------------------------
    st.markdown("### 🔍 Key Insights")

    st.markdown("""
- Strong demand for sustainable products in the UAE  
- Awareness significantly influences purchase intent  
- Price sensitivity remains a key barrier  
- Eco-conscious users show high conversion potential  
""")

    st.markdown("---")

    # -----------------------------
    # Business Opportunity
    # -----------------------------
    st.markdown("### 🚀 Strategic Opportunity")

    st.success("""
Focus on **price-sensitive but environmentally aware users**:

• Offer discounts & bundles  
• Highlight certifications & trust signals  
• Educate users through content  

👉 This segment offers the highest ROI potential.
""")
