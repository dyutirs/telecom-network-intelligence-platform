import numpy as np
from sklearn.neighbors import BallTree

EARTH_RADIUS_KM = 6371.0


class InterworkingEngine:
    """For locations where LTE wins the coverage-grid comparison, checks
    whether that's because there's no 5G nearby at all (expansion
    candidate) or because a known 5G site is close but still losing
    (underperforming, worth an antenna/beam check)."""

    def __init__(self, near_5g_km=0.3, no_5g_km=1.0):

        self.near_5g_km = near_5g_km
        self.no_5g_km = no_5g_km

    def analyze(self, coverage_grid, cell_5g_table):

        grid = coverage_grid.copy()

        g5_coords = np.radians(
            cell_5g_table[["latitude", "longitude"]].to_numpy()
        )

        tree = BallTree(g5_coords, metric="haversine")

        grid_coords = np.radians(
            grid[["grid_lat", "grid_lon"]].to_numpy()
        )

        dist, _ = tree.query(grid_coords, k=1)

        grid["nearest_5g_site_km"] = dist[:, 0] * EARTH_RADIUS_KM

        def classify(row):

            if row["winner"] == "5G":
                return "5G Serving"

            if row["nearest_5g_site_km"] <= self.near_5g_km:
                return "5G Underperforming Nearby"

            if row["nearest_5g_site_km"] > self.no_5g_km:
                return "No 5G Coverage (Expansion Candidate)"

            return "5G Out of Range"

        grid["interworking_status"] = grid.apply(classify, axis=1)

        return grid
