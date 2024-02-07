import pandas as pd

def get_data():
    df = pd.read_csv(r"C:\Users\malir\OneDrive\Old laptop\Find\scores.csv")
    df.sort_values(ascending=False, by="score", inplace= True)

    index = 220
    df = df[df["score"]>2][index:1000]
    return df["screen_name"].tolist() , index
