import pandas as pd


class OvershootingEngine:

    def analyze(
        self,
        cell_table
    ):

        results = []

        for _, row in cell_table.iterrows():

            issue = None

            # -105 dBm is RCA's own "clearly weak" cutoff, so requiring
            # only that here let borderline-weak cells pass as "decent
            # signal". Using -95 (RCA's zero-penalty threshold) means a
            # cell only counts as overshooting if RCA wouldn't have
            # flagged its coverage as weak in the first place.
            if (
                pd.notna(row["median_ta"])
                and
                row["median_ta"] > 25
                and
                row["median_rsrp"] >= -95
                and
                row["median_sinr"] > 0
            ):

                issue = "Overshooting"

            elif (
                pd.notna(row["median_ta"])
                and
                row["median_ta"] > 20
                and
                row["median_rsrp"] >= -95
                and
                row["median_sinr"] > 3
            ):

                issue = "Possible Overshooting"

            if issue:

                results.append(
                    {
                        "cell_id":
                            row["cell_id"],

                        "enb_id":
                            row["enb_id"],

                        "median_ta":
                            row["median_ta"],

                        "median_rsrp":
                            row["median_rsrp"],

                        "health_score":
                            row["health_score"],

                        "issue":
                            issue
                    }
                )

        return pd.DataFrame(
            results
        )