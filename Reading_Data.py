import pandas as pd


def get_data():
    df = pd.read_csv(r"C:\Users\malir\OneDrive\Old laptop\Find\scores.csv")
    df.sort_values(ascending=False, by="score", inplace=True)

    index = 520
    df = df[df["score"] > 2][index:]
    return df["screen_name"].tolist(), index
