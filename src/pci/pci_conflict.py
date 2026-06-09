import pandas as pd
from math import radians, sin, cos, sqrt, atan2


class PCIConflictAnalysis:

    def distance_km(
        self,
        lat1,
        lon1,
        lat2,
        lon2
    ):

        R = 6371

        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)

        a = (
            sin(dlat / 2) ** 2
            +
            cos(radians(lat1))
            *
            cos(radians(lat2))
            *
            sin(dlon / 2) ** 2
        )

        c = 2 * atan2(
            sqrt(a),
            sqrt(1 - a)
        )

        return R * c

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

                    # Real PCI conflict candidates
                    if d > 0.5 and d < 1.0:

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