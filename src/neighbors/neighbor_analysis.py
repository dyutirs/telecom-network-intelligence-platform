import pandas as pd
from math import radians
from math import sin
from math import cos
from math import sqrt
from math import atan2


class NeighborAnalysis:

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
        cell_info,
        cell_table
    ):

        merged = cell_table.copy()

        merged = merged.dropna(
            subset=[
                "latitude",
                "longitude"
            ]
        )

        print(
            "Cells with coordinates:",
            len(merged)
        )

        rows = merged.to_dict(
            "records"
        )

        results = []

        for row in rows:

            neighbor_sites = set()

        for other in rows:
             if row["cell_id"] == other["cell_id"]:
                  continue
             d = self.distance_km(
                  row["latitude"],
                  row["longitude"],
                  other["latitude"],
                  other["longitude"]
    )
             if d < 0.3:
                  neighbor_sites.add(
                       other["enb_id"]
        )
                  neighbor_count = len(
                  neighbor_sites
)

        issue = "Normal"
    

        if neighbor_count < 2:
            issue = "Missing Neighbors"

        if (
            pd.notna(
                row["median_ta"]
            )
            and
            row["median_ta"] > 20
        ):
            issue = "Overshooting"

        results.append(
                {
                    "cell_id":
                    row["cell_id"],

                    "enb_id":
                    row["enb_id"],

                    "neighbors":
                    neighbor_count,

                    "median_ta":
                    row["median_ta"],

                    "issue":
                    issue,

                    "health_score":
                    row["health_score"]
                }
            )

        return pd.DataFrame(
            results
        )