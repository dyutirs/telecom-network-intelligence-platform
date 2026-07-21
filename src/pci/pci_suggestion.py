import pandas as pd

from src.utils.geo import haversine_km

LTE_PCI_RANGE = range(0, 504)


class PCISuggestion:
    """For each detected PCI conflict, suggest a replacement PCI for the
    weaker of the two cells that is not reused within a safe distance."""

    def __init__(self, min_reuse_distance_km=1.0, pci_range=None):

        self.min_reuse_distance_km = min_reuse_distance_km
        self.pci_range = pci_range or LTE_PCI_RANGE

    def _is_pci_free(self, candidate_pci, lat, lon, cell_info, exclude_cell_id):

        same_pci = cell_info[
            (cell_info["pci"] == candidate_pci)
            & (cell_info["cell_id"] != exclude_cell_id)
        ]

        if len(same_pci) == 0:
            return True

        dists = same_pci.apply(
            lambda r: haversine_km(
                lat, lon, r["latitude"], r["longitude"]
            ),
            axis=1
        )

        return dists.min() >= self.min_reuse_distance_km

    def suggest(self, conflict_table, cell_info, cell_table):

        if len(conflict_table) == 0:
            return pd.DataFrame()

        health_lookup = cell_table.set_index("cell_id")["health_score"]

        results = []

        for _, row in conflict_table.iterrows():

            h1 = health_lookup.get(row["cell_1"], 100)
            h2 = health_lookup.get(row["cell_2"], 100)

            if h1 <= h2:
                target_cell_id = row["cell_1"]
                target_site = row["site_1"]
            else:
                target_cell_id = row["cell_2"]
                target_site = row["site_2"]

            target_row = cell_info[
                cell_info["cell_id"] == target_cell_id
            ]

            if len(target_row) == 0:
                continue

            lat = target_row.iloc[0]["latitude"]
            lon = target_row.iloc[0]["longitude"]

            suggested_pci = None

            for candidate in self.pci_range:

                if candidate == row["pci"]:
                    continue

                if self._is_pci_free(
                    candidate, lat, lon, cell_info, target_cell_id
                ):
                    suggested_pci = candidate
                    break

            results.append(
                {
                    "conflicting_pci": row["pci"],
                    "target_cell_id": target_cell_id,
                    "target_site": target_site,
                    "suggested_pci": suggested_pci,
                    "reason": (
                        f"Reassign lower-health cell {target_cell_id} "
                        f"away from conflicting PCI {row['pci']}"
                    )
                }
            )

        return pd.DataFrame(results)
