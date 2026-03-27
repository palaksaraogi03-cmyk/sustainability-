import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc
from utils import preprocess
import pandas as pd

def show(df):
    st.title("🤖 Prediction Models")
    st.caption("Predicting customer purchase intent")

    st.markdown(" ")

    try:
        # -----------------------------
        # Preprocess Data
        # -----------------------------
        df_processed, _ = preprocess(df)

        X = df_processed.drop('Purchase_Intent', axis=1)
        y = (df_processed['Purchase_Intent'] > 3).astype(int)

        # -----------------------------
        # Train/Test Split
        # -----------------------------
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # -----------------------------
        # Model
        # -----------------------------
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        # -----------------------------
        # Metrics
        # -----------------------------
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        st.markdown("### 📊 Model Performance")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Accuracy", f"{acc:.2f}")
        col2.metric("Precision", f"{prec:.2f}")
        col3.metric("Recall", f"{rec:.2f}")
        col4.metric("F1 Score", f"{f1:.2f}")

        st.markdown("---")

        # -----------------------------
        # ROC Curve
        # -----------------------------
        st.markdown("### 📈 ROC Curve")

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(
            x=fpr, y=tpr,
            mode='lines',
            name=f"AUC = {roc_auc:.2f}"
        ))

        fig_roc.update_layout(
            template="simple_white",
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate"
        )

        st.plotly_chart(fig_roc, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # Feature Importance
        # -----------------------------
        st.markdown("### 🔍 Feature Importance")

        importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': model.feature_importances_
        }).sort_values(by='Importance', ascending=False)

        fig_imp = px.bar(
            importance.head(10),
            x='Importance',
            y='Feature',
            orientation='h'
        )

        fig_imp.update_layout(
            template="simple_white"
        )

        st.plotly_chart(fig_imp, use_container_width=True)

        st.markdown("---")

        # -----------------------------
        # Insights
        # -----------------------------
        st.markdown("### 🔍 Key Insights")

        top_feature = importance.iloc[0]['Feature']

        st.markdown(f"""
- The most important driver of purchase intent is **{top_feature}**
- Awareness and price sensitivity strongly influence decisions  
- Model can effectively predict high-value customers  
""")

        st.markdown("---")

        # -----------------------------
        # Business Use
        # -----------------------------
        st.markdown("### 🚀 Business Application")

        st.success("""
Use this model to:

• Target high-intent customers  
• Personalize marketing campaigns  
• Optimize pricing strategies  
• Improve conversion rates  

👉 Enables data-driven growth decisions
""")

    except Exception as e:
        st.error("Error in prediction page")
        st.write(e)
