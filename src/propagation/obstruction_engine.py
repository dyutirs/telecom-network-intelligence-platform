import lzma
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer


class ObstructionEngine:
    """Building line-of-sight check for cells already flagged with a
    Coverage issue: is the weak signal explained by a building blocking
    the path between the tower and where the phone measured it, or is
    the path clear (pointing to distance/tilt/other causes instead)?

    Uses only the building-height raster (no terrain/elevation model),
    so ground level is treated as a flat reference plane. That's a
    simplification worth stating out loud, not a hidden assumption.
    """

    def __init__(
        self,
        raster_path,
        receiver_height_m=1.5,
        num_samples=12
    ):

        self.raster_path = raster_path
        self.receiver_height_m = receiver_height_m
        self.num_samples = num_samples
        self.transformer = Transformer.from_crs(
            "EPSG:4326", "EPSG:31287", always_xy=True
        )

    def _ensure_raster(self):
        """The building raster is ~2.7GB decompressed vs. ~15MB as the
        checked-in .xz - decompress on demand instead of keeping the
        large file around between runs."""

        raster_path = Path(self.raster_path)

        if raster_path.exists():
            return

        xz_path = raster_path.with_suffix(raster_path.suffix + ".xz")

        if not xz_path.exists():
            raise FileNotFoundError(
                f"Neither {raster_path} nor {xz_path} exist"
            )

        print(f"Decompressing {xz_path.name} (one-time, ~2.7GB)...")

        with lzma.open(xz_path) as fin, open(raster_path, "wb") as fout:
            shutil.copyfileobj(fin, fout)

    def _sample_building_heights(self, src, lons, lats):

        xs, ys = self.transformer.transform(lons, lats)

        coords = list(zip(xs, ys))

        values = np.array(
            [v[0] for v in src.sample(coords)],
            dtype=float
        )

        values = np.nan_to_num(values, nan=0.0)
        values[values < 0] = 0.0

        return values

    def _check_path(self, src, tower_lat, tower_lon, tower_height_m, rx_lat, rx_lon):

        fracs = np.linspace(0, 1, self.num_samples)

        lats = tower_lat + fracs * (rx_lat - tower_lat)
        lons = tower_lon + fracs * (rx_lon - tower_lon)

        building_heights = self._sample_building_heights(src, lons, lats)

        los_altitude = (
            tower_height_m
            + fracs * (self.receiver_height_m - tower_height_m)
        )

        clearance = los_altitude - building_heights

        min_clearance = float(clearance.min())

        return min_clearance < 0, round(min_clearance, 1)

    def analyze(self, rca_df, cell_table, cell_info):

        self._ensure_raster()

        coverage_cells = (
            rca_df.loc[rca_df["issue"] == "Coverage", ["cell_id"]]
            .merge(
                cell_table[["cell_id", "latitude", "longitude", "enb_id"]],
                on="cell_id",
                how="left"
            )
        )

        tower_info = (
            cell_info[["enb_id", "latitude", "longitude", "height_m"]]
            .drop_duplicates("enb_id")
            .rename(
                columns={
                    "latitude": "tower_lat",
                    "longitude": "tower_lon"
                }
            )
        )

        merged = coverage_cells.merge(
            tower_info, on="enb_id", how="left"
        ).dropna(
            subset=["tower_lat", "tower_lon", "latitude", "longitude"]
        )

        results = []

        with rasterio.open(self.raster_path) as src:

            for _, row in merged.iterrows():

                obstructed, clearance_m = self._check_path(
                    src,
                    row["tower_lat"],
                    row["tower_lon"],
                    row["height_m"],
                    row["latitude"],
                    row["longitude"]
                )

                results.append(
                    {
                        "cell_id": row["cell_id"],
                        "enb_id": row["enb_id"],
                        "min_clearance_m": clearance_m,
                        "diagnosis": (
                            "Building Obstruction (NLOS)"
                            if obstructed
                            else "Clear Line of Sight"
                        )
                    }
                )

        return pd.DataFrame(results)
