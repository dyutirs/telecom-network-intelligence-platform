# 🗼 Estimated Cell Deployment Information (Inferred Metadata)

This folder provides **estimated (inferred) cell deployment descriptors** for a representative subset of sites in the Vienna~4G/5G Drive-Test Dataset. The tables enable **geometry-conditioned** analyses (e.g., propagation modeling, radio-map estimation, and digital-twin calibration) by providing approximate **cell locations**, **sector orientations**, and **antenna heights**.

> **Important:** These descriptors are **not operator ground truth**. They are best-effort estimates derived from measurement-based inference and should be treated as approximate.

---

## 📄 Files in this folder

### LTE cell information

**Columns**
- `operator` – operator label (e.g., `A`)
- `technology` – `LTE`
- `enb_id` – eNodeB identifier
- `sector_id` – sector identifier within the site
- `cell_id` – LTE cell identifier (network-reported; recommended join key)
- `pci` – physical cell identity (PCI)
- `channel_number` – LTE channel number (EARFCN)
- `longitude`, `latitude` – estimated cell/sector position (WGS~84 / EPSG:4326)
- `height_m` – estimated antenna height (m)
- `azimuth_deg` – estimated sector azimuth (degrees)

**How to join**
- Join LTE measurements with this table via **`cell_id`**.

---

### 5G New Radio (5G~NR) cell information (NSA, auxiliary IDs)

**Columns**
- `operator` – operator label (e.g., `A`)
- `technology` – `5GNR`
- `gnb_id_dummy` – dataset-internal gNB identifier (gNodeB grouping)
- `cell_id_dummy` – dataset-internal NR cell identifier
- `pci` – physical cell identity (PCI)
- `channel_number` – NR channel number (NR-ARFCN)
- `longitude`, `latitude` – estimated cell/sector position (WGS~84 / EPSG:4326)
- `height_m` – estimated antenna height (m)
- `azimuth_deg` – estimated sector azimuth (degrees)

**How to join**
- Join 5G~NR measurements with this table via **`cell_id_dummy`** (cell-level) and/or **`gnb_id_dummy`** (site grouping), depending on the measurement table.

**Availability**
- Auxiliary identifiers and inferred 5G~NR cell descriptors are provided **where reliable** and may be restricted to specific operators (commonly operator `A`). Unavailable mappings appear as `NULL` in the measurement tables.

---

## 🧭 Coordinate system and conventions

- Coordinates are provided in **WGS~84 (EPSG:4326)**.
- `azimuth_deg` is the **sector pointing direction in degrees** (clockwise from geographic north).
- `height_m` is given in **meters**.

---

## ⚠️ Limitations

- These descriptors are **estimated** and may contain errors (especially in dense urban areas or where drive-test coverage is sparse).
- PCI reuse and multi-frequency deployments can complicate association; prefer the recommended join keys (`cell_id` for LTE, dummy IDs for 5G~NR).

---

## 📄 License

The inferred deployment descriptors and this documentation are released under  
**Creative Commons Attribution 4.0 International (CC BY 4.0)**. See the repository root for the full licensing statement and citation instructions.
