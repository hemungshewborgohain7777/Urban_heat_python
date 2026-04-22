# Urban Heat Island Analysis — Guwahati
**By Hemungshew Borgohain**

A Streamlit web app analysing the Urban Heat Island effect in Kamrup Metropolitan District
using MODIS LST, OpenStreetMap buildings, Sentinel-2 NDBI, and weather APIs.

---

## 📁 Folder Structure

```
your-repo/
├── app.py
├── requirements.txt
├── README.md
├── KamrupMetroAOI/
│   ├── KMetro_boundary.shp
│   ├── KMetro_boundary.dbf
│   ├── KMetro_boundary.prj
│   └── KMetro_boundary.shx
├── Geofabrik_Building_Data/
│   └── north-eastern-zone.gpkg
└── MODIS_LST/
    └── Kamrup_Metro_LST_May2023.tif
```

---

## 🚀 Deploy to Streamlit Cloud

1. Push this entire folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo, set **Main file path** to `app.py`
4. Before clicking Deploy, go to **Advanced settings → Secrets** and paste the GEE secret below
5. Click **Deploy**

---

## 🛰️ GEE Service Account Setup (for NDBI Section)

### Step 1 — Create a Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/) and select project `ee-hypeets`
2. Navigate to **IAM & Admin → Service Accounts → Create Service Account**
3. Name: `streamlit-gee` | Role: **Earth Engine Resource Viewer**
4. Click on the created account → **Keys → Add Key → JSON**
5. A `.json` file will download — open it in any text editor

### Step 2 — Add Secret to Streamlit Cloud
In **App Settings → Secrets**, paste the following (fill in values from your downloaded JSON):

```toml
[gee]
type = "service_account"
project_id = "ee-hypeets"
private_key_id = "PASTE_private_key_id_FROM_JSON"
private_key = "PASTE_private_key_FROM_JSON"
client_email = "PASTE_client_email_FROM_JSON"
client_id = "PASTE_client_id_FROM_JSON"
token_uri = "https://oauth2.googleapis.com/token"
```

> ⚠️ Never commit your `.json` key file or paste secrets into the code. Always use Streamlit Secrets.

### Step 3 — Register the Service Account in GEE
1. Go to [Google Earth Engine](https://code.earthengine.google.com/)
2. Click your profile → **Asset Manager**
3. Go to [earthengine.google.com/register](https://earthengine.google.com/register)
4. Register the service account email (`streamlit-gee@ee-hypeets.iam.gserviceaccount.com`)

---

## 💻 Run Locally

```bash
pip install -r requirements.txt
earthengine authenticate   # only needed once
streamlit run app.py
```
