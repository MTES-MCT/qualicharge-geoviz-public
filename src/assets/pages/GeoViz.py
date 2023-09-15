import os
import datetime as dt
import pandas as pd
import geopandas as gpd
from shapely import wkt

import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
from utils.geoviz_utils import render_map_from_gdf, convert_gdf_to_dict, extract_features_from_dict
from utils.qualiscore_utils import get_qualiscore_color
from utils.data_gather import get_tdg_latest_version


def select_rte_data_filepath()-> str:
    data_folder = "data/GeoData/RTEMap/"
    file_list = os.listdir(data_folder)
    shapefile_list = filter(lambda file: "shp" in file, file_list)
    result = st.selectbox("Choisissez le fichier à charger pour les données de cartographie :", options=shapefile_list)
    filepath = data_folder + result
    return filepath


@st.cache_data
def load_geodata(filepath: str)-> gpd.GeoDataFrame:
    rte_gdf = gpd.read_file(filepath, encoding="utf-8")
    rte_gdf["simplified_geo"] = rte_gdf.geometry
    rte_gdf["buffered_geo"] = rte_gdf.geometry.buffer(3000)
    return rte_gdf


def select_anon_data_filepath()-> str:
    data_folder = "data/Anon/"
    file_list = os.listdir(data_folder)
    csv_list = filter(lambda file: "csv" in file, file_list)
    result = st.selectbox("Choisissez le fichier à charger pour les données anonimisé :", options=csv_list)
    filepath = data_folder + result
    return filepath


@st.cache_data
def load_anon_data(filepath: str)-> gpd.GeoDataFrame:
    anon_gdf = pd.read_csv(filepath, parse_dates=["date_min", "date_max"], date_format="%Y-%m-%dT%H:%M:%S")
    anon_gdf['geometry'] = anon_gdf['geometry'].apply(wkt.loads)
    return anon_gdf


def display_rte_map(fmap: folium.map):
    # Using returned_objects=[] makes it so streamlit does not re 
    # render the page each time the user interact with it.
    st.write("Carte des autoroutes simplifiées utilisée pour l'analyse")
    st_folium(fmap, use_container_width=True, returned_objects=[])
    return


def select_saturation_data_filepath()-> str:
    data_folder = "data/Saturation/"
    file_list = os.listdir(data_folder)
    saturation_list = filter(lambda file: "saturation_" in file, file_list)
    result = st.selectbox("Choisissez le fichier à charger pour les données de saturation :", options=saturation_list)
    filepath = data_folder + result
    return filepath


def render_timelapse(sat_fr_filtered: gpd.GeoDataFrame, fmap: folium.Map, split_count: int):
    polygons = convert_gdf_to_dict(sat_fr_filtered, "geometry", "date_min", "qualicolor")
    features = extract_features_from_dict(polygons)
    period = "PT" + str(int(24 / split_count)) + "H"
    plugins.TimestampedGeoJson(
        {
            "type": "FeatureCollection",
            "features": features,
        },
        
        period=period,
        auto_play=True,
        loop=False,
        speed_slider=False,
        max_speed=4,
        add_last_point=False
    ).add_to(fmap)
    return fmap


def display_color_legend(saturation_france_segments: gpd.GeoDataFrame):
    st.write("Légende couleur pour le timelapse sur la saturation")
    color_legend = saturation_france_segments.groupby("qualicolor").agg(saturation_maximum_sur_la_periode=("max_saturation", max)).reset_index().sort_values("saturation_maximum_sur_la_periode")
    st.write(color_legend)
    return


def write():
    st.title("Qualicharge")
    st.write(
        """
     # Indicateurs d'impacts geographique
     """
    )
    # Récupération des données utiles pour la page
    tdg_gdf = get_tdg_latest_version(as_gdf=True)
    
    anon_filepath = select_anon_data_filepath()
    anon_gdf = load_anon_data(anon_filepath)

    rte_filepath = select_rte_data_filepath()
    rte_gdf = load_geodata(rte_filepath)
    

    st.write("### Carte des segments d'autoroutes simplifiés")
    fmap = render_map_from_gdf(rte_gdf, ["lib_rte"])
    display_rte_map(fmap)
    

    # Display timelapse
    #saturation_france_segments = anon_gdf.groupby(["lib_rte", "group_id", "segment", "date_min"]).agg(geometry=("geometry", "first"), max_saturation=("max_saturation", "mean")).reset_index()
    #saturation_france_segments = get_qualiscore_color(saturation_france_segments, "max_saturation")

    rte_list = anon_gdf["lib_rte"].unique()
    

    #Rajouter légende
    display_color_legend(anon_gdf)

    #Choix des autoroutes pour l'affichage
    multiselect = st.multiselect("Choisissez les autoroutes à afficher sur l'étude", options=rte_list)
    check = st.checkbox("Seulement A1, A6, A7 ?")
    if multiselect == []:
        autoroutes_etude = rte_list
    else:
        autoroutes_etude = multiselect
    if check:
        autoroutes_etude = ["A1", "A6", "A7"]
    
    

    sat_fr_filtered = anon_gdf[anon_gdf["lib_rte"].isin(autoroutes_etude)]
    sat_fr_filtered = sat_fr_filtered.set_geometry(sat_fr_filtered["geometry"], crs=2154)
    segments_grey_map = render_map_from_gdf(rte_gdf, ["lib_rte"], fond="cartodbpositron", color="grey")
    split_count = anon_gdf["period_of_day"].max() + 1
    
    timelapse_fmap = render_timelapse(sat_fr_filtered, segments_grey_map, split_count)
    st.write("### Affichage du timelapse de la saturation en France")
    #timelapse_fmap_stations = render_map_from_gdf(gdf_stations_afir[gdf_stations_afir["id_station_itinerance"].isin(station_list)], [], fmap=timelapse_fmap)
    
    st_folium(timelapse_fmap, use_container_width=True, returned_objects=[])
    filepath = st.text_input(label="filename", key="map_filepath")
    download = st.button(label="Télécharger la carte")
    if download:
        outfolder = "data/html/"
        timelapse_fmap.save(outfolder + filepath)
    
    
    # segments_grey_map = render_map_from_gdf(rte_gdf, ["lib_rte"], fond="cartodbpositron", color="lightgrey")
    # a6_7_map = render_map_wfrom_gdf(rte_gdf[rte_gdf["lib_rte"].isin(["A6", "A7"])], fmap=segments_grey_map, color="green", weight=6)
    # a6_7_map = render_map_from_gdf(stations_rte_gdf[stations_rte_gdf["lib_rte"].isin(["A6", "A7"])], ["sum_power"], fmap=a6_7_map)
    

    # Verifier la date
    
    #st_folium(a6_7_map, use_container_width=True, returned_objects=[]) 
    #a6_7_map.save("a6_7_map.html")


if __name__ == "__main__":
    write()