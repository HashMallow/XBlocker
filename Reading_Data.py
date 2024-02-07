import pandas as pd

def get_screen_names():
    df = pd.read_csv(r"C:\Users\malir\OneDrive\Old laptop\Find\scores.csv")
    df.sort_values(ascending=False, by="score", inplace= True)

    df = df[df["score"]>2][:50]
    return df["screen_name"].tolist()
