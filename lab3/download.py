from sklearn.datasets import load_diabetes
import pandas as pd


def download_data():
    data = load_diabetes(as_frame=True)
    df = data.frame.copy()
    df.to_csv("diabetes_raw.csv", index=False)
    return df


def clear_data(df):
    df = df.dropna().reset_index(drop=True)
    df.to_csv("df_clear.csv", index=False)
    return True


if __name__ == "__main__":
    df = download_data()
    clear_data(df)
