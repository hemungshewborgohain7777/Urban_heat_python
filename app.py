import streamlit as st
import os
import json
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from shapely.geometry import Point

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Urban Heat Island – Guwahati",
    page_icon="🌡️",
    layout="wide",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
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
    margin-bottom: 0.5rem;
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
.divider { border: none; border-top: 1px solid #222; margin: 2rem 0; }
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


# ─── File paths — all relative to this script ────────────────────────────────
BASE_DIR         = os.path.dirname(os.path.abspath(__file__))
Kamrup_Metro_shp = os.path.join(BASE_DIR, 'KamrupMetroAOI',          'KMetro_boundary.shp')
Urban_Buildings  = os.path.join(BASE_DIR, 'Geofabrik_Building_Data', 'north-eastern-zone.gpkg')
MODIS_raster     = os.path.join(BASE_DIR, 'MODIS_LST',               'Kamrup_Metro_LST_May2023.tif')


# ─── Helpers ─────────────────────────────────────────────────────────────────
def dark_ax(fig, ax, title=""):
    fig.patch.set_facecolor('#0d0d0d')
    ax.set_facecolor('#0d0d0d')
    if title:
        ax.set_title(title, fontsize=12, color='#e8e0d4', fontfamily='monospace', pad=12)
    ax.tick_params(colors='#444')
    for spine in ax.spines.values():
        spine.set_edgecolor('#222')

def stat_box(num, label):
    return f'<div class="stat-box"><div class="stat-num">{num}</div><div class="stat-label">{label}</div></div>'


# ════════════════════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════════════════════
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


# ════════════════════════════════════════════════════════════════════════════
# SECTION 1 — STUDY AREA
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">01 / Study Area</div>', unsafe_allow_html=True)
st.markdown("### Kamrup Metropolitan District")

import geopandas as gpd

gdf = None
try:
    with st.spinner("Loading boundary shapefile…"):
        gdf = gpd.read_file(Kamrup_Metro_shp)

    col1, col2 = st.columns([2, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(10, 7))
        dark_ax(fig, ax, "Kamrup Metropolitan District")
        gdf.plot(edgecolor='#ff6b35', color='#1a1a1a', linewidth=1.5, ax=ax)
        home = gpd.GeoDataFrame(geometry=[Point(91.834051, 26.132521)], crs="EPSG:4326")
        home.plot(ax=ax, color='#f7c59f', markersize=80, marker='*', zorder=5)
        ax.annotate("📍 My Home", xy=(91.834051, 26.132521), xytext=(10, 10),
                    textcoords="offset points", fontsize=9, color="#f7c59f", fontweight="bold")
        ax.set_xlabel("Longitude", color='#666', fontsize=9)
        ax.set_ylabel("Latitude",  color='#666', fontsize=9)
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("**CRS**")
        st.code(str(gdf.crs), language=None)
        st.markdown(f"**Features:** {len(gdf)}")
        b = gdf.total_bounds
        st.markdown(f"""
<div style='font-family:monospace;font-size:0.78rem;color:#888;'>
W: {b[0]:.4f}<br>S: {b[1]:.4f}<br>E: {b[2]:.4f}<br>N: {b[3]:.4f}
</div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("**Interactive Boundary Map**")
    st.components.v1.html(gdf.explore(color='#ff6b35')._repr_html_(), height=400)

except Exception as e:
    st.error(f"⚠️ Could not load shapefile: {e}\n\nExpected: `{Kamrup_Metro_shp}`")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SECTION 2 — BUILDING FOOTPRINTS
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">02 / Building Footprints</div>', unsafe_allow_html=True)
st.markdown("### OpenStreetMap Urban Buildings — Clipped to AOI")
st.markdown("""
<div class="section-card">
Building footprint data from OpenStreetMap (via Geofabrik), pre-clipped to the Kamrup Metro boundary.
Built-up density is compared against MODIS Land Surface Temperature to analyse the UHI effect.
</div>
""", unsafe_allow_html=True)

urban_clipped = None
try:
    with st.spinner("Loading building footprints…"):
        # File is already clipped — read it directly, no layer filter needed
        urban_clipped = gpd.read_file(Urban_Buildings)

        # Align CRS with boundary shapefile
        if gdf is not None and urban_clipped.crs != gdf.crs:
            urban_clipped = urban_clipped.to_crs(gdf.crs)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(stat_box(f"{len(urban_clipped):,}", "Building features"), unsafe_allow_html=True)
    with c2:
        st.markdown(stat_box(f"{len(urban_clipped.columns)}", "Attribute columns"), unsafe_allow_html=True)
    with c3:
        try:
            area_km2 = round(urban_clipped.to_crs(epsg=32646).geometry.area.sum() / 1e6, 2)
            st.markdown(stat_box(f"{area_km2} km²", "Total built-up area"), unsafe_allow_html=True)
        except Exception:
            st.markdown(stat_box("—", "Built-up area"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(10, 13))
        dark_ax(fig, ax, "Urban Building Footprints — Kamrup Metro")
        urban_clipped.plot(edgecolor='#ff6b35', facecolor='#ff6b3522', linewidth=0.5, ax=ax)
        if gdf is not None:
            gdf.plot(edgecolor='#f7c59f', color='none', linewidth=1.5, ax=ax)
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("**Building Types**")
        # Try common column names that Geofabrik exports use
        for col_name in ['type', 'building', 'fclass', 'class', 'code']:
            if col_name in urban_clipped.columns:
                counts = urban_clipped[col_name].value_counts().head(10).reset_index()
                counts.columns = ['Type', 'Count']
                st.dataframe(counts, use_container_width=True, hide_index=True)
                break
        else:
            st.markdown("**Available columns:**")
            st.write(list(urban_clipped.columns))

    st.markdown("**Interactive Buildings Map**")
    if gdf is not None:
        m = gdf.explore(color='#f7c59f', style_kwds={"fillOpacity": 0})
        urban_clipped.explore(m=m, color="#ff6b35")
    else:
        m = urban_clipped.explore(color="#ff6b35")
    st.components.v1.html(m._repr_html_(), height=450)

except Exception as e:
    st.error(f"⚠️ Could not load building data: {e}\n\nExpected: `{Urban_Buildings}`")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SECTION 3 — MODIS LST RASTER
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">03 / Land Surface Temperature</div>', unsafe_allow_html=True)
st.markdown("### MODIS LST — May 1–15, 2023")
st.markdown("""
<div class="section-card">
MODIS LST raster downloaded from Google Earth Engine.
Date range: <b>1 May – 15 May 2023</b> (median composite) — peak heat season in Guwahati.
</div>
""", unsafe_allow_html=True)

raster = None
try:
    with st.spinner("Loading MODIS raster…"):
        import rioxarray as rxr
        raster = rxr.open_rasterio(MODIS_raster, masked=True)

    mean_temp = float(raster.mean().values)
    max_temp  = float(raster.max().values)
    min_temp  = float(raster.min().values)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(stat_box(f"{round(mean_temp, 2)}°C", "Mean LST"), unsafe_allow_html=True)
    with c2: st.markdown(stat_box(f"{round(max_temp,  2)}°C", "Max LST"),  unsafe_allow_html=True)
    with c3: st.markdown(stat_box(f"{round(min_temp,  2)}°C", "Min LST"),  unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(16, 6))
    dark_ax(fig, ax, "MODIS Land Surface Temperature — Kamrup Metro (May 2023)")
    raster.plot(ax=ax, cmap="RdYlGn_r", add_colorbar=True,
                cbar_kwargs={"label": "Temperature (°C)", "shrink": 0.8})
    ax.set_xlabel("Longitude", color='#888', fontsize=9)
    ax.set_ylabel("Latitude",  color='#888', fontsize=9)
    st.pyplot(fig)
    plt.close()

except Exception as e:
    st.error(f"⚠️ Could not load raster: {e}\n\nExpected: `{MODIS_raster}`")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SECTION 4 — INTEGRATED LEAFMAP
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">04 / Integrated Map</div>', unsafe_allow_html=True)
st.markdown("### Leafmap — LST + Boundary + Buildings")

try:
    with st.spinner("Rendering leafmap…"):
        import leafmap.foliumap as leafmap

        m = leafmap.Map(center=[26.15, 91.75], zoom=11)
        m.add_basemap("CartoDB.DarkMatter")

        if raster is not None:
            m.add_raster(MODIS_raster, layer_name="LST MODIS", colormap="coolwarm")
        if gdf is not None:
            m.add_gdf(gdf, layer_name="Kamrup Boundary",
                      style={"color": "#f7c59f", "weight": 2, "fillOpacity": 0})
        if urban_clipped is not None:
            m.add_gdf(urban_clipped, layer_name="Urban Areas",
                      style={"color": "#ff6b35", "fillOpacity": 0.3})

        m.add_layer_control()
        st.components.v1.html(m.to_html(), height=520)

except Exception as e:
    st.error(f"⚠️ Leafmap render error: {e}")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SECTION 5 — LIVE WEATHER
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">05 / Live Weather</div>', unsafe_allow_html=True)
st.markdown("### OpenWeather API — Guwahati (Live)")

try:
    with st.spinner("Fetching live weather…"):
        OW_KEY = "ea8a54aef6a1c1b7fc43f2a7dac0d36f"
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": "Guwahati", "appid": OW_KEY, "units": "metric"},
            timeout=8
        )
        wd = resp.json()

    if resp.status_code == 200:
        cols = st.columns(5)
        cards = [
            ("🌡️", f"{wd['main']['temp']} °C",       "Temperature"),
            ("🤔",  f"{wd['main']['feels_like']} °C", "Feels Like"),
            ("💧",  f"{wd['main']['humidity']} %",    "Humidity"),
            ("🌬️", f"{wd['wind']['speed']} m/s",     "Wind Speed"),
            ("☁️",  wd['weather'][0]['main'],          "Condition"),
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
        st.warning(f"OpenWeather API returned {resp.status_code}: {wd.get('message', '')}")

except Exception as e:
    st.error(f"⚠️ Could not fetch live weather: {e}")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SECTION 6 — NASA POWER API
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">06 / Historical Temperature</div>', unsafe_allow_html=True)
st.markdown("### NASA POWER API — June 1–15, 2023")
st.markdown("""
<div class="section-card">
Temporal air temperature (T2M at 2 m) from NASA POWER for Kamrup Metro,
used to cross-validate MODIS LST for the study period.
</div>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def fetch_nasa_power():
    lat, lon = 26.1862, 91.751
    dates = [f"2023-06-{d:02d}" for d in range(1, 16)]
    results = {}
    for date in dates:
        try:
            r = requests.get(
                "https://power.larc.nasa.gov/api/temporal/daily/point",
                params={
                    "parameters": "T2M", "community": "RE",
                    "longitude": lon, "latitude": lat,
                    "start": date.replace("-", ""), "end": date.replace("-", ""),
                    "format": "JSON"
                }, timeout=10
            )
            results[date] = r.json()["properties"]["parameter"]["T2M"][date.replace("-", "")]
        except Exception:
            results[date] = None
    return results

try:
    with st.spinner("Fetching NASA POWER data (may take ~15 s)…"):
        nasa_data = fetch_nasa_power()

    valid = {k: v for k, v in nasa_data.items() if v is not None}

    if valid:
        x   = [datetime.strptime(d, "%Y-%m-%d") for d in valid]
        y   = list(valid.values())
        avg = sum(y) / len(y)

        fig, ax = plt.subplots(figsize=(14, 5))
        dark_ax(fig, ax, "NASA POWER — Air Temperature at 2 m (June 2023)")
        ax.fill_between(x, y, alpha=0.15, color='#ff6b35')
        ax.plot(x, y, color='#ff6b35', linewidth=2, marker='o', markersize=5,
                markerfacecolor='#f7c59f', markeredgecolor='#ff6b35')
        ax.axhline(avg, color='#f7c59f', linestyle='--', linewidth=1, alpha=0.8,
                   label=f"Avg: {avg:.2f} °C")
        ax.set_xlabel("Date", color='#888', fontsize=9)
        ax.set_ylabel("Temperature (°C)", color='#888', fontsize=9)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.tick_params(colors='#555', labelsize=8)
        ax.legend(facecolor='#141414', edgecolor='#333', labelcolor='#ccc', fontsize=9)
        st.pyplot(fig)
        plt.close()

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(stat_box(f"{round(avg, 2)}°C",    "Mean (NASA)"), unsafe_allow_html=True)
        with c2: st.markdown(stat_box(f"{round(max(y), 2)}°C", "Max"),         unsafe_allow_html=True)
        with c3: st.markdown(stat_box(f"{round(sum(y), 2)}°C", "Total Sum"),   unsafe_allow_html=True)
    else:
        st.warning("No valid data returned from NASA POWER.")

except Exception as e:
    st.error(f"⚠️ NASA POWER fetch failed: {e}")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SECTION 7 — NDBI via Google Earth Engine
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">07 / Built-Up Index</div>', unsafe_allow_html=True)
st.markdown("### NDBI — Normalised Difference Built-up Index (Sentinel-2)")
st.markdown("""
<div class="section-card">
NDBI is computed from Sentinel-2 SR Harmonized imagery (May 1–15, 2023, cloud &lt; 10%)
using the formula: <code>(B11 − B8) / (B11 + B8)</code>.
Higher values indicate denser built-up surfaces — a key driver of UHI.
</div>
""", unsafe_allow_html=True)


def init_gee():
    """
    Auto-detects auth context:
      • Streamlit Cloud  → reads service account from st.secrets["gee"]
      • Local machine    → uses token from `earthengine authenticate`
    """
    import ee

    try:
        gee_cfg = st.secrets.get("gee", {})
    except Exception:
        gee_cfg = {}

    if gee_cfg:
        creds_dict = dict(gee_cfg)
        creds_dict.setdefault("type", "service_account")
        credentials = ee.ServiceAccountCredentials(
            email=creds_dict["client_email"],
            key_data=json.dumps(creds_dict),
        )
        ee.Initialize(credentials=credentials,
                      project=creds_dict.get("project_id", "ee-hypeets"))
    else:
        ee.Initialize(project="ee-hypeets")


# Auth status hint
try:
    has_secret = bool(st.secrets.get("gee"))
except Exception:
    has_secret = False

if has_secret:
    st.markdown("""
<div class="note-box" style="border-color:#ff6b35;color:#ccc;">
✅ <b>GEE service account detected</b> — click the button below to render the NDBI map.
</div>""", unsafe_allow_html=True)
else:
    st.markdown("""
<div class="note-box">
ℹ️ <b>Local:</b> run <code>earthengine authenticate</code> once, then restart the app.<br><br>
<b>Streamlit Cloud:</b> add your service account JSON under <code>[gee]</code> in App Settings → Secrets.
</div>""", unsafe_allow_html=True)

if st.button("🛰️ Load NDBI Map (Sentinel-2 via GEE)"):
    with st.spinner("Connecting to Google Earth Engine and fetching imagery…"):
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
            st.success("✅ NDBI map loaded!")

        except Exception as e:
            st.error(f"GEE error: {e}")


# ════════════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer-note">
    <p><i>Thank you, Ujval Sir, for creating "Spatial Thoughts" and making high-quality geospatial education freely accessible. ❤️</i></p>
    <p style="margin-top:0.5rem;">Urban Heat Island Analysis · Guwahati · 2023 · Hemungshew Borgohain</p>
</div>
""", unsafe_allow_html=True)
