Project Overview
This is an Urban Heat Island (UHI) analysis of Guwahati (Kamrup Metropolitan District, Assam) by Hemungshew Borgohain, investigating whether higher building density correlates with higher Land Surface Temperature (LST). It's a personal, learning-driven project inspired by the Spatial Thoughts platform.
________________________________________
Key Findings & Conclusions
1. Land Surface Temperature is significantly elevated in built-up areas MODIS LST data for May 2023 (1st–15th) shows a mean surface temperature of 31.13°C, with a max of 39.23°C and a minimum of 24.91°C. The ~14°C spread within the same district strongly suggests spatial variation tied to land cover.
2. There is a large built-up footprint in the study area From OpenStreetMap (via Geofabrik), 13,339 building footprints were identified within Kamrup Metro after clipping from a broader dataset of 37,626. This dense urban fabric is a primary driver of the heat island effect.
3. MODIS LST vs. API air temperature shows a notable gap The NASA POWER API data for June 1–15, 2023 shows a daily average air temperature of ~28.77°C, compared to the MODIS LST mean of 31.13°C. This ~2–3°C difference is consistent with the known phenomenon where land surfaces absorb and re-radiate more heat than ambient air, confirming a measurable UHI signature.
4. NDBI analysis visually confirms built-up concentration The Normalized Difference Built-up Index (NDBI) map computed from Sentinel-2 imagery highlights high-density urban zones (shown in orange/red) concentrated in central Guwahati, which spatially align with the hotter LST zones — supporting the core hypothesis that built-up density drives higher surface temperatures.
________________________________________
Methodological Takeaways
The project demonstrates a solid multi-source geospatial workflow: boundary data (shapefile) → building footprints (OSM/Geofabrik) → satellite raster (MODIS LST) → spectral index (NDBI from Sentinel-2) → API validation (OpenWeather + NASA POWER). The use of geopandas, rioxarray, geemap, and leafmap together shows good command of the modern Python GIS ecosystem.
________________________________________
Overall Conclusion
The study provides evidence that denser built-up areas in Guwahati experience measurably higher land surface temperatures, consistent with Urban Heat Island theory. The convergence of MODIS LST, NDBI patterns, and air temperature comparisons all point in the same direction. A logical next step would be a formal statistical correlation (e.g., Pearson/Spearman) between NDBI values and LST pixel values to quantify the relationship more rigorously.
