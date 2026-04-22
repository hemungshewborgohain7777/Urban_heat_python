import streamlit as st
import os

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Urban Heat Island – Guwahati",
    page_icon="🌡️",
    layout="wide",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.main { background-color: #0d0d0d; color: #e8e0d4; }

h1, h2, h3 { font-family: 'Syne', sans-serif; font-weight: 800; }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ff6b35, #f7c59f, #efefd0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}
.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #888;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.author-tag {
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid #ff6b35;
    color: #ff6b35;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    padding: 4px 14px;
    border-radius: 2px;
    margin-bottom: 2rem;
    letter-spacing: 0.08em;
}
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #ff6b35;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.section-card {
    background: #141414;
    border: 1px solid #222;
    border-left: 3px solid #ff6b35;
    padding: 1.5rem 1.8rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
}
.stat-box {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-top: 2px solid #ff6b35;
    padding: 1rem 1.2rem;
    border-radius: 4px;
    text-align: center;
}
.stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #f7c59f;
}
.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #666;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.weather-card {
    background: linear-gradient(135deg, #1a1a1a 0%, #141414 100%);
    border: 1px solid #2a2a2a;
    padding: 1.2rem;
    border-radius: 6px;
    text-align: center;
}
.weather-icon { font-size: 2rem; margin-bottom: 0.3rem; }
.weather-val {
    font-family: 'Space Mono', monospace;
    font-size: 1.3rem;
    color: #f7c59f;
    font-weight: 700;
}
.weather-key {
    font-size: 0.7rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-family: 'Space Mono', monospace;
}
.divider {
    border: none;
    border-top: 1px solid #222;
    margin: 2rem 0;
}
.step-badge {
    display: inline-block;
    background: #ff6b35;
    color: #0d0d0d;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 2px;
    margin-right: 0.5rem;
    letter-spacing: 0.05em;
}
.note-box {
    background: #111;
    border: 1px dashed #333;
    padding: 1rem 1.2rem;
    border-radius: 4px;
    font-size: 0.85rem;
    color: #aaa;
    font-family: 'Space Mono', monospace;
}
.footer-note {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #555;
    text-align: center;
    padding: 2rem 0 1rem;
    border-top: 1px solid #1a1a1a;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)


# ─── Relative path definitions (same folder as app.py) ───────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Kamrup_Metro_shp  = os.path.join(BASE_DIR, 'KamrupMetroAOI', 'KMetro_boundary.shp')
Urban_Buildings   = os.path.join(BASE_DIR, 'Geofabrik_Building_Data', 'north-eastern-zone.gpkg')
MODIS_raster      = os.path.join(BASE_DIR, 'MODIS_LST', 'Kamrup_Metro_LST_May2023.tif')


# ════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════
st.markdown('<div class="hero-title">Urban Heat Island<br>Analysis of Guwahati</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">A Comparative Study of Built-Up Density & MODIS Land Surface Temperature</div>', unsafe_allow_html=True)
st.markdown('<div class="author-tag">— Hemungshew Borgohain</div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-card">
This study analyses the Urban Heat Island (UHI) effect in Kamrup Metropolitan District, Guwahati,
by integrating MODIS Land Surface Temperature data, OpenStreetMap building footprints, Sentinel-2 NDBI,
and cross-validated weather API data for May–June 2023.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# SECTION 1 — STUDY AREA
# ════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">01 / Study Area</div>', unsafe_allow_html=True)
st.markdown("### Kamrup Metropolitan District")

with st.spinner("Loading boundary shapefile…"):
    try:
        import geopandas as gpd
        import matplotlib.pyplot as plt
        from shapely.geometry import Point

        gdf = gpd.read_file(Kamrup_Metro_shp)

        col1, col2 = st.columns([2, 1])

        with col1:
            fig, ax = plt.subplots(figsize=(10, 7))
            fig.patch.set_facecolor('#0d0d0d')
            ax.set_facecolor('#0d0d0d')

            gdf.plot(edgecolor='#ff6b35', color='#1a1a1a', linewidth=1.5, ax=ax)

            home_point = gpd.GeoDataFrame(
                geometry=[Point(91.834051, 26.132521)],
                crs="EPSG:4326"
            )
            home_point.plot(ax=ax, color='#f7c59f', markersize=80, marker='*', zorder=5)

            ax.annotate(
                "📍 My Home",
                xy=(91.834051, 26.132521),
                xytext=(10, 10),
                textcoords="offset points",
                fontsize=9,
                color="#f7c59f",
                fontweight="bold"
            )

            ax.set_title("Kamrup Metropolitan District", fontsize=13, color='#e8e0d4',
                         fontfamily='monospace', pad=12)
            ax.set_xlabel("Longitude", color='#666', fontsize=9)
            ax.set_ylabel("Latitude", color='#666', fontsize=9)
            ax.tick_params(colors='#444')
            for spine in ax.spines.values():
                spine.set_edgecolor('#222')

            st.pyplot(fig)
            plt.close()

        with col2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("**CRS Info**")
            st.code(str(gdf.crs), language=None)
            st.markdown(f"**Features:** {len(gdf)}")
            bounds = gdf.total_bounds
            st.markdown(f"**Bounds:**")
            st.markdown(f"""
<div style='font-family:monospace;font-size:0.78rem;color:#888;'>
W: {bounds[0]:.4f}<br>
S: {bounds[1]:.4f}<br>
E: {bounds[2]:.4f}<br>
N: {bounds[3]:.4f}
</div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Interactive map
        st.markdown("**Interactive Boundary Map**")
        st.components.v1.html(gdf.explore(color='#ff6b35')._repr_html_(), height=400)

    except FileNotFoundError:
        st.error(f"⚠️ Shapefile not found at: `{Kamrup_Metro_shp}`\n\nMake sure the `KamrupMetroAOI/` folder is in the same directory as `app.py`.")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# SECTION 2 — BUILDING FOOTPRINTS (FIXED)
# ════════════════════════════════════════════════════════════

st.markdown('<div class="section-label">02 / Building Footprints</div>', unsafe_allow_html=True)
st.markdown("### OpenStreetMap Urban Buildings (Pre-Clipped)")

with st.spinner("Loading building footprints…"):
    try:
        import geopandas as gpd
        import fiona

        # Ensure file exists
        if not os.path.exists(Urban_Buildings):
            st.error(f"GPKG not found: {Urban_Buildings}")
            st.stop()

        # Detect layer
        layers = fiona.listlayers(Urban_Buildings)
        layer_name = layers[0]

        # Load directly (NO bbox, NO clipping)
        urban_clipped = gpd.read_file(Urban_Buildings, layer=layer_name)

        # Fix CRS if missing/mismatch
        if urban_clipped.crs != gdf.crs:
            urban_clipped = urban_clipped.to_crs(gdf.crs)

        # Store globally for later use
        st.session_state["urban_clipped"] = urban_clipped

        # Stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Buildings", f"{len(urban_clipped):,}")
        with col2:
            st.metric("Attributes", len(urban_clipped.columns))

        # Plot
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 10))
        fig.patch.set_facecolor('#0d0d0d')
        ax.set_facecolor('#0d0d0d')

        urban_clipped.plot(ax=ax, color='#ff6b35', linewidth=0.2)
        gdf.plot(ax=ax, edgecolor='#f7c59f', facecolor='none', linewidth=1.5)

        ax.set_title("Urban Buildings — Kamrup Metro", color='white')
        ax.axis('off')

        st.pyplot(fig)
        plt.close()

    except Exception as e:
        st.error(f"Building data error: {e}")
        st.stop()

# ════════════════════════════════════════════════════════════
# SECTION 3 — MODIS LST RASTER
# ════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">03 / Land Surface Temperature</div>', unsafe_allow_html=True)
st.markdown("### MODIS LST — May 1–15, 2023")

st.markdown("""
<div class="section-card">
MODIS LST raster downloaded from Google Earth Engine.
Date range: <b>1st May – 15th May 2023</b> (median composite) — peak heat season in Guwahati.
</div>
""", unsafe_allow_html=True)

with st.spinner("Loading MODIS raster…"):
    try:
        import rioxarray as rxr

        raster = rxr.open_rasterio(MODIS_raster, masked=True)

        mean_temp = float(raster.mean().values)
        max_temp  = float(raster.max().values)
        min_temp  = float(raster.min().values)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="stat-box"><div class="stat-num">{round(mean_temp,2)}°C</div><div class="stat-label">Mean LST</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-box"><div class="stat-num">{round(max_temp,2)}°C</div><div class="stat-label">Max LST</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="stat-box"><div class="stat-num">{round(min_temp,2)}°C</div><div class="stat-label">Min LST</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(16, 6))
        fig.patch.set_facecolor('#0d0d0d')
        ax.set_facecolor('#0d0d0d')

        raster.plot(
            ax=ax,
            cmap="RdYlGn_r",
            add_colorbar=True,
            cbar_kwargs={"label": "Temperature (°C)", "shrink": 0.8}
        )

        ax.set_title("MODIS Land Surface Temperature — Kamrup Metro (May 2023)",
                     fontsize=13, color='#e8e0d4', fontfamily='monospace', pad=12)
        ax.set_xlabel("Longitude", color='#888', fontsize=9)
        ax.set_ylabel("Latitude", color='#888', fontsize=9)
        ax.tick_params(colors='#444')
        for spine in ax.spines.values():
            spine.set_edgecolor('#222')

        st.pyplot(fig)
        plt.close()

    except FileNotFoundError:
        st.error(f"⚠️ Raster not found at: `{MODIS_raster}`\n\nMake sure the `MODIS_LST/` folder is in the same directory as `app.py`.")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# SECTION 4 — INTEGRATED LEAFMAP VISUALISATION
# ════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">04 / Integrated Map</div>', unsafe_allow_html=True)
st.markdown("### Leafmap — LST + Boundary + Buildings")

with st.spinner("Rendering leafmap…"):
    try:
        import leafmap.foliumap as leafmap

        # ── Initialize map ──
        m = leafmap.Map(center=[26.15, 91.75], zoom=11)
        m.add_basemap("CartoDB.DarkMatter")

        # ── Add raster (safe) ──
        if os.path.exists(MODIS_raster):
            m.add_raster(MODIS_raster, layer_name="LST MODIS", colormap="coolwarm")
        else:
            st.warning("MODIS raster not found, skipping raster layer.")

        # ── Add boundary (safe) ──
        if 'gdf' in locals():
            m.add_gdf(
                gdf,
                layer_name="Kamrup Boundary",
                style={"color": "#f7c59f", "weight": 2, "fillOpacity": 0}
            )
        else:
            st.warning("Boundary data not loaded.")

        # ── Add buildings (SAFE FIX) ──
        if 'urban_clipped' in locals() and not urban_clipped.empty:
            m.add_gdf(
                urban_clipped,
                layer_name="Urban Areas",
                style={"color": "#ff6b35", "fillOpacity": 0.3}
            )
        else:
            st.warning("Urban building layer not available or empty.")

        # ── Controls ──
        m.add_layer_control()

        # ── Render ──
        st.components.v1.html(m.to_html(), height=520)

    except Exception as e:
        st.error(f"Leafmap render failed: {e}")

st.markdown('<hr class="divider">', unsafe_allow_html=True)
# ════════════════════════════════════════════════════════════
# SECTION 5 — LIVE WEATHER (OpenWeather API)
# ════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">05 / Live Weather</div>', unsafe_allow_html=True)
st.markdown("### OpenWeather API — Guwahati (Live)")

import requests

API_KEY = "ea8a54aef6a1c1b7fc43f2a7dac0d36f"

with st.spinner("Fetching live weather…"):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": "Guwahati", "appid": API_KEY, "units": "metric"}
        response = requests.get(url, params=params, timeout=8)
        data = response.json()

        if response.status_code == 200:
            cols = st.columns(5)
            cards = [
                ("🌡️", f"{data['main']['temp']} °C",      "Temperature"),
                ("🤔", f"{data['main']['feels_like']} °C", "Feels Like"),
                ("💧", f"{data['main']['humidity']} %",    "Humidity"),
                ("🌬️", f"{data['wind']['speed']} m/s",    "Wind Speed"),
                ("☁️", data['weather'][0]['main'],          "Condition"),
            ]
            for col, (icon, val, label) in zip(cols, cards):
                with col:
                    st.markdown(f"""
<div class="weather-card">
<div class="weather-icon">{icon}</div>
<div class="weather-val">{val}</div>
<div class="weather-key">{label}</div>
</div>""", unsafe_allow_html=True)
        else:
            st.warning(f"API responded with status {response.status_code}: {data.get('message','')}")

    except Exception as e:
        st.error(f"Could not fetch live weather: {e}")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# SECTION 6 — NASA POWER API (Historical Temps)
# ════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">06 / Historical Temperature</div>', unsafe_allow_html=True)
st.markdown("### NASA POWER API — June 1–15, 2023")

st.markdown("""
<div class="section-card">
Temporal air temperature data (T2M at 2 m) for Kamrup Metro from NASA's POWER dataset,
used to cross-validate MODIS LST for the study period.
</div>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def fetch_nasa_power():
    lat, lon = 26.1862, 91.751
    dates = [
        "2023-06-01","2023-06-02","2023-06-03","2023-06-04","2023-06-05",
        "2023-06-06","2023-06-07","2023-06-08","2023-06-09","2023-06-10",
        "2023-06-11","2023-06-12","2023-06-13","2023-06-14","2023-06-15"
    ]
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    results = {}
    for date in dates:
        params = {
            "parameters": "T2M",
            "community": "RE",
            "longitude": lon,
            "latitude": lat,
            "start": date.replace("-", ""),
            "end": date.replace("-", ""),
            "format": "JSON"
        }
        try:
            r = requests.get(url, params=params, timeout=10)
            d = r.json()
            temp = d["properties"]["parameter"]["T2M"][date.replace("-", "")]
            results[date] = temp
        except Exception:
            results[date] = None
    return results

with st.spinner("Fetching NASA POWER data…"):
    try:
        nasa_data = fetch_nasa_power()
        valid = {k: v for k, v in nasa_data.items() if v is not None}

        if valid:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            from datetime import datetime

            x = [datetime.strptime(d, "%Y-%m-%d") for d in valid.keys()]
            y = list(valid.values())
            avg = sum(y) / len(y)

            fig, ax = plt.subplots(figsize=(14, 5))
            fig.patch.set_facecolor('#0d0d0d')
            ax.set_facecolor('#0d0d0d')

            ax.fill_between(x, y, alpha=0.15, color='#ff6b35')
            ax.plot(x, y, color='#ff6b35', linewidth=2, marker='o', markersize=5,
                    markerfacecolor='#f7c59f', markeredgecolor='#ff6b35')
            ax.axhline(avg, color='#f7c59f', linestyle='--', linewidth=1, alpha=0.7,
                       label=f"Avg: {avg:.2f}°C")

            ax.set_title("NASA POWER — Air Temperature at 2m (Jun 2023)", fontsize=12,
                         color='#e8e0d4', fontfamily='monospace', pad=10)
            ax.set_xlabel("Date", color='#888', fontsize=9)
            ax.set_ylabel("Temperature (°C)", color='#888', fontsize=9)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            ax.tick_params(colors='#555', labelsize=8)
            for spine in ax.spines.values():
                spine.set_edgecolor('#222')
            ax.legend(facecolor='#141414', edgecolor='#333', labelcolor='#ccc', fontsize=9)

            st.pyplot(fig)
            plt.close()

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="stat-box"><div class="stat-num">{round(avg,2)}°C</div><div class="stat-label">Mean (NASA)</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="stat-box"><div class="stat-num">{round(max(y),2)}°C</div><div class="stat-label">Max</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="stat-box"><div class="stat-num">{round(sum(y),2)}°C</div><div class="stat-label">Total Sum</div></div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"NASA POWER fetch failed: {e}")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# SECTION 7 — NDBI (Google Earth Engine + geemap)
# ════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">07 / Built-Up Index</div>', unsafe_allow_html=True)
st.markdown("### NDBI — Normalised Difference Built-up Index (Sentinel-2)")

st.markdown("""
<div class="section-card">
NDBI is computed from Sentinel-2 SR Harmonized imagery (May 1–15, 2023, cloud &lt;10%)
using the formula: <code>(B11 − B8) / (B11 + B8)</code>.
Higher NDBI values indicate denser built-up surfaces — a key driver of UHI.
</div>
""", unsafe_allow_html=True)


def init_gee():
    """
    Initialise GEE using whichever auth method is available:
      1. Streamlit Cloud  → reads credentials from st.secrets["gee"]
      2. Local machine    → uses the token cached by `earthengine authenticate`
    Returns True on success, raises on failure.
    """
    import ee
    import json

    # ── Streamlit Cloud path ──────────────────────────────────────────────
    if "gee" in st.secrets:
        creds_dict = dict(st.secrets["gee"])
        # earthengine-api needs the key "type" to equal "service_account"
        creds_dict.setdefault("type", "service_account")

        credentials = ee.ServiceAccountCredentials(
            email=creds_dict["client_email"],
            key_data=json.dumps(creds_dict),
        )
        ee.Initialize(credentials=credentials, project=creds_dict.get("project_id", "ee-hypeets"))

    # ── Local machine path ────────────────────────────────────────────────
    else:
        ee.Initialize(project="ee-hypeets")

    return True


# Check silently whether GEE secrets are already configured
gee_secrets_present = "gee" in st.secrets

if gee_secrets_present:
    st.markdown("""
<div class="note-box" style="border-color:#ff6b35; color:#aaa;">
✅ <b>GEE service account detected</b> — click the button below to render the NDBI map.
</div>
""", unsafe_allow_html=True)
else:
    st.markdown("""
<div class="note-box">
ℹ️ <b>Running locally?</b> Make sure you have run <code>earthengine authenticate</code> once in your terminal.<br><br>
<b>On Streamlit Cloud?</b> Add your service account JSON as a secret under the key <code>[gee]</code>
in <b>App Settings → Secrets</b> (see the README for the exact format).
</div>
""", unsafe_allow_html=True)

run_gee = st.button("🛰️ Load NDBI Map (Sentinel-2 via GEE)")

if run_gee:
    with st.spinner("Connecting to Google Earth Engine…"):
        try:
            import ee
            import geemap.foliumap as geemap

            init_gee()

            aoi = geemap.shp_to_ee(Kamrup_Metro_shp)

            collection = (
                ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                .filterBounds(aoi)
                .filterDate('2023-05-01', '2023-05-15')
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                .map(lambda img: img.clip(aoi))
            )

            median_image = collection.median()
            ndbi = median_image.normalizedDifference(['B11', 'B8']).rename('NDBI')

            ndbi_vis = {
                'min': -0.5, 'max': 0.5,
                'palette': ['#313695', '#74add1', '#ffffbf', '#f46d43', '#a50026']
            }
            rgb_vis = {'min': 0, 'max': 3000, 'bands': ['B4', 'B3', 'B2']}

            m = geemap.Map()
            m.centerObject(aoi, 11)
            m.addLayer(median_image, rgb_vis, 'Sentinel-2 RGB (Clipped)')
            m.addLayer(ndbi, ndbi_vis, 'NDBI (Built-up Index)')

            st.components.v1.html(m.to_html(), height=520)
            st.success("✅ NDBI map loaded successfully!")

        except Exception as e:
            st.error(f"GEE error: {e}")


# ════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer-note">
    <p><i>Thank you, Ujval Sir, for creating "Spatial Thoughts" and making high-quality geospatial education freely accessible. ❤️</i></p>
    <p style="margin-top:0.5rem;">Urban Heat Island Analysis · Guwahati · 2023 · Hemungshew Borgohain</p>
</div>
""", unsafe_allow_html=True)
