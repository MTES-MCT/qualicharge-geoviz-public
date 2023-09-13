import streamlit as st
import pandas as pd
import datetime as dt
from utils.data_gather import get_tdg_latest_version

def display_tdg_stats(df_tdg: pd.DataFrame):
    st.write("### Statistiques de déploiement de bornes en France")
    st.write("#### WORK IN PROGRESS")
    
    # IRVE COUNT
    irve_count = df_tdg["id_pdc_itinerance"].nunique()
    st.write("Nombre de bornes présentes sur Transport Data Gouv : ", str(irve_count))
    
    # IRVE Coverage
    total_irve = 100000
    irve_coverage = irve_count / total_irve * 100
    irve_coverage = round(irve_coverage, 2)
    st.write("Couverture par rapport au réseau total: ", str(irve_coverage), "%")
    st.write("*(Nombre de bornes recensées en France ~= 100000)*")
    # Ajouter un camembert ?

    # Map with IRVE or stations
    
    # Amenageur count
    cpo_count = df_tdg["nom_amenageur"].nunique()
    st.write("Nombre d'aménageurs ressensés sur Transport Data Gouv : ", str(cpo_count))
    return


def write():
    st.markdown(
        """
    ## A propos

    Qualicharge est un projet visant à analyser les données des bornes de recharges de véhicules électriques afin de mieux comprendre
    les problèmes actuels du réseaux de bornes français et pousser les acteurs vers le haut.
    """
    )

    st.markdown("""Sur cette page vous découvrirez : \
                
             - Des informations générales sur le déploiement des bornes de recharges de véhicules électriques en france \

             - Des informations sur la saturation du réseau pendant des weekends très chargés de Mai 2023
             """)
    
    tdg_gdf = get_tdg_latest_version(as_gdf=True)
    display_tdg_stats(tdg_gdf)
        

if __name__ == "__main__":
    st.set_page_config(
        layout="wide", page_icon="⚡️", page_title="Qualicharge -- DataViz"
    )
    write()