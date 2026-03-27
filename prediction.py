import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc
import pandas as pd

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

    st.title("🤖 Prediction Models")
    st.caption("Predicting customer purchase intent")

    try:
        df_model = df.copy()

        # -----------------------------
        # TARGET CREATION (SAFE)
        # -----------------------------
        if "Purchase_Intent" not in df_model.columns:
            st.error("Purchase_Intent column missing in dataset")
            return

        df_model["Target"] = (df_model["Purchase_Intent"] > 3).astype(int)

        # -----------------------------
        # SELECT FEATURES (SAFE)
        # -----------------------------
        features = [
            "Age",
            "Awareness",
            "Environmental_Concern",
            "Health_Concern",
            "Price_Sensitivity",
            "Social_Influence",
            "Certification_Importance",
            "Reviews_Importance"
        ]

        # Keep only available columns
        features = [col for col in features if col in df_model.columns]

        if len(features) == 0:
            st.error("No valid features found")
            return

        X = df_model[features]
        y = df_model["Target"]

        # -----------------------------
        # HANDLE MISSING VALUES
        # -----------------------------
        X = X.apply(pd.to_numeric, errors='coerce')
        X = X.fillna(X.mean())

        # -----------------------------
        # TRAIN TEST SPLIT
        # -----------------------------
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # -----------------------------
        # MODEL
        # -----------------------------
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        # -----------------------------
        # METRICS
        # -----------------------------
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        st.markdown("### 📊 Model Performance")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Accuracy", f"{acc:.2f}")
        col2.metric("Precision", f"{prec:.2f}")
        col3.metric("Recall", f"{rec:.2f}")
        col4.metric("F1 Score", f"{f1:.2f}")

        st.markdown("---")

        # -----------------------------
        # ROC CURVE (FIXED)
        # -----------------------------
        st.markdown("### 📈 ROC Curve")

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=fpr,
            y=tpr,
            mode='lines',
            name=f"AUC = {roc_auc:.2f}",
            line=dict(color="#52b788", width=3),
            fill='tozeroy',
            fillcolor='rgba(82,183,136,0.1)'
        ))

        fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode='lines',
            name="Random",
            line=dict(dash='dash', color='gray')
        ))

        fig.update_layout(
            template="simple_white",
            paper_bgcolor="#f7fcf9",
            plot_bgcolor="#f7fcf9",
            font=dict(color="#1b4332"),
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # FEATURE IMPORTANCE (SAFE)
        # -----------------------------
        st.markdown("### 🔍 Feature Importance")

        importance = pd.DataFrame({
            "Feature": X.columns,
            "Importance": model.feature_importances_
        }).sort_values(by="Importance", ascending=False)

        fig2 = px.bar(
            importance,
            x="Importance",
            y="Feature",
            orientation="h",
            color_discrete_sequence=["#74c69d"]
        )

        fig2.update_layout(
            template="simple_white",
            paper_bgcolor="#f7fcf9",
            plot_bgcolor="#f7fcf9",
            font=dict(color="#1b4332")
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # INSIGHTS
        # -----------------------------
        st.markdown("### 🧠 Key Insights")

        if not importance.empty:
            top_feature = importance.iloc[0]["Feature"]
        else:
            top_feature = "N/A"

        st.markdown(f"""
- Most important factor: **{top_feature}**  
- Awareness strongly influences purchase intent  
- Pricing impacts conversion  

👉 Helps target high-value customers
""")

        st.markdown("---")

        # -----------------------------
        # BUSINESS APPLICATION
        # -----------------------------
        st.markdown("### 🚀 Business Application")

        st.success("""
Use predictions to:

• Target high-intent users  
• Personalize campaigns  
• Optimize marketing spend  

👉 Enables data-driven decision making
""")

    except Exception as e:
        st.error("Error in prediction page")
        st.write(e)
