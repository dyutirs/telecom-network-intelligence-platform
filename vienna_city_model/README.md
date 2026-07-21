# 🏙️ Vienna Building and Terrain Model

This dataset provides **building heights** and **terrain elevation** information for the city of Vienna, Austria. It serves as a geospatial foundation for wireless signal modeling, especially for predicting propagation effects such as signal strength degradation in Non-Line-of-Sight (NLOS) conditions.

---

## 📁 Dataset Overview

This release contains two GeoTIFF rasters (EPSG:31287), covering the same area:

- **`bkm_complete_31287.tif`** – Building model, with structure height values (1 m resolution)  
- **`glm_complete_31287.tif`** – Terrain model, with ground elevation (referenced to *Wiener Null*)

---

## 🗜️ Compressed format

The GeoTIFF files in this folder are **XZ-compressed**.

To extract them:

- **Windows:** use 7-Zip → right click → *Extract Here*
- **Linux/macOS:**
  ```bash
  unxz bkm_complete_31287.tif.xz
  unxz glm_complete_31287.tif.xz
---

## 🌐 Data Sources

The data originates from **Stadtvermessung Wien** and is published via **Open Government Data Wien**:

- Building model (Baukörpermodell, LOD1.4):  
  https://www.wien.gv.at/stadtentwicklung/stadtvermessung/geodaten/bkm/
- Terrain model (Geländemodell, DGM):  
  https://www.wien.gv.at/stadtentwicklung/stadtvermessung/geodaten/dgm/

---

## 📄 License and Attribution

The building and terrain data are licensed under the  
**Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

**Required attribution:**

> Stadtvermessung Wien – Baukörpermodell (LOD1.4) and Geländemodell (DGM) –  
> Open Government Data Wien (CC BY 4.0)

When using or redistributing this data, please provide appropriate credit, include a link to the license, and indicate if changes were made.

---

## 🐍 Python integration

These raster files can be imported using the [`rasterio`](https://rasterio.readthedocs.io/en/stable/) Python package:

```python
import rasterio

with rasterio.open("bkm_complete_31287.tif") as bkm:
    buildings = bkm.read(1)

with rasterio.open("glm_complete_31287.tif") as glm:
    terrain = glm.read(1)
```

---

## 📏 Technical notes

- Coordinate system: **EPSG:31287** (Austria Lambert)
- Height reference: *Wiener Null* = 156.68 m above the Adriatic Sea
- Spatial resolution: **1 m**
