import streamlit as st
import os

st.set_page_config(page_title="Urban Heat Island – Guwahati", page_icon="🌡️", layout="wide")

# ─── Paths ─────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Kamrup_Metro_shp  = os.path.join(BASE_DIR, 'KamrupMetroAOI', 'KMetro_boundary.shp')
Urban_Buildings   = os.path.join(BASE_DIR, 'Geofabrik_Building_Data', 'north-eastern-zone.gpkg')
MODIS_raster      = os.path.join(BASE_DIR, 'MODIS_LST', 'Kamrup_Metro_LST_May2023.tif')

# ─── Load Boundary ─────────────────────────────
import geopandas as gpd

try:
    gdf = gpd.read_file(Kamrup_Metro_shp)
    st.session_state["gdf"] = gdf
except:
    st.error("Boundary not loaded")
    st.stop()

# ───────────────────────────────────────────────
# SECTION 2 — BUILDINGS (FIXED)
# ───────────────────────────────────────────────
st.header("Buildings")

try:
    import fiona

    layers = fiona.listlayers(Urban_Buildings)
    urban = gpd.read_file(Urban_Buildings, layer=layers[0])

    # CRS fix
    if urban.crs != gdf.crs:
        urban = urban.to_crs(gdf.crs)

    # IMPORTANT: no clipping
    st.session_state["urban"] = urban

    st.success(f"Loaded {len(urban):,} buildings")

except Exception as e:
    st.error(f"Building error: {e}")
    st.stop()

# ───────────────────────────────────────────────
# SECTION 3 — RASTER
# ───────────────────────────────────────────────
st.header("MODIS LST")

try:
    import rioxarray as rxr
    raster = rxr.open_rasterio(MODIS_raster, masked=True)
    st.session_state["raster"] = raster

    st.write("Mean Temp:", float(raster.mean()))

except:
    st.error("Raster not loaded")

# ───────────────────────────────────────────────
# SECTION 4 — LEAFMAP (FINAL FIX)
# ───────────────────────────────────────────────
st.header("Integrated Map")

with st.spinner("Rendering map..."):
    try:
        import leafmap.foliumap as leafmap

        m = leafmap.Map(center=[26.15, 91.75], zoom=11)
        m.add_basemap("CartoDB.DarkMatter")

        # Raster
        if os.path.exists(MODIS_raster):
            m.add_raster(MODIS_raster, layer_name="LST")

        # Boundary
        if "gdf" in st.session_state:
            m.add_gdf(
                st.session_state["gdf"],
                layer_name="Boundary",
                style={"color": "yellow", "fillOpacity": 0}
            )

        # Buildings
        if "urban" in st.session_state:
            urban = st.session_state["urban"]

            if not urban.empty:
                m.add_gdf(
                    urban,
                    layer_name="Buildings",
                    style={"color": "red", "fillOpacity": 0.3}
                )

        m.add_layer_control()
        st.components.v1.html(m.to_html(), height=500)

    except Exception as e:
        st.error(f"Map failed: {e}")

# ───────────────────────────────────────────────
# WEATHER
# ───────────────────────────────────────────────
st.header("Live Weather")

import requests

try:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": "Guwahati", "appid": "YOUR_API_KEY", "units": "metric"}
    res = requests.get(url, params=params).json()

    st.write("Temp:", res["main"]["temp"])
    st.write("Humidity:", res["main"]["humidity"])

except:
    st.warning("Weather API failed")
