import os
import streamlit as st
from PIL import Image
import awesome_streamlit as ast
from assets.pages import About, GeoViz


PAGES = {
    "❓ A propos": About,
    "🗺️ Analyse des données géographiques": GeoViz,
}


def main():
    """Main function of the app"""

    logo = Image.open("src/assets/medias/logo.png")
    st.sidebar.image(logo, width=300)
    st.sidebar.title("Navigation Qualicharge")
    selection = st.sidebar.radio("Choisir la page", list(PAGES.keys()))
    page = PAGES[selection]
    st.sidebar.markdown("""---""")
    with st.spinner(f"Chargement {selection} ..."):
        ast.shared.components.write_page(page)

    columns = st.sidebar.columns(2)
    if columns[0].button("Quitter l'Application"):
        os._exit(1)

    st.sidebar.info(
        """
        Info : Ceci est un POC
        """
    )


if __name__ == "__main__":
    st.set_page_config(
        layout="wide", page_icon="⚡️", page_title="Qualicharge -- DataViz"
    )
    main()