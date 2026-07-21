import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree

EARTH_RADIUS_KM = 6371.0


class NeighborAnalysis:
    """Automatic Neighbor Relation (ANR) style check: does each cell have
    enough distinct neighboring sites nearby to hand over to."""

    def __init__(self, radius_km=0.5, min_neighbor_sites=2):

        self.radius_km = radius_km
        self.min_neighbor_sites = min_neighbor_sites

    def analyze(self, cell_table):

        df = (
            cell_table
            .dropna(subset=["latitude", "longitude"])
            .reset_index(drop=True)
        )

        coords_rad = np.radians(
            df[["latitude", "longitude"]].to_numpy()
        )

        tree = BallTree(coords_rad, metric="haversine")

        radius_rad = self.radius_km / EARTH_RADIUS_KM

        neighbor_idx = tree.query_radius(coords_rad, r=radius_rad)

        enb_ids = df["enb_id"].to_numpy()

        results = []

        for i, idx in enumerate(neighbor_idx):

            own_site = enb_ids[i]

            neighbor_sites = {
                enb_ids[j] for j in idx if enb_ids[j] != own_site
            }

            neighbor_count = len(neighbor_sites)

            issue = (
                "Missing Neighbors"
                if neighbor_count < self.min_neighbor_sites
                else "Normal"
            )

            results.append(
                {
                    "cell_id": df.loc[i, "cell_id"],
                    "enb_id": own_site,
                    "neighbor_site_count": neighbor_count,
                    "issue": issue,
                    "health_score": df.loc[i, "health_score"]
                }
            )

        return pd.DataFrame(results)
