import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_data():
    return pd.read_csv("sustainable_marketplace_survey_uae_2000.csv")

def preprocess(df):
    df = df.copy()

    cat_cols = ['Gender', 'Income', 'Occupation', 'Preferred_Category', 'Purchase_Frequency']

    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    return df, None
