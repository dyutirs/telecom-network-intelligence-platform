import pandas as pd

from src.utils.geo import haversine_km


class PCIConflictAnalysis:

    def distance_km(
        self,
        lat1,
        lon1,
        lat2,
        lon2
    ):

        return haversine_km(lat1, lon1, lat2, lon2)

    def analyze(
        self,
        cell_info
    ):

        conflicts = []

        for pci in cell_info["pci"].dropna().unique():

            pci_cells = cell_info[
                cell_info["pci"] == pci
            ]

            if len(pci_cells) < 2:
                continue

            rows = pci_cells.to_dict(
                "records"
            )

            for i in range(len(rows)):

                for j in range(
                    i + 1,
                    len(rows)
                ):

                    # Skip same site
                    if (
                        rows[i]["enb_id"]
                        ==
                        rows[j]["enb_id"]
                    ):
                        continue

                    d = self.distance_km(
                        rows[i]["latitude"],
                        rows[i]["longitude"],
                        rows[j]["latitude"],
                        rows[j]["longitude"]
                    )

                    # Real PCI conflict candidates - interference risk
                    # only gets worse the closer two same-PCI sites are,
                    # so there is no safe lower bound here.
                    if d < 1.0:

                        conflicts.append(
                            {
                                "pci": pci,
                                "site_1":
                                    rows[i]["enb_id"],

                                "site_2":
                                    rows[j]["enb_id"],

                                "cell_1":
                                    rows[i]["cell_id"],

                                "cell_2":
                                    rows[j]["cell_id"],

                                "distance_km":
                                    round(d, 3)
                            }
                        )

        conflict_df = pd.DataFrame(
            conflicts
        )

        if len(conflict_df):

            conflict_df = (
                conflict_df
                .sort_values(
                    "distance_km"
                )
                .drop_duplicates(
                    subset=[
                        "site_1",
                        "site_2"
                    ]
                )
            )

        return conflict_df