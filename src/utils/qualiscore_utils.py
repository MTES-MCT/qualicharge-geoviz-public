import pandas as pd

def get_qualiscore_colormap():
    quali_cmap = {
        "A": "#00823f",
        "B": "#86bc2b",
        "C": "#fecc01",
        'D': "#ee8200",
        "E": "#e73c09"
    }
    # quali_cmap = {
    #     "A": "darkgreen",
    #     "B": "lightgreen",
    #     "C": "yellow",
    #     'D': "orange",
    #     "E": "red"
    # }
    return quali_cmap


def qualiscore_mapping(val: float)-> str:
    if val == 0:
         score = "A"
    elif val <= 1.5:
         score = "B"
    elif val <= 3:
         score = "C"
    elif val <= 6:
         score = "D"
    else:
        score = "E"
    dict = get_qualiscore_colormap()
    return dict[score]
    

def get_qualiscore_color(df: pd.DataFrame, col: str):
    #quali_cmap = get_qualiscore_colormap()
    #vmax = df[col].max()
    #fun = lambda val: quali_cmap[chr(65 + ceil(val / vmax * 4))]
    df["qualicolor"] = df[col].apply(qualiscore_mapping)
    return df