import geopandas as gpd
import folium
import webbrowser
import matplotlib.pyplot as plt


def viz_gdf(gdf: gpd.GeoDataFrame, fond: str='Stamen Toner', fenetre: bool=True):
    gdf = gdf.to_crs(epsg=4326)
    carte = folium.Map(tiles=fond, location=[46.7, 2.3], zoom_start=5)
    for _, r in gdf.iterrows() :
        geoj = gpd.GeoSeries(r['geometry']).to_json()
        geoj = folium.GeoJson(data=geoj)
        geoj.add_to(carte)
    if fenetre:
        carte.save("vfr.html")
        webbrowser.open("vfr.html")
        return
    return carte


def stylgen(gdf, parametre, cmap = 'viridis'):
    if gdf[parametre].dtype == str:
        return {
                "color": "blue",                
                "stroke": True
            }
    if gdf[parametre].dtype == bool:
        def style_function(feature):
            rt = gdf[parametre].get(int(feature["id"]), None)
            color_dict = {True: '#00ff00',
                          False: '#aaaaaa'
                }
            return {
                "color": color_dict[rt],                
                "stroke": True
            }
    else:
        lin = plt.get_cmap(cmap)
        def style_function(feature):
            rt = gdf[parametre].get(int(feature["id"]), None)
            vmax = gdf[parametre].max()
            return {
                "color": "#black" if rt is None else '#%02x%02x%02x' % tuple([int(x*256) for x in lin((vmax - rt)/vmax)[:3]]),
                "stroke": True
            }
    return style_function


def afficher_parametre_gdf(
        gdf: gpd.GeoDataFrame,
        parametres: list[str],
        fond: str = 'Stamen Toner',
        fenetre: bool=True 
        )-> folium.Map:
    gdf = gdf.to_crs(epsg=4326)
    carte = folium.Map(tiles=fond, location=[46.7, 2.3], zoom_start=5)
    trace = folium.features.GeoJson(
        gdf, 
        style_function = stylgen(gdf, parametres[0], 'viridis'),
        tooltip = folium.GeoJsonTooltip(parametres)
        )
    trace.add_to(carte)
    if fenetre:
        carte.save("vfr.html")
        webbrowser.open("vfr.html")
        return
    return carte


def render_map_from_gdf(gdf: gpd.GeoDataFrame, col_names: list[str]=[], fmap: folium.map=None, fond: str="cartodbpositron", color: str="orange", weight: int=3)-> folium.Map:
    if fmap == None:
        fmap = folium.Map(tiles=fond, location=[46.7, 2.3], zoom_start=6)
        #folium.TileLayer("cartodbpositron").add_to(fmap)
        #folium.LayerControl().add_to(fmap)
    gdf = gdf.to_crs(epsg=4326)
    geo_types = set(gdf["geometry"].geom_type.values)
    if "Polygon" in geo_types:
        return ValueError("Dataframe should have Linstring or Points, not Polygons")
    if "Point" in geo_types:
        for _, r in gdf.iterrows():
            popup = ""
            for col in col_names:
                popup += col + ": " + str(r[col]) + "\n"
            if col_names == []:
                popup = None
            folium.CircleMarker(
            location=[r["geometry"].y, r["geometry"].x],
            radius=4,
            color='lightblue',
            opacity=1,
            fill_opacity=1,
            fill=True,
            fill_color='lightblue',
            popup=popup
        ).add_to(fmap)
    else: # Linestring Case
        for _, r in gdf.iterrows():
            # Without simplifying the representation of each borough,
            # the map might not be displayed
            popup = ""
            for col in col_names:
                popup += col + ": " + str(r[col]) + "\n"
            if col_names == []:
                popup = None
            geo_j = gpd.GeoSeries(r["geometry"]).simplify(tolerance=0.001).to_json()
            geo_j = folium.GeoJson(data=geo_j, tooltip=popup, style_function=lambda x: {"color": color, "weight": weight})
            #folium.Popup(popup).add_to(geo_j)
            geo_j.add_to(fmap)
    return fmap


def convert_gdf_to_dict(gdf: gpd.GeoDataFrame, geo_col: str, date_col: str, color_col: str="color")-> list[dict]:
    gdf_ = gdf.copy().to_crs(epsg=4326)
    polygons = []
    for _, r in gdf_.iterrows():
        geom_type = r[geo_col].geom_type
        if  "Multi" in geom_type:
            coords_list = [list(geom.coords) for geom in r[geo_col].geoms]
            coords = [item for sublist in coords_list for item in sublist]
        else:
            coords = list(r[geo_col].coords)
        line = {
            "coordinates": coords,
            "dates": [r[date_col]] * len(coords),
            "color": r[color_col],
            "duration": 5
        }
        polygons.append(line)
    return polygons


def extract_features_from_dict(geo_dict: list[dict], feature_type: str="LineString")-> list[dict]:
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": feature_type,
                "coordinates": figure["coordinates"],
            },
            "properties": {
                "times": figure["dates"],
                "style": {
                "color": figure["color"],
                "stroke": True,
                "weight": figure["weight"] if "weight" in figure else 6,
                },
            }
        }
        for figure in geo_dict
    ]
    return features