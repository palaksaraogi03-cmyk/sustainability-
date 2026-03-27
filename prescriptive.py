import streamlit as st
import pandas as pd

def show(df):
    st.title("🚀 Prescriptive Analysis")
    st.caption("Turning insights into actionable business strategies")

    st.markdown(" ")

    try:
        # -----------------------------
        # Segment Logic (Simple Rules)
        # -----------------------------
        df = df.copy()

        df['Segment'] = "General"

        df.loc[
            (df['Awareness'] >= 4) & (df['Price_Sensitivity'] <= 2),
            'Segment'
        ] = "Eco Enthusiasts"

        df.loc[
            (df['Awareness'] >= 4) & (df['Price_Sensitivity'] >= 4),
            'Segment'
        ] = "Price-Conscious Greens"

        df.loc[
            (df['Awareness'] <= 2),
            'Segment'
        ] = "Unaware Users"

        # -----------------------------
        # Segment Distribution
        # -----------------------------
        st.markdown("### 📊 Segment Distribution")

        seg_counts = df['Segment'].value_counts().reset_index()
        seg_counts.columns = ['Segment', 'Count']

        import plotly.express as px

        fig = px.pie(seg_counts, names='Segment', values='Count')

        fig.update_layout(template="simple_white")

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # STRATEGY CARDS
        # -----------------------------
        st.markdown("### 🎯 Segment-Based Strategies")

        col1, col2 = st.columns(2)

        with col1:
            st.info("""
**🌱 Eco Enthusiasts**
- Premium product targeting  
- Subscription models  
- Loyalty programs  
""")

            st.warning("""
**💸 Price-Conscious Greens**
- Discounts & bundles  
- Limited-time offers  
- Value-based pricing  
""")

        with col2:
            st.success("""
**🤷 Unaware Users**
- Awareness campaigns  
- Educational content  
- Influencer marketing  
""")

            st.write("""
**🛍️ Occasional Buyers**
- Retargeting ads  
- Nudges & reminders  
- Personalized recommendations  
""")

        st.markdown("---")

        # -----------------------------
        # Conversion Strategy
        # -----------------------------
        st.markdown("### 🔄 Conversion Strategy")

        st.markdown("""
- High intent → Push immediate purchase  
- Medium intent → Offer incentives  
- Low intent → Build awareness  

👉 Optimize funnel using predictive scores
""")

        st.markdown("---")

        # -----------------------------
        # Pricing Strategy
        # -----------------------------
        st.markdown("### 💰 Pricing Strategy")

        st.markdown("""
- Use **price sensitivity** to segment users  
- Offer **tiered pricing models**  
- Provide **discounts for price-sensitive users**  
- Maintain premium pricing for low-sensitivity users  
""")

        st.markdown("---")

        # -----------------------------
        # Product Strategy
        # -----------------------------
        st.markdown("### 🛍️ Product Strategy")

        st.markdown("""
- Focus on **high-demand categories**  
- Promote eco-friendly essentials  
- Bundle frequently bought products  
""")

        st.markdown("---")

        # -----------------------------
        # FINAL INSIGHT
        # -----------------------------
        st.markdown("### 🧠 Final Insight")

        st.success("""
The highest ROI opportunity lies in converting  
**price-sensitive but environmentally conscious users**  

👉 Targeting this segment can significantly boost adoption and revenue.
""")

    except Exception as e:
        st.error("Error in prescriptive page")
        st.write(e)
