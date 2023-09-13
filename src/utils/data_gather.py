import geopandas as gpd
import pandas as pd
import numpy as np
import streamlit as st

def fix_missing_nom_amenageur(tdg_df: pd.DataFrame):
    fixed_tdg_df = tdg_df.copy()
    fixed_tdg_df["expl_unit"] = fixed_tdg_df["id_pdc_itinerance"].str[:5]
    expl_unit_df = fixed_tdg_df.copy()
    expl_unit_df = expl_unit_df.dropna(subset="nom_amenageur")
    expl_unit_df = expl_unit_df.groupby("expl_unit").agg(nom_amenageur_fix=("nom_amenageur", max)).reset_index()
    fixed_tdg_df = pd.merge(fixed_tdg_df, expl_unit_df, on="expl_unit")
    fixed_tdg_df["nom_amenageur"] = np.where(fixed_tdg_df["nom_amenageur"].isna(), fixed_tdg_df["nom_amenageur_fix"], fixed_tdg_df["nom_amenageur"])
    return fixed_tdg_df


@st.cache_data
def get_tdg_latest_version(as_gdf: bool=False)-> gpd.GeoDataFrame:
    tdg_adr = (
    "https://www.data.gouv.fr/fr/datasets/r/8d9398ae-3037-48b2-be19-412c24561fbb"
    )
    tdg_df = pd.read_csv(tdg_adr, parse_dates=["last_modified", "date_maj"])
    tdg_df = fix_missing_nom_amenageur(tdg_df)
    tdg_df = tdg_df.sort_values("date_maj", ascending=False).drop_duplicates("id_pdc_itinerance").dropna(subset=["nom_amenageur"])
    tdg_df["pnom_KW"] = np.where(tdg_df["puissance_nominale"] > 500, tdg_df["puissance_nominale"] / 1000, tdg_df["puissance_nominale"])
    if as_gdf:
        tdg_gdf = gpd.GeoDataFrame(tdg_df, geometry=gpd.points_from_xy(tdg_df.consolidated_longitude, tdg_df.consolidated_latitude)).set_crs(4326)
        tdg_gdf = tdg_gdf.to_crs(2154)
        return tdg_gdf
    return tdg_df